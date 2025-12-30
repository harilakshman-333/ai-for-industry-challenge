# Development Environment Setup

This guide will help you set up your development environment for the AI for Industry Challenge.

## Prerequisites

- Ubuntu 22.04 LTS (recommended)
- Python 3.10+
- Git
- At least 16GB RAM
- NVIDIA GPU (recommended for training)

## Installation Steps

### 1. Install ROS 2 Humble

```bash
# Set locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Setup sources
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2 packages
sudo apt update
sudo apt upgrade
sudo apt install ros-humble-desktop
sudo apt install ros-dev-tools

# Source ROS 2
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 2. Install Gazebo

```bash
# Install Gazebo Garden (compatible with ROS 2 Humble)
sudo apt-get update
sudo apt-get install ros-humble-gazebo-ros-pkgs
```

### 3. Install MoveIt2

```bash
sudo apt install ros-humble-moveit
```

### 4. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv ~/ai_challenge_env
source ~/ai_challenge_env/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install torch torchvision torchaudio
pip install numpy opencv-python scipy
pip install matplotlib seaborn
pip install jupyter notebook
pip install tensorboard
```

### 5. Install Additional Tools

```bash
# Install OpenCV with contrib modules
pip install opencv-contrib-python

# Install Point Cloud Library
sudo apt install libpcl-dev python3-pcl

# Install visualization tools
pip install open3d
```

### 6. Clone Challenge Repository

```bash
# Create workspace
mkdir -p ~/ai_challenge_ws/src
cd ~/ai_challenge_ws/src

# Clone your team repository
git clone https://github.com/your-username/ai-for-industry-challenge.git

# Build workspace
cd ~/ai_challenge_ws
colcon build
source install/setup.bash
```

### 7. Optional: Install NVIDIA Isaac Sim

For advanced physics simulation and training:

1. Download from [NVIDIA Isaac Sim](https://developer.nvidia.com/isaac-sim)
2. Follow installation instructions
3. Install Isaac Sim Python packages

```bash
pip install isaacsim
```

## Verify Installation

### Test ROS 2

```bash
ros2 run demo_nodes_cpp talker
# In another terminal:
ros2 run demo_nodes_py listener
```

### Test Gazebo

```bash
gazebo --verbose
```

### Test MoveIt2

```bash
ros2 launch moveit2_tutorials demo.launch.py
```

## Environment Variables

Add these to your `~/.bashrc`:

```bash
# ROS 2
source /opt/ros/humble/setup.bash
source ~/ai_challenge_ws/install/setup.bash

# Python virtual environment
source ~/ai_challenge_env/bin/activate

# CUDA (if using GPU)
export CUDA_HOME=/usr/local/cuda
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
```

## Troubleshooting

### Issue: ROS 2 commands not found
**Solution:** Make sure you've sourced the setup file:
```bash
source /opt/ros/humble/setup.bash
```

### Issue: Gazebo crashes on startup
**Solution:** Update graphics drivers and check GPU compatibility

### Issue: Python package conflicts
**Solution:** Use a clean virtual environment:
```bash
deactivate
rm -rf ~/ai_challenge_env
python3 -m venv ~/ai_challenge_env
source ~/ai_challenge_env/bin/activate
```

## Next Steps

1. Review the [Technical Strategy](technical-strategy.md)
2. Check your [Team Role](team.md)
3. Start working on your assigned module
4. Join the team communication channel

## Resources

- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [Gazebo Tutorials](https://gazebosim.org/docs)
- [MoveIt2 Tutorials](https://moveit.picknik.ai/main/index.html)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)

---

*For team-specific setup instructions, check the internal wiki.*
