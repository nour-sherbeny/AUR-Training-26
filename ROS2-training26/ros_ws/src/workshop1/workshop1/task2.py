import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

 #constants
TARGET_X = 10.0 #x coordinate of the goal
TARGET_Y = 10.0 #y coordinate of the goal
KP_LINEAR= 1.5   #Proportional gain for linear velocity(to inc velocity proportinal to distance from goal)
KP_ANGULAR = 6.0   #Proportional gain for angular velocity(to change angle proportinal to angle difference from goal)
ANGLE_TOLERANCE = 0.05  #this angle is close enough to the goal so we can stop now
DISTANCE_TOLERANCE = 0.1  #this distance is close enough to the goal so we can stop now

class GoToGoalNode(Node):
    def __init__(self):
        super().__init__("go_to_goal_node")

        self.goal_x = TARGET_X
        self.goal_y = TARGET_Y

        self.kp_linear = KP_LINEAR
        self.kp_angular = KP_ANGULAR

        self.distance_tolerance = DISTANCE_TOLERANCE
        self.angle_tolerance = ANGLE_TOLERANCE 

        self.current_pose = None #initially
        self.goal_reached = False #initially

        self.publisher = self.create_publisher(Twist,"/turtle1/cmd_vel",10) #publishes linear and angular velocity instructions to move the turtle node 
        self.subscriber = self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10) #turtle node continously receives its disance and angle
        self.timer=self.create_timer(0.05,self.timer_callback)
        self.get_logger().info(f'Navigating turtle to target goal: ({self.goal_x}, {self.goal_y})')

    def pose_callback(self, msg): #update current position
        self.current_pose = msg

    def normalize_angle(self, angle): #all angles in radian &normalized to be within [-pi,pi]
        while angle>math.pi:
            angle=angle-2*math.pi
        while angle<-math.pi:
            angle=angle+2*math.pi    
        return angle   
 
    def timer_callback(self):
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