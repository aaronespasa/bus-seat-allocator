import sys

def get_file_content(file_path)->str:
    """
    Gets the content of a file.
    """
    try:
        file = open(file_path, "r")
        content = file.read()
        file.close()
        return content
    except IOError:
        print("Error: File does not appear to exist.")
        sys.exit()