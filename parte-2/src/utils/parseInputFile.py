from enum import IntEnum, Enum

class StudentTypes(str, Enum):
    """
    Enum for the types of students.
    """
    NORMAL = "A"
    CONFLICTIVE = "C"
    REDUCED_MOBILITY = "M"
    CONFLICTIVE_REDUCED_MOBILITY = "X"

class StudentTuple(IntEnum):
    """
    Enum that represents the indexes of the tuple that represents a student.
    """
    TYPE = 0
    SEAT_NUMBER = 1

def parse_alumnos_input(file_content:str) -> tuple:
    """
    Parses the content of the file and returns a dictionary with the data
    and the number of students.

    The dictionary contains the student IDs as the keys.
    The values are tuples with the student type and the seat number.
    -> id: (type, seat_number)

    The possible values for the student type are:
        - "A": Students that are not conflictive nor have a reduced mobility.
        - "C": Students that are conflictive.
        - "M": Students that have a reduced mobility.
        - "X": Students that are conflictive and have a reduced mobility.
    
    """
    file_content = file_content[1:-1]
    file_content = file_content.replace("'", "")
    file_content = file_content.replace(" ", "")
    file_content = file_content.split(",")
    alumnos = {}
    alumnos_count = 0
    for alumno in file_content:
        name, seat_number = alumno.split(":")
        id = name[:-2]
        conflictive, reduced_mobility = name[-2:]
        
        # Get the student type
        if conflictive == "C" and reduced_mobility == "R":
            student_type = StudentTypes.CONFLICTIVE_REDUCED_MOBILITY
        elif conflictive == "C":
            student_type = StudentTypes.CONFLICTIVE
        elif reduced_mobility == "R":
            student_type = StudentTypes.REDUCED_MOBILITY
        else:
            student_type = StudentTypes.NORMAL
        
        # Add the student to the dictionary
        if id not in alumnos:
            alumnos[id] = (student_type, int(seat_number))
        
        alumnos_count += 1

    return alumnos, alumnos_count

def print_alumnos(alumnos:dict) -> None:
    """
    Prints the dictionary of students.
    """
    print(f"{' Alumnos (ID, NUMERO_ASIENTO) ':-^50}")
    print("Normal:")
    for alumno in alumnos:
        if alumnos[alumno][StudentTuple.TYPE] == StudentTypes.NORMAL:
            print(f"\t{alumno}: {alumnos[alumno][StudentTuple.SEAT_NUMBER]}")
    print("Conflictivo:")
    for alumno in alumnos:
        if alumnos[alumno][StudentTuple.TYPE] == StudentTypes.CONFLICTIVE:
            print(f"\t{alumno}: {alumnos[alumno][StudentTuple.SEAT_NUMBER]}")
    print("Movilidad reducida:")
    for alumno in alumnos:
        if alumnos[alumno][StudentTuple.TYPE] == StudentTypes.REDUCED_MOBILITY:
            print(f"\t{alumno}: {alumnos[alumno][StudentTuple.SEAT_NUMBER]}")
    print("Conflictivo y movilidad reducida:")
    for alumno in alumnos:
        if alumnos[alumno][StudentTuple.TYPE] == StudentTypes.CONFLICTIVE_REDUCED_MOBILITY:
            print(f"\t{alumno}: {alumnos[alumno][StudentTuple.SEAT_NUMBER]}")
    print(f"{'':-^50}")
