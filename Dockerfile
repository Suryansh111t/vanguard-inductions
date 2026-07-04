# Base: ROS 2 Humble + XFCE desktop + noVNC, all in one container.
# Source: https://github.com/Tiryoh/docker-ros2-desktop-vnc
FROM tiryoh/ros2-desktop-vnc:humble

USER root

# ---- Task 1: 3DOF Arm & Inverse Kinematics ----
# Xacro/URDF tooling, Gazebo Classic + ros2_control, MoveIt2 for IK/motion planning
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-xacro \
    ros-humble-joint-state-publisher \
    ros-humble-joint-state-publisher-gui \
    ros-humble-robot-state-publisher \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-gazebo-ros2-control \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-moveit \
    ros-humble-rviz2 \
    && rm -rf /var/lib/apt/lists/*

# ---- Turtlesim tasks (kept from the original induction pattern, if you reuse it) ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-turtlesim \
    ros-humble-teleop-twist-keyboard \
    && rm -rf /var/lib/apt/lists/*

# ---- Task 2 & 3: Kalman Filter + Panorama stitching (pure Python/CV, no ROS needed) ----
RUN pip3 install --no-cache-dir \
    numpy \
    matplotlib \
    scipy \
    opencv-contrib-python

# Pre-create the workspace + per-task source folders so bind-mounts land in a
# predictable place (these get overlaid by the tasks/taskN host folders at runtime)
RUN mkdir -p /home/ubuntu/vanguard_ws/src/task1 \
             /home/ubuntu/vanguard_ws/src/task2 \
             /home/ubuntu/vanguard_ws/src/task3

WORKDIR /home/ubuntu/vanguard_ws
