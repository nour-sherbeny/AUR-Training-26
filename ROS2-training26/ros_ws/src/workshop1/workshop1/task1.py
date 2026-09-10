import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class TurtleController(Node):
    def __init__(self):
        super().__init__("turtle_controller")

        self.get_logger().info("Turtle Controller Started!!")

        self.publisher = self.create_publisher(Twist,"/turtle1/cmd_vel",10) #publishes linear and angular velocity to move the turtle

        self.subscriber = self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10)  # Subscriber: Receives continuous pose updates from turtlesim

        self.counter = 0

        self.timer=self.create_timer(0.5, self.publishVelocity) #timer publishesvelocity commands every 0.5 sec/2 HZ

    def pose_callback(self, msg):
        self.get_logger().info(f"Pose: x={msg.x}, y={msg.y}, theta={msg.theta}")

    def publishVelocity(self):
        twist = Twist() #twist is an instance of the Twist message type, which contains linear and angular velocity
        twist.linear.x = 2.0
        twist.angular.z = 1.0
        self.publisher.publish(twist)



def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()