import json
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    apriltag_param_path = PathJoinSubstitution([
        FindPackageShare('apriltag_ros'),
        'cfg',
        'tags_36h11.yaml'
    ])

    # tag_map.jsonの読み込み
    tag_map_path = '/home/student/ros2_ws/src/apriltag_ros/cfg/tag_map.json'  # ここは実パス
    with open(tag_map_path, 'r') as f:
        tag_data = json.load(f)

    static_tf_nodes = []
    for tag_id, pose in tag_data.items():
        pos = pose['position']
        rpy = pose['orientation_rpy']
        static_tf_nodes.append(
            Node(
                package='tf2_ros',
                executable='static_transform_publisher',
                name=f'static_tf_{tag_id}',
                arguments=[
                    str(pos[0]), str(pos[1]), str(pos[2]),
                    str(rpy[0]), str(rpy[1]), str(rpy[2]),
                    'map', tag_id
                ]
            )
        )

    return LaunchDescription([
        Node(
            package='apriltag_ros',
            executable='apriltag_node',
            name='apriltag_node',
            output='screen',
            parameters=[apriltag_param_path],
            remappings=[
                ('image_rect', '/image_topic'),
                ('camera_info', '/dammy_camera_info'),
            ]
        )
    ] + static_tf_nodes)

