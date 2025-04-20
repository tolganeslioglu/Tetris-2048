################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################

import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types (shapes)

# The main function where this program starts execution
def start():
   # set the dimensions of the game grid
   grid_h, grid_w = 20, 12
   # set the size of the drawing canvas (the displayed window)
   canvas_h, canvas_w = 40 * grid_h, 40 * grid_w
   stddraw.setCanvasSize(canvas_w, canvas_h)
   # set the scale of the coordinate system for the drawing canvas
   stddraw.setXscale(-0.5, grid_w - 0.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)

   # set the game grid dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w
   # create the game grid and choose speed via merged menu
   grid = GameGrid(grid_h, grid_w)
   selected_speed = display_game_menu(grid_h, grid_w)
   grid.game_speed = selected_speed
   # create the first tetromino to enter the game grid
   # by using the create_tetromino function defined below
   current_tetromino = create_tetromino()
   grid.current_tetromino = current_tetromino

   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   # display_game_menu(grid_h, grid_w)

   # the main game loop
   while True:
      # check for any user interaction via the keyboard
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
         # if the left arrow key has been pressed
         if key_typed == "left":
            # move the active tetromino left by one
            current_tetromino.move(key_typed, grid)
         # if the right arrow key has been pressed
         elif key_typed == "right":
            # move the active tetromino right by one
            current_tetromino.move(key_typed, grid)
         # if the down arrow key has been pressed
         elif key_typed == "down":
            # move the active tetromino down by one
            # (soft drop: causes the tetromino to fall down faster)
            current_tetromino.move(key_typed, grid)
         
         elif key_typed == "C" or key_typed == "c":   
            # rotate the active tetromino clockwise
            current_tetromino.rotate_clockwise(grid) 

         elif key_typed == "Z" or key_typed == "z":
            # rotate the active tetromino counterclockwise
            current_tetromino.rotate_counter_clockwise(grid)
         
         elif key_typed == "space":
            # hard drop: move the active tetromino down until it lands
            while current_tetromino.move("down", grid):
                pass
         # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

      # move the active tetromino down by one at each iteration (auto fall)
      success = current_tetromino.move("down", grid)
      # lock the active tetromino onto the grid when it cannot go down anymore
      if not success:
         # get the tile matrix of the tetromino without empty rows and columns
         # and the position of the bottom left cell in this matrix
         tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
         # update the game grid by locking the tiles of the landed tetromino
         game_over = grid.update_grid(tiles, pos)
         # end the main game loop if the game is over
         if game_over:
            break
         
         # Merging and Clearing and Free Tiles
         grid.merge_tiles()
         grid.clear_full_rows()
         grid.handle_free_tiles()

         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         current_tetromino = create_tetromino()
         grid.current_tetromino = current_tetromino

      # display the game grid with the current tetromino
      grid.display()

   # print a message on the console when the game is over
   print("Game over")

# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
   # the type (shape) of the tetromino is determined randomly
   tetromino_types = ['I', 'O', 'Z', 'S', 'L', 'J', 'T']
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino

# A function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
    # colors used for the menu
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    # difficulty button setup
    btn_w, btn_h = 2.0, 1.0
    # center group of buttons on screen
    center_x = (grid_width - 1) / 2
    spacing = btn_w * 1.5
    centers = [center_x - spacing, center_x, center_x + spacing]
    labels = ["Easy", "Medium", "Hard"]
    speeds = [150, 100, 50]
    selected_speed = None

    # compute image placement
    current_dir = os.path.dirname(os.path.realpath(__file__))
    img_file = current_dir + "/images/menu_image.png"
    image_to_display = Picture(img_file)
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7

    # vertical position for difficulty buttons: shifted down a bit
    btn_center_y = grid_height / 2 - 2
    # layout for start button
    start_w, start_h = grid_width - 1.5, 2
    start_x = img_center_x - start_w / 2
    start_y = 4
    start_text_y = 5

    while True:
        stddraw.clear(background_color)
        # draw the image
        stddraw.picture(image_to_display, img_center_x, img_center_y)

        # draw difficulty buttons
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(20)
        for i, x in enumerate(centers):
            # button background
            stddraw.setPenColor(button_color)
            stddraw.filledRectangle(x - btn_w/2,
                                    btn_center_y - btn_h/2,
                                    btn_w, btn_h)
            # outline if selected
            if selected_speed == speeds[i]:
                stddraw.setPenColor(text_color)
                stddraw.rectangle(x - btn_w/2,
                                  btn_center_y - btn_h/2,
                                  btn_w, btn_h)
            # label
            stddraw.setPenColor(text_color)
            stddraw.text(x, btn_center_y, labels[i])

        # draw start button
        stddraw.setPenColor(button_color)
        stddraw.filledRectangle(start_x, start_y, start_w, start_h)
        stddraw.setFontSize(25)
        stddraw.setPenColor(text_color)
        stddraw.text(img_center_x, start_text_y, "Click Here to Start the Game")

        stddraw.show(50)
        if stddraw.mousePressed():
            mx, my = stddraw.mouseX(), stddraw.mouseY()
            # check difficulty clicks
            for i, x in enumerate(centers):
                if (x - btn_w/2) <= mx <= (x + btn_w/2) and \
                   (btn_center_y - btn_h/2) <= my <= (btn_center_y + btn_h/2):
                    selected_speed = speeds[i]
            # check start click
            if mx >= start_x and mx <= start_x + start_w and \
               my >= start_y and my <= start_y + start_h and \
               selected_speed is not None:
                return selected_speed


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
   start()
