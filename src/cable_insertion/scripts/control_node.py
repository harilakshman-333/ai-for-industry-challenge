#!/usr/bin/env python3
"""
Control node with hybrid position/force control
"""

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
from geometry_msgs.msg import WrenchStamped, TwistStamped
from std_msgs.msg import String
import numpy as np


class HybridController(Node):
    """Hybrid position/force controller"""
    
    def __init__(self):
        super().__init__('control_node')
        
        # Parameters
        self.declare_parameter('control_mode', 'position')  # position or force
        self.declare_parameter('target_force', 5.0)  # Newtons
        self.declare_parameter('force_kp', 0.1)
        self.declare_parameter('force_ki', 0.01)
        self.declare_parameter('force_kd', 0.05)
        self.declare_parameter('max_velocity', 0.5)  # m/s
        
        self.control_mode = self.get_parameter('control_mode').value
        self.target_force = self.get_parameter('target_force').value
        self.kp = self.get_parameter('force_kp').value
        self.ki = self.get_parameter('force_ki').value
        self.kd = self.get_parameter('force_kd').value
        self.max_velocity = self.get_parameter('max_velocity').value
        
        # PID state
        self.integral = 0.0
        self.prev_error = 0.0
        
        # Subscribers
        self.trajectory_sub = self.create_subscription(
            JointTrajectory, '/planned_trajectory',
            self.trajectory_callback, 10)
        self.force_sub = self.create_subscription(
            WrenchStamped, '/force_torque_sensor',
            self.force_callback, 10)
        
        # Publishers
        self.velocity_pub = self.create_publisher(
            TwistStamped, '/robot/cmd_vel', 10)
        self.status_pub = self.create_publisher(
            String, '/control/status', 10)
        
        # State
        self.current_trajectory = None
        self.current_force = None
        self.trajectory_index = 0
        
        # Control loop timer
        self.create_timer(0.01, self.control_loop)  # 100 Hz
        
        self.get_logger().info(f'Control node initialized in {self.control_mode} mode')
    
    def trajectory_callback(self, msg):
        """Receive new trajectory"""
        self.current_trajectory = msg
        self.trajectory_index = 0
        self.get_logger().info('Received new trajectory')
    
    def force_callback(self, msg):
        """Update force/torque measurements"""
        self.current_force = msg
    
    def control_loop(self):
        """Main control loop"""
        if self.control_mode == 'position':
            self.position_control()
        elif self.control_mode == 'force':
            self.force_control()
    
    def position_control(self):
        """Position-based control"""
        if self.current_trajectory is None:
            return
        
        # TODO: Implement position control
        # For now, just publish zero velocity
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = 'base_link'
        self.velocity_pub.publish(cmd)
    
    def force_control(self):
        """Force-based control for insertion"""
        if self.current_force is None:
            return
        
        # Measure current force magnitude
        fx = self.current_force.wrench.force.x
        fy = self.current_force.wrench.force.y
        fz = self.current_force.wrench.force.z
        current_force = np.sqrt(fx**2 + fy**2 + fz**2)
        
        # PID control
        error = self.target_force - current_force
        self.integral += error * 0.01  # dt = 0.01s
        derivative = (error - self.prev_error) / 0.01
        
        # Anti-windup
        self.integral = np.clip(self.integral, -10.0, 10.0)
        
        force_adjustment = (
            self.kp * error +
            self.ki * self.integral +
            self.kd * derivative
        )
        
        self.prev_error = error
        
        # Compute velocity command
        # Assuming insertion direction is along z-axis
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = 'base_link'
        
        # Limit velocity
        velocity = np.clip(force_adjustment, -self.max_velocity, self.max_velocity)
        cmd.twist.linear.z = velocity
        
        self.velocity_pub.publish(cmd)
        
        # Log force error
        if abs(error) > 1.0:
            self.get_logger().info(
                f'Force error: {error:.2f}N, velocity: {velocity:.3f}m/s')
    
    def switch_mode(self, mode):
        """Switch between position and force control"""
        if mode in ['position', 'force']:
            self.control_mode = mode
            self.integral = 0.0
            self.prev_error = 0.0
            self.get_logger().info(f'Switched to {mode} control mode')
            
            msg = String()
            msg.data = f'MODE_CHANGED_{mode.upper()}'
            self.status_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = HybridController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
