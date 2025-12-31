#!/bin/bash
# Test Gazebo launch in headless mode

echo "Testing Gazebo launch (headless mode)..."
echo "=========================================="

# Launch simulation in background
timeout 10 ros2 launch cable_insertion simulation.launch.py &
LAUNCH_PID=$!

# Wait a bit for nodes to start
sleep 5

# Check if Gazebo server is running
echo ""
echo "Checking Gazebo server..."
if pgrep -x "gzserver" > /dev/null; then
    echo "✅ Gazebo server is running"
else
    echo "❌ Gazebo server is NOT running"
fi

# Check ROS nodes
echo ""
echo "Checking ROS nodes..."
ros2 node list

# Check topics
echo ""
echo "Checking ROS topics..."
ros2 topic list | head -20

# Kill launch
kill $LAUNCH_PID 2>/dev/null

echo ""
echo "Test complete!"
