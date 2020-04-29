import pickle
from itertools import permutations
import queue
from sys import argv

class Node():
    def __init__(self, jugs):
        self.jugs = jugs
        self.next_node = None

    def addNextNode(self, node):
        self.next_node = node
    
    def printNode(self):
        print(self.jugs[0].current_level, self.jugs[1].current_level, self.jugs[2].current_level)

    def getNextNode(self):
        return self.next_node

    def J1(self):
        return self.jugs[0]

    def J2(self):
        return self.jugs[1]

    def J3(self):
        return self.jugs[2]


class Jug():
    def __init__(self, capacity, current_level):
        self.current_level = current_level
        self.capacity = capacity
    
    def printJug(self):
        print(self.current_level, self.capacity)

    def getCurrentLevel(self):
        return self.current_level

    def setCurrentLevel(self, new_level):
        self.current_level = new_level
    
    def setCapacity(self, new_capacity):
        self.capacity = new_capacity

    def getCapacity(self):
        return self.capacity


def getSteps(steps, node):
    steps.append((node.J1().getCurrentLevel(), node.J2().getCurrentLevel(), node.J3().getCurrentLevel()))  # add initial state to list
    while node.getNextNode(): # while next_node is not None
        steps.append((node.next_node.J1().getCurrentLevel(), node.next_node.J2().getCurrentLevel(), node.next_node.J3().getCurrentLevel())) # add next state to list
        node.addNextNode(node.getNextNode().getNextNode()) # go to next node (move to next state)
    steps.reverse() # reverse states so that the the initial state is at the beginning of the list
    return steps

def pour(jugA, jugB):
    # Pouring JugA into JugB
    if jugB.getCapacity() < jugA.getCurrentLevel() + jugB.getCurrentLevel(): # JugB can only hold some of JugA level, i.e the capacity for JugB is not great enough to hold all of JugA's current level plus JugB's current level
        jugA.current_level -= jugB.getCapacity() - jugB.getCurrentLevel()  # set JugA's new level
        jugB.setCurrentLevel(jugB.getCapacity()) # set JugB's current level to be JugB's capacity
    else: # JugB can hold all of JugA, i.e the capacity for JugB is large enough to hold all of JugA's current level plus JugB's current level
        jugB.current_level += jugA.getCurrentLevel() # set JugB's new level
        jugA.setCurrentLevel(0) # set JugA to zero


def jug_problem(jugs, target):
    q = queue.Queue()     # queue used in search for target
    steps = []            # stores steps to reach target
    vertices = set()      # set to keep track of nodes visited
    q.put(Node(jugs))     # add starting Node to queue

    while not q.empty():  # continue to loop while queue is not empty
        current_node = q.get()  # get and remove first node from queue

        # check to see if any jug levels meet the desired target
        if current_node.J1().getCurrentLevel() == target:
            steps = getSteps(steps, current_node)
            break
        elif current_node.J2().getCurrentLevel() == target:
            steps = getSteps(steps, current_node)
            break
        elif current_node.J3().getCurrentLevel() == target:
            steps = getSteps(steps, current_node)
            break


        # iterate over every jug permuation: which is ((0, 1), (0,2), (1, 2), (1, 0), (2, 0), (2, 1))
        for i, j in permutations(range(len(current_node.jugs)), 2):
            orginal_levels = (current_node.jugs[i].getCurrentLevel(), current_node.jugs[j].getCurrentLevel())       # store original levels in tuple

            pour(current_node.jugs[i], current_node.jugs[j])  # pour from one jug to another
            
            next_node = Node(pickle.loads(pickle.dumps(current_node.jugs)))     # create new node to add

            current_node.jugs[i].setCurrentLevel(orginal_levels[0]) # set back to original level
            current_node.jugs[j].setCurrentLevel(orginal_levels[1]) # set back to original level

            next_node.addNextNode(current_node) # add edge between next_node and current_node

            next_J1_level = next_node.J1().getCurrentLevel()  # get and assign level for J1
            next_J2_level = next_node.J2().getCurrentLevel()  # get and assign level for J2
            next_J3_level = next_node.J3().getCurrentLevel()  # get and assign level for J3

            possible_jugs = (next_J1_level, next_J2_level, next_J3_level) # create tuple out of J1, J2, and J3 levels
            if possible_jugs not in vertices:   # check if tuple is already in set
                q.put(next_node)    # add tuple to queue
                vertices.add(possible_jugs) # add tuple to set

    return steps


def printSteps(steps):
    print()
    for i in steps:
        print('\033[1;32;40m-' * 21)	
        print('\033[1;32;40m|\033[1;36;40m', 'J1'.rjust(3), 'J2'.rjust(5), 'J3'.rjust(5), '\033[1;32;40m', '|'.rjust(2))
        print('\033[1;32;40m|\033[1;36;40m', str(i[0]).rjust(3), str(i[1]).rjust(5), str(i[2]).rjust(5), '\033[1;32;40m', '|'.rjust(2))
    print('\033[1;32;40m-' * 21)
    print()

def main(j1, j2, j3, target):
   jugs = [Jug(j1, j1), Jug(j2, 0), Jug(j3, 0)]
   steps = jug_problem(jugs, target)

   if steps:
    printSteps(steps)
   else:
      print('The target could not be met.')


if __name__ == '__main__':
    main(int(argv[1]), int(argv[2]), int(argv[3]), int(argv[4]))
