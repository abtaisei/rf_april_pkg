import rclpy
from rclpy.node import Node

from apriltag_msgs.msg import AprilTagDetectionArray
from std_msgs.msg import Int32


class TagBridge(Node):
    def __init__(self):
        super().__init__('tag_bridge')

        self.sub = self.create_subscription(
            AprilTagDetectionArray,
            '/detections',
            self.callback,
            10
        )

        self.pub = self.create_publisher(Int32, '/detected_tag_id', 10)

        self.get_logger().info("tag_bridge node started")

    def callback(self, msg):
        if len(msg.detections) > 0:
            # AprilTag の id は list なので [0] が必要
            tag_id = msg.detections[0].id[0]
        else:
            tag_id = -1

        out = Int32()
        out.data = tag_id
        self.pub.publish(out)


def main(args=None):
    rclpy.init(args=args)
    node = TagBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
