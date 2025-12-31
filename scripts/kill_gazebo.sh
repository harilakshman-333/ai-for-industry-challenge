#!/bin/bash
# Helper script to kill all Gazebo processes

echo "Killing all Gazebo processes..."
pkill -9 gzserver
pkill -9 gzclient
sleep 1

echo "Checking for remaining Gazebo processes..."
if pgrep -x "gzserver" > /dev/null || pgrep -x "gzclient" > /dev/null; then
    echo "⚠️  Some Gazebo processes still running"
    ps aux | grep gz
else
    echo "✅ All Gazebo processes killed"
fi
