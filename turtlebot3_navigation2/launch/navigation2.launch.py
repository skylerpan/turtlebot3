# Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# /* Author: Darby Lim */

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir
from launch.actions import ExecuteProcess

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    map_dir = LaunchConfiguration('map', 
                                default=os.path.join(get_package_share_directory('turtlebot3_navigation2'), 'map', 'map.yaml'))

    param_dir = LaunchConfiguration('params', 
                                default=os.path.join(get_package_share_directory('turtlebot3_navigation2'), 'param', 'burger_params.yaml'))
    
    nav2_launch_file_dir = os.path.join(get_package_share_directory('nav2_bringup'), 'launch')
    rviz_config_dir = os.path.join(get_package_share_directory('turtlebot3_navigation2'), 'rviz', 'tb3_navigation2.rviz')

    return LaunchDescription([
        DeclareLaunchArgument(
            'map', 
            default_value=map_dir,
            description='Full path to map file to load'),

        DeclareLaunchArgument(
            'params', 
            default_value=param_dir,
            description='Full path to param file to load'),

        DeclareLaunchArgument(
            'use_sim_time', 
            default_value='false', 
            description='Use simulation (Gazebo) clock if true'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_launch_file_dir, '/nav2_bringup_1st_launch.py']),
            launch_arguments={'map': map_dir, 'use_sim_time': use_sim_time}.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_launch_file_dir, '/nav2_bringup_2nd_launch.py']),
            launch_arguments={'use_sim_time': use_sim_time, 'params': param_dir}.items(),
        ),

        Node(
            package='rviz2',
            node_executable='rviz2',
            node_name='rviz2',
            arguments=['-d', rviz_config_dir],
            output='screen'),

        ExecuteProcess(
            cmd=['ros2', 'param', 'set', '/world_model', 'use_sim_time', use_sim_time],
            output='screen'),

        ExecuteProcess(
            cmd=['ros2', 'param', 'set', '/global_costmap/global_costmap', 'use_sim_time', use_sim_time],
            output='screen'),

        ExecuteProcess(
            cmd=['ros2', 'param', 'set', '/local_costmap/local_costmap', 'use_sim_time', use_sim_time],
            output='screen')
    ])