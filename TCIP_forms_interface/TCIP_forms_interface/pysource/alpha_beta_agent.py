import math
import random
import time
import sys
import copy
from functools import reduce

##############
# Game Board #
##############

class Board(object):

    # Class constructor.
    #
    # PARAM [2D list of int] board: the board configuration, row-major
    # PARAM [int]            w:     the board width
    # PARAM [int]            h:     the board height
    # PARAM [int]            n:     the number of tokens to line up to win
    def __init__(self, board, w, h, n):
        """Class constructor"""
        # Board data
        self.board = board
        # Board width
        self.w = w
        # Board height
        self.h = h
        # How many tokens in a row to win
        self.n = n
        # Current player
        self.player = 1

    # Clone a board.
    #
    # RETURN [board.Board]: a deep copy of this object
    def copy(self):
        """Returns a copy of this board that can be independently modified"""
        cpy = Board(copy.deepcopy(self.board), self.w, self.h, self.n)
        cpy.player = self.player
        return cpy

    # Check if a line of identical tokens exists starting at (x,y) in direction (dx,dy)
    #
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # PARAM [int] dx: the step in the x direction
    # PARAM [int] dy: the step in the y direction
    # RETURN [Bool]: True if n tokens of the same type have been found, False otherwise
    def is_line_at(self, x, y, dx, dy):
        """Return True if a line of identical tokens exists starting at (x,y) in direction (dx,dy)"""
        # Avoid out-of-bounds errors
        if ((x + (self.n-1) * dx >= self.w) or
            (y + (self.n-1) * dy < 0) or (y + (self.n-1) * dy >= self.h)):
            return False
        # Get token at (x,y)
        t = self.board[y][x]
        # Go through elements
        for i in range(1, self.n):
            if self.board[y + i*dy][x + i*dx] != t:
                return False
        return True

    # Check if a line of identical tokens exists starting at (x,y) in any direction
    #
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # RETURN [Bool]: True if n tokens of the same type have been found, False otherwise
    def is_any_line_at(self, x, y):
        """Return True if a line of identical tokens exists starting at (x,y) in any direction"""
        return (self.is_line_at(x, y, 1, 0) or # Horizontal
                self.is_line_at(x, y, 0, 1) or # Vertical
                self.is_line_at(x, y, 1, 1) or # Diagonal up
                self.is_line_at(x, y, 1, -1)) # Diagonal down

    # Calculate the game outcome.
    #
    # RETURN [int]: 1 for Player 1, 2 for Player 2, and 0 for no winner
    def get_outcome(self):
        """Returns the winner of the game: 1 for Player 1, 2 for Player 2, and 0 for no winner"""
        for x in range(self.w):
            for y in range(self.h):
                if (self.board[y][x] != 0) and self.is_any_line_at(x,y):
                    return self.board[y][x]
        return 0

    # Adds a token for the current player at the given column
    #
    # PARAM [int] x: The column where the token must be added; the column is assumed not full.
    #
    # NOTE: This method switches the current player.
    def add_token(self, x):
        """Adds a token for the current player at column x; the column is assumed not full"""
        # Find empty slot for token
        y = 0
        while self.board[y][x] != 0:
            y = y + 1
        self.board[y][x] = self.player
        # Switch player
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    # Returns a list of the columns with at least one free slot.
    #
    # RETURN [list of int]: the columns with at least one free slot
    def free_cols(self):
        """Returns a list of the columns with at least one free slot"""
        return [x for x in range(self.w) if self.board[-1][x] == 0 ]

    # Prints the current board state.
    def print_it(self):
        print("+", "-" * self.w, "+", sep='')
        for y in range(self.h-1, -1, -1):
            print("|", sep='', end='')
            for x in range(self.w):
                if self.board[y][x] == 0:
                    print(" ", end='')
                else:
                    print(self.board[y][x], end='')
            print("|")
        print("+", "-" * self.w, "+", sep='')
        print(" ", end='')
        for i in range(self.w):
            print(i, end='')
        print("")


###########################
# Alpha-Beta Search Agent #
###########################

__score_weights = [0,10,50,5000,1000000]
__offensiveness = 0.35
__board_x = 6
__board_y = 7
__connect_n = 4
    # Heuristic that determines the maximum depth based on turn
def __depth_heuristic(state):
    turn = 0
    for r in state.board:
        for c in r:
            if c != 0:
                turn += 1
    print("Turn: ", turn)
    if (turn < (state.h-2) * (state.w-1) and state.n == 4) or turn < (state.h-1) * (state.w-1):
        depth = 6
    else:
        depth = (state.h * state.w) - turn
    return depth
    # Computes the value, action of a max value node in pruning
def __max_value(state, depth, alpha, beta):
    win_state = state.get_outcome()
    if win_state == state.player:
        return __score_weights[4], -1
    elif win_state != 0:
        return -__score_weights[4], -1
    if len(state.free_cols()) == 0:
        return 0, -1
    if depth >= 0:
        utility = __utility(state.board, state.player)
        return utility, -1
    
    else:
        best = (-math.inf,-1)
        for s, a in __get_successors(state):
            new_utility = __min_value(s, depth + 1, alpha, beta)
            if new_utility >= best[0]:
                best = (new_utility, a)
            alpha = max(alpha, best[0])
            if best[0] >= beta:
                return best
    return best
# Computes the value, action of a max value node in pruning
def __min_value(state, depth, alpha, beta):
    
    win_state = state.get_outcome()
    if win_state == state.player:
        return __score_weights[4]
    elif win_state != 0:
        return -__score_weights[4]
    if len(state.free_cols()) == 0:
        return 0
    if depth >= 0:
        return __utility(state.board, state.player)
    else:
        worst = math.inf

        for s, __ in __get_successors(state):
            new_utility, __ = __max_value(s, depth + 1, alpha, beta)
            worst = min(worst, new_utility)
            beta = min(beta, worst)
            if worst <= alpha:
                return worst
    return worst
            
        
# Pick a column for the agent to play (External interface).
def go(brd):
    """Search for the best move (choice of column for the token)"""
    depth = -__depth_heuristic(brd)
    __, action = __max_value(brd, depth, -math.inf, math.inf)
    return action

    # Get the successors of the given board.
def __get_successors(brd):
    """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
    # Get possible actions
    freecols = brd.free_cols()
    # Are there legal actions left?
    if not freecols:
        return []
    # Make a list of the new boards along with the corresponding actions
    succ = []
    for col in freecols:
        # Clone the original board
        nb = brd.copy()
        # Add a token to the new board
        # (This internally changes nb.player, check the method definition!)
        nb.add_token(col)
        # Add board to list of successors
        succ.append((nb,col))
    return succ

#Utility function that takes a board_state and its player value
def __utility(board_state, player):
    scores = [0,0] #Array that stores the score of both players as the function loops through the cells and directions
    for dx, dy in [(1,0),(1,1),(0,1),(1,-1)]:#Loops through directions/ dx dy combinations
        for i in range(__board_x): #Loops through rows
            for j in range(__board_y): #Loops through columns
                this = board_state[i][j] #Gets the value/piece in current cell (0-empty, 1-current player, 2-opponent)
                sequence = 1 if this != 0 else 0 #Initializes the sequence size if the first cell is not empty
                #Iterative variables for step
                i_step = i
                j_step = j
                for step in range(__connect_n-1): #Iterate steps from current cell
                    i_step += dx
                    j_step += dy
                    #Checks for off-bounds steps
                    if i_step >= __board_x or i_step < 0 or j_step >= __board_y or j_step < 0:
                        sequence = 0 #Reset sequence value to 0
                        break
                        
                    next = board_state[i_step][j_step] #Gets next cell
                    if this == 0 and next > 0:
                        # If all cells so far were empty and the next is not, update this sequence to match the player with piece on next cell
                        this = next
                        sequence = 1
                    elif this != next:
                        if next == 0:
                            continue
                        # If the cells dont match and are from different players, this sequence cant be a winning sequence for either
                        # Resets sequence to 0
                        sequence = 0
                        break
                    else:
                        # Else, the piece is from the same player and the sequence count increases
                        if this > 0:
                            sequence += 1
                    #Adds score based on sequence and weights predefined in the class
                scores[this-1] += __score_weights[sequence]
    score = __offensiveness * scores[0] - (1 - __offensiveness) * scores[1]
    if player == 2:
        score = -1 * score
    return score #Returns the score for the state

def makeDecision(grid):
    board = Board(grid,7,6,4)
    outcome = board.get_outcome()
    if outcome != 0:
        decision = -1*outcome
    else:
        decision = go(board) + 1
    return decision