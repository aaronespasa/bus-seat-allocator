"""
Este archivo contiene el que es el primer paso en la resolución del problema, 
la identificación de los datos y su transformación para su posterior utilización. 
"""
import csv
from enum import IntEnum
""" from constraint import * """

class CSPCargaBUS:
    def __init__(self, studentsCSVFilename:str, busCSVFilename:str):
        """
        Input:
            studentsCSVFilename (str): Nombre del archivo csv con los datos de los alumnos (dentro de CSP-tests).
            busCSVFilename (str): Nombre del archivo csv con los datos de los buses (dentro de CSP-tests).
        """
        self.TESTS_FOLDER = "CSP-tests/"
        self.ALUMNOS_CSV_PATH = self.TESTS_FOLDER + studentsCSVFilename
        self.BUS_CSV_PATH = self.TESTS_FOLDER + busCSVFilename

        self.alumnos_categorizados = self.transform_data_students()
        self.asientos = []
        #self.asientos_categorizados = self.trasform_data_bus()

        #! revisar 
        """ self.problem = Problem() """

    @staticmethod
    def csv_to_list(filename:str):
        """Transforma los datos de un archivo csv a una lista de las filas del csv"""
        csvfile = open(filename, 'r')

        # El lector de csv nos devuelve un iterador
        csvreader = csv.reader(csvfile)

        # Saltamos la primera fila para no incluirla en los datos
        header_info = next(csvreader)

        # Convertimos el iterador en una lista
        data = list(csvreader)

        csvfile.close()

        return header_info, data

    def transform_data_students(self):
        """Leer los datos de los alumnos y repartirlos en sus respectivos grupos
        Output (diccionario con los grupos de alumnos):
            - Alumnos del curso 1
            - Alumnos del curso 2
            - Alumnos con movilidad reducida
            - Alumnos conflictivos
            - Hermanos
        """
        alumnosCSVFields, alumnos = self.csv_to_list(self.ALUMNOS_CSV_PATH)

        class Alumno(IntEnum):
            ID = alumnosCSVFields.index("id")
            CURSO = alumnosCSVFields.index("Ciclo")
            CONFLICTIVO = alumnosCSVFields.index("Conflictivo")
            MOV_RED = alumnosCSVFields.index("Movilidad")
            ID_HERMANO = alumnosCSVFields.index("IdHermano")

        # Grupos en los que categorizaremos a los alumnos
        Alumnos_curso1 = []
        Alumnos_curso2 = []
        Alumnos_mov_red = []
        Alumnos_conf = []
        Hermanos = []
        aux_hermanos = []

        for alumno in alumnos:
            # Categorizarlos según su curso
            if alumno[Alumno.CURSO] == '1':
                Alumnos_curso1.append(alumno[Alumno.ID])
            else:
                Alumnos_curso2.append(alumno[Alumno.ID])

            # Categorizarlos según si son conflictivos
            if alumno[Alumno.CONFLICTIVO] == 'C':
                Alumnos_conf.append(alumno[Alumno.ID])
            
            # Categorizarlos según si tienen movilidad reducida
            if alumno[Alumno.MOV_RED] == 'R':
                Alumnos_mov_red.append(alumno[Alumno.ID])

            # Categorizarlos según si son hermanos
            if alumno[Alumno.ID_HERMANO] != '0' and alumno[Alumno.ID] not in aux_hermanos :
                aux_hermanos.append(alumno[Alumno.ID])
                aux_hermanos.append(alumno[Alumno.ID_HERMANO])
                Hermanos.append([alumno[Alumno.ID],alumno[Alumno.ID_HERMANO]])

        alumnos_categorizados = {
            "Alumnos_curso1": Alumnos_curso1,
            "Alumnos_curso2": Alumnos_curso2,
            "Alumnos_mov_red": Alumnos_mov_red,
            "Alumnos_conf": Alumnos_conf,
            "Hermanos": Hermanos
        }

        return alumnos_categorizados

    def trasform_data_bus(self):
        """Leer los datos de los buses y categorizar sus asientos
        Output (diccionario con las categorías de asientos):
            - Asientos de la ventanilla
            - Asientos para movilidad reducida
            - Asientos para el curso 1
            - Asientos para el curso 2
        """

        #! La vision que vamos a tener para los asientos del bus será la siguiente: 
        #! -Todos los asientos estarán representados en una matriz de 2 dimensiones; 
        #! -La primera dimensión representa las filas del bus, y la segunda las columnas;
        #! -Para identificar los asientos se utilizará una tupla (fila, columna);
        #! -Los asientos de la ventanilla estarán en la primera y última columna de la matriz;
        #! -Los asientos para movilidad reducida estarán en la primera cuarta y quinta filas de la matriz; 
        #! -Los asientos para el curso 1 estarán en las 4 primeras filas de la matriz; 
        #! -Los asientos para el curso 2 estarán en las 4 últimas filas de la matriz;


        """ busCSVFields, asientos = self.csv_to_list(self.BUS_CSV_PATH)

        class infoBus(IntEnum):
            capacidad = busCSVFields.index("capacidad")
            asientos_fila = busCSVFields.index("asientos_fila")
            filas_mov_red = busCSVFields.index("movilidad_reducida")
            filas_curso1 = busCSVFields.index("curso1")
            filas_curso2 = busCSVFields.index("curso2") """

        # Grupos en los que categorizaremos a los asientos
        #! Todo esto tiene que ir dentro de el nuevo archivo de configuración de bus 
        capacidad = 32
        asientos_fila = 4
        filas_mov_red = [0,3,4]
        filas_curso1 = [0,1,2,3]
        filas_curso2 = [4,5,6,7]
        
        
        count = 1
        
        for i in range(0, capacidad, asientos_fila):
            fila = []
            fila.append(count)
            fila.append(count+1)
            fila.append(count+2)
            fila.append(count+3)
            print(fila)
            self.asientos.append(fila)
            count += 4
            asientos_curso1 = []
            asientos_curso2= []
            asientos_curso1_M = []
            asientos_curso2_M = []

        for fila in filas_curso1:
            print(fila)
            #? Añadimos los asientos del curso 1 a una lista
            for i in range ( 0, len(self.asientos[fila])):
                asientos_curso1.append(self.asientos[fila][i])
                #? Añadimos los asientos de movilidad reducida del curso 1 a una lista
                if fila in filas_mov_red: 
                    asientos_curso1_M.append(self.asientos[fila][i])

        for fila in filas_curso2:
            
            #? Añadimos los asientos del curso 2 a una lista
            for i in range ( 0, len(self.asientos[fila])):
                asientos_curso2.append(self.asientos[fila][i])
                #? Añadimos los asientos de movilidad reducida del curso 2 a una lista
                if fila in filas_mov_red: 
                    asientos_curso2_M.append(self.asientos[fila][i])

        #* Los asientos en ventanilla se identificarán con los indices minimo y maximo de cada fila 

            



        """ asientos_categorizados = {
            # "ventanilla": ventanilla,
            "mov_red_1": asientos_curso1_M,
            "mov_red_2": asientos_curso2_M,
            "asientos_curso1": asientos_curso1,
            "asientos_curso2": asientos_curso2
        } """
        return self.asientos, asientos_curso1, asientos_curso2, asientos_curso1_M, asientos_curso2_M



    def print_students_data(self):
        print(f"Alumnos del curso 1: {self.alumnos_categorizados['Alumnos_curso1']}",
            f"Alumnos del curso 2: {self.alumnos_categorizados['Alumnos_curso2']}",
            f"Alumnos con movilidad reducida: {self.alumnos_categorizados['Alumnos_mov_red']}",
            f"Alumnos conflictivos: {self.alumnos_categorizados['Alumnos_conf']}",
            f"Hermanos: {self.alumnos_categorizados['Hermanos']}", sep = "\n", end="\n\n")

    def print_bus_data(self):
        print(self.trasform_data_bus())
        

# First of all we create the variables of the exercise
# All of them are represented in the transformed data. 

"""     def create_variables (self):
        #! Variables of the problem
        # we get the transformed data of students; They will be our variables
        Alumnos_curso1, Alumnos_curso2, Alumnos_mov_red, Alumnos_conf, Hermanos = self.alumnos_categorizados.values()

        # We obtain the domain of the variables
        asientos_ventanilla, asientos_mov_red_1,asientos_mov_red_2, asientos_curso1, asientos_curso2= self.asientos_categorizados.values()
        
        for alumno in Alumnos_curso1:
            if alumno in Alumnos_mov_red:
                self.problem.addVariable(alumno, asientos_mov_red_1)
            else:
                self.problem.addVariable(alumno, asientos_curso1)

        for alumno in Alumnos_curso2:
            if alumno in Alumnos_mov_red:
                self.problem.addVariable(alumno, asientos_mov_red_2)
            else:
                self.problem.addVariable(alumno, asientos_curso2)

        return self.problem
    def conflictive_conflictive (self): 
        #! Restrictions of the problem

        # we get the transformed data of students; They will be our variables
        Alumnos_curso1, Alumnos_curso2, Alumnos_mov_red, Alumnos_conf, Hermanos = self.alumnos_categorizados.values()

        # We obtain the domain of the variables
        asientos_ventanilla, asientos_mov_red_1,asientos_mov_red_2, asientos_curso1, asientos_curso2= self.asientos_categorizados.values()

         """
        

"""         for fila in filas_curso1:



        for asiento in asientos:
            # Categorizarlos según si están al lado de la ventanilla
            if asiento[Bus.VENTANILLA] == 'v':
                ventanilla.append(asiento[0])

            # Categorizarlos según su curso
            # Los primeros 16 asientos son para el curso 1
            # Los siguientes 16 asientos son para el curso 2
            if int(asiento[Bus.ID]) <= 16:
                
                # Categorizarlos según si son para movilidad reducida
                if asiento[Bus.MOV_RED] == 'r':
                    mov_red_1.append(asiento[0])
                else:
                    asientos_curso1.append(asiento[0])

            else:
                
                # Categorizarlos según si son para movilidad reducida
                if asiento[Bus.MOV_RED] == 'r':
                    mov_red_2.append(asiento[0])
                else:
                    asientos_curso2.append(asiento[0])

        









        f"Asientos de la ventanilla: {self.asientos_categorizados['ventanilla']}",
            f"Asientos con movilidad reducida: {self.asientos_categorizados['mov_red']}",
            f"Asientos del curso 1: {self.asientos_categorizados['asientos_curso1']}",
            f"Asientos del curso 2: {self.asientos_categorizados['asientos_curso2']}", sep = "\n", end="\n\n"






        def create_variables (self):
        #! Variables of the problem
        # we get the transformed data of students; They will be our variables
        Alumnos_curso1, Alumnos_curso2, Alumnos_mov_red, Alumnos_conf, Hermanos = self.alumnos_categorizados.values()

        # We obtain the domain of the variables
        asientos_ventanilla, asientos_mov_red_1,asientos_mov_red_2, asientos_curso1, asientos_curso2= self.asientos_categorizados.values()
        
        for alumno in Alumnos_curso1:
            if alumno in Alumnos_mov_red:
                self.problem.addVariable(alumno, asientos_mov_red_1)
            else:
                self.problem.addVariable(alumno, asientos_curso1)

        for alumno in Alumnos_curso2:
            if alumno in Alumnos_mov_red:
                self.problem.addVariable(alumno, asientos_mov_red_2)
            else:
                self.problem.addVariable(alumno, asientos_curso2)

        return self.problem 
 """
                

if __name__ == "__main__":
    # Creamos el objeto de la clase
    cspCargaBus = CSPCargaBUS("alumnos.csv", "bus.csv")
    cspCargaBus.print_students_data()
    cspCargaBus.print_bus_data()
