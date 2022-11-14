from constraint import *
from transform_data import transform_data_sudents
from transform_data import trasform_data_bus

# First of all we create the variables of the exercise
# All of them are represented in the transformed data. 

def create_all_variables (studensfile, busfile):
    # we get the transformed data of students; They will be our variables
    Alumnos_curso1, Alumnos_curso2, Alumnos_mov_red, Alumnos_conf, Hermanos = transform_data_sudents(studensfile)

    # We obtain the domain of the variables
    asientos_ventanilla, asientos_mov_red, asientos_curso1, asientos_curso2= trasform_data_bus(busfile)

