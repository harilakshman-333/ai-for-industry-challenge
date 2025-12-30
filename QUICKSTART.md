# AI for Industry Challenge - Quick Start Guide

## 🚀 Getting Started

### 1. Build and Run Docker Container

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Build and run container
./scripts/run_docker.sh
```

This will:
- Build the Docker image with ROS 2 Humble, Gazebo, and all dependencies
- Start the container with GUI support
- Drop you into a bash shell inside the container

### 2. Build ROS 2 Workspace

Inside the container:

```bash
# Build workspace
./scripts/build_workspace.sh

# Source workspace
source install/setup.bash
```

### 3. Launch Simulation

```bash
# Launch Gazebo simulation with all nodes
ros2 launch cable_insertion simulation.launch.py
```

This starts:
- Gazebo with cable insertion world
- Perception node (classical CV + deep learning)
- Planning node (MoveIt2)
- Control node (hybrid position/force)
- Safety monitor
- RViz for visualization

## 📁 Project Structure

```
ai-for-industry-challenge/
├── Dockerfile                 # Docker environment
├── docker-compose.yml         # Docker Compose configuration
├── src/
│   └── cable_insertion/       # Main ROS 2 package
│       ├── scripts/           # Python nodes
│       │   ├── perception_node.py
│       │   ├── planning_node.py
│       │   ├── control_node.py
│       │   ├── safety_monitor.py
│       │   └── rl_policy_node.py
│       ├── launch/            # Launch files
│       ├── worlds/            # Gazebo worlds
│       ├── config/            # Configuration files
│       └── models/            # Robot/object models
├── scripts/                   # Helper scripts
│   ├── run_docker.sh
│   ├── build_workspace.sh
│   └── train_sac.py          # RL training
├── data/                      # Training data
├── models/                    # Trained models
└── logs/                      # Training logs
```

## 🎯 Development Workflow

### Phase 1: Baseline System (Weeks 1-4)

1. **Test perception:**
   ```bash
   ros2 run cable_insertion perception_node.py
   ros2 topic echo /perception/connector_pose
   ```

2. **Test planning:**
   ```bash
   ros2 run cable_insertion planning_node.py
   ```

3. **Test control:**
   ```bash
   ros2 run cable_insertion control_node.py
   ```

4. **Monitor safety:**
   ```bash
   ros2 topic echo /safety/status
   ```

### Phase 2: Train Deep Learning Models (Weeks 5-8)

1. **Generate training data:**
   ```bash
   # TODO: Create data generation script
   python3 scripts/generate_data.py
   ```

2. **Train perception model:**
   ```bash
   # TODO: Create training script
   python3 scripts/train_perception.py
   ```

3. **Train RL policy:**
   ```bash
   python3 scripts/train_sac.py
   ```

4. **Evaluate models:**
   ```bash
   # TODO: Create evaluation script
   python3 scripts/evaluate.py
   ```

### Phase 3: Optimization (Weeks 9-10)

1. **Run benchmarks:**
   ```bash
   # TODO: Create benchmark script
   python3 scripts/benchmark.py
   ```

2. **Optimize hyperparameters:**
   ```bash
   # TODO: Create optimization script
   python3 scripts/optimize.py
   ```

3. **Test submission:**
   ```bash
   # TODO: Create submission script
   python3 scripts/submit.py
   ```

## 🔧 Configuration

### Perception Node Parameters

```yaml
perception_node:
  use_deep_learning: true
  model_path: "/workspace/models/pose_estimator.pth"
  confidence_threshold: 0.7
```

### Control Node Parameters

```yaml
control_node:
  control_mode: "position"  # or "force"
  target_force: 5.0  # Newtons
  force_kp: 0.1
  force_ki: 0.01
  force_kd: 0.05
  max_velocity: 0.5  # m/s
```

### Safety Monitor Parameters

```yaml
safety_monitor:
  max_force: 10.0  # Newtons
  max_velocity: 0.5  # m/s
  max_torque: 5.0  # Nm
  check_rate: 100.0  # Hz
```

## 📊 Monitoring

### View Topics

```bash
# List all topics
ros2 topic list

# Monitor perception
ros2 topic echo /perception/connector_pose

# Monitor planning status
ros2 topic echo /planning/status

# Monitor safety
ros2 topic echo /safety/status
```

### Visualize in RViz

RViz is automatically launched with the simulation. You can:
- View camera feeds
- See robot state
- Visualize planned trajectories
- Monitor TF transforms

### TensorBoard (for training)

```bash
tensorboard --logdir logs/
```

## 🐛 Troubleshooting

### Docker Issues

**Problem:** GUI not showing
```bash
# Allow X server access
xhost +local:docker
```

**Problem:** Container won't start
```bash
# Check Docker logs
docker logs ai_challenge_dev

# Rebuild container
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### ROS 2 Issues

**Problem:** Nodes not communicating
```bash
# Check ROS domain
echo $ROS_DOMAIN_ID

# List nodes
ros2 node list

# Check node info
ros2 node info /perception_node
```

**Problem:** Build errors
```bash
# Clean build
rm -rf build install log
colcon build --symlink-install
```

### Gazebo Issues

**Problem:** Gazebo crashes
```bash
# Check GPU drivers
nvidia-smi

# Run without GUI
ros2 launch cable_insertion simulation.launch.py gui:=false
```

## 📚 Useful Commands

```bash
# Build specific package
colcon build --packages-select cable_insertion

# Run tests
colcon test

# Clean workspace
rm -rf build install log

# Check dependencies
rosdep check --from-paths src --ignore-src

# Install dependencies
rosdep install --from-paths src --ignore-src -y
```

## 🎯 Next Steps

1. ✅ Set up environment
2. ✅ Test simulation
3. ⬜ Implement baseline perception
4. ⬜ Integrate MoveIt2
5. ⬜ Train deep learning models
6. ⬜ Train RL policy
7. ⬜ Optimize and submit

## 📖 Documentation

- [Competition Overview](docs/competition-overview.md)
- [Technical Strategy](docs/technical-strategy.md)
- [Winning Strategy](/home/kwalker96/.gemini/antigravity/brain/30d2fc12-9f69-450a-8296-92c0a4f60582/implementation_plan.md)
- [Setup Guide](docs/setup.md)

## 🆘 Getting Help

- Check the [troubleshooting section](#troubleshooting)
- Review ROS 2 logs: `ros2 run rqt_console rqt_console`
- Check Gazebo logs: `~/.gazebo/`
- Review Docker logs: `docker logs ai_challenge_dev`

---

**Good luck! Let's win this competition! 🏆**
