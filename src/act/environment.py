import time
import numpy as np
import collections
import matplotlib.pyplot as plt
import dm_env
import rclpy
import sys
sys.path.append("/home/niklas/master_ws/src/act/src/act")

from robot_utils import XArm, Tilburg, IntelRealSense, Digit360, Digit

from std_msgs.msg import Int32

import IPython
e = IPython.embed

class RealEnv:
    # Update documentation
    """
    Environment for real robot bi-manual manipulation
    Action space:      [left_arm_qpos (6),             # absolute joint position
                        left_gripper_positions (1),    # normalized gripper position (0: close, 1: open)
                        right_arm_qpos (6),            # absolute joint position
                        right_gripper_positions (1),]  # normalized gripper position (0: close, 1: open)

    Observation space: {"qpos": Concat[ left_arm_qpos (6),          # absolute joint position
                                        left_gripper_position (1),  # normalized gripper position (0: close, 1: open)
                                        right_arm_qpos (6),         # absolute joint position
                                        right_gripper_qpos (1)]     # normalized gripper position (0: close, 1: open)
                        "qvel": Concat[ left_arm_qvel (6),         # absolute joint velocity (rad)
                                        left_gripper_velocity (1),  # normalized gripper velocity (pos: opening, neg: closing)
                                        right_arm_qvel (6),         # absolute joint velocity (rad)
                                        right_gripper_qvel (1)]     # normalized gripper velocity (pos: opening, neg: closing)
                        "images": {"cam_high": (480x640x3),        # h, w, c, dtype='uint8'
                                   "cam_low": (480x640x3),         # h, w, c, dtype='uint8'
                                   "cam_left_wrist": (480x640x3),  # h, w, c, dtype='uint8'
                                   "cam_right_wrist": (480x640x3)} # h, w, c, dtype='uint8'
    """

    def __init__(self):
        rclpy.init()
        self.node = rclpy.create_node("act_eval_node")
        self.robot_arm_recorder = XArm(self.node)
        self.robot_hand_recorder = Tilburg(self.node)

        self.camera_recorder = IntelRealSense(self.node)
        self.digit_360_recorder = Digit360(self.node)
        self.digit_recorder = Digit(self.node)
        self.example_pub = self.node.create_publisher(Int32, 'topic', 10)
        # self.arm_command = D()
        # self.hand_command = E()
        self.DT = 0.02

    def get_qpos(self):
        arm_pos = self.robot_arm_recorder.get_qpos()
        hand_pos = self.robot_hand_recorder.get_qpos()
        out = hand_pos if hand_pos is not None else [0.0 for i in range(16)]
        if arm_pos is None:
            for i in range(9):
                out.append(0.0)
        else:
            out += arm_pos
            out.append(0.0)
            out.append(0.0)

        return np.array(out)

    def get_qvel(self):
        arm_qvel = self.robot_arm_recorder.get_qvel()
        hand_qvel = self.robot_hand_recorder.get_qvel()
        out = hand_qvel if hand_qvel is not None else [0.0 for i in range(16)]
        if arm_qvel is None:
            for i in range(9):
                out.append(0.0)
        else:
            out += arm_qvel
            out.append(0.0)
            out.append(0.0)

        return np.array(out)

    def get_effort(self):
        arm_effort = self.robot_arm_recorder.get_effort()
        hand_effort = self.robot_hand_recorder.get_effort()
        out = hand_effort if hand_effort is not None else [0.0 for i in range(16)]
        if arm_effort is None:
            for i in range(9):
                out.append(0.0)
        else:
            out += arm_effort
            out.append(0.0)
            out.append(0.0)

        return np.array(out)

    def get_images(self):
        digit_dict = self.digit_recorder.get_images()
        digit_360_dict = self.digit_360_recorder.get_images()
        camera_dict = self.camera_recorder.get_images()
        out = digit_dict | digit_360_dict | camera_dict
        return out

    def _move_hand(self, desired_action):
        pass

    def _move_arm(self, desired_action):
        out = Int32()
        out.data = 0
        self.example_pub.publish(out)

    def _reset_arm(self):
        # Implement resetting the arm here
        pass

    def _reset_hand(self):
        # Implement resetting the hand here
        pass 

    def get_observation(self):
        obs = collections.OrderedDict()
        obs['qpos'] = self.get_qpos()
        obs['qvel'] = self.get_qvel()
        obs['effort'] = self.get_effort()
        obs['images'] = self.get_images()
        if (obs['qpos'] is None) or (obs['qvel'] is None) or (obs['effort'] is None):
            return None
        for key, value in obs['images'].items():
            if value is None:
                return None
        return obs

    def get_reward(self):
        return 0

    def reset(self):
        self._reset_hand()
        self._reset_arm()

        return dm_env.TimeStep(
            step_type=dm_env.StepType.FIRST,
            reward=self.get_reward(),
            discount=None,
            observation=self.get_observation())

    def step(self, action):
        # Implement moving the robot here
        self._move_arm(None)
        self._move_hand(None)

        time.sleep(self.DT)
        return dm_env.TimeStep(
            step_type=dm_env.StepType.MID,
            reward=self.get_reward(),
            discount=None,
            observation=self.get_observation())

def get_action():
    # Not needed I think
    return None

def make_real_env():
    env = RealEnv()
    return env

def test_real_teleop():
    # """
    # Test bimanual teleoperation and show image observations onscreen.
    # It first reads joint poses from both master arms.
    # Then use it as actions to step the environment.
    # The environment returns full observations including images.

    # An alternative approach is to have separate scripts for teleoperation and observation recording.
    # This script will result in higher fidelity (obs, action) pairs
    # """

    # onscreen_render = True
    # render_cam = 'cam_left_wrist'

    # # source of data
    # master_bot_left = InterbotixManipulatorXS(robot_model="wx250s", group_name="arm", gripper_name="gripper",
    #                                           robot_name=f'master_left', init_node=True)
    # master_bot_right = InterbotixManipulatorXS(robot_model="wx250s", group_name="arm", gripper_name="gripper",
    #                                            robot_name=f'master_right', init_node=False)
    # setup_master_bot(master_bot_left)
    # setup_master_bot(master_bot_right)

    # # setup the environment
    # env = make_real_env(init_node=False)
    # ts = env.reset(fake=True)
    # episode = [ts]
    # # setup visualization
    # if onscreen_render:
    #     ax = plt.subplot()
    #     plt_img = ax.imshow(ts.observation['images'][render_cam])
    #     plt.ion()

    # for t in range(1000):
    #     action = get_action(master_bot_left, master_bot_right)
    #     ts = env.step(action)
    #     episode.append(ts)

    #     if onscreen_render:
    #         plt_img.set_data(ts.observation['images'][render_cam])
    #         plt.pause(DT)
    #     else:
    #         time.sleep(DT)
    pass

if __name__ == '__main__':
    test_real_teleop()
