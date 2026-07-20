"""
display.launch.py  -  Show the arm in RViz2 and move it to the target.

Starts:
  * robot_state_publisher  - reads the URDF, turns /joint_states into TF frames
  * rviz2                  - the 3D viewer (pre-loaded with rviz/arm.rviz)
  * either the move_arm node (default) OR joint_state_publisher_gui

Usage:
  ros2 launch arm3dof display.launch.py
  ros2 launch arm3dof display.launch.py target_x:=0.25 target_y:=-0.1 target_z:=0.3
  ros2 launch arm3dof display.launch.py use_gui:=true      # drag joints by hand
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory("arm3dof")
    urdf_path = os.path.join(pkg, "urdf", "arm3dof.urdf")
    rviz_path = os.path.join(pkg, "rviz", "arm.rviz")

    # Read the URDF file into the robot_description parameter.
    with open(urdf_path, "r") as f:
        robot_description = f.read()

    use_gui = LaunchConfiguration("use_gui")

    args = [
        DeclareLaunchArgument("use_gui", default_value="false",
            description="true = drag joints by hand; false = run the move_arm node"),
        DeclareLaunchArgument("target_x", default_value="0.30"),
        DeclareLaunchArgument("target_y", default_value="0.15"),
        DeclareLaunchArgument("target_z", default_value="0.20"),
        DeclareLaunchArgument("elbow_up", default_value="true"),
        DeclareLaunchArgument("move_duration", default_value="4.0"),
        DeclareLaunchArgument("start_delay", default_value="0.0",
            description="seconds to hold at Home before moving (lets RViz load)"),
    ]

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}],
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_path],
        output="screen",
    )

    # Manual mode: a GUI with three sliders publishes /joint_states.
    jsp_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        condition=IfCondition(use_gui),
    )

    # Automatic mode: our node solves IK and animates Home -> Target.
    move_arm = Node(
        package="arm3dof",
        executable="move_arm",
        output="screen",
        condition=UnlessCondition(use_gui),
        parameters=[{
            "target_x": LaunchConfiguration("target_x"),
            "target_y": LaunchConfiguration("target_y"),
            "target_z": LaunchConfiguration("target_z"),
            "elbow_up": LaunchConfiguration("elbow_up"),
            "move_duration": LaunchConfiguration("move_duration"),
            "start_delay": LaunchConfiguration("start_delay"),
            "use_controller": False,
        }],
    )

    return LaunchDescription(args + [robot_state_publisher, rviz, jsp_gui, move_arm])
