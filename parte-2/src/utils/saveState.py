from .parseInputFile import StudentTuple, StudentTypes

def get_student_name_in_file(student_id:str, alumnos:dict) -> str:
    """
    Returns the name of the student in the file.
    """
    conflictive = "X"
    reduced_mobility = "X"

    if alumnos[student_id][StudentTuple.TYPE] == StudentTypes.CONFLICTIVE_REDUCED_MOBILITY:
        conflictive = "C"
        reduced_mobility = "R"
    elif alumnos[student_id][StudentTuple.TYPE] == StudentTypes.CONFLICTIVE:
        conflictive = "C"
    elif alumnos[student_id][StudentTuple.TYPE] == StudentTypes.REDUCED_MOBILITY:
        reduced_mobility = "R"

    return f"{student_id}{conflictive}{reduced_mobility}"

def get_output_file_path(filename:str, heuristic_name:str, is_stat:bool) -> str:
    """Returns the output file path."""
    file_extension = "stat" if is_stat else "output"
    return f"./ASTAR-tests/{filename}-{heuristic_name}.{file_extension}"

def save_state(state:list, alumnos:dict, filename:str, heuristic_name:str) -> None:
    """Saves the state to the output file."""
    file_content = {}
    for i in range(len(state)):
        alumno_name = get_student_name_in_file(state[i], alumnos)
        file_content[alumno_name] = i + 1
    
    output_file_path = get_output_file_path(filename, heuristic_name, False)
    with open(output_file_path, "w") as file:
        file.write(str(file_content))

def save_statistics(statistics:str, filename:str, heuristic_name:str) -> None:
    """Saves the statistics to the output file."""
    output_file_path = get_output_file_path(filename, heuristic_name, True)
    with open(output_file_path, "w") as file:
        file.write(statistics)