#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Maze-Solving Project

This application uses Prim's algorithm to create random mazes and compares different maze solving methods, such as:

Breadth-First Search Method
Depth-First Search Method
Iterative Depth-First Search Method
Dijkstra Search Method
A* Search Method

"""

__author__ = "Eloi Giacobbo"
__email__ = "eloiluiz@gmail.com"
__version__ = "1.4.1"
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
import time


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

    def get_neighbors(self, coordinates=[], y=None, x=None):
        """Return the selected coordinate neighbors.

        Args:
            coordinates (list): The movement coordinates [y, x].
        """
        # Parse the input parameters
        _y = 0
        _x = 0
        if (len(coordinates) > 0):
            _y = coordinates[0]
            _x = coordinates[1]
        elif ((y != None) and (x != None)):
            _y = y
            _x = x
        else:
            return []
        # Get the possible neighbor positions
        candidate = [[(_y + 1), _x], [(_y - 1), _x], [_y, (_x - 1)], [_y, (_x + 1)]]
        # Return the valid neighbors
        neighbor = []
        for i in range(len(candidate)):
            if ((candidate[i][0] >= 0) and (candidate[i][1] >= 0) and (candidate[i][0] < self.__height) and
                (candidate[i][1] < self.__width)):
                neighbor.append(candidate[i])
        return neighbor

    def get_neighbor_values(self, y, x):
        """Returns the selected coordinate's neighbor values.

        Args:
            y (int): The selected position y coordinate.
            x (int): The selected position x coordinate.

        Returns:
            list: The neighbor value's list.
        """
        return [self.__map[y + 1, x], self.__map[y - 1, x], self.__map[y, x - 1], self.__map[y, x + 1]]

    def print_map_list(self):
        print("[")
        for row in range(len(self.__map)):
          text = "\t[" + str(self.__map[row, 0]) + ","
          for column in range(1, len(self.__map[0])):
              text += (" " + str(self.__map[row, column]) + ",")
          print(text + "],")
        print("]")

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
                    str = str + colored('=', None, 'on_red')
                elif (self.__map[y, x] == self.MARKED_START_INDEX):
                    str = str + colored('O', None, 'on_red')
                elif (self.__map[y, x] == self.MARKED_GOAL_INDEX):
                    str = str + colored('x', None, 'on_red')
                elif (self.__map[y, x] == self.SELECTED_HALL_INDEX):
                    str = str + colored(' ', 'yellow', 'on_yellow')
                elif (self.__map[y, x] == self.SELECTED_WALL_INDEX):
                    str = str + colored('=', None, 'on_yellow')
                elif (self.__map[y, x] == self.SELECTED_START_INDEX):
                    str = str + colored('O', None, 'on_yellow')
                elif (self.__map[y, x] == self.SELECTED_GOAL_INDEX):
                    str = str + colored('x', None, 'on_yellow')
            print(str)

    def mark_position(self, y, x):
        """Mark the input position in the map.

        Args:
            y (int): The marked position y coordinate.
            x (int): The marked position x coordinate.
        """
        if (self.__map[y, x] == self.SELECTED_HALL_INDEX):
            self.__map[y, x] = self.MARKED_HALL_INDEX
        elif (self.__map[y, x] == self.SELECTED_WALL_INDEX):
            self.__map[y, x] = self.MARKED_WALL_INDEX
        elif (self.__map[y, x] == self.SELECTED_START_INDEX):
            self.__map[y, x] = self.MARKED_START_INDEX
        elif (self.__map[y, x] == self.SELECTED_GOAL_INDEX):
            self.__map[y, x] = self.MARKED_GOAL_INDEX
        elif (self.__map[y, x] == self.HALL_INDEX):
            self.__map[y, x] = self.MARKED_HALL_INDEX
        elif (self.__map[y, x] == self.WALL_INDEX):
            self.__map[y, x] = self.MARKED_WALL_INDEX
        elif (self.__map[y, x] == self.START_INDEX):
            self.__map[y, x] = self.MARKED_START_INDEX
        elif (self.__map[y, x] == self.GOAL_INDEX):
            self.__map[y, x] = self.MARKED_GOAL_INDEX

    def select_position(self, y, x):
        """Select the input position in the map.

        Args:
            y (int): The selected position y coordinate.
            x (int): The selected position x coordinate.
        """
        if (self.__map[y, x] == self.MARKED_HALL_INDEX):
            self.__map[y, x] = self.SELECTED_HALL_INDEX
        elif (self.__map[y, x] == self.MARKED_WALL_INDEX):
            self.__map[y, x] = self.SELECTED_WALL_INDEX
        elif (self.__map[y, x] == self.MARKED_START_INDEX):
            self.__map[y, x] = self.SELECTED_START_INDEX
        elif (self.__map[y, x] == self.MARKED_GOAL_INDEX):
            self.__map[y, x] = self.SELECTED_GOAL_INDEX
        elif (self.__map[y, x] == self.HALL_INDEX):
            self.__map[y, x] = self.SELECTED_HALL_INDEX
        elif (self.__map[y, x] == self.WALL_INDEX):
            self.__map[y, x] = self.SELECTED_WALL_INDEX
        elif (self.__map[y, x] == self.START_INDEX):
            self.__map[y, x] = self.SELECTED_START_INDEX
        elif (self.__map[y, x] == self.GOAL_INDEX):
            self.__map[y, x] = self.SELECTED_GOAL_INDEX

    def set_path(self, coordinates=[]):
        """Mark the input coordinates in the map.

        Args:
            coordinates (list): The movement coordinates [x, y].
        """
        for y, x in coordinates:
            if (self.__map[y, x] == self.HALL_INDEX):
                self.__map[y, x] = self.MARKED_HALL_INDEX
            if (self.__map[y, x] == self.WALL_INDEX):
                self.__map[y, x] = self.MARKED_WALL_INDEX
            if (self.__map[y, x] == self.START_INDEX):
                self.__map[y, x] = self.MARKED_START_INDEX
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
        self._path_length = 0
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


class AgentSearchNode:
    """Agent Search Method node.

    This class represents a node in the A* search path.
    """

    def __init__(self, parent, rank, cost, position, path, break_wall):
        self.parent = parent
        self.rank = rank
        self.cost = cost
        self.position = position
        self.agent_path = path
        self.break_wall = break_wall

    def __cmp__(self, other):
        """Compare two nodes using the rank attribute as reference.

        Args:
            other (AgentSearchNode): The other node under comparison.

        Returns:
            int: Returns 1 if self rank is bigger, 0 if both are equal and -1 if other rank is bigger.
        """
        return (self.rank > other.rank) - (self.rank < other.rank)

    def __lt__(self, other):
        """Compare two nodes using the rank attribute as reference.

        Args:
            other (AgentSearchNode): The other node under comparison.

        Returns:
            bool: Returns True if self rank is less than other and False otherwise.
        """
        return (self.rank < other.rank)

    def __le__(self, other):
        """Compare two nodes using the rank attribute as reference.

        Args:
            other (AgentSearchNode): The other node under comparison.

        Returns:
            bool: Returns True if self rank is less or equal than other and False otherwise.
        """
        return (self.rank <= other.rank)

    def __gt__(self, other):
        """Compare two nodes using the rank attribute as reference.

        Args:
            other (AgentSearchNode): The other node under comparison.

        Returns:
            bool: Returns True if self rank is greater than other and False otherwise.
        """
        return (self.rank > other.rank)

    def __ge__(self, other):
        """Compare two nodes using the rank attribute as reference.

        Args:
            other (AgentSearchNode): The other node under comparison.

        Returns:
            bool: Returns True if self rank is greater or equal than other and False otherwise.
        """
        return (self.rank >= other.rank)


class DijkstraAgent(Agent):
    """Dijkstra Search Method.

    This class implements the Dijkstra Search algorithm.

    Args:
        Agent (object): The search algorithm intelligent agent parent class.

    Returns:
        object: The Dijkstra agent object.
    """

    def __init__(self, maze, return_first=True, break_wall=0):
        """Initialize the search agent and execute.
        """
        # Initialization process
        Agent.__init__(self, maze)
        self._path = []
        self._goal_position = self._maze.get_goal_position()
        self._frontier = queue.PriorityQueue()
        self._explored = set()
        self._return_first = return_first
        self._break_wall = break_wall

    def start(self):
        """Method that starts the goal search process and returns the resulting path.
        """
        # Execute the search
        start_node = AgentSearchNode(0, 0, self._heuristics(self._start_position), self._start_position,
                                     [self._start_position], self._break_wall)
        return self._search(start_node)

    def _movement_cost(self, origin=[], destination=[]):
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

    def _heuristics(self, coordinates=[]):
        """Agent heuristic function the calculates movement costs to the goal position.

        This is a heuristic function that estimates the cost of the cheapest path from the input coordinate values to 
        the goal. This algorithm uses the Manhattan distance as this is the standard heuristic for a square grid.

        Args:
            coordinates (list): The movement coordinates [y, x].

        Returns:
            int: The movement cost estimation.
        """
        return self._movement_cost(coordinates, self._goal_position)

    def _search(self, node):
        """Agent search method.

        Args:
            node (AgentSearchNode): current A* node used in the search process.

        Returns:
            bool: The movement result, where True means the goal position is reached and False that it hasn't.
        """

        # Rename the input node
        current_node = node
        # Update the visited positions list
        self._frontier.put(current_node)

        # Iterate over the frontier queue
        while (not self._frontier.empty()):

            # Remove the lowest ranking node from the queue
            current_node = self._frontier.get()
            current_position = current_node.position

            # Include current node to the explored list
            self._explored.add(current_node)

            # Print current movement step
            if (PRINT_DEBUG == True):
                print("Current position = ", current_position)
                for agent_position in current_node.agent_path:
                    self._maze.mark_position(agent_position[0], agent_position[1])
                self._maze.select_position(current_position[0], current_position[1])
                self._maze.print_map()
                input("PRESS ANY KEY TO CONTINUE...")
                self._maze.clear_path()

            # Test for goal position
            # If True, store the path just found (if it is shorter)
            if (self.is_goal_position(current_position[0], current_position[1])):
                new_path = current_node.agent_path
                new_path_length = len(new_path)
                # Check for the shorter path
                if ((self._path_length == 0) or (new_path_length < self._path_length)):
                    self._path = new_path
                    self._path_length = new_path_length
                # Check if the search must continue or stop at the first path found
                if (self._return_first == True):
                    return True
                else:
                    continue

            # If current position isn't the goal, search it's neighbors
            for neighbor_position in self._maze.get_neighbors(current_position):

                # First, check if the neighbor is a valid position (frontier path or breakable wall)
                neighbor_break_wall = current_node.break_wall
                neighbor_position_value = self._maze.get_position_value(neighbor_position[0], neighbor_position[1])
                if (neighbor_position_value == 1):
                    if (neighbor_break_wall > 0):
                        neighbor_break_wall -= 1
                    else:
                        continue

                # Check if neighbor is at current path already
                is_neighbor_in_agent_path = False
                for agent_path_position in current_node.agent_path:
                    if (neighbor_position == agent_path_position):
                        is_neighbor_in_agent_path = True
                        break

                # Checks if the cost of the current path is already greater than the best result found
                neighbor_path = current_node.agent_path[:]
                neighbor_path.append(neighbor_position)
                neighbor_path_length = len(neighbor_path)
                if ((self._path_length > 0) and (self._path_length < neighbor_path_length)):
                    # Discard neighbor if it's path is too long
                    continue

                # If neighbor is not in any of the lists, add it to frontier
                if (is_neighbor_in_agent_path == False):
                    neighbor_new_cost = current_node.cost + self._movement_cost(current_position, neighbor_position)
                    neighbor_rank = self._heuristics(neighbor_position)
                    neighbor_node = AgentSearchNode(current_node, neighbor_rank, neighbor_new_cost, neighbor_position,
                                                    neighbor_path, neighbor_break_wall)
                    self._frontier.put(neighbor_node)

            # Print current search
            if (PRINT_DEBUG == True):
                for explored_node in self._explored:
                    self._maze.mark_position(explored_node.position[0], explored_node.position[1])
                for frontier_node in self._frontier.queue:
                    self._maze.select_position(frontier_node.position[0], frontier_node.position[1])
                self._maze.select_position(current_position[0], current_position[1])
                self._maze.print_map()
                input("PRESS ANY KEY TO CONTINUE...")
                self._maze.clear_path()

        # If the frontier list gets empty, the goal was not found
        return False


class AStarAgent(Agent):
    """A* Search Method

    This class implements the A* Search algorithm.

    Args:
        Agent (object): The search algorithm intelligent agent parent class.

    Returns:
        object: The A* agent object.
    """

    def __init__(self, maze, return_first=True, break_wall=0):
        """Initialize the search agent and execute.
        """
        # Initialization process
        Agent.__init__(self, maze)
        self._path = []
        self._goal_position = self._maze.get_goal_position()
        self._frontier = queue.PriorityQueue()
        self._explored = set()
        self._return_first = return_first
        self._break_wall = break_wall

    def start(self):
        """Method that starts the goal search process and returns the resulting path.
        """
        # Execute the search
        start_node = AgentSearchNode(0, 0, self._heuristics(self._start_position), self._start_position,
                                     [self._start_position], self._break_wall)
        return self._search(start_node)

    def _movement_cost(self, origin=[], destination=[]):
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

    def _heuristics(self, coordinates=[]):
        """Agent heuristic function the calculates movement costs to the goal position.

        This is a heuristic function that estimates the cost of the cheapest path from the input coordinate values to 
        the goal. This algorithm uses the Manhattan distance as this is the standard heuristic for a square grid.

        Args:
            coordinates (list): The movement coordinates [y, x].

        Returns:
            int: The movement cost estimation.
        """
        return self._movement_cost(coordinates, self._goal_position)

    def _search(self, node):
        """Agent search method.

        Args:
            node (AgentSearchNode): current A* node used in the search process.

        Returns:
            bool: The movement result, where True means the goal position is reached and False that it hasn't.
        """

        # Rename the input node
        current_node = node
        # Update the frontier list (search border)
        self._frontier.put(current_node)

        # Iterate over the frontier queue
        while (not self._frontier.empty()):

            # Remove the lowest ranking node from the queue
            current_node = self._frontier.get()
            current_position = current_node.position

            # Include current node to the explored list
            self._explored.add(current_node)

            # Print current movement step
            if (PRINT_DEBUG == True):
                print("Current position = ", current_position)
                for agent_position in current_node.agent_path:
                    self._maze.mark_position(agent_position[0], agent_position[1])
                self._maze.select_position(current_position[0], current_position[1])
                self._maze.print_map()
                input("PRESS ANY KEY TO CONTINUE...")
                self._maze.clear_path()

            # Test for goal position
            # If True, store the path just found (if it is shorter)
            if (self.is_goal_position(current_position[0], current_position[1])):
                new_path = current_node.agent_path
                new_path_length = len(new_path)
                # Check for the shorter path
                if ((self._path_length == 0) or (new_path_length < self._path_length)):
                    self._path = new_path
                    self._path_length = new_path_length
                # Check if the search must continue or stop at the first path found
                if (self._return_first == True):
                    return True
                else:
                    continue

            # If current position isn't the goal, search it's neighbors
            for neighbor_position in self._maze.get_neighbors(current_position):

                # First, check if the neighbor is a valid position (frontier path or breakable wall)
                neighbor_break_wall = current_node.break_wall
                neighbor_position_value = self._maze.get_position_value(neighbor_position[0], neighbor_position[1])
                if (neighbor_position_value == 1):
                    if (neighbor_break_wall > 0):
                        neighbor_break_wall -= 1
                    else:
                        continue

                # Check if neighbor is at current path already
                is_neighbor_in_agent_path = False
                for agent_path_position in current_node.agent_path:
                    if (neighbor_position == agent_path_position):
                        is_neighbor_in_agent_path = True
                        break

                # Checks if the cost of the current path is already greater than the best result found
                neighbor_path = current_node.agent_path[:]
                neighbor_path.append(neighbor_position)
                neighbor_path_length = len(neighbor_path)
                if ((self._path_length > 0) and (self._path_length < neighbor_path_length)):
                    # Discard neighbor if it's path is too long
                    continue

                # If neighbor is not in any of the lists, add it to frontier
                if (is_neighbor_in_agent_path == False):
                    neighbor_new_cost = current_node.cost + self._movement_cost(current_position, neighbor_position)
                    neighbor_rank = neighbor_new_cost + self._heuristics(neighbor_position)
                    neighbor_node = AgentSearchNode(current_node, 0, neighbor_new_cost, neighbor_position,
                                                    neighbor_path, neighbor_break_wall)
                    self._frontier.put(neighbor_node)

            # Print current search
            if (PRINT_DEBUG == True):
                for explored_node in self._explored:
                    self._maze.mark_position(explored_node.position[0], explored_node.position[1])
                for frontier_node in self._frontier.queue:
                    self._maze.select_position(frontier_node.position[0], frontier_node.position[1])
                self._maze.select_position(current_position[0], current_position[1])
                self._maze.print_map()
                input("PRESS ANY KEY TO CONTINUE...")
                self._maze.clear_path()

        # If the frontier list gets empty, the goal was not found
        return False


# **************************************************************
#                  Application Entry Point
# **************************************************************
if __name__ == "__main__":
    # Create a randomized map and print
    maze_height = rand(5, 50)
    maze_width = rand(5, 50)
    maze = Maze(maze_height, maze_width, .75, .75)
    # maze.print_map_list()
    maze.print_map()

    # Solve the maze using the BFS algorithm
    start_time = time.time_ns()
    bfs_agent = BFS_Search(maze)
    bfs_time = int((time.time_ns() - start_time) / 1000000)
    print("\n BFS Search:")
    maze.set_path(bfs_agent.get_path())
    maze.print_map()
    maze.clear_path()

    # Solve the maze using the DFS algorithm
    start_time = time.time_ns()
    dfs_agent = DFS_Search(maze)
    dfs_time = int((time.time_ns() - start_time) / 1000000)
    print("\n DFS Search:")
    maze.set_path(dfs_agent.get_path())
    maze.print_map()
    maze.clear_path()

    # Solve the maze using the IDFS algorithm
    start_time = time.time_ns()
    idfs_agent = IDFS_Search(maze)
    idfs_time = int((time.time_ns() - start_time) / 1000000)
    print("\n IDFS Search:")
    maze.set_path(idfs_agent.get_path())
    maze.print_map()
    maze.clear_path()

    # Solve the maze using the Dijkstra algorithm
    start_time = time.time_ns()
    dijkstra_agent = DijkstraAgent(maze, return_first=False, break_wall=1)
    dijkstra_agent.start()
    dijkstra_time = int((time.time_ns() - start_time) / 1000000)
    print("\n Dijkstra - Dijkstra Search:")
    maze.set_path(dijkstra_agent.get_path())
    maze.print_map()
    maze.clear_path()

    # Solve the maze using the Dijkstra algorithm
    start_time = time.time_ns()
    as_agent = AStarAgent(maze, return_first=False, break_wall=1)
    as_agent.start()
    as_time = int((time.time_ns() - start_time) / 1000000)
    print("\n A* - A* Search:")
    maze.set_path(as_agent.get_path())
    maze.print_map()
    maze.clear_path()

    print("\n Search Summary")
    print("Method\tLength\tTime")
    summary = queue.PriorityQueue()
    summary.put((len(bfs_agent.get_path()), bfs_time, "BFS:     "))
    summary.put((len(dfs_agent.get_path()), dfs_time, "DFS:     "))
    summary.put((len(idfs_agent.get_path()), idfs_time, "IDFS:    "))
    summary.put((len(dijkstra_agent.get_path()), dijkstra_time, "Dijkstra:"))
    summary.put((len(as_agent.get_path()), as_time, "A*:      "))

    while (not summary.empty()):
        length, elapsed_time, name = summary.get()
        print(" " + name + " " + str(length) + "\t" + str(elapsed_time))
