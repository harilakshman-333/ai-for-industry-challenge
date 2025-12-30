# Technical Strategy

## 🎯 Overview

This document outlines our comprehensive technical approach to winning the AI for Industry Challenge Qualification round.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Perception Module                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ RGB-D Camera │  │ Pose Estimator│  │Cable Tracker │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         └──────────────────┴──────────────────┘              │
└─────────────────────────┬───────────────────────────────────┘
                          │ State Estimate
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Planning Module                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Motion Planner│  │  RL Policy   │  │Force Planner │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         └──────────────────┴──────────────────┘              │
└─────────────────────────┬───────────────────────────────────┘
                          │ Action Commands
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     Control Module                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Joint Control │  │Force Control │  │Safety Monitor│      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         └──────────────────┴──────────────────┘              │
└─────────────────────────┬───────────────────────────────────┘
                          │ Motor Commands
                          ▼
                    ┌──────────┐
                    │  Robot   │
                    └──────────┘
```

## 🔍 Module 1: Perception

### Objectives
- Detect cable and connector poses with < 2mm accuracy
- Track cable deformation in real-time
- Operate at ≥ 20 Hz for control loop

### Approach

#### Classical Computer Vision Pipeline
```python
class ClassicalPerception:
    def __init__(self):
        self.color_segmenter = ColorSegmenter()
        self.edge_detector = CannyEdgeDetector()
        self.pose_estimator = PnPSolver()
    
    def process(self, rgb_image, depth_image):
        # Segment cable and connector
        cable_mask = self.color_segmenter.segment(rgb_image, 'cable')
        connector_mask = self.color_segmenter.segment(rgb_image, 'connector')
        
        # Detect edges for fine alignment
        edges = self.edge_detector.detect(rgb_image)
        
        # Estimate 3D pose using depth
        cable_pose = self.pose_estimator.estimate(
            cable_mask, depth_image
        )
        connector_pose = self.pose_estimator.estimate(
            connector_mask, depth_image
        )
        
        return cable_pose, connector_pose
```

#### Deep Learning Pipeline
```python
class LearnedPerception:
    def __init__(self):
        self.pose_network = PoseEstimationNetwork()
        self.cable_tracker = DeformableObjectTracker()
    
    def process(self, rgb_image, depth_image):
        # Concatenate RGB-D
        rgbd = torch.cat([rgb_image, depth_image], dim=0)
        
        # Predict poses
        predictions = self.pose_network(rgbd)
        
        # Track cable deformation
        cable_points = self.cable_tracker.track(
            rgb_image, predictions['cable_mask']
        )
        
        return {
            'connector_pose': predictions['connector_pose'],
            'cable_shape': cable_points,
            'confidence': predictions['confidence']
        }
```

### Training Strategy
1. **Synthetic Data Generation**
   - Randomize cable configurations in simulation
   - Vary lighting conditions
   - Add sensor noise
   - Generate 50k+ training samples

2. **Data Augmentation**
   - Random rotations, translations
   - Color jittering
   - Gaussian noise on depth
   - Occlusion simulation

3. **Loss Functions**
   ```python
   loss = (
       pose_loss(pred_pose, gt_pose) +
       0.5 * shape_loss(pred_shape, gt_shape) +
       0.1 * confidence_loss(pred_conf, success)
   )
   ```

## 🗺️ Module 2: Planning

### Motion Planning with MoveIt2

```python
class MotionPlanner:
    def __init__(self):
        self.moveit = MoveItInterface()
        self.planner = "RRTConnect"
    
    def plan_to_grasp(self, target_pose):
        # Set target pose
        self.moveit.set_pose_target(target_pose)
        
        # Plan collision-free trajectory
        plan = self.moveit.plan()
        
        if plan.success:
            return plan.trajectory
        else:
            # Fallback: try different planner
            self.planner = "RRTstar"
            return self.moveit.plan().trajectory
```

### Reinforcement Learning Policy

#### State Space
```python
state = {
    'connector_pose': np.array([x, y, z, qx, qy, qz, qw]),  # 7D
    'target_pose': np.array([x, y, z, qx, qy, qz, qw]),     # 7D
    'cable_points': np.array([...]),                         # Nx3
    'robot_joints': np.array([...]),                         # 7D
    'force_torque': np.array([fx, fy, fz, tx, ty, tz]),     # 6D
    'gripper_state': float                                   # 1D
}
```

#### Action Space
```python
action = {
    'end_effector_delta': np.array([dx, dy, dz, drx, dry, drz]),  # 6D
    'gripper_command': float  # 0-1
}
```

#### Reward Function
```python
def compute_reward(state, action, next_state):
    # Success bonus
    if task_successful(next_state):
        return 100.0
    
    # Distance to target
    dist_reward = -np.linalg.norm(
        state['connector_pose'][:3] - state['target_pose'][:3]
    )
    
    # Orientation alignment
    orient_reward = orientation_similarity(
        state['connector_pose'][3:], state['target_pose'][3:]
    )
    
    # Collision penalty
    collision_penalty = -50.0 if has_collision(next_state) else 0.0
    
    # Force penalty
    force_penalty = -np.clip(
        np.linalg.norm(state['force_torque']) - 5.0, 0, 10
    )
    
    # Time penalty (encourage efficiency)
    time_penalty = -0.1
    
    return (
        dist_reward + 
        5.0 * orient_reward + 
        collision_penalty + 
        force_penalty + 
        time_penalty
    )
```

#### Training Algorithm: SAC (Soft Actor-Critic)
```python
class SACAgent:
    def __init__(self, state_dim, action_dim):
        self.actor = ActorNetwork(state_dim, action_dim)
        self.critic1 = CriticNetwork(state_dim, action_dim)
        self.critic2 = CriticNetwork(state_dim, action_dim)
        self.target_critic1 = copy.deepcopy(self.critic1)
        self.target_critic2 = copy.deepcopy(self.critic2)
        
    def train(self, replay_buffer, batch_size=256):
        # Sample batch
        states, actions, rewards, next_states, dones = \
            replay_buffer.sample(batch_size)
        
        # Update critics
        with torch.no_grad():
            next_actions, next_log_probs = self.actor(next_states)
            target_q1 = self.target_critic1(next_states, next_actions)
            target_q2 = self.target_critic2(next_states, next_actions)
            target_q = torch.min(target_q1, target_q2)
            target_q = rewards + (1 - dones) * 0.99 * (
                target_q - self.alpha * next_log_probs
            )
        
        # Critic loss
        q1 = self.critic1(states, actions)
        q2 = self.critic2(states, actions)
        critic_loss = F.mse_loss(q1, target_q) + F.mse_loss(q2, target_q)
        
        # Update actor
        new_actions, log_probs = self.actor(states)
        q1_new = self.critic1(states, new_actions)
        q2_new = self.critic2(states, new_actions)
        q_new = torch.min(q1_new, q2_new)
        actor_loss = (self.alpha * log_probs - q_new).mean()
        
        return critic_loss, actor_loss
```

## 🎮 Module 3: Control

### Hybrid Control Strategy

```python
class HybridController:
    def __init__(self):
        self.position_controller = PositionController()
        self.force_controller = ForceController()
        self.mode = 'position'  # or 'force'
    
    def compute_command(self, state, target):
        if self.mode == 'position':
            # Use position control for approach
            cmd = self.position_controller.compute(state, target)
            
            # Switch to force control near insertion
            if self.near_insertion(state, target):
                self.mode = 'force'
        
        else:  # force mode
            # Use compliant force control for insertion
            cmd = self.force_controller.compute(state, target)
            
            # Monitor for completion or failure
            if self.insertion_complete(state):
                self.mode = 'position'
        
        return cmd
```

### Force Control for Insertion
```python
class ForceController:
    def __init__(self):
        self.target_force = 5.0  # Newtons
        self.kp = 0.1
        self.ki = 0.01
        self.kd = 0.05
        self.integral = 0.0
        self.prev_error = 0.0
    
    def compute(self, state, target):
        # Measure current force
        current_force = np.linalg.norm(state['force_torque'][:3])
        
        # PID control
        error = self.target_force - current_force
        self.integral += error
        derivative = error - self.prev_error
        
        force_adjustment = (
            self.kp * error +
            self.ki * self.integral +
            self.kd * derivative
        )
        
        self.prev_error = error
        
        # Compute velocity command
        direction = self.compute_insertion_direction(state, target)
        velocity = direction * force_adjustment
        
        return velocity
```

## 🛡️ Module 4: Safety

### Safety Monitor
```python
class SafetyMonitor:
    def __init__(self):
        self.max_force = 10.0  # Newtons
        self.max_velocity = 0.5  # m/s
        self.workspace_bounds = [...]
    
    def check_safety(self, state, command):
        violations = []
        
        # Force limit
        if np.linalg.norm(state['force_torque'][:3]) > self.max_force:
            violations.append('FORCE_EXCEEDED')
        
        # Velocity limit
        if np.linalg.norm(command['velocity']) > self.max_velocity:
            violations.append('VELOCITY_EXCEEDED')
        
        # Workspace bounds
        if not self.in_workspace(state['robot_pose']):
            violations.append('WORKSPACE_VIOLATION')
        
        # Collision check
        if self.collision_detected(state):
            violations.append('COLLISION')
        
        if violations:
            return False, violations
        return True, []
    
    def emergency_stop(self):
        # Send zero velocity command
        return {'velocity': np.zeros(6), 'gripper': 'hold'}
```

## 📊 Module 5: Evaluation & Testing

### Benchmarking Framework
```python
class BenchmarkSuite:
    def __init__(self):
        self.scenarios = self.load_scenarios()
        self.metrics = MetricsCollector()
    
    def run_benchmark(self, policy):
        results = []
        
        for scenario in self.scenarios:
            # Reset environment
            env = self.create_env(scenario)
            state = env.reset()
            
            # Run episode
            done = False
            episode_data = []
            
            while not done:
                action = policy.predict(state)
                next_state, reward, done, info = env.step(action)
                episode_data.append({
                    'state': state,
                    'action': action,
                    'reward': reward,
                    'info': info
                })
                state = next_state
            
            # Compute metrics
            metrics = self.metrics.compute(episode_data)
            results.append({
                'scenario': scenario,
                'success': info['success'],
                'metrics': metrics
            })
        
        return self.aggregate_results(results)
```

### Key Metrics
```python
class MetricsCollector:
    def compute(self, episode_data):
        return {
            'success': self.check_success(episode_data),
            'cycle_time': self.compute_cycle_time(episode_data),
            'precision_error': self.compute_precision(episode_data),
            'collision_count': self.count_collisions(episode_data),
            'force_violations': self.count_force_violations(episode_data),
            'path_efficiency': self.compute_path_efficiency(episode_data)
        }
```

## 🔄 Integration & Pipeline

### Main Control Loop
```python
class CableInsertionSystem:
    def __init__(self):
        self.perception = LearnedPerception()
        self.planner = MotionPlanner()
        self.rl_policy = SACAgent.load('best_model.pth')
        self.controller = HybridController()
        self.safety = SafetyMonitor()
    
    def execute_task(self):
        # Phase 1: Perception
        state = self.perception.process(
            self.get_rgb_image(),
            self.get_depth_image()
        )
        
        # Phase 2: Planning
        if self.use_rl:
            action = self.rl_policy.predict(state)
        else:
            trajectory = self.planner.plan_to_grasp(
                state['connector_pose']
            )
            action = trajectory.get_next_waypoint()
        
        # Phase 3: Safety check
        safe, violations = self.safety.check_safety(state, action)
        if not safe:
            action = self.safety.emergency_stop()
        
        # Phase 4: Control
        command = self.controller.compute_command(state, action)
        
        # Phase 5: Execute
        self.robot.execute(command)
        
        return state, action, command
```

## 🎯 Success Criteria

| Metric | Target | Stretch Goal |
|--------|--------|--------------|
| Success Rate | > 85% | > 95% |
| Precision Error | < 3mm | < 2mm |
| Collision Rate | < 5% | < 2% |
| Cycle Time | < 15s | < 10s |
| Force Violations | < 5% | < 1% |

## 📈 Development Priorities

1. **Week 1-2:** Baseline perception + simple planner → 50% success
2. **Week 3-5:** Learned perception → 70% success
3. **Week 6-8:** RL policy + force control → 85% success
4. **Week 9-10:** Optimization + safety tuning → 90%+ success

---

For implementation details, see the [Setup Guide](setup.md) and module-specific documentation.
