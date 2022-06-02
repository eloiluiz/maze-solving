#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Maze-Solving Project

This application uses Prim's algorithm to create random mazes and compares different maze solving methods, such as:

Breadth-First Search Method
Depth-First Search Method
Iterative Depth-First Search Method

"""


__author__ = "Eloi Giacobbo"
__email__ = "eloiluiz@gmail.com"
__version__ = "1.0.0"
__status__ = "Production"


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


# **************************************************************
#                           Maze Class
# **************************************************************
class Maze:
    """Class designed to create a maze using the Randomized Prim’s Algorithm.
    """

    def __init__(self, width=5, height=5, complexity=0.75, density=0.75):
        """Initializes the maze creation class.

        Define atributes and generate a randomized maze.

        Args:
            width (int, optional): Defines the maze's width. Defaults to 5.
            height (int, optional): Defines the maze's height. Defaults to 5.
            complexity (float, optional): Defines the maze's complexity. Defaults to 0.75.
            density (float, optional): Defines the maze's density. Defaults to 0.75.
        """

        if(width > 5):
            self.__width = width
        else:
            self.__width = 5

        if(height > 5):
            self.__height = height
        else:
            self.__height = 5

        if(complexity <= 1):
            self.__complexity = complexity
        else:
            self.__complexity = 0.75

        if(density <= 1):
            self.__density = density
        else:
            self.__density = 0.75

        # Genarate the maze
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
                neighbours = []
                if (x > 1):
                    neighbours.append((y, (x - 2)))
                if (x < (shape[1] - 2)):
                    neighbours.append((y, (x + 2)))
                if (y > 1):
                    neighbours.append(((y - 2), x))
                if (y < (shape[0] - 2)):
                    neighbours.append(((y + 2), x))
                if (len(neighbours)):
                    y_, x_ = neighbours[rand(0, (len(neighbours) - 1))]
                    if (self.__map[y_, x_] == 0):
                        self.__map[y_, x_] = 1
                        self.__map[y_ + ((y - y_) // 2), x_ + ((x - x_) // 2)] = 1
                        x = x_
                        y = y_

        # Define starting point
        while True:
            self.__start_position = [rand(1, shape[0]-1), rand(1, shape[1]-1)]
            if(self.__map[self.__start_position[0], self.__start_position[1]] == 0):
                self.__map[self.__start_position[0], self.__start_position[1]] = 2
                break

        # Define goal point
        while True:
            self.__goal_position = [rand(1, shape[0]-1), rand(1, shape[1]-1)]
            if(self.__map[self.__goal_position[0], self.__goal_position[1]] == 0):
                self.__map[self.__goal_position[0], self.__goal_position[1]] = 3
                break

    def print_map(self):
        """Prints the maze on screen.
        """
        for y in range((self.__height // 2)*2+1):
            str = " "
            for x in range((self.__width // 2)*2+1):
                if(self.__map[y, x] == 0):
                    str = str + " "
                elif(self.__map[y, x] == 1):
                    str = str + colored(' ', 'white', 'on_white')
                elif(self.__map[y, x] == 2):
                    str = str + colored('O', 'green')
                elif(self.__map[y, x] == 3):
                    str = str + colored('x', 'red')
                elif(self.__map[y, x] == 4):
                    str = str + colored(' ', 'red', 'on_red')
                elif(self.__map[y, x] == 5):
                    str = str + colored('x', 'white', 'on_red')
            print(str)

    def get_start_position(self):
        """Returns the defined start position coordinates [x, y].

        Returns:
            list: Returns a list containing the [x, y] coordinate values.
        """
        return [self.__start_position[0], self.__start_position[1]]

    # Return value of specified position
    def get_position_value(self, x, y):
        """Returns the selected position value.

        Args:
            x (int): The selected position x coordinate.
            y (int): The selected position y coordinate.

        Returns:
            int: The selected position value.
        """
        return self.__map[y, x]

    def get_neighbour_values(self, x, y):
        """Returns the selected coordinate's neighbour values.

        Args:
            x (int): The selected position x coordinate.
            y (int): The selected position y coordinate.

        Returns:
            list: The neighbour value's list.
        """
        return [self.__map[y+1, x], self.__map[y-1, x], self.__map[y, x-1], self.__map[y, x+1]]

    def set_path(self, x, y):
        """Sets the value of the selected coordinate within the maze to a movement value.

        Args:
            x (int): The selected position x coordinate.
            y (int): The selected position y coordinate.
        """
        if(self.__map[y, x] == 0):
            self.__map[y, x] = 4
        elif(self.__map[y, x] == 3):
            self.__map[y, x] = 5

    def clear_path(self):
        """Clears any movement values within the maze.
        """
        for y in range(((self.__height // 2) * 2) + 1):
            for x in range(((self.__width // 2) * 2) + 1):
                if(self.__map[y, x] == 4):
                    self.__map[y, x] = 0
                elif(self.__map[y, x] == 5):
                    self.__map[y, x] = 3


# **************************************************************
#                          Agent Class
# **************************************************************
class Agent:
    """Intelligent agent base class.
    """
    def __init__(self):
        """Initializes the agent attributes.
        """
        self._start_position = maze.get_start_position()
        self._path = numpy.array([[self._start_position[0], self._start_position[1]]])
        self._visited = numpy.array([[self._start_position[0], self._start_position[1]]])

    # Goal test method
    def is_goal_position(self, x, y):
        """Verifies if the agent has reached the goal position using the input coordinates.

        Args:
            x (int): The selected position x coordinate.
            y (int): The selected position y coordinate.

        Returns:
            bool: The verification result, where True means the goal position is reached and False that it hasn't.
        """
        if(maze.get_position_value(x, y) == 3):
            return True
        else:
            return False

    def is_agent_new(self, x, y):
        """Verifies if the agent is new using the input coordinate values.

        Args:
            x (int): The selected position x coordinate.
            y (int): The selected position y coordinate.

        Returns:
            bool: The verification result, where True means the agent is new and False means other coordinates have been visited already.
        """
        test = numpy.array([[y, x]])
        size = numpy.shape(self._visited)
        for i in range(size[0]):
            if((self._visited[i, :] == test).all()):
                return False
        return True


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

    def __init__(self):
        """Initialize the search agent and execute.
        """
        # Initialization process
        Agent.__init__(self)
        # Execute the search
        self.move(self._start_position[1], self._start_position[0])
        # Print the search result
        print("\n\nBFS – Breadth-First Search:")
        print("Path Length = ", str(numpy.shape(self._path)[0]))
        # Print the complete path
        if (PRINT_INFO == True):
            print("Path = \t", self._path[0, :])
            for i in range(1, numpy.shape(self._path)[0]):
                print("\t", self._path[i, :])
        # Print the result map
        maze.print_map()

    def move(self, x, y):
        """Agent movement method.

        Args:
            x (int): The selected position x coordinate.
            y (int): The selected position y coordinate.

        Returns:
            bool: The movement result, where True means the goal position is reached and False that it hasn't.
        """

        # Update current coordinate
        current = numpy.array([[y, x]])
        # Update the visited positions list
        if((current != self._start_position).any()):
            self._visited = numpy.concatenate((self._visited, current), axis = 0)

        # Check if current level belongs to the level under analisys
        if(self._current_level == self._level):

            # Print current movement step
            if (PRINT_DEBUG == True):
                maze.set_path(x,y)
                maze.print_map()
                print("Current level = ", self._current_level)
                print("Current position = ", current)
                print("Current search level = ", self._level)
                input("PRESS ANY KEY TO CONTINUE...")
                maze.clear_path()

            # Test for goal position
            # Return True if it is the goal position
            if(self.is_goal_position(x, y) == True):
                self._path = self._visited
                maze.set_path(x, y)
                return True

        # If the current position isn't the goal,
        # Check the need to go for the next level
        if(self._current_level < self._level):

            self._current_level += 1

            # Search on upper coordinate
            # Check if the position is part of an path,
            if(maze.get_position_value(x, (y + 1)) != 1):
                if(self.is_agent_new(x, (y + 1))):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move(x, (y + 1))):
                        maze.set_path(x, y)
                        return True

            # Search on lower coordinate
            # If the position is part of an path,
            if(maze.get_position_value(x, (y - 1)) != 1):
                if(self.is_agent_new(x, (y - 1))):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move(x, (y - 1))):
                        maze.set_path(x, y)
                        return True

            # Search on lower coordinate
            # If the position is part of an path,
            if(maze.get_position_value((x - 1), y) != 1):
                if(self.is_agent_new((x - 1), y)):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move((x - 1), y)):
                        maze.set_path(x, y)
                        return True

            # Search on lower coordinate
            # If the position is part of an path,
            if(maze.get_position_value((x + 1), y) != 1):
                if(self.is_agent_new((x + 1), y)):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move((x + 1), y)):
                        maze.set_path(x, y)
                        return True

            # If none of its sons is part of path,
            # This node is removed from path and return false.
            self._current_level -= 1

        # In case this is the first movement action, go to the next level
        if((current == self._start_position).all()):
            self._level += 1
            self._visited = current
            self.move(self._start_position[1], self._start_position[0])
        
        # Lastly, at this point we know this position is not part of the path
        # This node is removed from path and return false.
        else:
            self._visited = numpy.delete(self._visited, (numpy.shape(self._visited)[0] - 1), axis = 0)
            return False


class DFS_Search(Agent):
    """Depth-First Search Method

    This class implements the Depth-First Search algorithm.

    Args:
        Agent (object): The search algorithm intelligent agent parent class.

    Returns:
        object: The DFS agent object.
    """

    def __init__(self):
        """Initialize the search agent and execute.
        """
        # Initialization process
        Agent.__init__(self)
        # Execute the search
        self.move(self._start_position[1], self._start_position[0])
        # Print the search result
        print("\n\nDFS – Depth-First Search:")
        print("Path Length = ", str(numpy.shape(self._path)[0]))
        # Print the complete path
        if (PRINT_INFO == True):
            print("Path = \t", self._path[0, :])
            for i in range(1, numpy.shape(self._path)[0]):
                print("\t", self._path[i, :])
        # Print the result map
        maze.print_map()

    def move(self, x, y):
        """Agent movement method.

        Args:
            x (int): The selected position x coordinate.
            y (int): The selected position y coordinate.

        Returns:
            bool: The movement result, where True means the goal position is reached and False that it hasn't.
        """

        # Update current coordinate
        current = numpy.array([[y, x]])
        # Update the visited positions list
        self._visited = numpy.concatenate((self._visited, current), axis = 0)

        # Print current movement step
        if (PRINT_DEBUG == True):
            maze.set_path(x,y)
            maze.print_map()
            print("Current position = ", current)
            input("PRESS ANY KEY TO CONTINUE...")
            maze.clear_path()

        # Test for goal position
        # If True, set path and return True
        if(self.is_goal_position(x, y)):
            self._path = numpy.array([[y, x]])
            maze.set_path(x, y)
            return True

        # If the current position isn't the goal,

        # Search on upper coordinate
        # Check if the position is part of an path,
        if(maze.get_position_value(x, (y + 1)) != 1):
            if(self.is_agent_new(x, (y + 1))):

                # Move to this coordinate.
                # If this action returns True, the goal was found.
                # Save the curent coordinate as part of the path and return True
                if(self.move(x, (y + 1))):
                    pos = numpy.array([[y, x]])
                    self._path = numpy.concatenate((pos, self._path), axis = 0)
                    maze.set_path(x, y)
                    return True

        # Search on lower coordinate
        # If the position is part of an path,
        if(maze.get_position_value(x, (y - 1)) != 1):
            if(self.is_agent_new(x, (y - 1))):

                # Move to this coordinate.
                # If this action returns True, the goal was found.
                # Save the curent coordinate as part of the path and return True
                if(self.move(x, (y - 1))):
                    pos = numpy.array([[y, x]])
                    self._path = numpy.concatenate((pos, self._path), axis = 0)
                    maze.set_path(x, y)
                    return True

        # Search on left coordinate
        # If the position is part of an path,
        if(maze.get_position_value((x - 1), y) != 1):
            if(self.is_agent_new((x - 1), y)):

                # Move to this coordinate.
                # If this action returns True, the goal was found.
                # Save the curent coordinate as part of the path and return True
                if(self.move((x - 1), y)):
                    pos = numpy.array([[y, x]])
                    self._path = numpy.concatenate((pos, self._path), axis = 0)
                    maze.set_path(x, y)
                    return True

        # Search on right coordinate
        # If the position is part of an path,
        if(maze.get_position_value((x + 1), y) != 1):
            if(self.is_agent_new((x + 1), y)):

                # Move to this coordinate.
                # If this action returns True, the goal was found.
                # Save the curent coordinate as part of the path and return True
                if(self.move((x + 1), y)):
                    pos = numpy.array([[y, x]])
                    self._path = numpy.concatenate((pos, self._path), axis = 0)
                    maze.set_path(x, y)
                    return True

        # If none of its neighbours is part of path, return false
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

    def __init__(self):
        """Initialize the search agent and execute.
        """
        # Initialization process
        Agent.__init__(self)
        # Execute the search
        self.move(self._start_position[1], self._start_position[0])
        # Print the search result
        print("\n\nIDFS – Iterative Depth-First Search:")
        print("Path Length = ", str(numpy.shape(self._path)[0]))
        # Print the complete path
        if (PRINT_INFO == True):
            print("Path = \t", self._path[0, :])
            for i in range(1, numpy.shape(self._path)[0]):
                print("\t", self._path[i, :])
        # Print the result map
        maze.print_map()

    def move(self, x, y):
        """Agent movement method.

        Args:
            x (int): The selected position x coordinate.
            y (int): The selected position y coordinate.

        Returns:
            bool: The movement result, where True means the goal position is reached and False that it hasn't.
        """

        # Update current coordinate
        current = numpy.array([[y, x]])
        # Update the visited positions list
        if((current != self._start_position).any()):
            self._visited = numpy.concatenate((self._visited, current), axis = 0)

        # Test for goal position
        # Return True if it is the goal position
        if(self.is_goal_position(x, y)):
            self._path = self._visited
            maze.set_path(x, y)
            return True

        # Print current movement step
        if (PRINT_DEBUG == True):
            maze.set_path(x,y)
            maze.print_map()
            print("Current level = ", self._current_level)
            print("Current position = ", current)
            print("Current search level = ", self._level)
            input("PRESS ANY KEY TO CONTINUE...")
            maze.clear_path()

        # If current position isn't the goal,
        # Check the need to go for the next level
        if(self._current_level < self._level):

            self._current_level += 1

            # Search on upper coordinate
            # Check if the position is part of an path,
            if(maze.get_position_value(x, (y + 1)) != 1):
                if(self.is_agent_new(x, (y + 1))):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move(x, (y + 1))):
                        maze.set_path(x, y)
                        return True

            # Search on lower coordinate
            # If the position is part of an path,
            if(maze.get_position_value(x, (y - 1)) != 1):
                if(self.is_agent_new(x, (y - 1))):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move(x, (y - 1))):
                        maze.set_path(x, y)
                        return True

            # Search on left coordinate
            # If the position is part of an path,
            if(maze.get_position_value((x - 1), y) != 1):
                if(self.is_agent_new((x - 1), y)):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move((x - 1), y)):
                        maze.set_path(x, y)
                        return True

            # Search on right coordinate
            # If the position is part of an path,
            if(maze.get_position_value((x + 1), y) != 1):
                if(self.is_agent_new((x + 1), y)):

                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move((x + 1), y)):
                        maze.set_path(x, y)
                        return True

            # If none of its sons is part of path,
            # This node is removed from path and return false.
            self._current_level -= 1

        # In case this is the first movement action, go to the next level
        if((current == self._start_position).all()):
            self._level += 1
            self._visited = current
            self.move(self._start_position[1], self._start_position[0])
            
        # Lastly, at this point we know this position is not part of the path
        # This node is removed from path and return false.
        else:
            self._visited = numpy.delete(self._visited, (numpy.shape(self._visited)[0] - 1), axis = 0)
            return False


# **************************************************************
#                  Application Entry Point
# **************************************************************
if __name__ == "__main__":
    # Create a randomized map and print
    maze = Maze(100, 10, .75, .75)
    maze.print_map()
    # Solve the maze using the BFS algorithm
    robot1 = BFS_Search()
    maze.clear_path()
    # Solve the maze using the DFS algorithm
    robot2 = DFS_Search()
    maze.clear_path()
    # Solve the maze using the IDFS algorithm
    robot2 = IDFS_Search()
