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
   canvas_h, canvas_w = 40 * grid_h, (40 * grid_w) + (40 * grid_w/3)
   stddraw.setCanvasSize(canvas_w, canvas_h)
   # set the scale of the coordinate system for the drawing canvas
   stddraw.setXscale(-0.5, grid_w + (grid_w / 3) - 0.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)

   # set the game grid dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w
   # create the game grid
   grid = GameGrid(grid_h, grid_w)
   # create the first tetromino to enter the game grid
   # by using the create_tetromino function defined below
   grid.current_tetromino = create_tetromino()
   grid.next_tetromino = create_tetromino()
   grid.current_tetromino = grid.current_tetromino

   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   display_game_menu(grid_h, grid_w)

   reset = False  

   stddraw.clearKeysTyped()  # clear the queue of the pressed keys for a smoother interaction

   # the main game loop
   while True:
      # check for any user interaction via the keyboard
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped()  # the most recently pressed key

         if key_typed == "P" or key_typed == "p":
            # pause the game when the p key is pressed
            reset = display_pause_menu(grid_w, grid_h)  # Show pause menu
         

         if not reset:  # Only allow controls if game isn't paused
            # if the left arrow key has been pressed
            if key_typed == "left":
               # move the active tetromino left by one
               grid.current_tetromino.move(key_typed, grid)
            # if the right arrow key has been pressed
            elif key_typed == "right":
               # move the active tetromino right by one
               grid.current_tetromino.move(key_typed, grid)
            # if the down arrow key has been pressed
            elif key_typed == "down":
               # move the active tetromino down by one
               # (soft drop: causes the tetromino to fall down faster)
               grid.current_tetromino.move(key_typed, grid)



            
            elif key_typed == "C" or key_typed == "c":   
               # rotate the active tetromino clockwise
               grid.current_tetromino.rotate_clockwise(grid) 
            
            elif key_typed == "Z" or key_typed == "z":
               # rotate the active tetromino counterclockwise
               grid.current_tetromino.rotate_counter_clockwise(grid)

         # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

      if reset:
         do_reset(grid)  # Reset the game grid
         display_game_menu(grid_h, grid_w)
         reset = False
         continue
      else:
         # move the active tetromino down by one at each iteration (auto fall)
         success = grid.current_tetromino.move("down", grid)
         # lock the active tetromino onto the grid when it cannot go down anymore
         if not success:
            # get the tile matrix of the tetromino without empty rows and columns
            # and the position of the bottom left cell in this matrix
            tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)
            # update the game grid by locking the tiles of the landed tetromino
            game_over = grid.update_grid(tiles, pos)
            # end the main game loop if the game is over
            if game_over:
               grid.game_over = True
               # display the game over screen by using the display_game_over function defined below
               reset = display_game_over(grid_w, grid_h, grid.score)
               if reset:
                  do_reset(grid)  # Reset the game grid
                  display_game_menu(grid_h, grid_w)  # Display the game menu again
                  reset = False  # Reset the flag to False
                  continue  # Restart the game      
            # create the next tetromino to enter the game grid
            # by using the create_tetromino function defined below
            grid.current_tetromino = grid.next_tetromino
            grid.next_tetromino = create_tetromino()

      # display the game grid with the current tetromino
      grid.display()

def do_reset(grid):
   grid.reset_scene()  # Reset the game grid
   # create the first tetromino to enter the game grid
   grid.current_tetromino = create_tetromino()
   grid.next_tetromino = create_tetromino()

   # clear the queue of the pressed keys for a smoother interaction
   stddraw.clearKeysTyped()  # clear the queue of the pressed keys for a smoother interaction

# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
   # the type (shape) of the tetromino is determined randomly
   tetromino_types = ['I', 'O', 'Z']
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino

def display_game_over(grid_height, grid_width, current_score):
   background_color = Color(238, 228, 218)
   button_color = Color(119, 110, 101)
   text_color = Color(238, 228, 218)
   
   stddraw.clear(background_color)
   
   center_x = (grid_width - 1) / 2
   top_y = grid_height - 4  # Başlık için üst kısım

   # --- Game Over Başlığı ---
   stddraw.setFontSize(60)
   stddraw.setPenColor(button_color)
   stddraw.boldText(center_x, top_y, "Game Over")

   # --- Skorlar ---
   stddraw.setFontSize(30)
   score_y = top_y - 3
   stddraw.text(center_x, score_y, f"Score: {current_score}")
   stddraw.text(center_x, score_y - 1.5, f"High Score: {load_high_score(current_score)}")

   # --- Restart Butonu ---
   button_w, button_h = 8, 2
   button_y = score_y - 5  # Skordan sonra boşluk bırak
   button_blc_x = center_x - button_w / 2
   
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_y, button_w, button_h)
   
   stddraw.setFontSize(35)
   stddraw.setPenColor(text_color)
   stddraw.text(center_x, button_y + button_h / 2, "Restart")

   # --- Click Kontrol ---
   while True:
      stddraw.show(50)
      if stddraw.mousePressed():
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         if button_blc_x <= mouse_x <= button_blc_x + button_w and button_y <= mouse_y <= button_y + button_h:
            return True

# High score işlemi ayrı fonksiyonda daha temiz olur
def load_high_score(current_score):
   if not os.path.exists("highscore.txt"):
      with open("highscore.txt", "w") as f:
         f.write("0")
   with open("highscore.txt", "r") as f:
      highscore = int(f.read())
   if current_score > highscore:
      with open("highscore.txt", "w") as f:
         f.write(str(current_score))
      return current_score
   return highscore



def display_pause_menu(grid_height, grid_width):
    
    # Colors for pause menu
    background_color = Color(238, 228, 218)
    button_color = Color(119, 110, 101)
    text_color = Color(238, 228, 218)

    # Clear screen with background color
    stddraw.clear(background_color)

    canvas_total_width = grid_width + (grid_width / 3)
    center_x = canvas_total_width / 2 - 0.5
    center_y = grid_height / 2

    # Draw "Paused" text
    stddraw.setFontSize(40)
    stddraw.setPenColor(Color(242, 177, 121))
    stddraw.boldText(center_x-5, center_y + 4, "PAUSED")

    # Button dimensions
    button_w, button_h = 6, 2

    offset = 5

    # Resume Button
    resume_x = center_x - button_w / 2 - offset
    resume_y = center_y
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(resume_x, resume_y, button_w, button_h)
    stddraw.setPenColor(text_color)
    stddraw.setFontSize(20)
    stddraw.text(resume_x + button_w / 2, resume_y + button_h / 2, "Resume")

    # Restart Button
    restart_y = center_y - 3
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(resume_x, restart_y, button_w, button_h)
    stddraw.setPenColor(text_color)
    stddraw.text(resume_x + button_w / 2, restart_y + button_h / 2, "Restart")

    reset = False  # Flag to indicate if the game should be restarted
    # Wait for user click
    while True:
        stddraw.show(50)
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()

            # Check Resume button
            if resume_x <= mouse_x <= resume_x + button_w and resume_y <= mouse_y <= resume_y + button_h:
                reset = False  # Resume
                break

            # Check Restart button
            if resume_x <= mouse_x <= resume_x + button_w and restart_y <= mouse_y <= restart_y + button_h:
                reset = True  # Restart
                break

        stddraw.show(50)
    return reset  # Return the reset flag



# A function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
   # the colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background drawing canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # compute the path of the image file
   img_file = current_dir + "/images/menu_image.png"

   canvas_total_width = grid_width + (grid_width / 3)
   canvas_center_x = canvas_total_width / 2 - 0.5

   # the coordinates to display the image centered horizontally
   img_center_x, img_center_y = canvas_center_x, grid_height - 7
   # the image is modeled by using the Picture class
   image_to_display = Picture(img_file)
   # add the image to the drawing canvas
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # the dimensions for the start game button
   button_w, button_h = 9, 2
   # the coordinates of the bottom left corner for the start game button
   button_blc_x, button_blc_y = canvas_center_x - button_w / 2, 4
   # add the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # add the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Click Here to Start the Game"
   stddraw.text(canvas_center_x, button_blc_y + button_h / 2, text_to_display)
   # the user interaction loop for the simple menu
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the start game button
      if stddraw.mousePressed():
         # get the coordinates of the most recent location at which the mouse
         # has been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break  # break the loop to end the method and start the game


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
   start()
