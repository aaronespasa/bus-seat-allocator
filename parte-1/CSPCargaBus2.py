"""
Este archivo contiene el que es el primer paso en la resolución del problema, 
la identificación de los datos y su transformación para su posterior utilización. 
"""
import csv

from enum import IntEnum
""" from . import CAPACIDAD, ASIENTOS_FILA, FILAS_MOV_RED, FILAS_CURSO1, FILAS_CURSO2 """

from constraint import *

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

        self.problem = Problem()

        #? Información de el bus que se va a utilizar
        #todo: Leer el archivo con los datos del bus
        self.capacidad = 32
        self.asientos_fila = 4
        self.filas_mov_red =[0,3,4]
        self.filas_curso1 = [0,1,2,3]
        self.filas_curso2 = [4,5,6,7]
        self.right_column = []
        self.left_column = []

        self.asientos = []
        self.asientos_curso1=[]
        self.asientos_curso2=[]
        self.asientos_curso1_M=[]
        self.asientos_curso2_M=[]
        



        #? Información de los alumnos categorizados
        self.Alumnos_curso1 = []
        self.Alumnos_curso2 = []
        self.Alumnos_mov_red = []
        self.Alumnos_conf = []
        self.Hermanos = []
        
        #?Llamadas a las funciones básicas 
        self.alumnos_categorizados = self.transform_data_students()
        self.asientos_categorizados = self.trasform_data_bus()
        self.create_variables()
        self.create_restrictions()
        #self.asientos = self.trasform_data_bus()['asientos']
        #self.asientos_categorizados = self.trasform_data_bus()

        

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
            - self.Hermanos
        """
        alumnosCSVFields, alumnos = self.csv_to_list(self.ALUMNOS_CSV_PATH)

        class Alumno(IntEnum):
            ID = alumnosCSVFields.index("id")
            CURSO = alumnosCSVFields.index("Ciclo")
            CONFLICTIVO = alumnosCSVFields.index("Conflictivo")
            MOV_RED = alumnosCSVFields.index("Movilidad")
            ID_HERMANO = alumnosCSVFields.index("IdHermano")

        
        aux_hermanos = []

        for alumno in alumnos:
            # Categorizarlos según su curso
            if alumno[Alumno.CURSO] == '1':
                self.Alumnos_curso1.append(alumno[Alumno.ID])
            else:
                self.Alumnos_curso2.append(alumno[Alumno.ID])

            # Categorizarlos según si son conflictivos
            if alumno[Alumno.CONFLICTIVO] == 'C':
                self.Alumnos_conf.append(alumno[Alumno.ID])
            
            # Categorizarlos según si tienen movilidad reducida
            if alumno[Alumno.MOV_RED] == 'R':
                self.Alumnos_mov_red.append(alumno[Alumno.ID])

            # Categorizarlos según si son self.hermanos
            if alumno[Alumno.ID_HERMANO] != '0' and alumno[Alumno.ID] not in aux_hermanos :
                aux_hermanos.append(alumno[Alumno.ID])
                aux_hermanos.append(alumno[Alumno.ID_HERMANO])
                self.Hermanos.append([alumno[Alumno.ID],alumno[Alumno.ID_HERMANO]])
    
        # print(self.Hermanos)

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

        # class infoBus(IntEnum):
        #     capacidad = busCSVFields.index("capacidad")
        #     asientos_fila = busCSVFields.index("asientos_fila")
        #     filas_mov_red = busCSVFields.index("movilidad_reducida")
        #     filas_curso1 = busCSVFields.index("curso1")
        #     filas_curso2 = busCSVFields.index("curso2")

        # Grupos en los que categorizaremos a los asientos
        #! Todo esto tiene que ir dentro de el nuevo archivo de configuración de bus 

        
        count = 1
        
        for i in range(0, self.capacidad, self.asientos_fila):
            fila = []
            fila.append(count)
            fila.append(count+1)
            fila.append(count+2)
            fila.append(count+3)
            self.asientos.append(fila)
            count += 4
            

        for fila in self.filas_curso1:
            # print(fila)
            #? Añadimos los asientos del curso 1 a una lista incluyendo los de movilidad reducida
            for i in range ( 0, len(self.asientos[fila])):
                self.asientos_curso1.append(self.asientos[fila][i])
                #? Añadimos los asientos de movilidad reducida del curso 1 a una lista
                if fila in self.filas_mov_red: 
                    self.asientos_curso1_M.append(self.asientos[fila][i])

        for fila in self.filas_curso2:
            
            #? Añadimos los asientos del curso 2 a una lista (incluyendo los de mov reducida)
            for i in range ( 0, len(self.asientos[fila])):
                self.asientos_curso2.append(self.asientos[fila][i])
                #? Añadimos los asientos de movilidad reducida del curso 2 a una lista
                if fila in self.filas_mov_red: 
                    self.asientos_curso2_M.append(self.asientos[fila][i])

        #* Las listas contienen los indices de los asientos, no los asientos en sí
        media_fila = self.asientos_fila/2
        for i in range(self.asientos_fila):
            if i < media_fila:
                self.left_column.append(i)
            else:
                self.right_column.append(i)


# First of all we create the variables of the exercise
# All of them are represented in the transformed data. 

    def create_variables (self):
        #! Variables of the problem

        
        hermanos_list = []
        for alumno in (self.Alumnos_curso1 + self.Alumnos_curso2):
            for alumno2 in (self.Alumnos_curso1 + self.Alumnos_curso2):
                brothers = [alumno, alumno2]
                if brothers in self.Hermanos:
                    if (alumno2 in self.Alumnos_curso1 or alumno in self.Alumnos_curso1):
                        if alumno in self.Alumnos_mov_red:
                            self.problem.addVariable(alumno, self.asientos_curso1_M)
                            print(f"El alumno {alumno} puede sentarse en {self.asientos_curso1_M}")
                        else:
                            self.problem.addVariable(alumno, self.asientos_curso1)
                            print(f"El alumno {alumno} puede sentarse en {self.asientos_curso1}")
                        if alumno2 in self.Alumnos_mov_red:
                            self.problem.addVariable(alumno2, self.asientos_curso1_M)
                            print(f"El alumno {alumno2} puede sentarse en {self.asientos_curso1_M}")
                        else:
                            self.problem.addVariable(alumno2, self.asientos_curso1)
                            print(f"El alumno {alumno2} puede sentarse en {self.asientos_curso1}")
                        # Los self.hermanos mayores tienen que poder sentarse solo en el curso del pequeño
                        # siempre que haya uno de primer curso
                        hermanos_list.append(alumno)
                        hermanos_list.append(alumno2)
        print(hermanos_list)
        for alumno in self.Alumnos_curso1:
            if alumno not in hermanos_list:             
                if alumno in self.Alumnos_mov_red:
                    self.problem.addVariable(alumno,self.asientos_curso1_M)
                    print(f"El alumno {alumno} puede sentarse en {self.asientos_curso1_M}")
                else:
                    self.problem.addVariable(alumno, self.asientos_curso1)
                    print(f"El alumno {alumno} puede sentarse en {self.asientos_curso1}")
                    

        for alumno in self.Alumnos_curso2:
            if alumno not in hermanos_list:             
                if alumno in self.Alumnos_mov_red:
                    self.problem.addVariable(alumno, self.asientos_curso2_M)
                    print(f"El alumno {alumno} puede sentarse en {self.asientos_curso2_M}")
                else:
                    self.problem.addVariable(alumno, self.asientos_curso2)
                    print(f"El alumno {alumno} puede sentarse en {self.asientos_curso2}")

    def get_possible_brothers(self, alumno1, alumno2) -> tuple:
        return [alumno1, alumno2], [alumno2, alumno1]

    def create_restrictions (self):
        #! Restrictions of the problem
        #? Restriccion para que todos los alumnos ocupen asientos diferentes 
        for alumno1 in self.Alumnos_curso1 + self.Alumnos_curso2:
            for alumno2 in self.Alumnos_curso1 + self.Alumnos_curso2:
                if alumno1 != alumno2:
                    #print(f"El alumno {alumno1} no puede sentarse en el mismo asiento que {alumno2}")
                    self.problem.addConstraint(self.AllDifferentConstraint, (alumno1, alumno2))

        #? Restriccion para que los hermanos se sienten juntos excepto si uno de ellos es de movilidad reducida
        for alumno1 in self.Alumnos_curso1 + self.Alumnos_curso2:
            for alumno2 in self.Alumnos_curso2 + self.Alumnos_curso1:
                posibles_hermanos1, posibles_hermanos2 = self.get_possible_brothers(alumno1, alumno2)
                if alumno1 != alumno2:
                    if alumno1 not in self.Alumnos_mov_red and alumno2 not in self.Alumnos_mov_red:
                        if posibles_hermanos1 in self.Hermanos or posibles_hermanos2 in self.Hermanos:
                            print("hi")
                            #print(f"Los alumnos {alumno1} y {alumno2} son hermanos")
                            self.problem.addConstraint(self.hermanos, (alumno1, alumno2))
        #? Restriccion para que los hermanos mayores siempre estén en el pasillo. 
        for alumno1 in self.Alumnos_curso1:
            for alumno2 in self.Alumnos_curso2:
                posibles_hermanos1, posibles_hermanos2 = self.get_possible_brothers(alumno1, alumno2)
                if alumno1 != alumno2:
                    if posibles_hermanos1 in self.Hermanos or posibles_hermanos2 in self.Hermanos:
                        #print(f"Los alumnos {alumno1} y {alumno2} son hermanos")
                        self.problem.addConstraint(self.hermanos_1_2, (alumno1, alumno2))
                    
        #? Restriccion para que los alumnos conflictivos no se sienten juntos
        for alumno1 in self.Alumnos_conf:
            for alumno2 in self.Alumnos_conf: 
                posibles_hermanos1, posibles_hermanos2 = self.get_possible_brothers(alumno1, alumno2)
                # print(f"Los alumnos {alumno1} y {alumno2} son conflictivos"
                # print(f"Hermanos posibles 1: {posibles_hermanos1}")
                # print(f"Self hermanos: {self.Hermanos}")
                if posibles_hermanos1 not in self.Hermanos and posibles_hermanos2 not in self.Hermanos:
                    print("no son hermanos")
                    if alumno1 != alumno2:
                        #and posibles_hermanos1 not in self.Hermanos and posibles_hermanos2 not in self.Hermanos:
                        #print(f"Los alumnos {alumno1} y {alumno2} son conflictivos")
                        self.problem.addConstraint(self.conflictivos, (alumno1, alumno2))
                    
        #? Restriccion para que los alumnos de movilidad reducida tengan espacio a los lados
        for alumno in self.Alumnos_mov_red:
            for alumno2 in self.Alumnos_curso1 + self.Alumnos_curso2:
                
                if alumno != alumno2:
                    # print(f"El alumno {alumno} tiene que tener espacio a los lados")
                    print(f"Somos {alumno} y {alumno2}")	
                    self.problem.addConstraint(self.mov_red, (alumno, alumno2))

    def mov_red(self, alumno1, alumno2):
        fila_alumno1, columna_alumno1 = self.encontrar_indices(alumno1) 
        fila_alumno2, columna_alumno2 = self.encontrar_indices(alumno2)
       
        if fila_alumno1 == fila_alumno2:
            if columna_alumno1 in self.left_column and columna_alumno2 in self.right_column:
                # print(f"Los alumnos {alumno1} y {alumno2} okay movred (misma fila y lados)")
                return True
            elif columna_alumno2 in self.right_column and columna_alumno1 in self.left_column:
                # print(f"Los alumnos {alumno1} y {alumno2} okay movred (misma fila y lados)")
                return True
            else: 
                # En el modelo que nos dan no haría falta, pero edsta way para generalizarlo 
                # para otros buses con más asientos por fila
                if abs(fila_alumno1-fila_alumno2) >=2: 
                    # print(f"Los alumnos {alumno1} y {alumno2} okay movred no tiene que salir")
                    return True
                else:
                    return False
        else: 
            # print(f"Los alumnos {alumno1} y {alumno2} okay movred")
            return True


    def conflictivos(self, alumno1, alumno2):
        fila_alumno1, columna_alumno1 = self.encontrar_indices(alumno1)
         
        fila_alumno2, columna_alumno2 = self.encontrar_indices(alumno2)

        if abs(columna_alumno1 - columna_alumno2) <2 and abs(fila_alumno1 - fila_alumno2) <2:
            return False
        else:
            return True


    def hermanos_1_2 (self, alumno1, alumno2):
        """ EL mayor debe estar en la posición del pasillo """
        # Para usarlo para mas asientos habría que darle una vuelta 
        fila_alumno1, columna_alumno1 = self.encontrar_indices(alumno1)
         
        fila_alumno2, columna_alumno2 = self.encontrar_indices(alumno2)

        if fila_alumno1 != fila_alumno2: 
            return False
        else:
            if columna_alumno1 in self.left_column and columna_alumno2 in self.right_column:
                return False
            elif columna_alumno1 in self.right_column and columna_alumno2 in self.left_column:
                return False
            elif (columna_alumno1 in self.left_column and columna_alumno2 in self.left_column) :
                if columna_alumno2 > columna_alumno1:
                #esto significaria que el mayor esta en el pasillo 
                    #print(f"el mayor esta donde debe estar {alumno1} y {alumno2}")
                    return True
                else: 
                    #print(f"el mayor no esta donde debe estar {alumno1} y {alumno2}")
                    return False
            else:
                if columna_alumno1 > columna_alumno2:
                        #esto significaria que el mayor esta en el pasillo 
                    #print(f"el mayor esta donde debe estar {alumno1} y {alumno2}")
                    return True
                else: 
                    #print(f"el mayor no esta donde debe estar {alumno1} y {alumno2}")
                    return False
    def AllDifferentConstraint(self,alumno1, alumno2):
        if alumno1 != alumno2:
            return True
        else:
            return False

    def hermanos(self, alumno1, alumno2):
        fila_alumno1, columna_alumno1 = self.encontrar_indices(alumno1)
        fila_alumno2, columna_alumno2 = self.encontrar_indices(alumno2)

        if fila_alumno1 != fila_alumno2: 
            return False
        else:
            if columna_alumno1 in self.left_column and columna_alumno2 in self.right_column:
                return False
            elif columna_alumno1 in self.right_column and columna_alumno2 in self.left_column:
                return False
            else:
                
                if abs(columna_alumno1 - columna_alumno2) == 1:
                    return True

    def encontrar_indices(self, id): 
        x, y = -1, -1
        
        for fila in range(len(self.asientos)):
            
            if id in self.asientos[fila]:
                #print(f"asiento: {self.asientos[fila]}")
                x=fila
                y=self.asientos[fila].index(id)

        if x == -1 or y == -1:
            raise Exception(f"No se ha encontrado el asiento con id {id}")

        return x, y

    
    def print_bus_data(self):
        """Imprimir los datos de los buses"""

        print("asientos: ", self.asientos)
        print("asientos_curso1: ", self.asientos_curso1)
        print("asientos_curso2: ", self.asientos_curso2)
        print("mov_red_1: ", self.asientos_curso1_M)
        print("mov_red_2: ", self.asientos_curso2_M)

    def print_students_data(self):
        print(f"Alumnos del curso 1: {self.Alumnos_curso1}",
            f"Alumnos del curso 2: {self.Alumnos_curso2}",
            f"Alumnos con movilidad reducida: {self.Alumnos_mov_red}",
            f"Alumnos conflictivos: {self.Alumnos_conf}",
            f"self.Hermanos: {self.Hermanos}", sep = "\n", end="\n\n")

def print_solution(solution):
    """Imprimir la solución"""
    if solution is None:
        print("\nNo hay solución")
    else:
        print("\nEl problema tiene al menos una solución")
        print("Solución:")
        for student_id, seat_number in solution.items():
            print(f"Alumno {student_id} se sienta en el asiento {seat_number}")
    print("\n")

if __name__ == "__main__":
    # Creamos el objeto de la clase
    cspCargaBus = CSPCargaBUS("alumnos.csv", "bus.csv")
    # cspCargaBus.print_students_data() 
    # cspCargaBus.print_bus_data()          
    print_solution(cspCargaBus.problem.getSolution())

# First of all we create the variables of the exercise
# All of them are represented in the transformed data. 