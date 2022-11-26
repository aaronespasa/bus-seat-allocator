"""
A Star Search Algorithm implementation that fills a bus queue with passengers.
"""
import sys
from src.utils.parseArguments import parse_arguments
from src.utils.parseInputFile import parse_alumnos_input
from src.utils.getFileContent import get_file_content

class ASTARColaBus:
    """
    A Star Search Algorithm implementation that fills a bus queue with passengers.
    """
    def __init__(self, alumnos:dict, heuristic_name:str) -> None:
        self.alumnos = alumnos
        self.heuristic = self.get_heuristic(heuristic_name)
    
    def heuristic_count_alumnos(self) -> int:
        """
        Counts the number of alumnos in the state.
        """
        pass

    def get_heuristic(self, heuristic_name:str) -> callable:
        """
        Gets the heuristic function to use.
        """
        if heuristic_name == "1":
            return self.heuristic_count_alumnos
        elif heuristic_name == "2":
            pass
        else:
            print("Error: Invalid heuristic name.")
            sys.exit()

    def __str__(self) -> str:
        return f"ASTARColaBus(alumnos={self.alumnos})"

if __name__ == "__main__":
    # Parse arguments and get the position of the students as a dictionary called "alumnos"
    alumnos_path, heuristic_name = parse_arguments(sys.argv[1:])
    alumnos_content = get_file_content(alumnos_path)
    alumnos = parse_alumnos_input(alumnos_content)

    # Create the ASTARColaBus object using the given dictionary of students
    # and the heuristic name
    astar = ASTARColaBus(alumnos, heuristic_name)
    
    print(astar)