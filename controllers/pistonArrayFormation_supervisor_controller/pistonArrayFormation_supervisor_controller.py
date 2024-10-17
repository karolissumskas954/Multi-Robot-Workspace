"""pistonArrayFormation_supervisor_controller controller."""
from controller import Supervisor
import re

TIME_STEP = 32
num_rows = 9
num_cols = 9
initial_translation = (0.1, 0.1, 0.04)
spacing = 0.11
name_prefix = "Robot"
robot = Supervisor()
root_node = robot.getRoot()
children_field = root_node.getField('children')

def create_robot_instances_square(num_rows, num_cols, initial_translation, spacing, name_prefix):
    """
    Creates multiple instances of the robot definition in a square formation, along with corresponding boxes.

    Args:
        num_rows: The number of rows in the square formation.
        num_cols: The number of columns in the square formation.
        initial_translation: The initial translation value for the top-left corner robot.
        spacing: The distance between robots in both the x and y directions.
        name_prefix: The prefix for the robot names.

    Returns:
        A list of robot definitions and a list of box definitions.
    """

    robot_definitions = []
    box_definitions = []

    for row in range(num_rows):
        for col in range(num_cols):
            translation_x = initial_translation[0] + col * spacing
            translation_y = initial_translation[1] + row * spacing
            translation_z = initial_translation[2]

            robot_name = f"{name_prefix}{row}_{col}"
            box_name = f"Box_{row}_{col}"

            robot_definition = f'''DEF Piston_bot{row}_{col} Piston_bot {{
                translation {translation_x} {translation_y} {translation_z}
                name "{robot_name}"
            }}'''
            box_definition = f'''Top_box {{
                translation {translation_x} {translation_y} {translation_z + 0.15}
                name "{box_name}"
            }}'''

            robot_definitions.append(robot_definition)
            box_definitions.append(box_definition)

    return robot_definitions, box_definitions

robot_definitions, box_definitions = create_robot_instances_square(num_rows, num_cols, initial_translation, spacing, name_prefix)

i = 0
while robot.step(TIME_STEP) != -1:
    if i == 0:
        for definition in robot_definitions:
            children_field.importMFNodeFromString(-1, definition)
        for definition in box_definitions:
            children_field.importMFNodeFromString(-1, definition)
    i += 1
