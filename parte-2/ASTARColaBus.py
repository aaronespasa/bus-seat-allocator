"""
A Star Search Algorithm implementation that fills a bus queue with passengers.
"""
import sys
from src.utils.parseArguments import parse_arguments
from src.utils.parseInputFile import parse_alumnos_input, \
                                     print_alumnos, \
                                     StudentTuple, \
                                     StudentTypes
from src.utils.saveState import save_state
from src.utils.getFileContent import get_file_content

class ASTARColaBus:
    """
    A Star Search Algorithm implementation that fills a bus queue with passengers.
    """
    def __init__(self, alumnos:dict, queue_length:int, heuristic_name:str) -> None:
        self.alumnos = alumnos
        self.heuristic = self.get_heuristic(heuristic_name)
    
        self.empty_element = "-"
        self.state = ["4", "3", "7", "2", "1", "5", "6", "8"]
        # self.state = self.initialize_state(queue_length)
    
    def initialize_state(self, queue_length) -> list:
        """Initializes the state with the queue length."""
        return [self.empty_element for _ in range(queue_length)]

    def heuristic_count_queue_spaces(self) -> int:
        """Counts the number of empty spaces in the queue."""
        return self.state.count(self.empty_element)

    def get_heuristic(self, heuristic_name:str) -> callable:
        """Gets the heuristic function to use."""
        if heuristic_name == "1":
            return self.heuristic_count_queue_spaces
        else:
            raise Exception("Invalid heuristic name")

    def get_state(self) -> list:
        """Returns the current state."""
        return self.state
        

if __name__ == "__main__":
    # Parse arguments and get the position of the students as a dictionary called "alumnos"
    filename, alumnos_path, heuristic_name = parse_arguments(sys.argv[1:])
    alumnos_content = get_file_content(alumnos_path)
    alumnos, alumnos_count = parse_alumnos_input(alumnos_content)
    # Uncomment the following line to print the students in the input file
    # print_alumnos(alumnos)
    
    # Create the ASTARColaBus object using the given dictionary of students
    # and the heuristic name
    astar = ASTARColaBus(alumnos, alumnos_count, heuristic_name)
    final_state = astar.get_state()
    save_state(final_state, alumnos, filename, heuristic_name)