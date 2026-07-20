"""
gazebo.launch.py  -  OPTIONAL bonus: run the arm in Gazebo Classic with physics.

This is more involved than the RViz path (it needs ros2_control controllers).
If you only want to satisfy the task, the RViz demo (display.launch.py) is
enough. Use this if you specifically want a Gazebo recording.

Starts: Gazebo + robot_state_publisher, spawns the arm, loads the controllers,
then runs move_arm in controller mode to send a trajectory to the target.

Usage:
  ros2 launch arm3dof gazebo.launch.py
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, IncludeLaunchDescription,
                            RegisterEventHandler, TimerAction)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory("arm3dof")
    urdf_path = os.path.join(pkg, "urdf", "arm3dof.urdf")
    with open(urdf_path, "r") as f:
        robot_description = f.read()

    gazebo_ros = get_package_share_directory("gazebo_ros")
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros, "launch", "gazebo.launch.py")),
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}],
    )

    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "robot_description", "-entity", "arm3dof"],
        output="screen",
    )

    # Load controllers once the robot is spawned.
    load_jsb = Node(
        package="controller_manager", executable="spawner",
        arguments=["joint_state_broadcaster"], output="screen",
    )
    load_arm = Node(
        package="controller_manager", executable="spawner",
        arguments=["arm_controller"], output="screen",
    )

    # Send the target trajectory a few seconds after controllers are up.
    move_arm = TimerAction(period=6.0, actions=[Node(
        package="arm3dof", executable="move_arm", output="screen",
        parameters=[{
            "target_x": LaunchConfiguration("target_x"),
            "target_y": LaunchConfiguration("target_y"),
            "target_z": LaunchConfiguration("target_z"),
            "elbow_up": LaunchConfiguration("elbow_up"),
            "move_duration": LaunchConfiguration("move_duration"),
            "use_controller": True,
        }],
    )])

    return LaunchDescription([
        DeclareLaunchArgument("target_x", default_value="0.30"),
        DeclareLaunchArgument("target_y", default_value="0.15"),
        DeclareLaunchArgument("target_z", default_value="0.20"),
        DeclareLaunchArgument("elbow_up", default_value="true"),
        DeclareLaunchArgument("move_duration", default_value="4.0"),
        gazebo,
        robot_state_publisher,
        spawn_entity,
        # chain the controller spawners after the entity spawns
        RegisterEventHandler(OnProcessExit(
            target_action=spawn_entity, on_exit=[load_jsb])),
        RegisterEventHandler(OnProcessExit(
            target_action=load_jsb, on_exit=[load_arm])),
        move_arm,
    ])
