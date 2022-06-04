#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Maze-Solving Project

This application uses Prim's algorithm to create random mazes and compares different maze solving methods, such as:

Breadth-First Search Method
Depth-First Search Method
Iterative Depth-First Search Method
A* Search Method

"""

__author__ = "Eloi Giacobbo"
__email__ = "eloiluiz@gmail.com"
__version__ = "1.1.2"
__status__ = "Development"

# **************************************************************
#                    Configuration Parameters
# **************************************************************
PRINT_INFO = False
PRINT_DEBUG = False

# **************************************************************
#                           Libraries
# **************************************************************
from random import randint as rand
from termcolor import colored
import numpy
import queue


# **************************************************************
#                           Maze Class
# **************************************************************
class Maze:
    """Class designed to create a maze using the Randomized Prim's Algorithm.
    """

    HALL_INDEX = 0
    WALL_INDEX = 1
    START_INDEX = 2
    GOAL_INDEX = 3
    MARKED_HALL_INDEX = 4
    MARKED_WALL_INDEX = 5
    MARKED_START_INDEX = 6
    MARKED_GOAL_INDEX = 7
    SELECTED_HALL_INDEX = 8
    SELECTED_WALL_INDEX = 9
    SELECTED_START_INDEX = 10
    SELECTED_GOAL_INDEX = 11

    def __init__(self, width=5, height=5, complexity=0.75, density=0.75):
        """Initializes the maze creation class.

        Define attributes and generate a randomized maze.

        Args:
            width (int, optional): Defines the maze's width. Defaults to 5.
            height (int, optional): Defines the maze's height. Defaults to 5.
            complexity (float, optional): Defines the maze's complexity. Defaults to 0.75.
            density (float, optional): Defines the maze's density. Defaults to 0.75.
        """

        if (width > 5):
            self.__width = width
        else:
            self.__width = 5

        if (height > 5):
            self.__height = height
        else:
            self.__height = 5

        if (complexity <= 1):
            self.__complexity = complexity
        else:
            self.__complexity = 0.75

        if (density <= 1):
            self.__density = density
        else:
            self.__density = 0.75

        self._last_mark = []

        # Generate the maze
        self.generate()

    def generate(self):
        """Maze generation method.
        """

        # Defines an odd shape
        shape = (((self.__height // 2) * 2) + 1, ((self.__width // 2) * 2) + 1)

        # Adjust complexity and density relative to maze size
        self.__complexity = int(self.__complexity * (5 * (shape[0] + shape[1])))
        self.__density = int(self.__density * ((shape[0] // 2) * (shape[1] // 2)))

        # Build actual maze
        self.__map = numpy.zeros(shape, dtype=int)

        # Fill borders
        self.__map[0, :] = self.__map[-1, :] = 1
        self.__map[:, 0] = self.__map[:, -1] = 1

        # Make aisles
        for i in range(self.__density):
            x = rand(0, (shape[1] // 2)) * 2
            y = rand(0, (shape[0] // 2)) * 2
            self.__map[y, x] = 1
            for j in range(self.__complexity):
                neighbors = []
                if (x > 1):
                    neighbors.append((y, (x - 2)))
                if (x < (shape[1] - 2)):
                    neighbors.append((y, (x + 2)))
                if (y > 1):
                    neighbors.append(((y - 2), x))
                if (y < (shape[0] - 2)):
                    neighbors.append(((y + 2), x))
                if (len(neighbors)):
                    y_, x_ = neighbors[rand(0, (len(neighbors) - 1))]
                    if (self.__map[y_, x_] == 0):
                        self.__map[y_, x_] = 1
                        self.__map[y_ + ((y - y_) // 2), x_ + ((x - x_) // 2)] = 1
                        x = x_
                        y = y_

        # Define starting point
        while True:
            self.__start_position = [rand(1, shape[0] - 1), rand(1, shape[1] - 1)]
            if (self.__map[self.__start_position[0], self.__start_position[1]] == 0):
                self.__map[self.__start_position[0], self.__start_position[1]] = 2
                break

        # Define goal point
        while True:
            self.__goal_position = [rand(1, shape[0] - 1), rand(1, shape[1] - 1)]
            if (self.__map[self.__goal_position[0], self.__goal_position[1]] == 0):
                self.__map[self.__goal_position[0], self.__goal_position[1]] = 3
                break

    def print_map(self):
        """Prints the maze on screen.
        """
        for y in range((self.__height // 2) * 2 + 1):
            str = " "
            for x in range((self.__width // 2) * 2 + 1):
                if (self.__map[y, x] == self.HALL_INDEX):
                    str = str + " "
                elif (self.__map[y, x] == self.WALL_INDEX):
                    str = str + colored(' ', 'white', 'on_white')
                elif (self.__map[y, x] == self.START_INDEX):
                    str = str + colored('O', 'green')
                elif (self.__map[y, x] == self.GOAL_INDEX):
                    str = str + colored('x', 'red')
                elif (self.__map[y, x] == self.MARKED_HALL_INDEX):
                    str = str + colored(' ', 'red', 'on_red')
                elif (self.__map[y, x] == self.MARKED_WALL_INDEX):
                    str = str + colored(' ', 'red', 'on_white')
                elif (self.__map[y, x] == self.MARKED_START_INDEX):
                    str = str + colored('x', None, 'on_red')
                elif (self.__map[y, x] == self.MARKED_GOAL_INDEX):
                    str = str + colored('x', None, 'on_red')
                elif (self.__map[y, x] == self.SELECTED_HALL_INDEX):
                    str = str + colored(' ', 'yellow', 'on_yellow')
                elif (self.__map[y, x] == self.SELECTED_WALL_INDEX):
                    str = str + colored(' ', 'yellow', 'on_white')
                elif (self.__map[y, x] == self.SELECTED_START_INDEX):
                    str = str + colored('x', None, 'on_yellow')
                elif (self.__map[y, x] == self.SELECTED_GOAL_INDEX):
                    str = str + colored('x', None, 'on_yellow')
            print(str)

    def get_start_position(self):
        """Returns the defined start position coordinates [y, x].

        Returns:
            list: Returns a list containing the [y, x] coordinate values.
        """
        return [self.__start_position[0], self.__start_position[1]]

    def get_goal_position(self):
        """Returns the goal start position coordinates [y, x].

        Returns:
            list: Returns a list containing the [y, x] coordinate values.
        """
        return [self.__goal_position[0], self.__goal_position[1]]

    # Return value of specified position
    def get_position_value(self, y, x):
        """Returns the selected position value.

        Args:
            y (int): The selected position y coordinate.
            x (int): The selected position x coordinate.

        Returns:
            int: The selected position value.
        """
        return self.__map[y, x]

    def get_neighbor_values(self, y, x):
        """Returns the selected coordinate's neighbor values.

        Args:
            y (int): The selected position y coordinate.
            x (int): The selected position x coordinate.

        Returns:
            list: The neighbor value's list.
        """
        return [self.__map[y + 1, x], self.__map[y - 1, x], self.__map[y, x - 1], self.__map[y, x + 1]]

    def mark_position(self, y, x):
        """Mark the input position in the map.

        Args:
            y (int): The selected position y coordinate.
            x (int): The selected position x coordinate.
        """
        # Unselect and mark the last position
        if (self._last_mark != []):
            if (self.__map[self._last_mark[0], self._last_mark[1]] == self.SELECTED_HALL_INDEX):
                self.__map[self._last_mark[0], self._last_mark[1]] = self.MARKED_HALL_INDEX
            elif (self.__map[self._last_mark[0], self._last_mark[1]] == self.SELECTED_WALL_INDEX):
                self.__map[self._last_mark[0], self._last_mark[1]] = self.MARKED_WALL_INDEX
            elif (self.__map[self._last_mark[0], self._last_mark[1]] == self.SELECTED_START_INDEX):
                self.__map[self._last_mark[0], self._last_mark[1]] = self.MARKED_START_INDEX
            elif (self.__map[self._last_mark[0], self._last_mark[1]] == self.SELECTED_GOAL_INDEX):
                self.__map[self._last_mark[0], self._last_mark[1]] = self.MARKED_GOAL_INDEX
        # Select the new position
        if (self.__map[y, x] == self.HALL_INDEX):
            self.__map[y, x] = self.SELECTED_HALL_INDEX
        elif (self.__map[y, x] == self.WALL_INDEX):
            self.__map[y, x] = self.SELECTED_WALL_INDEX
        elif (self.__map[y, x] == self.START_INDEX):
            self.__map[y, x] = self.SELECTED_START_INDEX
        elif (self.__map[y, x] == self.GOAL_INDEX):
            self.__map[y, x] = self.SELECTED_GOAL_INDEX
        # Update the last mark position
        self._last_mark = [y, x]

    def set_path(self, coordinates=[]):
        """Mark the input coordinates in the map.

        Args:
            coordinates (list): The movement coordinates [x, y].
        """
        for y, x in coordinates:
            if (self.__map[y, x] == self.HALL_INDEX):
                self.__map[y, x] = self.MARKED_HALL_INDEX
            elif (self.__map[y, x] == self.GOAL_INDEX):
                self.__map[y, x] = self.MARKED_GOAL_INDEX

    def clear_path(self):
        """Clears any movement values within the maze.
        """
        for y in range(((self.__height // 2) * 2) + 1):
            for x in range(((self.__width // 2) * 2) + 1):
                if (self.__map[y, x] == self.SELECTED_HALL_INDEX):
                    self.__map[y, x] = self.HALL_INDEX
                elif (self.__map[y, x] == self.SELECTED_WALL_INDEX):
                    self.__map[y, x] = self.WALL_INDEX
                elif (self.__map[y, x] == self.SELECTED_START_INDEX):
                    self.__map[y, x] = self.START_INDEX
                elif (self.__map[y, x] == self.SELECTED_GOAL_INDEX):
                    self.__map[y, x] = self.GOAL_INDEX
                elif (self.__map[y, x] == self.MARKED_HALL_INDEX):
                    self.__map[y, x] = self.HALL_INDEX
                elif (self.__map[y, x] == self.MARKED_WALL_INDEX):
                    self.__map[y, x] = self.WALL_INDEX
                elif (self.__map[y, x] == self.MARKED_START_INDEX):
                    self.__map[y, x] = self.START_INDEX
                elif (self.__map[y, x] == self.MARKED_GOAL_INDEX):
                    self.__map[y, x] = self.GOAL_INDEX
        self._last_mark = []


# **************************************************************
#                          Agent Class
# **************************************************************
class Agent:
    """Intelligent agent base class.
    """

    def __init__(self, maze):
        """Initializes the agent attributes.
        """
        self._maze = maze
        self._start_position = self._maze.get_start_position()
        self._path = numpy.array([[self._start_position[0], self._start_position[1]]])
        self._visited = numpy.array([[self._start_position[0], self._start_position[1]]])

    # Goal test method
    def is_goal_position(self, y, x):
        """Verifies if the agent has reached the goal position using the input coordinates.

        Args:
            y (int): The selected position y coordinate.
            x (int): The selected position x coordinate.

        Returns:
            bool: The verification result, where True means the goal position is reached and False that it hasn't.
        """
        if (self._maze.get_position_value(y, x) == 3):
            return True
        else:
            return False

    def is_agent_new(self, y, x):
        """Verifies if the agent is new using the input coordinate values.

        Args:
            y (int): The selected position y coordinate.
            x (int): The selected position x coordinate.

        Returns:
            bool: The verification result, where True means the agent is new and False means other coordinates have been visited already.
        """
        test = numpy.array([[y, x]])
        size = numpy.shape(self._visited)
        for i in range(size[0]):
            if ((self._visited[i, :] == test).all()):
                return False
        return True

    def get_path(self):
        """Return the agent mapped path

        Returns:
            list: The mapped path from the start position to the goal.
        """
        return self._path


class BFS_Search(Agent):
    """Breadth-First Search Method

    This class implements the Breadth-First Search algorithm.

    Args:
        Agent (object): The search algorithm intelligent agent parent class.

    Returns:
        object: The BFS agent object.
    """

    _level = 1
    _current_level = 0

    def __init__(self, maze):
        """Initialize the search agent and execute.
        """
        # Initialization process
        Agent.__init__(self, maze)
        # Execute the search
        self.move(self._start_position[0], self._start_position[1])

    def move(self, y, x):
        """Agent movement method.

        Args:
            y (int): The selected position y coordinate.
            x (int): The selected position x coordinate.

        Returns:
            bool: The movement result, where True means the goal position is reached and False that it hasn't.
        """

        # Update current coordinate
        current = numpy.array([[y, x]])
        # Update the visited positions list
        if ((current != self._start_position).any()):
            self._visited = numpy.concatenate((self._visited, current), axis=0)

        # Check if current level belongs to the level under analysis
        if (self._current_level == self._level):

            # Print current movement step
            if (PRINT_DEBUG == True):
                self._maze.mark_position(y, x)
                self._maze.print_map()
                print("Current level = ", self._current_level)
                print("Current position = ", current)
                print("Current search level = ", self._level)
                input("PRESS ANY KEY TO CONTINUE...")
                self._maze.clear_path()

            # Test for goal position
            # Return True if it is the goal position
            if (self.is_goal_position(y, x) == True):
                self._path = self._visited
                return True

        # If the current position isn't the goal,
        # Check the need to go for the next level
        if (self._current_level < self._level):

            self._current_level += 1

            # Search on upper coordinate
            # Check if the position is part of an path,
            if (self._maze.get_position_value((y + 1), x) != 1):
                if (self.is_agent_new((y + 1), x)):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the current coordinate as part of the path and return True
                    if (self.move((y + 1), x)):
                        return True

            # Search on lower coordinate
            # If the position is part of an path,
            if (self._maze.get_position_value((y - 1), x) != 1):
                if (self.is_agent_new((y - 1), x)):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the current coordinate as part of the path and return True
                    if (self.move((y - 1), x)):
                        return True

            # Search on lower coordinate
            # If the position is part of an path,
            if (self._maze.get_position_value(y, (x - 1)) != 1):
                if (self.is_agent_new(y, (x - 1))):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the current coordinate as part of the path and return True
                    if (self.move(y, (x - 1))):
                        return True

            # Search on lower coordinate
            # If the position is part of an path,
            if (self._maze.get_position_value(y, (x + 1)) != 1):
                if (self.is_agent_new(y, (x + 1))):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the current coordinate as part of the path and return True
                    if (self.move(y, (x + 1))):
                        return True

            # If none of its sons is part of path,
            # This node is removed from path and return false.
            self._current_level -= 1

        # In case this is the first movement action, go to the next level
        if ((current == self._start_position).all()):
            self._level += 1
            self._visited = current
            self.move(self._start_position[0], self._start_position[1])

        # Lastly, at this point we know this position is not part of the path
        # This node is removed from path and return false.
        else:
            self._visited = numpy.delete(self._visited, (numpy.shape(self._visited)[0] - 1), axis=0)
            return False


class DFS_Search(Agent):
    """Depth-First Search Method

    This class implements the Depth-First Search algorithm.

    Args:
        Agent (object): The search algorithm intelligent agent parent class.

    Returns:
        object: The DFS agent object.
    """

    def __init__(self, maze):
        """Initialize the search agent and execute.
        """
        # Initialization process
        Agent.__init__(self, maze)
        # Execute the search
        self.move(self._start_position[0], self._start_position[1])

    def move(self, y, x):
        """Agent movement method.

        Args:
            y (int): The selected position y coordinate.
            x (int): The selected position x coordinate.

        Returns:
            bool: The movement result, where True means the goal position is reached and False that it hasn't.
        """

        # Update current coordinate
        current = numpy.array([[y, x]])
        # Update the visited positions list
        self._visited = numpy.concatenate((self._visited, current), axis=0)

        # Print current movement step
        if (PRINT_DEBUG == True):
            self._maze.mark_position(y, x)
            self._maze.print_map()
            print("Current position = ", current)
            input("PRESS ANY KEY TO CONTINUE...")
            self._maze.clear_path()

        # Test for goal position
        # If True, set path and return True
        if (self.is_goal_position(y, x)):
            self._path = numpy.array([[y, x]])
            return True

        # If the current position isn't the goal,

        # Search on upper coordinate
        # Check if the position is part of an path,
        if (self._maze.get_position_value((y + 1), x) != 1):
            if (self.is_agent_new((y + 1), x)):

                # Move to this coordinate.
                # If this action returns True, the goal was found.
                # Save the current coordinate as part of the path and return True
                if (self.move((y + 1), x)):
                    pos = numpy.array([[y, x]])
                    self._path = numpy.concatenate((pos, self._path), axis=0)
                    return True

        # Search on lower coordinate
        # If the position is part of an path,
        if (self._maze.get_position_value((y - 1), x) != 1):
            if (self.is_agent_new((y - 1), x)):

                # Move to this coordinate.
                # If this action returns True, the goal was found.
                # Save the current coordinate as part of the path and return True
                if (self.move((y - 1), x)):
                    pos = numpy.array([[y, x]])
                    self._path = numpy.concatenate((pos, self._path), axis=0)
                    return True

        # Search on left coordinate
        # If the position is part of an path,
        if (self._maze.get_position_value(y, (x - 1)) != 1):
            if (self.is_agent_new(y, (x - 1))):

                # Move to this coordinate.
                # If this action returns True, the goal was found.
                # Save the current coordinate as part of the path and return True
                if (self.move(y, (x - 1))):
                    pos = numpy.array([[y, x]])
                    self._path = numpy.concatenate((pos, self._path), axis=0)
                    return True

        # Search on right coordinate
        # If the position is part of an path,
        if (self._maze.get_position_value(y, (x + 1)) != 1):
            if (self.is_agent_new(y, (x + 1))):

                # Move to this coordinate.
                # If this action returns True, the goal was found.
                # Save the current coordinate as part of the path and return True
                if (self.move(y, (x + 1))):
                    pos = numpy.array([[y, x]])
                    self._path = numpy.concatenate((pos, self._path), axis=0)
                    return True

        # If none of its neighbors is part of path, return false
        return False


class IDFS_Search(Agent):
    """Iterative Depth-First Search Method

    This class implements the Iterative Depth-First Search algorithm.

    Args:
        Agent (object): The search algorithm intelligent agent parent class.

    Returns:
        object: The IDFS agent object.
    """

    _level = 1
    _current_level = 0

    def __init__(self, maze):
        """Initialize the search agent and execute.
        """
        # Initialization process
        Agent.__init__(self, maze)
        # Execute the search
        self.move(self._start_position[0], self._start_position[1])

    def move(self, y, x):
        """Agent movement method.

        Args:
            y (int): The selected position y coordinate.
            x (int): The selected position x coordinate.

        Returns:
            bool: The movement result, where True means the goal position is reached and False that it hasn't.
        """

        # Update current coordinate
        current = numpy.array([[y, x]])
        # Update the visited positions list
        if ((current != self._start_position).any()):
            self._visited = numpy.concatenate((self._visited, current), axis=0)

        # Test for goal position
        # Return True if it is the goal position
        if (self.is_goal_position(y, x)):
            self._path = self._visited
            return True

        # Print current movement step
        if (PRINT_DEBUG == True):
            self._maze.mark_position(y, x)
            self._maze.print_map()
            print("Current level = ", self._current_level)
            print("Current position = ", current)
            print("Current search level = ", self._level)
            input("PRESS ANY KEY TO CONTINUE...")
            self._maze.clear_path()

        # If current position isn't the goal,
        # Check the need to go for the next level
        if (self._current_level < self._level):

            self._current_level += 1

            # Search on upper coordinate
            # Check if the position is part of an path,
            if (self._maze.get_position_value((y + 1), x) != 1):
                if (self.is_agent_new((y + 1), x)):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the current coordinate as part of the path and return True
                    if (self.move((y + 1), x)):
                        return True

            # Search on lower coordinate
            # If the position is part of an path,
            if (self._maze.get_position_value((y - 1), x) != 1):
                if (self.is_agent_new((y - 1), x)):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the current coordinate as part of the path and return True
                    if (self.move((y - 1), x)):
                        return True

            # Search on left coordinate
            # If the position is part of an path,
            if (self._maze.get_position_value(y, (x - 1)) != 1):
                if (self.is_agent_new(y, (x - 1))):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the current coordinate as part of the path and return True
                    if (self.move(y, (x - 1))):
                        return True

            # Search on right coordinate
            # If the position is part of an path,
            if (self._maze.get_position_value(y, (x + 1)) != 1):
                if (self.is_agent_new(y, (x + 1))):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the current coordinate as part of the path and return True
                    if (self.move(y, (x + 1))):
                        return True

            # If none of its sons is part of path,
            # This node is removed from path and return false.
            self._current_level -= 1

        # In case this is the first movement action, go to the next level
        if ((current == self._start_position).all()):
            self._level += 1
            self._visited = current
            self.move(self._start_position[0], self._start_position[1])

        # Lastly, at this point we know this position is not part of the path
        # This node is removed from path and return false.
        else:
            self._visited = numpy.delete(self._visited, (numpy.shape(self._visited)[0] - 1), axis=0)
            return False


class A_Star_Node:
    """A* Search Methode node.

    This class represents a node in the A* search path.
    """

    def __init__(self, parent, rank, cost, position):
        self.parent = parent
        self.rank = rank
        self.cost = cost
        self.position = position

    def __cmp__(self, other):
        """Compare two nodes using the rank attribute as reference.

        Args:
            other (A_Star_Node): The other node under comparison.

        Returns:
            int: Returns 1 if self rank is bigger, 0 if both are equal and -1 if other rank is bigger.
        """
        return (self.rank > other.rank) - (self.rank < other.rank)

    def __lt__(self, other):
        """Compare two nodes using the rank attribute as reference.

        Args:
            other (A_Star_Node): The other node under comparison.

        Returns:
            bool: Returns True if self rank is less than other and False otherwise.
        """
        return (self.rank < other.rank)

    def __le__(self, other):
        """Compare two nodes using the rank attribute as reference.

        Args:
            other (A_Star_Node): The other node under comparison.

        Returns:
            bool: Returns True if self rank is less or equal than other and False otherwise.
        """
        return (self.rank <= other.rank)

    def __gt__(self, other):
        """Compare two nodes using the rank attribute as reference.

        Args:
            other (A_Star_Node): The other node under comparison.

        Returns:
            bool: Returns True if self rank is greater than other and False otherwise.
        """
        return (self.rank > other.rank)

    def __ge__(self, other):
        """Compare two nodes using the rank attribute as reference.

        Args:
            other (A_Star_Node): The other node under comparison.

        Returns:
            bool: Returns True if self rank is greater or equal than other and False otherwise.
        """
        return (self.rank >= other.rank)


class A_Star_Search(Agent):
    """A* Search Method

    This class implements the A* Search algorithm.

    Args:
        Agent (object): The search algorithm intelligent agent parent class.

    Returns:
        object: The A* agent object.
    """

    def __init__(self, maze):
        """Initialize the search agent and execute.
        """
        # Initialization process
        Agent.__init__(self, maze)
        self._path = []
        self._goal_position = self._maze.get_goal_position()
        self._open = queue.PriorityQueue()
        self._closed = []
        # Execute the search
        start_node = A_Star_Node(0, 0, self.f(self._start_position), self._start_position)
        self.search(start_node)

    def movement_cost(self, origin=[], destination=[]):
        """Agent heuristic function that calculates movement costs.

        This algorithm uses the Manhattan distance to calculates movement cost as this is the standard heuristic for a
        square grid.

        Args:
            origin (list): The origin (start) position coordinates [y, x].
            destination (list): The destination (end) position coordinates [y, x].

        Returns:
            int: The movement cost estimation.
        """
        dy = abs(destination[0] - origin[0])
        dx = abs(destination[1] - origin[1])
        return (dx + dy)

    def g(self, coordinates=[]):
        """Agent heuristic function that calculates movement costs from the start position.

        This is a heuristic function that represents the exact cost of the path from the start position to the input 
        coordinate values. This algorithm uses the Manhattan distance as this is the standard heuristic for a square 
        grid.

        Args:
            coordinates (list): The movement coordinates [x, y].

        Returns:
            int: The movement cost estimation.
        """
        return self.movement_cost(self._start_position, coordinates)

    def h(self, coordinates=[]):
        """Agent heuristic function the calculates movement costs to the goal position.

        This is a heuristic function that estimates the cost of the cheapest path from the input coordinate values to 
        the goal. This algorithm uses the Manhattan distance as this is the standard heuristic for a square grid.

        Args:
            coordinates (list): The movement coordinates [y, x].

        Returns:
            int: The movement cost estimation.
        """
        return self.movement_cost(coordinates, self._goal_position)

    def f(self, coordinates=[]):
        """Agent heuristic function the calculates the total cost of the selected coordinate.

        This is a heuristic function that estimates the total movement cost of the input coordinate. This algorithm uses
        the Manhattan distance as this is the standard heuristic for a square grid.

        Args:
            coordinates (list): The movement coordinates [y, x].

        Returns:
            int: The movement cost estimation.
        """
        return (self.g(coordinates) + self.h(coordinates))

    def get_neighbors(self, coordinates=[]):
        """Return the selected coordinate neighbors.

        Args:
            coordinates (list): The movement coordinates [y, x].
        """
        y = coordinates[0]
        x = coordinates[1]
        return [[(y + 1), x], [(y - 1), x], [y, (x - 1)], [y, (x + 1)]]

    def search(self, node):
        """Agent search method.

        Args:
            node (A_Star_Node): current A* node used in the search process.

        Returns:
            bool: The movement result, where True means the goal position is reached and False that it hasn't.
        """

        # Rename the input node
        current_node = node
        # Update the visited positions list
        self._open.put(current_node)

        # Iterate over the open queue
        while (not self._open.empty()):

            # Remove the lowest ranking node from the queue
            current_node = self._open.get()
            current_position = current_node.position

            # Put the visited node to the closed list
            self._closed.append(current_node)

            # Print current movement step
            if (PRINT_DEBUG == True):
                self._maze.mark_position(current_position[0], current_position[1])
                self._maze.print_map()
                print("Current position = ", current_position)
                input("PRESS ANY KEY TO CONTINUE...")
                self._maze.clear_path()

            # Test for goal position
            # If True, set path and return True
            if (self.is_goal_position(current_position[0], current_position[1])):
                while (current_node != 0):
                    self._path.append(current_node.position)
                    current_node = current_node.parent
                return True

            # If current position isn't the goal, search it's neighbors
            for neighbor_position in self.get_neighbors(current_position):

                # First, check if the neighbor is a valid position (open path)
                neighbor_position_value = self._maze.get_position_value(neighbor_position[0], neighbor_position[1])
                if (neighbor_position_value == 1):
                    continue

                # Calculate the neighbor costs (from current and from start position)
                neighbor_new_cost = current_node.cost + self.movement_cost(current_position, neighbor_position)
                neighbor_gcost = self.g(neighbor_position)

                # Check if the neighbor is at any of the open and closed lists
                is_neighbor_open = False
                is_neighbor_closed = False

                # Check if neighbor is at the open list and is a viable path
                for open_node in self._open.queue:
                    open_position = open_node.position
                    if (neighbor_position == open_position):
                        if (neighbor_new_cost < neighbor_gcost):
                            # Remove position from the open queue
                            self._open.queue.remove(open_node)
                        else:
                            is_neighbor_open = True

                # Check if neighbor is at the closed list and is a viable path
                for closed_node in self._closed:
                    closed_position = closed_node.position
                    if (neighbor_position == closed_position):
                        if (neighbor_new_cost < neighbor_gcost):
                            # Remove position from the closed list
                            self._closed.remove(closed_node)
                        else:
                            is_neighbor_closed = True

                # If neightbor is not in any of the lists, add it to open
                if ((is_neighbor_open == False) and (is_neighbor_closed == False)):
                    neighbor_node = A_Star_Node(current_node, neighbor_new_cost + self.f(neighbor_position),
                                                neighbor_new_cost, neighbor_position)
                    self._open.put(neighbor_node)

        # If the open list gets empty, the goal was not found
        return False


# **************************************************************
#                  Application Entry Point
# **************************************************************
if __name__ == "__main__":
    # Create a randomized map and print
    maze = Maze(50, 10, .75, .75)
    maze.print_map()

    # Solve the maze using the BFS algorithm
    bfs_agent = BFS_Search(maze)
    print("\n BFS Search:")
    maze.set_path(bfs_agent.get_path())
    maze.print_map()
    maze.clear_path()

    # Solve the maze using the DFS algorithm
    dfs_agent = DFS_Search(maze)
    maze.set_path(dfs_agent.get_path())
    print("\n DFS Search:")
    maze.print_map()
    maze.clear_path()

    # Solve the maze using the IDFS algorithm
    idfs_agent = IDFS_Search(maze)
    print("\n IDFS Search:")
    maze.set_path(idfs_agent.get_path())
    maze.print_map()
    maze.clear_path()

    # Solve the maze using the A* algorithm
    as_agent = A_Star_Search(maze)
    print("\n A* - A* Search:")
    maze.set_path(as_agent.get_path())
    maze.print_map()
    maze.clear_path()

    print("\n Search Summary")
    summary = queue.PriorityQueue()
    summary.put((len(bfs_agent.get_path()), "BFS:"))
    summary.put((len(dfs_agent.get_path()), "DFS:"))
    summary.put((len(idfs_agent.get_path()), "IDFS:"))
    summary.put((len(as_agent.get_path()), "A*:"))

    while (not summary.empty()):
        length, name = summary.get()
        print(" " + name + "\t" + str(length))
