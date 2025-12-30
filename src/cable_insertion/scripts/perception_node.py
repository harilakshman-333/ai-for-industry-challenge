#!/usr/bin/env python3
"""
Perception node for cable and connector detection
Implements both classical CV and deep learning approaches
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped
from cv_bridge import CvBridge
import cv2
import numpy as np
import torch
import torch.nn as nn


class PoseEstimationNetwork(nn.Module):
    """Deep learning model for pose estimation"""
    def __init__(self):
        super().__init__()
        # Simple CNN for pose estimation
        self.features = nn.Sequential(
            nn.Conv2d(4, 32, 3, padding=1),  # RGB-D input
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.pose_head = nn.Sequential(
            nn.Linear(128 * 80 * 60, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 7)  # x, y, z, qx, qy, qz, qw
        )
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        pose = self.pose_head(x)
        return pose


class PerceptionNode(Node):
    """ROS 2 node for perception"""
    
    def __init__(self):
        super().__init__('perception_node')
        
        # Parameters
        self.declare_parameter('use_deep_learning', True)
        self.declare_parameter('model_path', '')
        self.declare_parameter('confidence_threshold', 0.7)
        
        self.use_dl = self.get_parameter('use_deep_learning').value
        self.confidence_threshold = self.get_parameter('confidence_threshold').value
        
        # CV Bridge
        self.bridge = CvBridge()
        
        # Deep learning model
        if self.use_dl:
            self.model = PoseEstimationNetwork()
            model_path = self.get_parameter('model_path').value
            if model_path:
                self.model.load_state_dict(torch.load(model_path))
            self.model.eval()
        
        # Subscribers
        self.rgb_sub = self.create_subscription(
            Image, '/camera/image_raw', self.rgb_callback, 10)
        self.depth_sub = self.create_subscription(
            Image, '/depth_camera/depth/image_raw', self.depth_callback, 10)
        
        # Publishers
        self.connector_pose_pub = self.create_publisher(
            PoseStamped, '/perception/connector_pose', 10)
        self.cable_pose_pub = self.create_publisher(
            PoseStamped, '/perception/cable_pose', 10)
        self.debug_image_pub = self.create_publisher(
            Image, '/perception/debug_image', 10)
        
        # State
        self.rgb_image = None
        self.depth_image = None
        
        self.get_logger().info('Perception node initialized')
    
    def rgb_callback(self, msg):
        """Process RGB image"""
        self.rgb_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        self.process_images()
    
    def depth_callback(self, msg):
        """Process depth image"""
        self.depth_image = self.bridge.imgmsg_to_cv2(msg, '32FC1')
    
    def process_images(self):
        """Main perception pipeline"""
        if self.rgb_image is None or self.depth_image is None:
            return
        
        if self.use_dl:
            connector_pose, cable_pose = self.deep_learning_perception()
        else:
            connector_pose, cable_pose = self.classical_perception()
        
        # Publish poses
        if connector_pose is not None:
            self.publish_pose(connector_pose, self.connector_pose_pub)
        if cable_pose is not None:
            self.publish_pose(cable_pose, self.cable_pose_pub)
    
    def classical_perception(self):
        """Classical computer vision approach"""
        # Color segmentation
        hsv = cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2HSV)
        
        # Detect blue connector (adjust HSV range as needed)
        lower_blue = np.array([100, 50, 50])
        upper_blue = np.array([130, 255, 255])
        connector_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # Find contours
        contours, _ = cv2.findContours(
            connector_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None, None
        
        # Get largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get centroid
        M = cv2.moments(largest_contour)
        if M['m00'] == 0:
            return None, None
        
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        
        # Get 3D position from depth
        depth = self.depth_image[cy, cx]
        
        # Convert to 3D (simplified camera model)
        fx = 525.0  # focal length (adjust based on camera)
        fy = 525.0
        cx_cam = 320.0
        cy_cam = 240.0
        
        x = (cx - cx_cam) * depth / fx
        y = (cy - cy_cam) * depth / fy
        z = depth
        
        connector_pose = {
            'position': [x, y, z],
            'orientation': [0, 0, 0, 1]  # Identity quaternion
        }
        
        # Cable detection (simplified)
        cable_pose = None
        
        return connector_pose, cable_pose
    
    def deep_learning_perception(self):
        """Deep learning approach"""
        # Prepare input
        rgb = cv2.resize(self.rgb_image, (640, 480))
        depth = cv2.resize(self.depth_image, (640, 480))
        
        # Normalize
        rgb = rgb.astype(np.float32) / 255.0
        depth = np.expand_dims(depth, axis=2)
        depth = (depth - depth.min()) / (depth.max() - depth.min() + 1e-6)
        
        # Concatenate RGB-D
        rgbd = np.concatenate([rgb, depth], axis=2)
        rgbd = np.transpose(rgbd, (2, 0, 1))  # HWC to CHW
        rgbd = torch.from_numpy(rgbd).unsqueeze(0).float()
        
        # Inference
        with torch.no_grad():
            pose = self.model(rgbd)
        
        pose = pose.squeeze().numpy()
        
        connector_pose = {
            'position': pose[:3].tolist(),
            'orientation': pose[3:].tolist()
        }
        
        cable_pose = None  # TODO: Implement cable tracking
        
        return connector_pose, cable_pose
    
    def publish_pose(self, pose_dict, publisher):
        """Publish pose message"""
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_link'
        
        msg.pose.position.x = pose_dict['position'][0]
        msg.pose.position.y = pose_dict['position'][1]
        msg.pose.position.z = pose_dict['position'][2]
        
        msg.pose.orientation.x = pose_dict['orientation'][0]
        msg.pose.orientation.y = pose_dict['orientation'][1]
        msg.pose.orientation.z = pose_dict['orientation'][2]
        msg.pose.orientation.w = pose_dict['orientation'][3]
        
        publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
