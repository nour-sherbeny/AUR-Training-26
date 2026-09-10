import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import SetBool



class GoToGoalNode(Node):
    def __init__(self):
        super().__init__("go_to_goal")
        
        self.declare_parameter("target_x", 10.0)
        self.declare_parameter("target_y", 10.0)
        self.declare_parameter("kp_linear", 1.5)
        self.declare_parameter("kp_angular", 6.0)
        self.declare_parameter("angle_tolerance", 0.05)
        self.declare_parameter("distance_tolerance", 0.1)
        self.declare_parameter("loop_rate", 20.0)

        self.goal_x = self.get_parameter("target_x").value
        self.goal_y = self.get_parameter("target_y").value
        self.kp_linear = self.get_parameter("kp_linear").value
        self.kp_angular = self.get_parameter("kp_angular").value
        self.distance_tolerance = self.get_parameter("distance_tolerance").value
        self.angle_tolerance = self.get_parameter("angle_tolerance").value
        self.loop_rate = self.get_parameter("loop_rate").value


        self.current_pose = None #initially
        self.goal_reached = False #initially
        self.movement_enabled = False #initially

        self.publisher = self.create_publisher(Twist,"/turtle1/cmd_vel",10) #publishes linear and angular velocity instructions to move the turtle node 
        self.subscriber = self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10) #turtle node continously receives its disance and angle

        self.server = self.create_service(SetBool,'start_movement',self.start_movement_callback)

        self.timer=self.create_timer(1.0/self.loop_rate,self.timer_callback)

        self.get_logger().info(f'Navigating turtle to target goal: ({self.goal_x}, {self.goal_y})')

    def start_movement_callback(self,request,response): 
        if request.data:
            self.movement_enabled=True
            response.success=True
            response.message="Movement started"   
        else:
            self.movement_enabled=False
            response.success=True
            response.message="Movement stopped"

        return response  

    def pose_callback(self, msg): #update current position
        self.current_pose = msg

    def normalize_angle(self, angle): #all angles in radian &normalized to be within [-pi,pi]
        while angle>math.pi:
            angle=angle-2*math.pi
        while angle<-math.pi:
            angle=angle+2*math.pi    
        return angle   
 
    def timer_callback(self):
        if not self.movement_enabled:
            return
        if self.current_pose==None or self.goal_reached:
            return
        dx=self.goal_x-self.current_pose.x
        dy=self.goal_y-self.current_pose.y

        distance_error=math.sqrt(dx**2+dy**2)  # Euclidean Distance Error: sqrt((x_g - x)^2 + (y_g - y)^2)
        target_angle=math.atan2(dy,dx)
        angle_error=self.normalize_angle(target_angle-self.current_pose.theta) #angle error is the difference between the target angle and the current angle of the turtle

        msg=Twist()

        #check if the calculated errors are within the defined tolerances
        if distance_error < self.distance_tolerance:
            msg.linear.x = 0.0 #to stop 5alas
            msg.angular.z = 0.0
            self.publisher.publish(msg)
            self.goal_reached = True
            self.get_logger().info('Goal Reached Successfully!')
            return
        
        if abs(angle_error) > self.angle_tolerance:
            msg.linear.x = 0.0
            msg.angular.z = self.kp_angular * angle_error # Proportional control for angular velocity
        else:
            # Proportional control for linear and angular velocity of turtle
            msg.linear.x = min(self.kp_linear * distance_error, 2.0)  #max speed is 2.0 m/s
            msg.angular.z = self.kp_angular * angle_error

        self.publisher.publish(msg)
        

     

def main(args=None):
    rclpy.init(args=args)
    node = GoToGoalNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()