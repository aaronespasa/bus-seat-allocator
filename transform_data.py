import csv 

# Este archivo contiene el que es el primer paso en la resolución del problema, 
# la identificación de los datos y su transformación para su posterior utilización. 

# Transformamos los datos de csv a una lista de listas, alumnos, una matriz que contiene 
# los datos de cada alumno. 
def transform_data_sudents(filename):
    """ Transforma los datos de un archivo csv a una lista de listas.
    Devuelve Alumnos_curso1, Alumnos_curso2, Alumnos_mov_red, Alumnos_conf, Hermanos """

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        alumnos = []
        for alumno in csvreader:
            alumnos.append(alumno)


    # ? Creamos los distintos grupos en los que categorizaremos a los alumnos

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


def trasform_data_bus(filename):
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


print(trasform_data_bus('bus.csv'))












""" print("Alumnos del curso 1: ", Alumnos_curso1)
print("Alumnos del curso 2: ", Alumnos_curso2)
print("Alumnos de movilidad red: ", Alumnos_mov_red)
print("Alumnos conflictivos: ", Alumnos_conf)
print("Hermanos: ", Hermanos) """