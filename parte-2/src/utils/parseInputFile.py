def parse_alumnos_input(file_content:str) -> dict:
    """
    Parses the content of the file and returns a dictionary with the data.
    """
    # convert the string Example of the file_content argument:
    # "{'3XX': 11, '1CX': 12, '6XX': 15, '5XX': 16, '8XR': 18, '4CR': 20, '2XX': 31, '7CX': 32}"
    # to a dictionary
    file_content = file_content[1:-1]
    file_content = file_content.replace("'", "")
    file_content = file_content.replace(" ", "")
    file_content = file_content.split(",")
    alumnos = {}
    for alumno in file_content:
        key, value = alumno.split(":")
        alumnos[key] = int(value)

    return alumnos

