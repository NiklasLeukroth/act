import rclpy
import numpy as np
from PIL import Image as PIL_IMAGE

from sensor_msgs.msg import Image, JointState

glob_height = 848
glob_width = 480

class IntelRealSense():
    rgb_image = np.zeros((glob_width, glob_height, 3))
    depth_image = np.zeros((glob_width, glob_height, 3))

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
        rgb_array = np.frombuffer(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, 3))
        img = PIL_IMAGE.fromarray(rgb_array, 'RGB')
        resized_image = img.resize((glob_height, glob_width))
        self.rgb_image = np.array(resized_image)

    def cb_image_depth(self, msg):
        rgb_array = np.frombuffer(msg.data, dtype=np.uint16).reshape((msg.height, msg.width, 1))
        rgb_list = rgb_array.tolist()
        for i in range(len(rgb_list)):
            for j in range(len(rgb_list[i])):
                rgb_list[i][j].append(rgb_list[i][j][0])
                rgb_list[i][j].append(rgb_list[i][j][0])

        rgb_array = np.array(rgb_list)
        img = PIL_IMAGE.fromarray(rgb_array, 'RGB')
        resized_image = img.resize((glob_height, glob_width))
        self.depth_image = np.array(resized_image)


class Digit360():
    rgb_image = np.zeros((glob_width, glob_height, 3))

    def __init__(self, node):
        self.node = node
        self.subscription_rgb = self.node.create_subscription(
            Image,
            '/image_raw/index_0',
            self.cb_image_raw,
            3)
        self.rgb_image = load_image_and_resize("/home/niklas/master_ws/src/act/src/image_fake/d360.png")

    def get_images(self):
        image_dict = dict()
        image_dict["digit360_image_0"] = self.rgb_image
        return image_dict
    
    def cb_image_raw(self, msg):
        rgb_array = np.frombuffer(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, 3))
        img = PIL_IMAGE.fromarray(rgb_array, 'RGB')
        resized_image = img.resize((glob_height, glob_width))
        self.rgb_image = np.array(resized_image)


class Digit():
    rgb_image_0 = np.zeros((glob_width, glob_height, 3))
    rgb_image_1 = np.zeros((glob_width, glob_height, 3))
    rgb_image_2 = np.zeros((glob_width, glob_height, 3))
    rgb_image_3 = np.zeros((glob_width, glob_height, 3))

    def __init__(self, node):
        self.node = node
        self.subscription_rgb_0 = self.node.create_subscription(
            Image,
            '/digit_rgb/index_0',
            self.cb_image_raw_0,
            3)
        
        self.subscription_rgb_1 = self.node.create_subscription(
            Image,
            '/digit_rgb/index_1',
            self.cb_image_raw_1,
            3)
        
        self.subscription_rgb_2 = self.node.create_subscription(
            Image,
            '/digit_rgb/index_2',
            self.cb_image_raw_2,
            3)
        
        self.subscription_rgb_3 = self.node.create_subscription(
            Image,
            '/digit_rgb/index_3',
            self.cb_image_raw_3,
            3)
        
        self.rgb_image_0 = load_image_and_resize("/home/niklas/master_ws/src/act/src/image_fake/digit0.png")
        self.rgb_image_1 = load_image_and_resize("/home/niklas/master_ws/src/act/src/image_fake/digit1.png")
        self.rgb_image_2 = load_image_and_resize("/home/niklas/master_ws/src/act/src/image_fake/digit2.png")
        self.rgb_image_3 = load_image_and_resize("/home/niklas/master_ws/src/act/src/image_fake/digit3.png")


    def get_images(self):
        image_dict = dict()
        image_dict["digit_rgb_image_0"] = self.rgb_image_0
        image_dict["digit_rgb_image_1"] = self.rgb_image_1
        image_dict["digit_rgb_image_2"] = self.rgb_image_2
        image_dict["digit_rgb_image_3"] = self.rgb_image_3
        return image_dict
    
    def cb_image_raw_0(self, msg):
        rgb_array = np.frombuffer(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, 3))
        img = PIL_IMAGE.fromarray(rgb_array, 'RGB')
        resized_image = img.resize((glob_height, glob_width))
        self.rgb_image_0 = np.array(resized_image)

    def cb_image_raw_1(self, msg):
        rgb_array = np.frombuffer(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, 3))
        img = PIL_IMAGE.fromarray(rgb_array, 'RGB')
        resized_image = img.resize((glob_height, glob_width))
        self.rgb_image_1 = np.array(resized_image)

    def cb_image_raw_2(self, msg):
        rgb_array = np.frombuffer(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, 3))
        img = PIL_IMAGE.fromarray(rgb_array, 'RGB')
        resized_image = img.resize((glob_height, glob_width))
        self.rgb_image_2 = np.array(resized_image)
    
    def cb_image_raw_3(self, msg):
        rgb_array = np.frombuffer(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, 3))
        img = PIL_IMAGE.fromarray(rgb_array, 'RGB')
        resized_image = img.resize((glob_height, glob_width))
        self.rgb_image_3 = np.array(resized_image)


class XArm():
    position = None
    velocity = None
    effort = None

    def __init__(self, node):
        self.node = node
        self.subscription_robot_states = self.node.create_subscription(
            JointState,
            '/xarm/joint_states',
            self.cb_robot_states,
            3)

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


def load_image_and_resize(path) -> np.array:
    image = PIL_IMAGE.open(path)
    resized_image = image.resize((glob_height, glob_width))
    return np.array(resized_image)