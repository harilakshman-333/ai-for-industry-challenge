#!/usr/bin/env python3
"""
Launch file for cable insertion simulation in Gazebo
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Declare arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    gui = LaunchConfiguration('gui', default='false')  # Default to headless
    world = LaunchConfiguration('world', default='cable_insertion.world')
    
    # Package directories
    pkg_gazebo_ros = FindPackageShare('gazebo_ros')
    pkg_cable_insertion = FindPackageShare('cable_insertion')
    
    # Get URDF file path
    urdf_file = os.path.join(
        get_package_share_directory('cable_insertion'),
        'urdf',
        'simple_robot.urdf'
    )
    
    # Read robot description
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()
    
    # World file path
    world_file = PathJoinSubstitution([
        pkg_cable_insertion,
        'worlds',
        world
    ])
    
    # Gazebo server
    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([pkg_gazebo_ros, 'launch', 'gzserver.launch.py'])
        ]),
        launch_arguments={
            'world': world_file,
            'verbose': 'true'
        }.items()
    )
    
    # Gazebo client (GUI) - only if gui=true
    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([pkg_gazebo_ros, 'launch', 'gzclient.launch.py'])
        ]),
        condition=IfCondition(gui)
    )
    
    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': robot_desc
        }]
    )
    
    # Perception node
    perception_node = Node(
        package='cable_insertion',
        executable='perception_node.py',
        name='perception_node',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time
        }]
    )
    
    # Planning node
    planning_node = Node(
        package='cable_insertion',
        executable='planning_node.py',
        name='planning_node',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time
        }]
    )
    
    # Control node
    control_node = Node(
        package='cable_insertion',
        executable='control_node.py',
        name='control_node',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time
        }]
    )
    
    # Safety monitor
    safety_monitor = Node(
        package='cable_insertion',
        executable='safety_monitor.py',
        name='safety_monitor',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'max_force': 10.0,
            'max_velocity': 0.5
        }]
    )
    
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('gui', default_value='false'),  # Headless by default
        DeclareLaunchArgument('world', default_value='cable_insertion.world'),
        
        gazebo_server,
        gazebo_client,
        robot_state_publisher,
        perception_node,
        planning_node,
        control_node,
        safety_monitor
    ])
