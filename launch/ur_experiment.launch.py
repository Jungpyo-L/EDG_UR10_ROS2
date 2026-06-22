#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    ati_ip = LaunchConfiguration("ati_ip")
    robot_ip = LaunchConfiguration("robot_ip")

    rqt_config = PathJoinSubstitution([
        FindPackageShare("edg_ur10"),
        "launch",
        "rqt_multiplot_ATI.xml",
    ])

    return LaunchDescription([
        DeclareLaunchArgument("ati_ip", default_value="192.168.1.42"),
        DeclareLaunchArgument("robot_ip", default_value="10.0.0.1"),
        Node(
            package="edg_ur10",
            executable="robotStatePublisher.py",
            name="robot_state_publisher",
            output="screen",
            parameters=[{"robot_ip": robot_ip}],
        ),
        Node(
            package="netft_utils",
            executable="netft_node",
            name="netft_node",
            output="screen",
            arguments=[ati_ip],
        ),
        Node(
            package="edg_ur10",
            executable="data_logger.py",
            name="data_logger",
            output="screen",
        ),
        Node(
            package="rqt_multiplot",
            executable="rqt_multiplot",
            name="rqt_multiplot_node",
            output="screen",
            arguments=["--multiplot-run-all", "--multiplot-config", rqt_config],
        ),
    ])
