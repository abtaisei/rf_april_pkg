import os
import json
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # AprilTagパラメータのYAMLファイル
    apriltag_param_path = PathJoinSubstitution([
        FindPackageShare('apriltag_ros'),
        'cfg',
        'tags_36h11.yaml'
    ])

    # tag_map.json のパスをROSパッケージ相対に変更
    tag_map_path = os.path.join(
        get_package_share_directory('apriltag_ros'),
        'cfg',
        'tag_map.json'
    )

    # JSONファイルを読み込む
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
                ('image_rect', '/camera/color/image_raw'),
                ('camera_info', '/camera/color/camera_info'),
            ]
        )
    ] + static_tf_nodes)
