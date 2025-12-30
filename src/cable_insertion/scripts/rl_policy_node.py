#!/usr/bin/env python3
"""
Reinforcement Learning policy node using SAC algorithm
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, TwistStamped, WrenchStamped
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool, Float32MultiArray
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class Actor(nn.Module):
    """SAC Actor network"""
    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super().__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.mean = nn.Linear(hidden_dim, action_dim)
        self.log_std = nn.Linear(hidden_dim, action_dim)
        
    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        mean = self.mean(x)
        log_std = self.log_std(x)
        log_std = torch.clamp(log_std, -20, 2)
        return mean, log_std
    
    def sample(self, state):
        mean, log_std = self.forward(state)
        std = log_std.exp()
        normal = torch.distributions.Normal(mean, std)
        x_t = normal.rsample()
        action = torch.tanh(x_t)
        log_prob = normal.log_prob(x_t) - torch.log(1 - action.pow(2) + 1e-6)
        log_prob = log_prob.sum(1, keepdim=True)
        return action, log_prob


class RLPolicyNode(Node):
    """RL policy node for cable insertion"""
    
    def __init__(self):
        super().__init__('rl_policy_node')
        
        # Parameters
        self.declare_parameter('model_path', '')
        self.declare_parameter('state_dim', 28)  # Adjust based on state space
        self.declare_parameter('action_dim', 6)  # End-effector velocity (6-DOF)
        self.declare_parameter('use_policy', False)
        
        state_dim = self.get_parameter('state_dim').value
        action_dim = self.get_parameter('action_dim').value
        self.use_policy = self.get_parameter('use_policy').value
        
        # Initialize actor network
        self.actor = Actor(state_dim, action_dim)
        
        # Load trained model if available
        model_path = self.get_parameter('model_path').value
        if model_path:
            try:
                self.actor.load_state_dict(torch.load(model_path))
                self.actor.eval()
                self.get_logger().info(f'Loaded model from {model_path}')
            except Exception as e:
                self.get_logger().error(f'Failed to load model: {e}')
        
        # Subscribers
        self.connector_pose_sub = self.create_subscription(
            PoseStamped, '/perception/connector_pose',
            self.connector_pose_callback, 10)
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states',
            self.joint_state_callback, 10)
        self.force_sub = self.create_subscription(
            WrenchStamped, '/force_torque_sensor',
            self.force_callback, 10)
        
        # Publishers
        self.action_pub = self.create_publisher(
            TwistStamped, '/rl/action', 10)
        self.state_pub = self.create_publisher(
            Float32MultiArray, '/rl/state', 10)
        
        # State variables
        self.connector_pose = None
        self.joint_states = None
        self.force_torque = None
        self.target_pose = np.array([0.5, 0.0, 0.85, 0, 0, 0, 1])  # Target socket
        
        # Policy execution timer
        if self.use_policy:
            self.create_timer(0.05, self.policy_step)  # 20 Hz
        
        self.get_logger().info('RL policy node initialized')
    
    def connector_pose_callback(self, msg):
        """Update connector pose"""
        self.connector_pose = np.array([
            msg.pose.position.x,
            msg.pose.position.y,
            msg.pose.position.z,
            msg.pose.orientation.x,
            msg.pose.orientation.y,
            msg.pose.orientation.z,
            msg.pose.orientation.w
        ])
    
    def joint_state_callback(self, msg):
        """Update joint states"""
        self.joint_states = np.array(msg.position)
    
    def force_callback(self, msg):
        """Update force/torque"""
        self.force_torque = np.array([
            msg.wrench.force.x,
            msg.wrench.force.y,
            msg.wrench.force.z,
            msg.wrench.torque.x,
            msg.wrench.torque.y,
            msg.wrench.torque.z
        ])
    
    def get_state(self):
        """Construct state vector"""
        if (self.connector_pose is None or 
            self.joint_states is None or 
            self.force_torque is None):
            return None
        
        # State: [connector_pose(7), target_pose(7), joint_states(7), force_torque(6), gripper(1)]
        state = np.concatenate([
            self.connector_pose,
            self.target_pose,
            self.joint_states[:7] if len(self.joint_states) >= 7 else np.zeros(7),
            self.force_torque,
            np.array([1.0])  # Gripper state (placeholder)
        ])
        
        return state
    
    def policy_step(self):
        """Execute one step of the policy"""
        state = self.get_state()
        if state is None:
            return
        
        # Publish state for monitoring
        state_msg = Float32MultiArray()
        state_msg.data = state.tolist()
        self.state_pub.publish(state_msg)
        
        # Get action from policy
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        
        with torch.no_grad():
            action, _ = self.actor.sample(state_tensor)
            action = action.squeeze().numpy()
        
        # Publish action
        action_msg = TwistStamped()
        action_msg.header.stamp = self.get_clock().now().to_msg()
        action_msg.header.frame_id = 'base_link'
        
        # Map action to velocity command
        action_msg.twist.linear.x = float(action[0])
        action_msg.twist.linear.y = float(action[1])
        action_msg.twist.linear.z = float(action[2])
        action_msg.twist.angular.x = float(action[3])
        action_msg.twist.angular.y = float(action[4])
        action_msg.twist.angular.z = float(action[5])
        
        self.action_pub.publish(action_msg)


def main(args=None):
    rclpy.init(args=args)
    node = RLPolicyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
