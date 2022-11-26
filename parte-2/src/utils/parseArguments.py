from ..CONSTANTS import HEURISTIC_NAMES


INCORRECT_ARGUMENTS_MSG = """
The correct way to run the program is:
    $ python ASTARColaBus.py <alumnos_path> <heuristic_name>

Make sure that the heuristic name is one of the following:
    - 1: Count the number of students that are not in the bus.

Example:
    $ python ASTARColaBus.py ./ASTAR-tests/alumnos.prob 1
"""

def parse_arguments(cmd_args: list) -> tuple:
    """
    This function checks that the arguments are correct and returns the
    arguments in a list.

    The arguments should be:
        - The name of the file to be read containing the bus position of the students.
        - The name of the heuristic to be used.
    
    Possible heuristic names are:
        - 1: Count the number of students that are not in the bus.
    """
    if len(cmd_args) != 2:
        raise ValueError("The number of arguments is not correct.\n" + INCORRECT_ARGUMENTS_MSG)
    
    alumnos_path = cmd_args[0]

    if not alumnos_path.endswith(".prob"):
        raise ValueError("The file name should end with .prob.\n" + INCORRECT_ARGUMENTS_MSG)

    heuristic_name = cmd_args[1]

    if heuristic_name not in HEURISTIC_NAMES:
        raise ValueError("The heuristic name is not correct.\n" + INCORRECT_ARGUMENTS_MSG)

    return alumnos_path, heuristic_name