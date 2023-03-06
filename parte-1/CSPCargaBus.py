"""
Este archivo contiene el que es el primer paso en la resolución del problema, 
la identificación de los datos y su transformación para su posterior utilización. 
"""
import csv
import sys
import json

from enum import IntEnum
from utils.bus import CAPACIDAD, ASIENTOS_FILA, FILAS_MOV_RED, FILAS_CURSO1, FILAS_CURSO2

from constraint import *

class CSPCargaBUS:
    def __init__(self, studentsCSVFilename:str, busjsonFilename:str):
        """
        Input:
            studentsCSVFilename (str): Nombre del archivo csv con los datos de los alumnos (dentro de CSP-tests).
            busCSVFilename (str): Nombre del archivo csv con los datos de los buses (dentro de CSP-tests).
        """
        self.ALUMNOS_CSV_PATH = studentsCSVFilename

        self.problem = Problem()

        #? Información de el bus que se va a utilizar
        #todo: Leer el archivo con los datos del bus
        # leer los datos de bus.json
        
        self.fill_data_bus(busjsonFilename)

        self.right_column = []
        self.left_column = []

        #? Categorizamos lo que será el dominio de nuestras variables 
        self.asientos = []
        self.asientos_curso1=[]
        self.asientos_curso2=[]
        self.asientos_curso1_M=[]
        self.asientos_curso2_M=[]
        



        #? Listas empleadas para categorizar nuestras varibles, los alumnos, 
        #? de modo que se les puedan aplicar dominios y restricciones por grupos
        self.Alumnos_curso1 = []
        self.Alumnos_curso2 = []
        self.Alumnos_mov_red = []
        self.Alumnos_conf = []
        self.Hermanos = []

        # Para que el output este en el formato correcto al finalizar la ejecución, 
        # creamos un diccionario con el id  como indice que devuelva el nombre de la 
        # variable con el formato correcto 
        self.correct_variables = {}
        
        #?Llamadas a las funciones básicas 
        self.alumnos_categorizados = self.transform_data_students()
        self.asientos_categorizados = self.trasform_data_bus()
        self.create_variables()
        self.create_restrictions()


    def fill_data_bus(self, busjsonFilename:str):
        """Lee los datos del bus y los almacena en las variables de la clase"""
        busdata = None
        with open(busjsonFilename, 'r') as busfile:
            busdata = json.load(busfile)

        if busdata is None:
            print("Error al leer el archivo de datos del bus")
            sys.exit(1)

        self.capacidad = busdata['capacidad']
        self.asientos_fila = busdata['asientos_fila']
        self.filas_mov_red = busdata['filas_mov_red']
        self.filas_curso1 = busdata['filas_curso1']
        self.filas_curso2 = busdata['filas_curso2']
        

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

            # Para que el output este en el formato correcto al finalizar la ejecución, 
            # creamos un diccionario con el id  como indice que devuelva el nombre de la 
            # variable con el formato correcto 
            if alumno[Alumno.ID] in self.Alumnos_conf:
                if alumno[Alumno.ID] in self.Alumnos_mov_red:
                    self.correct_variables[str(alumno[Alumno.ID])] = f"{alumno[Alumno.ID]}CR"
                else: 
                    self.correct_variables[str(alumno[Alumno.ID])] = f"{alumno[Alumno.ID]}CX"
            else:
                if alumno[Alumno.ID] in self.Alumnos_mov_red:
                    self.correct_variables[str(alumno[Alumno.ID])] = f"{alumno[Alumno.ID]}XR"
                else: 
                    self.correct_variables[str(alumno[Alumno.ID])] = f"{alumno[Alumno.ID]}XX"


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

        
        count = 1
        # Emplea las caracteristicas especificadas del bus para crear una matriz de asientos;
        # De estemodo el algoritmo es aplicable a cualquier bus con caracteristicas similares 
        # ( ej: más asientos con la misma estructura )
        for i in range(0, self.capacidad, self.asientos_fila):

            fila = []
            for j in range(0, self.asientos_fila):
                fila.append(count+j)

            self.asientos.append(fila)
            count += self.asientos_fila
            

        for fila in self.filas_curso1:
            #? Añadimos los asientos del curso 1 a una lista incluyendo los de movilidad reducida
            #? La decisión de que estén incluidos es debido a que las personas sin movilidad reducida 
            #? pueden ocupar los asientos de movilidad reducida
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

        #* Notese que aunque las listas contienen el número de asiento, 
        #* este solo se empleapara obtener el índice

        # Gracias a estas listas podemos identificar que columnas están a cada
        # lado del pasillo, facilitando enormemente la asignación de asientos
        media_fila = self.asientos_fila/2
        for i in range(self.asientos_fila):
            if i < media_fila:
                self.left_column.append(i)
            else:
                self.right_column.append(i)



# Teniendo todo lo anterior, podemos crear las variables del problema
    def create_variables (self):
        """Crear las variables del problema"""

        hermanos_list = []
        for alumno in (self.Alumnos_curso1 + self.Alumnos_curso2):
            for alumno2 in (self.Alumnos_curso1 + self.Alumnos_curso2):
                brothers = [alumno, alumno2]
                if brothers in self.Hermanos:
                    if (alumno2 in self.Alumnos_curso1 or alumno in self.Alumnos_curso1):
                        # De este modo los alumnos de 2º con un hermano en primero tienen asignado un asiento en el curso  
                        if alumno in self.Alumnos_mov_red:
                            # se añade el dominio de los asientos de movilidad reducida 
                            self.problem.addVariable(alumno, self.asientos_curso1_M)
                            
                        else:
                            # se añade el dominio a los alumnos que no tienen movilidad reducida
                            self.problem.addVariable(alumno, self.asientos_curso1)
                            
                        if alumno2 in self.Alumnos_mov_red:
                            # se añade el dominio de los asientos de movilidad reducida 
                            self.problem.addVariable(alumno2, self.asientos_curso1_M)
                            
                        else:
                            # se añade el dominio a los alumnos que no tienen movilidad reducida
                            self.problem.addVariable(alumno2, self.asientos_curso1)
                            
                        # se añaden los alumnos a una lista para que no se repitan
                        hermanos_list.append(alumno)
                        hermanos_list.append(alumno2)
        
        for alumno in self.Alumnos_curso1:
            if alumno not in hermanos_list:             
                if alumno in self.Alumnos_mov_red:
                    # se añade el dominio de los asientos de movilidad reducida de primero
                    # de aquellos alumnos con movilidad reducida que aun no tienen 
                    # dominio asignado
                    self.problem.addVariable(alumno,self.asientos_curso1_M)
                   
                else:
                    # se añade el dominio de los asientos de primero
                    # a aquellos alumnos de primero que aun no tienen 
                    # dominio asignado
                    self.problem.addVariable(alumno, self.asientos_curso1)
                 
                    

        for alumno in self.Alumnos_curso2:
            if alumno not in hermanos_list:             
                if alumno in self.Alumnos_mov_red:
                    # se añade el dominio de los asientos de movilidad reducida de segundo
                    # de aquellos alumnos con movilidad reducida que aun no tienen 
                    # dominio asignado
                    self.problem.addVariable(alumno, self.asientos_curso2_M)
                    
                else:
                    # se añade el dominio de los asientos de segundo
                    # a aquellos alumnos de segundo que aun no tienen 
                    # dominio asignado
                    self.problem.addVariable(alumno, self.asientos_curso2)
                    

    def get_possible_brothers(self, alumno1, alumno2) -> tuple:
        """Devuelve dos listas en ambos ordenes de los alumnos dados 
        para facilitar la comprobación de hermanos"""
        return [alumno1, alumno2], [alumno2, alumno1]

    def create_restrictions (self):
        """Crear las restricciones del problema"""
        #? Restriccion para que todos los alumnos ocupen asientos diferentes 
        for alumno1 in self.Alumnos_curso1 + self.Alumnos_curso2:
            for alumno2 in self.Alumnos_curso1 + self.Alumnos_curso2:
                if alumno1 != alumno2:
                    self.problem.addConstraint(self.AllDifferentConstraint, (alumno1, alumno2))

        #? Restriccion para que los alumnos de movilidad reducida tengan espacio a los lados
        for alumno in self.Alumnos_mov_red:
            for alumno2 in self.Alumnos_curso1 + self.Alumnos_curso2:
                if alumno != alumno2:
                    self.problem.addConstraint(self.mov_red, (alumno, alumno2))

        #? Restriccion para que los hermanos se sienten juntos excepto si uno de ellos es de movilidad reducida
        for alumno1 in self.Alumnos_curso1 + self.Alumnos_curso2:
            for alumno2 in self.Alumnos_curso2 + self.Alumnos_curso1:
                posibles_hermanos1, posibles_hermanos2 = self.get_possible_brothers(alumno1, alumno2)
                if alumno1 != alumno2:
                    if alumno1 not in self.Alumnos_mov_red and alumno2 not in self.Alumnos_mov_red:
                        if posibles_hermanos1 in self.Hermanos or posibles_hermanos2 in self.Hermanos:
                            self.problem.addConstraint(self.hermanos, (alumno1, alumno2))

        #? Restriccion para que los hermanos mayores siempre estén en el pasillo. 
        for alumno1 in self.Alumnos_curso1:
            for alumno2 in self.Alumnos_curso2:
                posibles_hermanos1, posibles_hermanos2 = self.get_possible_brothers(alumno1, alumno2)
                if alumno1 != alumno2:
                    if alumno1 not in self.Alumnos_mov_red and alumno2 not in self.Alumnos_mov_red:
                        if posibles_hermanos1 in self.Hermanos or posibles_hermanos2 in self.Hermanos:
                            
                            self.problem.addConstraint(self.hermanos_1_2, (alumno1, alumno2))
                    
        #? Restriccion para que los alumnos conflictivos no se sienten juntos
        for alumno1 in self.Alumnos_conf:
            for alumno2 in self.Alumnos_conf: 
                posibles_hermanos1, posibles_hermanos2 = self.get_possible_brothers(alumno1, alumno2)
                if posibles_hermanos1 not in self.Hermanos and posibles_hermanos2 not in self.Hermanos:
                    if alumno1 != alumno2:
                        self.problem.addConstraint(self.conflictivos, (alumno1, alumno2))
                    


    def mov_red(self, alumno1, alumno2):
        """Restriccion para que los alumnos de movilidad reducida tengan espacio a los lados"""
        fila_alumno1, columna_alumno1 = self.encontrar_indices(alumno1) 
        fila_alumno2, columna_alumno2 = self.encontrar_indices(alumno2)
       # si los alumnos no están en la misma fila no hay problema
        if fila_alumno1 == fila_alumno2:
            # En el primer caso y el segundo, los alumnos estan en distintos lados del pasillo, 
            # por lo que no hay problema
            # Sin embargo en el tercer caso, los alumnos estan en el mismo lado del pasillo,
            # por lo que el bus base esto nunca sería válido. 
            if columna_alumno1 in self.left_column and columna_alumno2 in self.right_column:
                return True
            elif columna_alumno2 in self.right_column and columna_alumno1 in self.left_column:
                return True
            else: 
                # En el modelo que nos dan no haría falta, pero ayudaría a generalizarlo a un bus con 
                # más asientos por fila
                # Notese que no se han logrado resultados positivos en esta generalización por 
                # falta de tiempo
                if abs(columna_alumno1-columna_alumno2) >=2: 
                    return True
                else:
                    return False
        else: 
            return True


    def conflictivos(self, alumno1, alumno2):
        """ Restriccion para que los alumnos conflictivos no se sienten cerca """
        fila_alumno1, columna_alumno1 = self.encontrar_indices(alumno1)
         
        fila_alumno2, columna_alumno2 = self.encontrar_indices(alumno2)

        if abs(columna_alumno1 - columna_alumno2) <2 and abs(fila_alumno1 - fila_alumno2) <2:
            #si no se dan ambas condiciones a la vez, no hay problema ya que no estarían cerca
            return False
        else:
            return True


    def hermanos_1_2 (self, alumno1, alumno2):
        """ Restricción para que el hermano mayor esté en la posición del pasillo """

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
                    return True
                else: 
                    return False
            else:
                if columna_alumno1 > columna_alumno2:
                        #esto significaria que el mayor esta en el pasillo 
                    return True
                else: 
                    return False

    def AllDifferentConstraint(self,alumno1, alumno2):
        """ Restriccion para que a todos los alumnos se les asigne un asiento diferente"""
        if alumno1 != alumno2:
            return True
        else:
            return False

    def hermanos(self, alumno1, alumno2):
        """ Restriccion para que los hermanos se sienten juntos """

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
            # si están sentados en la misma fila y en el mismo lado del pasillo,
            # se comprueba que estén sentados juntos dado el bus propuesto
                if abs(columna_alumno1 - columna_alumno2) == 1:
                    return True

    def encontrar_indices(self, id): 
        x, y = -1, -1
        
        for fila in range(len(self.asientos)):
            
            if id in self.asientos[fila]:
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
    def transform_output(self, output):
        """Transformar la salida del solver a un formato más legible"""
        transformed_output = {}
        for alumno in self.Alumnos_curso1 + self.Alumnos_curso2:
            Asiento_para_alumno = output[alumno]
            # print(f"nueva funcion: Alumno {alumno} -> Asiento {Asiento_para_alumno}")
            transformed_output[self.correct_variables[alumno]] = Asiento_para_alumno

        return transformed_output
    def print_solution(self,solution):
        """Imprimir la solución"""
        if solution is None:
            print("\nNo hay solución")
        else:
            print("\nEl problema tiene al menos una solución")

        printable = self.transform_output(solution)
        # la función transform_output devuelve un diccionario con el formato correcto
        # para su empleo en la parte dos del proyecto
        print(f"El formato de la solucion es {printable}")
        print("\n")
        # Exportamos la solución a un archivo .prob
        with open('alumnos.prob', 'w') as f:
            f.write(str(printable))
        print("La solucion se ha exportado a solution.prob")


if __name__ == "__main__":
    # sys.argv[0] = "cspCargaBus.py"
    # sys.argv[1] = "alumnos.csv"
    # sys.argv[2] = "bus.csv"
    studentsFilename = sys.argv[1]
    busFilename = sys.argv[2]
    # Creamos el objeto de la clase
    cspCargaBus = CSPCargaBUS(studentsFilename, busFilename)       
    cspCargaBus.print_solution(cspCargaBus.problem.getSolution())
