import os
import numpy as np

from tesseract_robotics.tesseract_environment import Environment
from tesseract_robotics.tesseract_common import FilesystemPath, ManipulatorInfo
from tesseract_robotics.tesseract_kinematics import KinGroupIKInput, KinGroupIKInputs
from ..tesseract_support_resource_locator import TesseractSupportResourceLocator

def get_environment():
    env = Environment()
    locator = TesseractSupportResourceLocator()
    tesseract_support = os.environ["TESSERACT_SUPPORT_DIR"]
    urdf_path = FilesystemPath(os.path.join(tesseract_support, "urdf/abb_irb2400.urdf"))
    srdf_path = FilesystemPath(os.path.join(tesseract_support, "urdf/abb_irb2400.srdf"))
    assert env.init(urdf_path, srdf_path, locator)
    manip_info = ManipulatorInfo()
    manip_info.manipulator = "manipulator"
    manip_info.tcp_frame = "tool0"
    manip_info.working_frame = "base_link"
    joint_names = list(env.getJointGroup("manipulator").getJointNames())

    return env, manip_info, joint_names

def test_get_environment():
    get_environment()

def test_kinematic_group():

    env, manip_info, joint_names = get_environment()

    kin_group = env.getKinematicGroup(manip_info.manipulator).release()
    
    joint_vals = np.ones((6,),dtype=np.float64)*0.1
    pose_map = kin_group.calcFwdKin(joint_vals)
    pose = pose_map[manip_info.tcp_frame]

    ik = KinGroupIKInput()
    ik.pose = pose
    ik.tip_link_name = "tool0"
    ik.working_frame = "base_link"
    iks = KinGroupIKInputs()
    iks.append(ik)

    invkin1 = kin_group.calcInvKin(iks,joint_vals*0.1)
    invkin = invkin1[0]

    np.testing.assert_allclose(invkin.flatten(),joint_vals)


