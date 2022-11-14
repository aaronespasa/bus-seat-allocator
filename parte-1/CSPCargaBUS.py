"""
Este archivo contiene el que es el primer paso en la resolución del problema, 
la identificación de los datos y su transformación para su posterior utilización. 
"""
import csv
from constraint import *

TESTS_FOLDER = "CSP-tests/"
ALUMNOS_CSV = TESTS_FOLDER + "alumnos.csv"
BUS_CSV = TESTS_FOLDER + "bus.csv"
 
def transform_data_students(filename:str):
    """Transforma los datos de un archivo csv a una lista de listas.
    Devuelve Alumnos_curso1, Alumnos_curso2, Alumnos_mov_red, Alumnos_conf, Hermanos """

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        _ = next(csvreader)
        alumnos = []
        for alumno in csvreader:
            alumnos.append(alumno)

    # Creamos los distintos grupos en los que categorizaremos a los alumnos
    Alumnos_curso1 = []
    Alumnos_curso2 = []
    Alumnos_mov_red = []
    Alumnos_conf = []
    Hermanos = []

    aux_hermanos = []

    for i in range(0,len(alumnos)): 
        if alumnos[i][1] == '1':
            Alumnos_curso1.append(alumnos[i][0])
        else :
            Alumnos_curso2.append(alumnos[i][0])

        if alumnos[i][2] == 'C':
            Alumnos_conf.append(alumnos[i][0])
        
        if alumnos[i][3] == 'R':
            Alumnos_mov_red.append(alumnos[i][0])

        if alumnos[i][4] != '0' and alumnos[i][0] not in aux_hermanos :
            aux_hermanos.append(alumnos[i][0])
            aux_hermanos.append(alumnos[i][4])
            Hermanos.append([alumnos[i][0],alumnos[i][4]])

    return Alumnos_curso1, Alumnos_curso2, Alumnos_mov_red, Alumnos_conf, Hermanos


def trasform_data_bus(filename:str):
    """ Transforma los datos de un archivo csv a una lista de listas.
    Devuelve ventanilla, mov_red, asientos_curso1, asientos_curso2 """

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        asientos = []
        for bus in csvreader:
            asientos.append(bus)

    ventanilla = []
    mov_red = []
    asientos_curso1 = []
    asientos_curso2 = []
    # pasillo = []

    for i in range(0,len(asientos)):
            if asientos[i][1] == 'v':
                ventanilla.append(asientos[i][0])

            if asientos[i][2] == 'r':
                mov_red.append(asientos[i][0])

            if int(asientos[i][0]) <= 16:
                asientos_curso1.append(asientos[i][0])
            else:
                asientos_curso2.append(asientos[i][0])

    return  ventanilla, mov_red, asientos_curso1, asientos_curso2

# First of all we create the variables of the exercise
# All of them are represented in the transformed data. 

def create_all_variables (studensfile, busfile):
    # we get the transformed data of students; They will be our variables
    Alumnos_curso1, Alumnos_curso2, Alumnos_mov_red, Alumnos_conf, Hermanos = transform_data_students(studensfile)

    # We obtain the domain of the variables
    asientos_ventanilla, asientos_mov_red, asientos_curso1, asientos_curso2= trasform_data_bus(busfile)

def print_students_data():
    (Alumnos_curso1,
     Alumnos_curso2,
     Alumnos_mov_red,
     Alumnos_conf,
     Hermanos) = transform_data_students(ALUMNOS_CSV)

    print(f"Alumnos del curso 1: {Alumnos_curso1}",
          f"Alumnos del curso 2: {Alumnos_curso2}",
          f"Alumnos con movilidad reducida: {Alumnos_mov_red}",
          f"Alumnos conflictivos: {Alumnos_conf}",
          f"Hermanos: {Hermanos}", sep = "\n", end="\n\n")

def print_bus_data():
    (ventanilla,
     mov_red,
     asientos_curso1,
     asientos_curso2) = trasform_data_bus(BUS_CSV)

    print(f"Asientos de la ventanilla: {ventanilla}",
          f"Asientos con movilidad reducida: {mov_red}",
          f"Asientos del curso 1: {asientos_curso1}",
          f"Asientos del curso 2: {asientos_curso2}", sep = "\n", end="\n\n")

if __name__ == "__main__":
    print_students_data()
    print_bus_data()
