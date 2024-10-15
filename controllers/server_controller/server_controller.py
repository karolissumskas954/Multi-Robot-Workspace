"""server_controller controller."""
import sys
from controller import Supervisor

robot = Supervisor()
TIME_STEP = 32



while robot.step(TIME_STEP) != -1:
    pass