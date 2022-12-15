"""
A Star Search Algorithm implementation that fills a bus queue with passengers.
"""
import sys
from src.utils.parseArguments import parse_arguments
from src.utils.parseInputFile import parse_alumnos_input, \
                                     print_alumnos, \
                                     StudentTuple, \
                                     StudentTypes
from src.utils.saveState import save_state, save_statistics
from src.utils.getFileContent import get_file_content
from functools import cmp_to_key
from datetime import datetime

class ASTARColaBus:
    """
    A Star Search Algorithm implementation that fills a bus queue with passengers.
    """
    def __init__(self, alumnos:dict, queue_length:int, heuristic_name:str) -> None:
        """Initializes the A Star Search Algorithm.
            - alumnos_tuples: Dictionary whose keys are the student IDs and the values are tuples
                              with the student type and the seat number (StudentTuple).
            - nodes: Dictionary whose keys are the student IDs and the values are boolean values
                     that indicate if the student has been added to the queue or not (visited or not).
                     All the values are initialized to False as they haven't been visited yet.
            - open_list: List of nodes that have been visited but have not been expanded yet.
        """
        self.__alumnos_tuples = alumnos
        self.__nodes = {key: False for key in self.__alumnos_tuples.keys()}
        self.__start_node = self.get_starting_node()
        self.__open_list = []
        self.__get_heuristic_value = self.get_heuristic(heuristic_name)
        self.__queue_length = queue_length
        # self.__empty_element = "0"
        self.__state = self.initialize_state(queue_length)
        # self.__state = ["4", "3", "7", "2", "1", "5", "6", "8"]
    
    @property
    def get_state(self) -> list:
        """Returns the current state."""
        return self.__state

    def get_starting_node(self) -> str:
        """Returns the starting node and removes it from the nodes list
           so it doesn't get added to the open_list."""

        # The starting node is the one with the smallest time (normal type).
        # Priority: 1. Normal, 2. Reduced Mobility, 3. Conflictive, 4. Reduced Mobility Conflictive
        for student_id in self.__nodes.keys():
            if self.__alumnos_tuples[student_id][StudentTuple.TYPE] == StudentTypes.NORMAL:
                self.__nodes[student_id] = True
                return student_id
        for student_id in self.__nodes.keys(): # executed in the case that there are no normal students
            if self.__alumnos_tuples[student_id][StudentTuple.TYPE] == StudentTypes.REDUCED_MOBILITY:
                self.__nodes[student_id] = True
                return student_id
        for student_id in self.__nodes.keys(): # no normal or reduced mobility students
            if self.__alumnos_tuples[student_id][StudentTuple.TYPE] == StudentTypes.CONFLICTIVE:
                self.__nodes[student_id] = True
                return student_id

        # if there are no normal, reduced mobility or conflictive students, then the starting node
        # is the first one in the list
        self.__nodes[0] = True
        return self.__nodes[0]

    def heuristic_count_queue_spaces(self, _) -> int:
        """Counts the number of empty spaces in the queue when adding a new node."""
        return self.__queue_length - len(self.__state)
    
    def heuristic_weights(self, node:str) -> int:
        """Ponderate the students that are left and sum them all."""
        total_students = self.__alumnos_tuples.keys()
        # create a list that substracts the elements from self.__state from total_students
        temporal_state = [node] + [x for x in total_students if x not in self.__state]

        value = 0
        for student_id in temporal_state:
            is_conflictive = self.__alumnos_tuples[student_id][StudentTuple.TYPE] == StudentTypes.CONFLICTIVE
            weight = 0

            if is_conflictive:
                weight = 5
            elif self.has_reduced_mobility(student_id):
                weight = 2
            else: # not conflictive and not reduced mobility
                weight = 3
            
            # multiply by the number of students in order to adapt the A* algorith for longer queues
            value += weight * len(total_students)

        return value

    def get_heuristic(self, heuristic_name:str) -> callable:
        """Gets the heuristic function to use."""
        if heuristic_name == "1":
            return self.heuristic_weights
        elif heuristic_name == "2":
            return self.heuristic_count_queue_spaces
        else:
            raise Exception("Invalid heuristic name")

    def initialize_state(self, queue_length) -> list:
        """Initializes the state with the queue length."""
        # return [self.__empty_element for _ in range(queue_length)]
        return []
    
    def is_conflictive(self, node:str) -> bool:
        """Checks if the node is conflictive."""
        return self.__alumnos_tuples[node][StudentTuple.TYPE] == StudentTypes.CONFLICTIVE or \
               self.__alumnos_tuples[node][StudentTuple.TYPE] == StudentTypes.CONFLICTIVE_REDUCED_MOBILITY
    
    def has_reduced_mobility(self, node:str) -> bool:
        """Checks if the node is reduced mobility."""
        return self.__alumnos_tuples[node][StudentTuple.TYPE] == StudentTypes.REDUCED_MOBILITY or \
               self.__alumnos_tuples[node][StudentTuple.TYPE] == StudentTypes.CONFLICTIVE_REDUCED_MOBILITY

    def get_seat_number(self, node:str) -> int:
        """Gets the seat number of the given node."""
        return self.__alumnos_tuples[node][StudentTuple.SEAT_NUMBER]

    def get_cost_of_state(self, state:list) -> int:
        """Gets the cost of the given state."""
        cost = 0
        previous_had_reduced_mobility = False

        for i in range(len(state)):
            state_cost = 1 # normal cost

            # if the previous student had reduced mobility, then the current student cost is 0
            if previous_had_reduced_mobility:
                state_cost = 0
                previous_had_reduced_mobility = False
            
            if self.has_reduced_mobility(state[i]):
                state_cost = 3
                previous_had_reduced_mobility = True

            # conflictive students duplicate the cost of the previous and next students
            if i + 1 < len(state) and self.is_conflictive(state[i + 1]):
                state_cost *= 2
            if i - 1 >= 0 and self.is_conflictive(state[i - 1]):
                state_cost *= 2

            # check if the previous students were conflictive
            for j in range(i): 
                seat_j, seat_i = self.get_seat_number(state[j]), self.get_seat_number(state[i])
                if self.is_conflictive(state[j]) and seat_j < seat_i:
                    state_cost *= 2

            cost += state_cost
            # cost += state_cost * conflictive_duplication
        
        return cost

    def get_cost_of_adding(self, node:str) -> int:
        """Gets the cost of adding a node to the queue."""
        temporal_state = self.__state.copy() + [node]
        cost = self.get_cost_of_state(temporal_state)
        return cost
    
    def compare_value_h_and_g(self, first_node:str, second_node:str) -> bool:
        """Compares the value of the heuristic + the cost of two give nodes."""
        first_node_value = self.get_cost_of_adding(first_node) + self.__get_heuristic_value(first_node)
        second_node_value = self.get_cost_of_adding(second_node) + self.__get_heuristic_value(second_node)
        # print("Comparing: \'", first_node, "\' with \'", second_node, "\' -> ", first_node_value, " vs ", second_node_value, sep="")
        return first_node_value < second_node_value

    def get_next_node(self) -> str:
        """Gets the next node to expand by sorting the open_list
           and picking the node with the smallest h_value and g_value in that vector."""
        self.__open_list.sort(key=lambda node: self.get_cost_of_adding(node) + self.__get_heuristic_value(node))
        return self.__open_list.pop(0)

    def can_be_added(self, node:str) -> bool:
        """Restrictions -> Checks if the node can be added to the queue."""
        # Do not allow two consectuvie reduced mobility students
        if self.has_reduced_mobility(node) and self.has_reduced_mobility(self.__state[-1]):
            return False
        
        # A reduced mobility student cannot be added at the end of the queue
        if self.has_reduced_mobility(node) and len(self.__state) == self.__queue_length - 1:
            return False

        return True

    def get_neighbors(self, node:str) -> list:
        """Gets the neighbors of the given node."""
        neighbors = []
        for student_id in self.__nodes.keys():
            if self.__nodes[student_id] == False and self.can_be_added(student_id):
                neighbors.append(student_id)
        return neighbors

    def add_neighbors(self, node:str) -> list:
        """
        Add the neighbors of the node to the open_list.

        Check if the node can be added to the queue by checking the restrictions
        and checking that the node has not been added to the queue yet.
        """
        neighbors = self.get_neighbors(node)
        self.__open_list = []
        self.__nodes[node] = True

        for neighbor in neighbors:
            if neighbor not in self.__state:
                self.__open_list.append(neighbor)
                # self.__nodes[neighbor] = True # mark the node as visited

    def has_finished(self) -> bool:
        """Checks if the algorithm has finished."""
        return len(self.__state) == self.__queue_length

    def get_statistics(self, time_diff_in_ms:int, expanded_nodes:int) -> str:
        """Gets the statistics of the algorithm."""
        statistics_str = f"Tiempo total: {time_diff_in_ms:.3f} ms\n"
        statistics_str += f"Coste total: {self.get_cost_of_state(self.__state)}\n"
        statistics_str += f"Longitud del plan: {len(self.__state)}\n"
        statistics_str += f"Nodos expandidos: {expanded_nodes}"
        return statistics_str

    def run(self) -> None:
        """Runs the A Star Search Algorithm.
        
        Add the first node to the open_list. Then, go through all the nodes adding their neighbors and
        taking the one with the lowest sum of G + H values until you find the end node. Then, 
        return the path from the first node to that end node.
        """
        initial_time = datetime.now()
        expanded_nodes = 0

        self.__open_list.append(self.__start_node)
        while len(self.__open_list) > 0 and not self.has_finished():
            current_node = self.get_next_node()
            self.__state.append(current_node)
            self.add_neighbors(current_node)
            expanded_nodes += 1
        
        final_time = datetime.now()
        time_delta = final_time - initial_time

        if len(self.__state) != self.__queue_length:
            raise Exception("No se ha encontrado una solución")
        # elLeft = [x for x in self.__alumnos_tuples.keys() if x not in self.__state]
        # if len(elLeft) > 0:
        #     print("\nElements left: ")
        #     for el in elLeft:
        #         print("-", self.__alumnos_tuples[el][StudentTuple.TYPE].value)

        return self.get_statistics(time_delta.total_seconds() * 1000, expanded_nodes)

    
    def __str__(self) -> str:
        """Returns the types of the students in the queue."""
        state_types = []
        seat_numbers = []
        for studentid in self.__state:
            state_types.append(self.__alumnos_tuples[studentid][StudentTuple.TYPE].value)
            seat_numbers.append(self.__alumnos_tuples[studentid][StudentTuple.SEAT_NUMBER])
        return f"IDs in queue: {self.__state}\nTypes in queue: {state_types}\nSeat numbers: {seat_numbers}"

if __name__ == "__main__":
    # Parse arguments and get the position of the students as a dictionary called "alumnos"
    filename, alumnos_path, heuristic_name = parse_arguments(sys.argv[1:])
    alumnos_content = get_file_content(alumnos_path)
    alumnos, alumnos_count = parse_alumnos_input(alumnos_content)
    # Uncomment the following line to print the students in the input file
    # print_alumnos(alumnos)
    
    # Create the ASTARColaBus object, run it and save the final state
    astar = ASTARColaBus(alumnos, alumnos_count, heuristic_name)
    statistics = astar.run()
    print(astar, statistics, sep="\n\n")
    # save_state(astar.get_state, alumnos, filename, heuristic_name)
    # save_statistics(statistics, filename, heuristic_name)