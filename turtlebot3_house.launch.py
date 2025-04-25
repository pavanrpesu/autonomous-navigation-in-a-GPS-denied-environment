import os

# Import function to get the path to a package's shared directory
from ament_index_python.packages import get_package_share_directory

# ROS 2 launch system imports
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    # Get the path to the 'launch' folder of the turtlebot3_gazebo package
    launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')
    
    # Get the path to the 'gazebo_ros' package
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # Define launch configuration variables 
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')  
    x_pose = LaunchConfiguration('x_pose', default='-2.0')              
    y_pose = LaunchConfiguration('y_pose', default='-0.5')           

    # Define the path to the Gazebo world file
    world = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'worlds',
        'turtlebot3_house.world'  
    )

    # Launch Gazebo server with the selected world file
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items()  # Pass the world file to the server
    )

    # Launch Gazebo client (the graphical interface)
    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    # reading the robot's URDF (Unified Robot Description Format) model and broadcast the robot’s transform tree using simulation time.
    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()  
    )

    # Spawn TurtleBot3 in the Gazebo simulation at the specified location
    spawn_turtlebot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'spawn_turtlebot3.launch.py')
        ),
        launch_arguments={
            'x_pose': x_pose,
            'y_pose': y_pose
        }.items()  
    )

    # Create the final launch description and add all actions to it
    ld = LaunchDescription()
    ld.add_action(gzserver_cmd)               
    ld.add_action(gzclient_cmd)              
    ld.add_action(robot_state_publisher_cmd)  
    ld.add_action(spawn_turtlebot_cmd)       

    return ld  
