#!/bin/bash
# Build ROS 2 workspace

set -e

# Source ROS 2 environment
echo "Sourcing ROS 2 environment..."
source /opt/ros/humble/setup.bash

cd /workspace

echo "Installing dependencies..."
rosdep install --from-paths src --ignore-src -r -y

echo "Building workspace..."
colcon build --symlink-install

echo "Sourcing workspace..."
source install/setup.bash

echo "Build complete!"
echo "To use the workspace, run: source /workspace/install/setup.bash"
