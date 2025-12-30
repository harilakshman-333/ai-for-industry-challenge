#!/bin/bash
# Build ROS 2 workspace

set -e

cd /workspace

echo "Installing dependencies..."
rosdep install --from-paths src --ignore-src -r -y

echo "Building workspace..."
colcon build --symlink-install

echo "Sourcing workspace..."
source install/setup.bash

echo "Build complete!"
