#!/usr/bin/env python3
"""
move_arm  -  ROS 2 node that moves the 3-DOF arm from HOME to a TARGET point.

It (1) reads a target (x, y, z) from parameters, (2) solves inverse kinematics
to get the three joint angles, (3) prints a forward-kinematics check so you can
see the solution really lands on the target, and (4) smoothly animates the arm
there.

Two output modes:

  * RViz mode  (default, use_controller:=false)
      Publishes sensor_msgs/JointState on /joint_states. robot_state_publisher
      turns those joint angles into TF frames, and RViz draws the arm moving.
      No physics / controllers needed - simplest and most reliable to record.

  * Gazebo mode (use_controller:=true)
      Publishes a trajectory_msgs/JointTrajectory to
      /arm_controller/joint_trajectory, so a ros2_control controller drives the
      joints inside the Gazebo physics simulation.

Parameters (all have defaults):
    target_x, target_y, target_z : target point in metres      (0.30, 0.15, 0.20)
    elbow_up                     : pick elbow-up IK solution    (true)
    move_duration                : seconds Home -> Target       (4.0)
    publish_rate                 : Hz for the RViz animation    (50.0)
    use_controller               : Gazebo trajectory mode       (false)
"""

import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

from arm3dof.ik import inverse_kinematics, forward_kinematics

JOINT_NAMES = ["base_yaw", "shoulder_pitch", "elbow_pitch"]
HOME = [0.0, 0.0, 0.0]          # arm pointing straight up


def smoothstep(u):
    """Ease-in/ease-out blend factor for u in [0, 1] (0->0, 1->1)."""
    u = max(0.0, min(1.0, u))
    return u * u * (3.0 - 2.0 * u)


class MoveArm(Node):
    def __init__(self):
        super().__init__("move_arm")

        # --- parameters ---
        self.declare_parameter("target_x", 0.30)
        self.declare_parameter("target_y", 0.15)
        self.declare_parameter("target_z", 0.20)
        self.declare_parameter("elbow_up", True)
        self.declare_parameter("move_duration", 4.0)
        self.declare_parameter("publish_rate", 50.0)
        self.declare_parameter("use_controller", False)

        tx = self.get_parameter("target_x").value
        ty = self.get_parameter("target_y").value
        tz = self.get_parameter("target_z").value
        elbow_up = self.get_parameter("elbow_up").value
        self.duration = float(self.get_parameter("move_duration").value)
        self.use_controller = bool(self.get_parameter("use_controller").value)
        rate = float(self.get_parameter("publish_rate").value)

        # --- solve inverse kinematics ---
        try:
            self.target_q = list(inverse_kinematics(tx, ty, tz, elbow_up=elbow_up))
        except ValueError as exc:
            self.get_logger().error(str(exc))
            self.get_logger().warn("Holding at HOME because the target is unreachable.")
            self.target_q = list(HOME)

        # --- report the solution and verify it with forward kinematics ---
        check = forward_kinematics(*self.target_q)
        err = math.dist((tx, ty, tz), check)
        self.get_logger().info(
            f"Target (x,y,z) = ({tx:.3f}, {ty:.3f}, {tz:.3f}) m")
        self.get_logger().info(
            "IK solution (deg): "
            f"base_yaw={math.degrees(self.target_q[0]):.1f}, "
            f"shoulder_pitch={math.degrees(self.target_q[1]):.1f}, "
            f"elbow_pitch={math.degrees(self.target_q[2]):.1f}")
        self.get_logger().info(
            f"FK check: tip lands at ({check[0]:.3f}, {check[1]:.3f}, "
            f"{check[2]:.3f}) m  ->  error {err*1000:.3f} mm")

        if self.use_controller:
            self._start_controller_mode()
        else:
            self._start_rviz_mode(rate)

    # ---------------- RViz mode: publish /joint_states ----------------
    def _start_rviz_mode(self, rate):
        self.pub = self.create_publisher(JointState, "/joint_states", 10)
        self.start_time = self.get_clock().now()
        self.timer = self.create_timer(1.0 / rate, self._tick)
        self.get_logger().info("RViz mode: animating on /joint_states ...")

    def _tick(self):
        elapsed = (self.get_clock().now() - self.start_time).nanoseconds * 1e-9
        alpha = smoothstep(elapsed / self.duration) if self.duration > 0 else 1.0
        positions = [HOME[i] + alpha * (self.target_q[i] - HOME[i]) for i in range(3)]

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = JOINT_NAMES
        msg.position = positions
        self.pub.publish(msg)

        if elapsed >= self.duration and not getattr(self, "_arrived", False):
            self._arrived = True
            self.get_logger().info("Arrived at target. (Still publishing to hold pose.)")

    # ------------- Gazebo mode: publish a JointTrajectory -------------
    def _start_controller_mode(self):
        self.pub = self.create_publisher(
            JointTrajectory, "/arm_controller/joint_trajectory", 10)
        # Give the controller a moment to come up, then send a couple of times.
        self._sent = 0
        self.timer = self.create_timer(1.0, self._send_trajectory)
        self.get_logger().info(
            "Gazebo mode: sending trajectory to /arm_controller/joint_trajectory ...")

    def _send_trajectory(self):
        traj = JointTrajectory()
        traj.joint_names = JOINT_NAMES

        p = JointTrajectoryPoint()
        p.positions = list(self.target_q)
        secs = int(self.duration)
        p.time_from_start = Duration(sec=secs,
                                     nanosec=int((self.duration - secs) * 1e9))
        traj.points.append(p)

        self.pub.publish(traj)
        self._sent += 1
        if self._sent >= 3:
            self.get_logger().info("Trajectory sent. Shutting node down.")
            self.timer.cancel()
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = MoveArm()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == "__main__":
    main()
