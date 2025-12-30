# Competition Overview

## 🤖 What is the AI for Industry Challenge?

The **AI for Industry Challenge** is an open competition for developers, roboticists, and AI practitioners to solve a real-world industrial robotics problem involving **dexterous manipulation** — specifically **cable handling and connector insertion in electronics assembly**.

These tasks are extremely challenging for robots due to:
- Complex physics of deformable objects (cables)
- High precision requirements for connector insertion
- Need for robust perception in industrial environments
- Safety constraints to avoid damage

## 🎯 Challenge Objectives

The competition is designed to:
1. **Push the boundary of AI + robotics** by bridging simulation and real-world deployment
2. **Advance industrial automation** in electronics manufacturing
3. **Foster innovation** in perception, planning, and control for dexterous manipulation
4. **Build practical solutions** that can transfer from simulation to real robots

## 📅 Timeline

| Date | Event |
|------|-------|
| **April 17, 2026** | Registration deadline |
| **February 11, 2026** | Challenge begins |
| **~6 months** | Total competition duration |
| **July/August 2026** | Final phase & winners announced |

## 🏗️ Three-Phase Structure

### 🥇 Qualification Round (Simulation)

**Goal:** Train an AI model to handle cable manipulation in simulation

**What you'll do:**
- Develop perception, planning, and control systems
- Train models using open-source simulators (Gazebo, Isaac Sim, MuJoCo)
- Use standard robotics interfaces (ROS 2)
- Submit solutions for automated evaluation

**Evaluation:**
- Model validity (no errors, valid commands)
- Task success rate
- Precision of connector placement
- Safety (collision avoidance)
- Efficiency (cycle time)

**Deliverable:** Working simulation-based solution

---

### 🥈 Phase 1: Development in Flowstate

**Goal:** Build complete solution using Intrinsic's development tools

**What you'll get:**
- Access to **Intrinsic Flowstate** development environment
- **Intrinsic Vision Model (IVM)** for industrial perception
- Advanced development and debugging tools

**What you'll do:**
- Integrate your trained models with Flowstate
- Leverage IVM for robust perception
- Refine and optimize your solution
- Prepare for real-world deployment

**Who qualifies:** Top teams from Qualification round

---

### 🥉 Phase 2: Real Robot Deployment

**Goal:** Deploy and validate solution on physical hardware

**What you'll do:**
- Test your solution on real robot workcells
- Validate sim-to-real transfer
- Demonstrate performance on actual hardware
- Compete for final rankings

**Where:** Intrinsic headquarters

**Who qualifies:** Top teams from Phase 1

## 🎯 The Technical Challenge

### Task Description

Develop a robotic system that can:

1. **Perceive** the environment
   - Identify cable positions and orientations
   - Detect connector poses
   - Track deformable cable shapes

2. **Plan** manipulation strategies
   - Generate collision-free trajectories
   - Handle cable deformation
   - Adapt to varying configurations

3. **Execute** precise insertions
   - Align connectors accurately
   - Apply appropriate forces
   - Avoid collisions and damage

### Why This is Hard

**Deformable Objects:** Cables don't behave like rigid bodies — they bend, twist, and have unpredictable dynamics.

**High Precision:** Connector insertion requires sub-millimeter accuracy and precise orientation alignment.

**Safety Critical:** Excessive forces can damage connectors or the robot itself.

**Perception Challenges:** Cables can be occluded, have varying appearances, and are difficult to track.

**Sim-to-Real Gap:** Solutions must transfer from simulation to physical robots.

## 📊 Evaluation Criteria

Your solution will be scored on:

| Criterion | Description | Weight |
|-----------|-------------|--------|
| **Model Validity** | Generates valid, error-free commands | Required |
| **Task Success** | Percentage of successful insertions | High |
| **Precision** | Accuracy of connector placement | High |
| **Safety** | Collision avoidance, force limits | High |
| **Efficiency** | Cycle time, speed of execution | Medium |

**Note:** All criteria must be balanced — a fast but unsafe solution will score poorly.

## 🏆 Prizes

Total prize pool: **$180,000**

| Place | Prize |
|-------|-------|
| 🥇 1st | $100,000 |
| 🥈 2nd | $40,000 |
| 🥉 3rd | $20,000 |
| 🏅 4th | $10,000 |
| 🏅 5th | $10,000 |

## 👥 Eligibility

### Who Can Participate
- Developers, researchers, robotics teams
- Individuals (must use team name)
- Teams up to **10 people**

### Requirements
- Must be **18 years or older**
- Must meet **U.S. export control/sanctions requirements**
- Certain countries may be restricted based on U.S. law

## 🛠️ Tools & Technologies

### Provided by Challenge
- Scene descriptions and task specifications
- Robot models (URDF/SDF)
- Sensor models
- Standardized ROS 2 interfaces
- Baseline controllers
- Evaluation framework

### Your Choice
- **Simulators:** Gazebo (baseline), Isaac Sim, MuJoCo
- **ML Frameworks:** PyTorch, TensorFlow, JAX
- **Planning:** MoveIt2, OMPL, custom planners
- **Perception:** OpenCV, PCL, custom vision models

### Phase 1+ Only
- Intrinsic Flowstate
- Intrinsic Vision Model (IVM)

## 📚 Key Resources

- **Official Challenge Page:** [intrinsic.ai/events/ai-for-industry-challenge](https://www.intrinsic.ai/events/ai-for-industry-challenge)
- **ROS 2 Documentation:** [docs.ros.org](https://docs.ros.org/en/humble/)
- **Gazebo Tutorials:** [gazebosim.org](https://gazebosim.org/docs)
- **MoveIt2:** [moveit.picknik.ai](https://moveit.picknik.ai/)

## 🎓 What You'll Learn

Participating in this challenge will give you experience with:
- Industrial robotics and automation
- Sim-to-real transfer techniques
- Dexterous manipulation
- Perception for deformable objects
- Reinforcement learning for robotics
- Production-grade robotics development tools

## 🚀 Why Participate?

✅ **Real-world impact** — solve actual industrial problems
✅ **Significant prizes** — $180k total prize pool
✅ **Cutting-edge tools** — access to Intrinsic's platform
✅ **Career opportunities** — showcase skills to industry leaders
✅ **Learning experience** — work with state-of-the-art robotics
✅ **Networking** — connect with robotics community

---

Ready to get started? Check out our [Technical Strategy](technical-strategy.md) and [Setup Guide](setup.md)!
