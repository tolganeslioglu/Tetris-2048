from tile import Tile  # used for modeling each tile on the tetrominoes
from point import Point  # used for tile positions
import copy as cp  # the copy module is used for copying tiles and positions
import random  # the random module is used for generating random values
import numpy as np  # the fundamental Python module for scientific computing

# A class for modeling tetrominoes with 7 different types: I, O, Z, S, J, L and T
class Tetromino:
   # the dimensions of the game grid (defined as class variables)
   grid_height, grid_width = None, None

   # A constructor for creating a tetromino with a given shape (type)
   def __init__(self, shape):
      self.type = shape  # set the type of this tetromino
      # determine the occupied (non-empty) cells in the tile matrix based on
      # the shape of this tetromino (see the documentation given with this code)
      occupied_cells = []
      if self.type == 'I':
         n = 4  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino I in its initial rotation state
         occupied_cells.append((1, 0))  # (column_index, row_index)
         occupied_cells.append((1, 1))
         occupied_cells.append((1, 2))
         occupied_cells.append((1, 3))
      elif self.type == 'O':
         n = 2  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino O in its initial rotation state
         occupied_cells.append((0, 0))  # (column_index, row_index)
         occupied_cells.append((1, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
      elif self.type == 'Z':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial rotation state
         occupied_cells.append((0, 1))  # (column_index, row_index)
         occupied_cells.append((1, 1))
         occupied_cells.append((1, 2))
         occupied_cells.append((2, 2))
      elif self.type == 'S':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino S in its initial rotation state
         occupied_cells.append((1, 1))
         occupied_cells.append((2, 1))
         occupied_cells.append((0, 2))
         occupied_cells.append((1, 2))
      elif self.type == 'J':
         n = 3
         # shape of the tetromino J in its initial rotation state
         occupied_cells.append((0, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
         occupied_cells.append((2, 1))
      elif self.type == 'L':
         n = 3
         # shape of the tetromino L in its initial rotation state
         occupied_cells.append((2, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
         occupied_cells.append((2, 1))
      elif self.type == 'T':
         n = 3
         # shape of the tetromino T in its initial rotation state
         occupied_cells.append((1, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
         occupied_cells.append((2, 1))
      # create a matrix of numbered tiles based on the shape of this tetromino
      self.tile_matrix = np.full((n, n), None)
      # create the four tiles (minos) of this tetromino and place these tiles
      # into the tile matrix
      for i in range(len(occupied_cells)):
         col_index, row_index = occupied_cells[i][0], occupied_cells[i][1]
         # pick 4 with %10 change, otherwise 2
         tile_number = 4 if random.random() < 0.1 else 2
         # create a tile for each occupied cell of this tetromino
         self.tile_matrix[row_index][col_index] = Tile(tile_number)
      # initialize the position of this tetromino (as the bottom left cell in
      # the tile matrix) with a random horizontal position above the game grid
      self.bottom_left_cell = Point()
      self.bottom_left_cell.y = Tetromino.grid_height - 1
      self.bottom_left_cell.x = random.randint(0, Tetromino.grid_width - n)

   # A method that computes and returns the position of the cell in the tile
   # matrix specified by the given row and column indexes
   def get_cell_position(self, row, col):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      position = Point()
      # horizontal position of the cell
      position.x = self.bottom_left_cell.x + col
      # vertical position of the cell
      position.y = self.bottom_left_cell.y + (n - 1) - row
      return position

   # A method to return a copy of the tile matrix without any empty row/column,
   # and the position of the bottom left cell when return_position is set
   def get_min_bounded_tile_matrix(self, return_position=False):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      # determine rows and columns to copy (omit empty rows and columns)
      min_row, max_row, min_col, max_col = n - 1, 0, n - 1, 0
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               if row < min_row:
                  min_row = row
               if row > max_row:
                  max_row = row
               if col < min_col:
                  min_col = col
               if col > max_col:
                  max_col = col
      # copy the tiles from the tile matrix of this tetromino
      copy = np.full((max_row - min_row + 1, max_col - min_col + 1), None)
      for row in range(min_row, max_row + 1):
         for col in range(min_col, max_col + 1):
            if self.tile_matrix[row][col] is not None:
               row_ind = row - min_row
               col_ind = col - min_col
               copy[row_ind][col_ind] = cp.deepcopy(self.tile_matrix[row][col])
      # return just the matrix copy when return_position is not set (as True)
      # the argument return_position defaults to False when a value is not given
      if not return_position:
         return copy
      # otherwise return the position of the bottom left cell in copy as well
      else:
         blc_position = cp.copy(self.bottom_left_cell)
         blc_position.translate(min_col, (n - 1) - max_row)
         return copy, blc_position

   # A method for drawing the tetromino on the game grid
   def draw(self, pred = False, next_display=False):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      for row in range(n):
         for col in range(n):
            # draw each occupied cell as a tile on the game grid
            if self.tile_matrix[row][col] is not None:
               # get the position of the tile
               position = self.get_cell_position(row, col)

               if next_display:
                  self.tile_matrix[row][col].draw(position, is_next=True)
               # draw only the tiles that are inside the game grid
               if position.y < Tetromino.grid_height:
                  self.tile_matrix[row][col].draw(position, is_pred=pred)

   # A method for moving this tetromino in a given direction by 1 on the grid
   def move(self, direction, game_grid):
      # check if this tetromino can be moved in the given direction by using
      # the can_be_moved method defined below
      if not (self.can_be_moved(direction, game_grid)):
         return False  # the tetromino cannot be moved in the given direction
      # move this tetromino by updating the position of its bottom left cell
      if direction == "left":
         self.bottom_left_cell.x -= 1
      elif direction == "right":
         self.bottom_left_cell.x += 1
      else:  # direction == "down"
         self.bottom_left_cell.y -= 1
      return True  # a successful move in the given direction

   # A method for checking if this tetromino can be moved in a given direction
   def can_be_moved(self, direction, game_grid):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      # check for moving left or right
      if direction == "left" or direction == "right":
         for row_index in range(n):
            for col_index in range(n):
               # direction = left --> check the leftmost tile of each row
               row, col = row_index, col_index
               if direction == "left" and self.tile_matrix[row][col] is not None:
                  # the position of the leftmost tile of the current row
                  leftmost = self.get_cell_position(row, col)
                  # if any leftmost tile is at x = 0
                  if leftmost.x == 0:
                     return False  # this tetromino cannot be moved left
                  # if the grid cell on the left of a leftmost tile is occupied
                  if game_grid.is_occupied(leftmost.y, leftmost.x - 1):
                     return False  # this tetromino cannot be moved left
                  # as the leftmost tile of the current row is checked
                  break  # end the inner for loop
               # direction = right --> check the rightmost tile of each row
               row, col = row_index, n - 1 - col_index
               if direction == "right" and self.tile_matrix[row][col] is not None:
                  # the position of the rightmost tile of the current row
                  rightmost = self.get_cell_position(row, col)
                  # if any rightmost tile is at x = grid_width - 1
                  if rightmost.x == Tetromino.grid_width - 1:
                     return False  # this tetromino cannot be moved right
                  # if the grid cell on the right of a rightmost tile is occupied
                  if game_grid.is_occupied(rightmost.y, rightmost.x + 1):
                     return False  # this tetromino cannot be moved right
                  # as the rightmost tile of the current row is checked
                  break  # end the inner for loop
      # direction = down --> check the bottommost tile of each column
      else:
         for col in range(n):
            for row in range(n - 1, -1, -1):
               # if the current cell of the tetromino is occupied by a tile
               if self.tile_matrix[row][col] is not None:
                  # the position of the bottommost tile of the current col
                  bottommost = self.get_cell_position(row, col)
                  # if any bottommost tile is at y = 0
                  if bottommost.y == 0:
                     return False  # this tetromino cannot be moved down
                  # if the grid cell below any bottommost tile is occupied
                  if game_grid.is_occupied(bottommost.y - 1, bottommost.x):
                     return False  # this tetromino cannot be moved down
                  # as the bottommost tile of the current row is checked
                  break  # end the inner for loop
      # if this method does not end by returning False before this line
      return True  # this tetromino can be moved in the given direction
   
   # A method for checking if this tetromino can be rotated on the game grid
   def can_be_rotated(self, game_grid):
      compact_matrix, blc_position = self.get_min_bounded_tile_matrix(True)
      n_rows, n_cols = len(compact_matrix), len(compact_matrix[0])
      for col in range(n_cols):
         for row in range(n_rows):            
            # place each tile onto the game grid
            if compact_matrix[row][col] is not None:
               # compute the position of the tile on the game grid
               pos = Point()
               pos.x = blc_position.x + col
               pos.y = blc_position.y + (n_rows - 1) - row
               if not game_grid.is_inside(pos.y, pos.x):
                  return False
               if game_grid.tile_matrix[pos.y][pos.x] is not None:
                  return False
      return True
   
   # A method for rotating this tetromino clockwise by 90 degrees
   def rotate_clockwise(self, game_grid):
      # rotate the tile matrix of this tetromino clockwise by 90 degrees
      self.tile_matrix = np.rot90(self.tile_matrix, -1)
       # check if the tetromino can be rotated or not
      if not self.can_be_rotated(game_grid):
         # if the tetromino cannot be rotated, rotate it back to its original
         # position by rotating it counter-clockwise by 90 degrees
         self.tile_matrix = np.rot90(self.tile_matrix, 1)
         return False
      # otherwise return True to indicate a successful rotation
      return True

   # A method for rotating this tetromino counter-clockwise by 90 degrees
   def rotate_counter_clockwise(self, game_grid):
      # rotate the tile matrix of this tetromino counter-clockwise by 90 degrees
      self.tile_matrix = np.rot90(self.tile_matrix, 1)
      # check if the tetromino can be rotated or not
      if not self.can_be_rotated(game_grid):
         # if the tetromino cannot be rotated, rotate it back to its original
         # position by rotating it clockwise by 90 degrees
         self.tile_matrix = np.rot90(self.tile_matrix, -1)
         return False
      # otherwise return True to indicate a successful rotation
      return True

