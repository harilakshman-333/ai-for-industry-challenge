#!/usr/bin/env python3
"""
Safety monitor node
Monitors force, velocity, and collisions
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import WrenchStamped, TwistStamped
from std_msgs.msg import Bool, String
import numpy as np


class SafetyMonitor(Node):
    """Safety monitoring node"""
    
    def __init__(self):
        super().__init__('safety_monitor')
        
        # Parameters
        self.declare_parameter('max_force', 10.0)  # Newtons
        self.declare_parameter('max_velocity', 0.5)  # m/s
        self.declare_parameter('max_torque', 5.0)  # Nm
        self.declare_parameter('check_rate', 100.0)  # Hz
        
        self.max_force = self.get_parameter('max_force').value
        self.max_velocity = self.get_parameter('max_velocity').value
        self.max_torque = self.get_parameter('max_torque').value
        
        # Subscribers
        self.force_sub = self.create_subscription(
            WrenchStamped, '/force_torque_sensor',
            self.force_callback, 10)
        self.velocity_sub = self.create_subscription(
            TwistStamped, '/robot/cmd_vel',
            self.velocity_callback, 10)
        
        # Publishers
        self.emergency_stop_pub = self.create_publisher(
            Bool, '/emergency_stop', 10)
        self.safety_status_pub = self.create_publisher(
            String, '/safety/status', 10)
        self.violation_pub = self.create_publisher(
            String, '/safety/violations', 10)
        
        # State
        self.current_force = None
        self.current_velocity = None
        self.violations = []
        self.emergency_stop_active = False
        
        # Safety check timer
        check_period = 1.0 / self.get_parameter('check_rate').value
        self.create_timer(check_period, self.safety_check)
        
        self.get_logger().info('Safety monitor initialized')
        self.get_logger().info(f'Max force: {self.max_force}N, Max velocity: {self.max_velocity}m/s')
    
    def force_callback(self, msg):
        """Update force/torque measurements"""
        self.current_force = msg
    
    def velocity_callback(self, msg):
        """Update velocity command"""
        self.current_velocity = msg
    
    def safety_check(self):
        """Perform safety checks"""
        self.violations = []
        
        # Check force limits
        if self.current_force is not None:
            fx = self.current_force.wrench.force.x
            fy = self.current_force.wrench.force.y
            fz = self.current_force.wrench.force.z
            force_magnitude = np.sqrt(fx**2 + fy**2 + fz**2)
            
            if force_magnitude > self.max_force:
                self.violations.append(
                    f'FORCE_EXCEEDED: {force_magnitude:.2f}N > {self.max_force}N')
            
            # Check torque limits
            tx = self.current_force.wrench.torque.x
            ty = self.current_force.wrench.torque.y
            tz = self.current_force.wrench.torque.z
            torque_magnitude = np.sqrt(tx**2 + ty**2 + tz**2)
            
            if torque_magnitude > self.max_torque:
                self.violations.append(
                    f'TORQUE_EXCEEDED: {torque_magnitude:.2f}Nm > {self.max_torque}Nm')
        
        # Check velocity limits
        if self.current_velocity is not None:
            vx = self.current_velocity.twist.linear.x
            vy = self.current_velocity.twist.linear.y
            vz = self.current_velocity.twist.linear.z
            velocity_magnitude = np.sqrt(vx**2 + vy**2 + vz**2)
            
            if velocity_magnitude > self.max_velocity:
                self.violations.append(
                    f'VELOCITY_EXCEEDED: {velocity_magnitude:.3f}m/s > {self.max_velocity}m/s')
        
        # Handle violations
        if self.violations:
            self.handle_violations()
        else:
            # Publish safe status
            if self.emergency_stop_active:
                self.clear_emergency_stop()
            self.publish_status('SAFE')
    
    def handle_violations(self):
        """Handle safety violations"""
        # Log violations
        for violation in self.violations:
            self.get_logger().warn(f'Safety violation: {violation}')
            
            # Publish violation
            msg = String()
            msg.data = violation
            self.violation_pub.publish(msg)
        
        # Trigger emergency stop for critical violations
        if any('EXCEEDED' in v for v in self.violations):
            self.trigger_emergency_stop()
    
    def trigger_emergency_stop(self):
        """Trigger emergency stop"""
        if not self.emergency_stop_active:
            self.get_logger().error('EMERGENCY STOP TRIGGERED')
            self.emergency_stop_active = True
            
            msg = Bool()
            msg.data = True
            self.emergency_stop_pub.publish(msg)
            
            self.publish_status('EMERGENCY_STOP')
    
    def clear_emergency_stop(self):
        """Clear emergency stop"""
        self.get_logger().info('Emergency stop cleared')
        self.emergency_stop_active = False
        
        msg = Bool()
        msg.data = False
        self.emergency_stop_pub.publish(msg)
    
    def publish_status(self, status):
        """Publish safety status"""
        msg = String()
        msg.data = status
        self.safety_status_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = SafetyMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
