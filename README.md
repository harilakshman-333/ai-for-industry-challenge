# AI for Industry Challenge

[![Competition](https://img.shields.io/badge/Competition-Intrinsic-blue)](https://www.intrinsic.ai/events/ai-for-industry-challenge)
[![Prize Pool](https://img.shields.io/badge/Prize%20Pool-$180k-green)](https://www.intrinsic.ai/events/ai-for-industry-challenge)
[![Status](https://img.shields.io/badge/Status-Registration%20Open-orange)](https://www.intrinsic.ai/events/ai-for-industry-challenge)

A robotics and AI competition project for solving real-world industrial cable handling and connector insertion tasks.

## 🎯 Challenge Overview

The **AI for Industry Challenge** is an open competition organized by **Intrinsic** in partnership with **Open Robotics** to solve dexterous manipulation problems in electronics assembly — specifically **cable handling and connector insertion**.

### Key Dates

- **Registration Deadline:** April 17, 2026
- **Challenge Start:** February 11, 2026
- **Duration:** ~6 months (Feb–July/Aug 2026)

### Prize Pool: $180,000

- 🥇 **1st Place:** $100,000
- 🥈 **2nd Place:** $40,000
- 🥉 **3rd Place:** $20,000
- 🏅 **4th & 5th:** $10,000 each

## 🏗️ Challenge Structure

### Phase 0: Qualification (Simulation)
Train an AI model to handle cable manipulation in simulation using open-source tools (Gazebo, Isaac Sim, MuJoCo) and standard robotics interfaces (ROS).

### Phase 1: Development in Flowstate
Qualified teams gain access to **Intrinsic Flowstate** development environment and the **Intrinsic Vision Model** (IVM) to build complete solutions.

### Phase 2: Real Robot Deployment
Top teams deploy and test their solutions on physical robot workcells at Intrinsic's headquarters.

## 🎯 Technical Challenge

### The Task
Develop a robotic system capable of:
- **Perception:** Identifying cable and connector poses
- **Motion Control:** Precisely guiding the robot to manipulate cables
- **Insertion:** Aligning and inserting connectors with minimal collisions

### Evaluation Criteria
- ✅ **Model Validity:** Valid commands without errors
- ✅ **Task Success:** Successful cable insertions
- ✅ **Precision:** Accurate connector placement
- ✅ **Safety:** Minimal collisions and forces
- ✅ **Efficiency:** Fast cycle times

## 🛠️ Technology Stack

### Core Tools
- **ROS** (Robot Operating System) for communication
- **Gazebo** for baseline simulation
- **NVIDIA Isaac Sim** or **MuJoCo** for advanced training
- **Intrinsic Flowstate** for development & integration
- **Intrinsic Vision Model (IVM)** for perception

### Development Areas
- Simulation & Environment Setup
- Perception Module (Computer Vision + ML)
- Planning & Control (Motion Planning + RL)
- Safety & Efficiency Optimization

## 📋 Project Roadmap

| Week | Focus |
|------|-------|
| 1–2  | Registration + Simulation Setup (Gazebo/ROS) |
| 2–5  | Perception Model Development |
| 4–8  | Planner + Controller + RL Policy |
| 8–9  | Safety & Efficiency Tuning |
| 9–10 | Testing, Benchmarking & Submissions |

## 🧠 Technical Strategy

### 1. Perception Module
- Classical computer vision (OpenCV, edge detection, depth heuristics)
- Learned perception (deep networks with RGB-D input)
- Pose estimation for connectors and cable segments

### 2. Planning & Control
- **Motion Planning:** MoveIt2 for collision-aware trajectories
- **Feedback Control:** Closed-loop control with force/torque feedback
- **Learning-based Policy:** RL policy for adaptive manipulation

### 3. Safety & Efficiency
- Force thresholds to detect abnormal contact
- Collision avoidance constraints
- Optimized cycle times through parallel processing

## 👥 Team Structure

Maximum team size: **10 people**

Recommended roles:
- Simulation Engineer (ROS & Gazebo)
- Perception Specialist (Vision + ML)
- Control & Planning Engineer
- Reinforcement Learning Specialist
- Team Lead (manages submissions)

## 📚 Resources

- [Official Challenge Page](https://www.intrinsic.ai/events/ai-for-industry-challenge)
- [Intrinsic LinkedIn Announcement](https://www.linkedin.com/posts/intrinsic_iccv2025-intrinsic-aiforindustrychallenge-activity-7388603592573808640-x0R0)

## 🚀 Getting Started

1. **Register for the challenge** (by April 17, 2026)
2. **Set up development environment** (ROS + Gazebo)
3. **Install challenge toolkit** (scene descriptions, robot models)
4. **Begin perception module development**
5. **Develop planning and control systems**
6. **Test and iterate** on simulation benchmarks

## 📝 License

This project is developed for the AI for Industry Challenge competition.

---

**Note:** Participants must be 18+ and meet U.S. export control/sanctions requirements.
