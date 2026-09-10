import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class ServiceClientNode(Node):

    def __init__(self):
        super().__init__('service_client')

        self.client = self.create_client(SetBool,'start_movement')

        self.timer = self.create_timer(5.0,self.call_start_service)

    def call_start_service(self):
        self.timer.cancel()

        if not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('start_movement service not available')
            return

        request = SetBool.Request()
        request.data = True

        future = self.client.call_async(request)
        future.add_done_callback(
            self.service_response_callback
        )

    def service_response_callback(self, future):

        response = future.result()

        if response.success:
            self.get_logger().info(
                f'Service response: {response.message}'
            )
        else:
            self.get_logger().warn(
                'Service request was rejected'
            )


def main(args=None):
    rclpy.init(args=args)

    node = ServiceClientNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()