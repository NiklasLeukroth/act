import rclpy
import numpy as np

from sensor_msgs.msg import Image, JointState, CompressedImage

# from xarm_msgs.msg import RobotMsg

class IntelRealSense():
    rgb_image = np.zeros((480, 848, 3))
    depth_image = np.zeros((480, 848, 3))

    def __init__(self, node):
        self.node = node
        self.subscription_rgb = self.node.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.cb_image_raw,
            3)
        
        self.subscription_depth = self.node.create_subscription(
            Image,
            '/camera/camera/depth/image_rect_raw',
            self.cb_image_depth,
            3)

    def get_images(self):
        image_dict = dict()
        image_dict["realsense_image_raw"] = self.rgb_image
        image_dict["realsense_image_depth"] = self.depth_image
        return image_dict
    
    def cb_image_raw(self, msg):
        self.rgb_image = msg.data

    def cb_image_depth(self, msg):
        self.depth_image = msg.data

class Digit360():
    rgb_image = np.zeros((480, 848, 3))

    def __init__(self, node):
        self.node = node
        self.subscription_rgb = self.node.create_subscription(
            Image,
            '/image_raw/index_0',
            self.cb_image_raw,
            3)

    def get_images(self):
        image_dict = dict()
        image_dict["digit360_image_0"] = self.rgb_image
        return image_dict
    
    def cb_image_raw(self, msg):
        self.rgb_image = msg.data


class Digit():
    rgb_image_0 = np.zeros((480, 848, 3))
    rgb_image_1 = np.zeros((480, 848, 3))
    rgb_image_2 = np.zeros((480, 848, 3))

    def __init__(self, node):
        self.node = node
        self.subscription_rgb_0 = self.node.create_subscription(
            CompressedImage,
            '/digit_rgb/index_0',
            self.cb_image_raw_0,
            3)
        
        self.subscription_rgb_1 = self.node.create_subscription(
            CompressedImage,
            '/digit_rgb/index_1',
            self.cb_image_raw_1,
            3)
        
        self.subscription_rgb_2 = self.node.create_subscription(
            CompressedImage,
            '/digit_rgb/index_2',
            self.cb_image_raw_2,
            3)

    def get_images(self):
        image_dict = dict()
        image_dict["digit_rgb_image_0"] = self.rgb_image_0
        image_dict["digit_rgb_image_1"] = self.rgb_image_1
        image_dict["digit_rgb_image_2"] = self.rgb_image_2
        return image_dict
    
    def cb_image_raw_0(self, msg):
        self.rgb_image_0 = msg.data

    def cb_image_raw_1(self, msg):
        self.rgb_image_1 = msg.data

    def cb_image_raw_2(self, msg):
        self.rgb_image_2 = msg.data

class XArm():
    position = None
    velocity = None
    effort = None

    def __init__(self, node):
        self.node = node
        # self.subscription_robot_states = self.node.create_subscription(
        #     RobotMsg,
        #     '/xarm/robot_states',
        #     self.cb_robot_states,
        #     3)

    def get_effort(self):
        return self.effort
    
    def get_qvel(self):
        return self.velocity
    
    def get_qpos(self):
        return self.position
    
    def cb_robot_states(self, msg):
        self.position = msg.position
        self.velocity = msg.velocity
        self.effort = msg.effort


class Tilburg():
    position = None
    velocity = None
    effort = None

    def __init__(self, node):
        self.node = node
        self.subscription_robot_states = self.node.create_subscription(
            JointState,
            '/th_right/joint_states',
            self.cb_hand_states,
            3)

    def get_effort(self):
        return self.effort
    
    def get_qvel(self):
        return self.velocity
    
    def get_qpos(self):
        return self.position
    
    def cb_hand_states(self, msg):
        self.position = msg.position
        self.velocity = msg.velocity
        self.effort = msg.effort