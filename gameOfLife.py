import copy
import matplotlib.pyplot as plt
from matplotlib import colors as c


class game_of_life(object):
    
    """
        Class containing the functions to run the Game of Life

        To test with different starting boards please specify a
        starting board at the bottom of this file where indicated
    """
    

    def __init__(self, intial_grid):
        # The intial board state is passed to the class, this 
        # is a 2D array of 0's and 1's with 1 representing 
        # alive cells and 0 representing dead cells
        self.board = intial_grid
        

    def play_game(self):
        """
            Takes a number of iterations from the user and runs the game displaying 
            the board after each iteration on the console as well as graphically
        """

        print("\n\n************** Welcome to the Game of life! ************** \n ")

        iterations = input("Please enter the number of iterations you would like to run: ")
        
        i = 0
        self.draw_board(i)
        while(i < int(iterations)):
            
            print("\n------------------ Iteration ", i, " --------------\n")

            # Run a single iteration
            self.run_iteration()

            # Print the board to console
            self.display_board()
            print()

            # Display the board as a coloured graph
            self.draw_board(i)

            # Increment the iteration counter
            i += 1


    def run_iteration(self):
        """
            Runs a single iteration of the board, goes through each cell and updates it based
            on the rules of the game
        """

        # Make a copy of the board to search through but not update to avoid inconsistent updates
        # within the same iteration
        board_copy = copy.deepcopy(self.board)
        
        # Add two layers of zeros around the board copy
        # to be able to search all edge cases of the original board
        board_copy = self.zero_pad(board_copy)
        board_copy = self.zero_pad(board_copy)

        # the offset gives the index difference between the zero padded board copy and the
        # corresponding cell in the non padded board, this number is adapted in cases
        # where cells off the edge of the non padded board become alive   
        offset = 2

        # Tag to determine if the board has been zero padded in order to create life
        # on an outer layer
        zero_padded = False

        # Loop through the whole grid store positions needing updating
        for i in range(1, len(board_copy) -1):
            for j in range(1, len(board_copy[0])-1):

                # Get number of alive neighbours for the given cell
                neighbours = self.get_num_live_neighbour_cells(i, j, board_copy)

                # first check if the cell is alive 
                if (board_copy[i][j]  == 1):

                    # 1) Underpopulation
                    if (neighbours < 2):
                        self.cell_dies(i-offset, j-offset)

                    # 2) Overcrowding
                    if (neighbours > 3):
                        self.cell_dies(i-offset,j-offset)

                    # Do nothing for 3) Survival
                    #if (neighbours == 2 or neighbours == 3):
                        # do nothing
                else:
                    # 4) Creation of life
                    if (neighbours == 3):
                        # Check if the new cell is outside the current square of live cells
                        # Only need to do this a maximum of once per iteration
                        if (i < 2 or i > len(self.board) or j < 2 or j > len(self.board[0])):
                            #if it is pad the boarder with zeros then create life 
                            if not zero_padded:
                                self.board = self.zero_pad(self.board)
                                offset = 1
                                zero_padded = True

                        self.create_life(i-offset,j-offset)


    def get_num_live_neighbour_cells(self, row, col, brd):

        """
            Takes in a board and cell location and return the number of live neighbours
            of the given cell 
        """
        live_count = 0

        if brd[row + 1][col + 1] == 1:
            live_count = live_count + 1 
        if brd[row + 1][col] == 1:
            live_count = live_count + 1 
        if brd[row][col + 1] == 1:
            live_count = live_count + 1 
        if brd[row - 1][col - 1] == 1:
            live_count = live_count + 1 
        if brd[row - 1][col] == 1:
            live_count = live_count + 1 
        if brd[row][col - 1] == 1:
            live_count = live_count + 1 
        if brd[row + 1][col - 1] == 1:
            live_count = live_count + 1 
        if brd[row -1][col + 1] == 1:
            live_count = live_count + 1

        return live_count 


    def zero_pad(self, brd):
        """
            Takes a board and adds a layer of zeroes (dead cells) to the outside
            of the board as these may become live cells
        """

        # Bottom and top layer
        brd.append([0]*len(brd[0]))
        brd.insert(0, [0]*len(brd[0]))

        # Left and right 
        for row in brd:
            row.append(0)
            row.insert(0, 0)

        return brd


    def cell_dies(self, i, j):
        """ Kill the cell at position i, j """
        self.board[i][j] = 0

    def create_life(self, i, j):
        """ Give life to the cell at position i, j"""
        self.board[i][j] = 1

    def display_board(self):
        """
            Print out the board's current state as a grid to console
        """
        for row in self.board:
            for cell in row:

                print(" ", cell, " | ", end=""),

            print()

    def draw_board(self, iteration):

        """
            Displays the board graphically, green squares for alive cells 
            white for dead
        """
        cMap = c.ListedColormap(['white','green'])
        
        p = plt.pcolormesh(self.board, cmap=cMap)  
        fig = plt.figure(1)
        plt.grid(1)
        plt.title("Iteration #" + str(iteration))
        plt.draw()

        ###### Set time between iterations ######
        plt.pause(2)
        #########################################


#############################################################################

# *** PLEASE ENTER A STARTING BOARDD as a 2D ARRAY ***, 
# 1 = Alive cells, 0 = Dead cells
# e.g the test case given in the question sheet is: [[0,0,0], [1,1,1], [0,0,0]]
# P.S [[0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1], [0,1,0,1,0,1,0,1,0,1,0], [1,0,1,0,1,0,1,0,1,0,1], [0,1,0,1,0,1,0,1,0,1,0]]

#############---Edit this line to change the starting board---##############
STARTING_BOARD = [[0,0,0], [1,1,1], [0,0,0]]

# The Game is instantiated and started here
gol = game_of_life(STARTING_BOARD)
gol.play_game()

#############################################################################

