#!/usr/bin/env python3
"""
Planning node using MoveIt2 for motion planning
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Pose
from trajectory_msgs.msg import JointTrajectory
from std_msgs.msg import String
import numpy as np


class PlanningNode(Node):
    """ROS 2 node for motion planning"""
    
    def __init__(self):
        super().__init__('planning_node')
        
        # Parameters
        self.declare_parameter('planner', 'RRTConnect')
        self.declare_parameter('planning_time', 5.0)
        self.declare_parameter('max_velocity_scaling', 0.5)
        self.declare_parameter('max_acceleration_scaling', 0.5)
        
        self.planner = self.get_parameter('planner').value
        self.planning_time = self.get_parameter('planning_time').value
        
        # Subscribers
        self.connector_pose_sub = self.create_subscription(
            PoseStamped, '/perception/connector_pose', 
            self.connector_pose_callback, 10)
        self.cable_pose_sub = self.create_subscription(
            PoseStamped, '/perception/cable_pose',
            self.cable_pose_callback, 10)
        
        # Publishers
        self.trajectory_pub = self.create_publisher(
            JointTrajectory, '/planned_trajectory', 10)
        self.status_pub = self.create_publisher(
            String, '/planning/status', 10)
        
        # State
        self.connector_pose = None
        self.cable_pose = None
        self.current_state = 'IDLE'  # IDLE, PLANNING, EXECUTING
        
        # Timer for planning loop
        self.create_timer(0.1, self.planning_loop)
        
        self.get_logger().info('Planning node initialized')
    
    def connector_pose_callback(self, msg):
        """Update connector pose"""
        self.connector_pose = msg
    
    def cable_pose_callback(self, msg):
        """Update cable pose"""
        self.cable_pose = msg
    
    def planning_loop(self):
        """Main planning loop"""
        if self.current_state == 'IDLE' and self.connector_pose is not None:
            self.plan_to_connector()
    
    def plan_to_connector(self):
        """Plan trajectory to connector"""
        self.current_state = 'PLANNING'
        self.get_logger().info('Planning trajectory to connector')
        
        # TODO: Integrate with MoveIt2
        # For now, create a simple trajectory
        trajectory = self.create_simple_trajectory()
        
        if trajectory is not None:
            self.trajectory_pub.publish(trajectory)
            self.publish_status('TRAJECTORY_READY')
            self.current_state = 'IDLE'
        else:
            self.publish_status('PLANNING_FAILED')
            self.current_state = 'IDLE'
    
    def create_simple_trajectory(self):
        """Create a simple trajectory (placeholder)"""
        # This is a placeholder - real implementation would use MoveIt2
        msg = JointTrajectory()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        
        # Joint names (adjust for your robot)
        msg.joint_names = [
            'joint_1', 'joint_2', 'joint_3',
            'joint_4', 'joint_5', 'joint_6'
        ]
        
        # TODO: Actual trajectory planning
        
        return msg
    
    def publish_status(self, status):
        """Publish planning status"""
        msg = String()
        msg.data = status
        self.status_pub.publish(msg)
        self.get_logger().info(f'Planning status: {status}')


def main(args=None):
    rclpy.init(args=args)
    node = PlanningNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
