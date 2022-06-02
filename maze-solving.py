# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 23:53:00 2015

@Author: eloiluiz

@Reference: 

    Maze generation algorithm: http://en.wikipedia.org/wiki/Maze_generation_algorithm

"""

#**************************************************************
#                           Libraries
#**************************************************************
import numpy
from numpy.random import random_integers as rand

from termcolor import colored      #Print collors on terminal


#**************************************************************
#                       Environment Class
#**************************************************************
class Environment:

    # Define atributes and generate map
    def __init__(self, width=5, height=5, complexity=.75, density=.75):
        
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
            self.__complexity = .75
            
        if(density <= 1):
            self.__density = density
        else:
            self.__density = .75

        #Genarate map
        self.gen()
       
    #Generate map
    def gen(self):
        
        # Only odd shapes
        shape = ((self.__height // 2) * 2 + 1, (self.__width // 2) * 2 + 1)
        
        # Adjust complexity and density relative to maze size
        self.__complexity = int(self.__complexity * (5 * (shape[0] + shape[1])))
        self.__density    = int(self.__density * (shape[0] // 2 * shape[1] // 2))
        
        # Build actual maze
        self.__map = numpy.zeros(shape, dtype=int)
        
        # Fill borders
        self.__map[0, :] = self.__map[-1, :] = 1
        self.__map[:, 0] = self.__map[:, -1] = 1
        
        # Make aisles
        for i in range(self.__density):
            x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2
            self.__map[y, x] = 1
            for j in range(self.__complexity):
                neighbours = []
                if x > 1:             neighbours.append((y, x - 2))
                if x < shape[1] - 2:  neighbours.append((y, x + 2))
                if y > 1:             neighbours.append((y - 2, x))
                if y < shape[0] - 2:  neighbours.append((y + 2, x))
                if len(neighbours):
                    y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                    if self.__map[y_, x_] == 0:
                        self.__map[y_, x_] = 1
                        self.__map[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                        x, y = x_, y_        
                
        # Define starting point
        while True:
            self.__startp = [rand(1, shape[0]-1), rand(1, shape[1]-1)]
            
            if(self.__map[self.__startp[0], self.__startp[1]] == 0):
                    self.__map[self.__startp[0], self.__startp[1]] = 2               
                    break
        
        # Define goal point
        while True:
            self.__goalp = [rand(1, shape[0]-1), rand(1, shape[1]-1)]
            
            if(self.__map[self.__goalp[0], self.__goalp[1]] == 0):
                    self.__map[self.__goalp[0], self.__goalp[1]] = 3               
                    break
    
    # Print map
    def print_map(self):
        for y in range((self.__height // 2)*2+1):

            str = " "            
            for x in range((self.__width // 2)*2+1):
                
                if(self.__map[y,x] == 0):               
                    str = str + " "
                else:
                    if(self.__map[y,x] == 1):               
                        str = str + colored(' ', 'white', 'on_white')
                    else:
                        if(self.__map[y,x] == 2):               
                            str = str + colored('O', 'green')
                        else:
                            if(self.__map[y,x] == 3):               
                                str = str + colored('x', 'red')
                            else:
                                if(self.__map[y,x] == 4):               
                                    str = str + colored(' ', 'red', 'on_red')
                                else:
                                    if(self.__map[y,x] == 5):               
                                        str = str + colored('x', 'white', 'on_red')
                
            print(str)

    # Return starting position
    def get_startp(self):
        return [self.__startp[0], self.__startp[1]]

    # Return value of specified position
    def get_position(self, x, y):
        return self.__map[y,x]

    # Return neighbours of specified position
    def get_neighbours(self, x, y):
        return [self.__map[y+1,x],self.__map[y-1,x],self.__map[y,x-1],self.__map[y,x+1]]
        
    # Define movement path
    def set_path(self, x, y):
        if(self.__map[y,x] == 0):
           self.__map[y,x] = 4 
        else: 
            if(self.__map[y,x] == 3):
               self.__map[y,x] = 5
    
    # Clear movement path
    def clear_path(self):
        for y in range((self.__height // 2)*2+1):         
            for x in range((self.__width // 2)*2+1):
                if(self.__map[y,x] == 4):
                    self.__map[y,x] = 0
                else:
                    if(self.__map[y,x] == 5):
                        self.__map[y,x] = 3


#**************************************************************
#                       Create Environment
#**************************************************************
maze = Environment(100, 10, .75, .75)
maze.print_map()


#**************************************************************
#                          Agent Class
#**************************************************************
class Agent:

    def __init__(self):
        self._startp = maze.get_startp()
        self._path = numpy.array([[self._startp[0], self._startp[1]]])
        self._visited = numpy.array([[self._startp[0], self._startp[1]]])

    # Goal test method        
    def goal_test(self, x, y):
        if(maze.get_position(x,y) == 3):
            return True
        else:
            return False
            
    # Verifies if current node is new or have been visited already
    def check_new(self, x, y):
        test = numpy.array([[y,x]])        
        size = numpy.shape(self._visited)
        
        for i in range(size[0]):
            if((self._visited[i,:] == test).all()):
                return False
            
        return True
    

# BFS – Breadth-First Search Method
class BFS_Search(Agent):

    _level = 1
    _current_level = 0

    def __init__(self):
        Agent.__init__(self)        
        self.move(self._startp[1], self._startp[0])
        
        print("\n\nBFS – Breadth-First Search:")
        print("\nPath = \t", self._path[0,:])
        
        for i in range(1, numpy.shape(self._path)[0]):
            print("\t", self._path[i,:])
        
        print("\n")
        
        maze.print_map()

    # Action method
    # x and y variables represent the transition result (new position)
    def move(self, x, y):
        
        current = numpy.array([[y,x]])

        if((current != self._startp).any()):
            self._visited = numpy.concatenate((self._visited, current), axis=0)

        # Test for goal position, if belongs to the analised level
        # Return True if it is the goal position
        if(self._current_level == self._level):
            
#            maze.set_path(x,y)        
#            maze.print_map()
#            
#            print("Current level = ", self._current_level)
#            print("Current position = ", current)
#            print("Current search level = ", self._level)
#            raw_input("PRESS ANY KEY TO CONTINUE...")
#    
#            maze.clear_path()            
            
            if(self.goal_test(x,y)):
                self._path = self._visited
                maze.set_path(x,y)
                return True

        # If the current position isn't the goal,
        # Check the need to go for the next level
        
    
        if(self._current_level < self._level):
            
            self._current_level += 1
            
            # Search on upper coordinate
            # Check if the position is part of an path,
            if(maze.get_position(x,y+1) != 1):
                if(self.check_new(x,y+1)):
                    
                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move(x,y+1)):
                        maze.set_path(x,y)
                        return True
        
            # Search on lower coordinate
            # If the position is part of an path,
            if(maze.get_position(x,y-1) != 1):
                if(self.check_new(x,y-1)):
        
                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move(x,y-1)):
                        maze.set_path(x,y)
                        return True
        
            # Search on lower coordinate
            # If the position is part of an path,
            if(maze.get_position(x-1,y) != 1):
                if(self.check_new(x-1,y)):
        
                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move((x-1),y)):
                        maze.set_path(x,y)
                        return True
        
            # Search on lower coordinate
            # If the position is part of an path,
            if(maze.get_position(x+1,y) != 1):
                if(self.check_new(x+1,y)):
        
                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move(x+1,y)):
                        maze.set_path(x,y)
                        return True
            
            # If none of its sons is part of path, 
            # This node is removed from path and return false.
            self._current_level -= 1
    
        if((current == self._startp).all()):
            self._level += 1
            self._visited = current
            self.move(self._startp[1], self._startp[0])
        else:
            self._visited = numpy.delete(self._visited, numpy.shape(self._visited)[0]-1, axis=0)
            return False


# DFS – Depth-First Search Method
class DFS_Search(Agent):

    def __init__(self):
        Agent.__init__(self)
        self.move(self._startp[1], self._startp[0])
        
        print("\n\nDFS – Depth-First Search:")
        print("\nPath = \t", self._path[0,:])
        
        for i in range(1, numpy.shape(self._path)[0]):
            print("\t", self._path[i,:])
        
        print("\n")       
        
        maze.print_map()

    # Action method
    # x and y variables represent the transition result (new position)
    def move(self, x, y):
        
        current = numpy.array([[y,x]])
        self._visited = numpy.concatenate((self._visited, current), axis=0)        
        
#        maze.set_path(x,y)        
#        maze.print_map()
#        
#        print("Current position = ", current)
#        raw_input("PRESS ANY KEY TO CONTINUE...")
#
#        maze.clear_path()            
        
        # Test for goal position
        # If True, set path and return True
        if(self.goal_test(x,y)):
            self._path = numpy.array([[y,x]])
            maze.set_path(x,y)
            return True
    
        # If the current position isn't the goal,
        # Search on upper coordinate
            
        # Check if the position is part of an path,
        if(maze.get_position(x,y+1) != 1):
            if(self.check_new(x,y+1)):
                
                # Move to this coordinate.
                # If this action returns True, the goal was found.
                # Save the curent coordinate as part of the path and return True
                if(self.move(x,y+1)):
                    pos = numpy.array([[y,x]])
                    self._path = numpy.concatenate((pos, self._path), axis=0)
                    maze.set_path(x,y)
                    return True
    
        # Search on lower coordinate
        # If the position is part of an path,
        if(maze.get_position(x,y-1) != 1):
            if(self.check_new(x,y-1)):
    
                # Move to this coordinate.
                # If this action returns True, the goal was found.
                # Save the curent coordinate as part of the path and return True
                if(self.move(x,y-1)):
                    pos = numpy.array([[y,x]])
                    self._path = numpy.concatenate((pos, self._path), axis=0)
                    maze.set_path(x,y)
                    return True
    
        # Search on lower coordinate
        # If the position is part of an path,
        if(maze.get_position(x-1,y) != 1):
            if(self.check_new(x-1,y)):
    
                # Move to this coordinate.
                # If this action returns True, the goal was found.
                # Save the curent coordinate as part of the path and return True
                if(self.move((x-1),y)):
                    pos = numpy.array([[y,x]])
                    self._path = numpy.concatenate((pos, self._path), axis=0)
                    maze.set_path(x,y)
                    return True
    
        # Search on lower coordinate
        # If the position is part of an path,
        if(maze.get_position(x+1,y) != 1):
            if(self.check_new(x+1,y)):
    
                # Move to this coordinate.
                # If this action returns True, the goal was found.
                # Save the curent coordinate as part of the path and return True
                if(self.move(x+1,y)):
                    pos = numpy.array([[y,x]])
                    self._path = numpy.concatenate((pos, self._path), axis=0)
                    maze.set_path(x,y)
                    return True
        
        # If none of its neighbours is part of path, return false
        return False


# IDFS – Iterative Depth-First Search Method
class IDFS_Search(Agent):

    _level = 1
    _current_level = 0

    def __init__(self):
        Agent.__init__(self)        
        self.move(self._startp[1], self._startp[0])
        
        print("\n\nIDFS – Iterative Depth-First Search:")
        print("\nPath = \t", self._path[0,:])
        
        for i in range(1, numpy.shape(self._path)[0]):
            print("\t", self._path[i,:])
        
        print("\n")
        
        maze.print_map()

    # Action method
    # x and y variables represent the transition result (new position)
    def move(self, x, y):
        
        current = numpy.array([[y,x]])

        if((current != self._startp).any()):
            self._visited = numpy.concatenate((self._visited, current), axis=0)

        # Test for goal position
        # Return True if it is the goal position

        if(self.goal_test(x,y)):
            self._path = self._visited
            maze.set_path(x,y)
            return True

        # If the current position isn't the goal,
        # Check the need to go for the next level
        
#        maze.set_path(x,y)        
#        maze.print_map()
#        
#        print("Current level = ", self._current_level)
#        print("Current position = ", current)
#        print("Current search level = ", self._level)
#        raw_input("PRESS ANY KEY TO CONTINUE...")
#
#        maze.clear_path()
    
        if(self._current_level < self._level):
            
            self._current_level += 1
            
            # Search on upper coordinate
            # Check if the position is part of an path,
            if(maze.get_position(x,y+1) != 1):
                if(self.check_new(x,y+1)):
                    
                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move(x,y+1)):
                        maze.set_path(x,y)
                        return True
        
            # Search on lower coordinate
            # If the position is part of an path,
            if(maze.get_position(x,y-1) != 1):
                if(self.check_new(x,y-1)):
        
                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move(x,y-1)):
                        maze.set_path(x,y)
                        return True
        
            # Search on lower coordinate
            # If the position is part of an path,
            if(maze.get_position(x-1,y) != 1):
                if(self.check_new(x-1,y)):
        
                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move((x-1),y)):
                        maze.set_path(x,y)
                        return True
        
            # Search on lower coordinate
            # If the position is part of an path,
            if(maze.get_position(x+1,y) != 1):
                if(self.check_new(x+1,y)):
        
                    # Move to this coordinate.
                    # If this action returns True, the goal was found.
                    # Save the curent coordinate as part of the path and return True
                    if(self.move(x+1,y)):
                        maze.set_path(x,y)
                        return True
            
            # If none of its sons is part of path, 
            # This node is removed from path and return false.
            self._current_level -= 1
    
        if((current == self._startp).all()):
            self._level += 1
            self._visited = current
            self.move(self._startp[1], self._startp[0])
        else:
            self._visited = numpy.delete(self._visited, numpy.shape(self._visited)[0]-1, axis=0)
            return False            
                
                
#**************************************************************
#                  Create Agent and Solve Maze
#**************************************************************        
robot1 = BFS_Search()
maze.clear_path()
robot2 = DFS_Search()
maze.clear_path()
robot2 = IDFS_Search()
