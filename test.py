#Test for joint movements
from isaacsim import SimulationApp

# Launch Isaac Sim
app = SimulationApp({"headless": False})  # headless=False opens the GUI

import numpy as np
from omni.isaac.core import World
from omni.isaac.core.robots import Robot
from omni.isaac.core.utils.stage import add_reference_to_stage

# Create world
world = World()
world.scene.add_default_ground_plane()

# Load mycobot URDF
urdf_path = "urdf/mycobot_280_m5/mycobot_280_m5.urdf"
add_reference_to_stage(usd_path=urdf_path, prim_path="/World/mycobot")
robot = world.scene.add(Robot(prim_path="/World/mycobot", name="mycobot"))

world.reset()

# Slowly wave each joint back and forth
joint_index = 0
direction = 1
angle = 0.0
step = 0

print("Starting joint movement test...")

while app.is_running():
    world.step(render=True)
    step += 1

    # Every 60 steps, sweep current joint and move to next
    if step % 200 == 0:
        joint_index = (joint_index + 1) % robot.num_dof
        print(f"Now moving joint {joint_index}")

    # Oscillate the current joint
    angle = np.sin(step * 0.05) * np.radians(45)
    joint_positions = np.zeros(robot.num_dof)
    joint_positions[joint_index] = angle

    robot.set_joint_positions(joint_positions)

app.close()