# Gazebo Launch Issues & Solutions

## Issue 1: "Address already in use" Error

**Problem:** Gazebo server fails with "Unable to start server[bind: Address already in use]"

**Cause:** Previous Gazebo instance still running

**Solution:**
```bash
# Kill all Gazebo processes
./scripts/kill_gazebo.sh

# Or manually:
pkill -9 gzserver
pkill -9 gzclient
```

## Issue 2: Perception Node cv_bridge NumPy Incompatibility

**Problem:** 
```
AttributeError: _ARRAY_API not found
A module that was compiled using NumPy 1.x cannot be run in NumPy 2.2.6
```

**Cause:** System cv_bridge package was compiled with NumPy 2.x, but we need NumPy <2

**Solutions:**

### Option 1: Remove cv_bridge dependency (Quick Fix)
For now, perception node can work without cv_bridge by using direct NumPy arrays:
- Comment out `from cv_bridge import CvBridge` in perception_node.py
- Use NumPy arrays directly instead of ROS Image messages

### Option 2: Rebuild cv_bridge from source (Proper Fix)
```bash
# Inside container
cd /workspace/src
git clone https://github.com/ros-perception/vision_opencv.git -b humble
cd vision_opencv/cv_bridge
# Build with current NumPy version
cd /workspace
colcon build --packages-select cv_bridge
```

### Option 3: Use NumPy 2.x (Alternative)
Update Dockerfile to use NumPy 2.x and rebuild cv_bridge compatibility layer

## Recommended Workflow

**Before each launch:**
```bash
# 1. Enter container
docker exec -it ai_challenge_dev /bin/bash

# 2. Kill any existing Gazebo
pkill -9 gzserver gzclient

# 3. Source environment
source /opt/ros/humble/setup.bash
source /workspace/install/setup.bash

# 4. Launch simulation
ros2 launch cable_insertion simulation.launch.py
```

## Current Status

✅ **Working:**
- Gazebo server (headless mode)
- Robot state publisher with URDF
- Planning node
- Control node (position mode)
- Safety monitor

⚠️ **Needs Fix:**
- Perception node (cv_bridge/NumPy incompatibility)

## Quick Test Commands

```bash
# Check if Gazebo is running
pgrep -x gzserver

# List ROS nodes
ros2 node list

# Check topics
ros2 topic list

# Monitor safety status
ros2 topic echo /safety/status

# Monitor planning status
ros2 topic echo /planning/status
```
