# AI for Industry Challenge - Development Environment
FROM osrf/ros:humble-desktop-full

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble
ENV WORKSPACE=/workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-vcstool \
    git \
    wget \
    curl \
    vim \
    nano \
    build-essential \
    cmake \
    libopencv-dev \
    python3-opencv \
    libpcl-dev \
    ros-${ROS_DISTRO}-gazebo-ros-pkgs \
    ros-${ROS_DISTRO}-moveit \
    ros-${ROS_DISTRO}-controller-manager \
    ros-${ROS_DISTRO}-joint-state-publisher \
    ros-${ROS_DISTRO}-robot-state-publisher \
    ros-${ROS_DISTRO}-xacro \
    ros-${ROS_DISTRO}-rviz2 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip first
RUN pip3 install --upgrade pip

# Install Python packages for ML/AI
RUN pip3 install --no-cache-dir \
    numpy \
    scipy \
    matplotlib \
    scikit-learn \
    pandas \
    opencv-contrib-python \
    transforms3d

# Install PyTorch (CPU version) - ignore system packages to avoid conflicts
RUN pip3 install --no-cache-dir --ignore-installed sympy \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install RL and visualization packages
RUN pip3 install --no-cache-dir \
    tensorboard \
    gymnasium \
    stable-baselines3[extra]

# Install 3D visualization (optional, can be heavy)
RUN pip3 install --no-cache-dir open3d || echo "open3d installation skipped"

# Create workspace
RUN mkdir -p ${WORKSPACE}/src

# Set working directory
WORKDIR ${WORKSPACE}

# Initialize rosdep
RUN rosdep update

# Source ROS setup in bashrc
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc
RUN echo "source ${WORKSPACE}/install/setup.bash 2>/dev/null || true" >> ~/.bashrc

# Set up display for Gazebo/RViz
ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1

# Default command
CMD ["/bin/bash"]
