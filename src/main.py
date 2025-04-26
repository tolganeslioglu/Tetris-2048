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
# sound lib
import vlc

# The main function where this program starts execution
def start():
   # —— Background music (MP3) via VLC ——
   base_dir   = os.path.dirname(os.path.abspath(__file__))
   music_path = os.path.join(base_dir, "music", "main_music.mp3")
   player     = vlc.MediaPlayer(music_path)
   player.audio_set_volume(50)  # adjust 0–100 to taste
   player.play()
   # When the track ends, restart it
   ev = player.event_manager()
   ev.event_attach(vlc.EventType.MediaPlayerEndReached, lambda e: player.play())

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
   # create the game grid and choose speed via merged menu
   grid = GameGrid(grid_h, grid_w)
   selected_speed = display_game_menu(grid_h, grid_w)
   grid.game_speed = selected_speed
   # create the first tetromino to enter the game grid
   # by using the create_tetromino function defined below
   grid.current_tetromino = create_tetromino()
   grid.next_tetromino = create_tetromino()
   grid.current_tetromino = grid.current_tetromino

   # initialize pause state
   reset = False

   has_won = False

   # the main game loop
   while True:
      # input handling (including pause toggle)
      if stddraw.hasNextKeyTyped():
         key_typed = stddraw.nextKeyTyped()
         if key_typed == "P" or key_typed == "p":
            # pause the game when the p key is pressed
            reset = display_pause_menu(grid_w, grid_h)  # Show pause menu
            
         if not reset:
            # original key-driven moves
            if key_typed == 'left':
               grid.current_tetromino.move(key_typed, grid)
            elif key_typed == 'right':
               grid.current_tetromino.move(key_typed, grid)
            elif key_typed == 'down':
               grid.current_tetromino.move(key_typed, grid)
            elif key_typed in ('C','c'):
               grid.current_tetromino.rotate_clockwise(grid)
            elif key_typed in ('Z','z'):
               grid.current_tetromino.rotate_counter_clockwise(grid)
            elif key_typed == 'space':
               while grid.current_tetromino.move('down', grid):
                  pass
         stddraw.clearKeysTyped()

      # if paused, show PAUSED text and skip updates
      if reset:
         do_reset(grid)  # Reset the game grid
         display_game_menu(grid_h, grid_w)
         reset = False
         continue

      # auto-fall and locking logic
      success = grid.current_tetromino.move('down', grid)

      if not success:
         tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)
         game_over = grid.update_grid(tiles, pos)
         # check if the game is over by using the check_win_condition function defined below
         if not has_won and check_win_condition(grid.score):
            # display the win screen by using the display_win_screen function defined below
            reset = display_win_screen(grid_h, grid_w, grid.score, grid)
            has_won = True  # Artık tekrar win ekranı gelmez

            if reset:
               do_reset(grid)
               display_game_menu(grid_h, grid_w)  # Display the game menu again
               reset = False  # Reset the flag to False
               continue  # Restart the game

         if game_over:
            grid.game_over = True
            # display the game over screen by using the display_game_over function defined below
            reset = display_game_over(grid_w, grid_h, grid.score, grid)
            if reset:
               do_reset(grid)  # Reset the game grid
               display_game_menu(grid_h, grid_w)  # Display the game menu again
               reset = False  # Reset the flag to False
               continue  # Restart the game      

         MERGE_ANIM_DELAY = 150 # how long (in ms) to show each merge / cleared phase
         while True: # The Game Loop
            merged  = grid.merge_tiles()
            cleared = grid.clear_full_rows()
            freed   = grid.handle_free_tiles()
            # draw this intermediate state with a short pause
            if merged or cleared or freed:
               # take the max out of delay and the game
               delay_speed = max(MERGE_ANIM_DELAY, grid.game_speed)
               old_speed = grid.game_speed
               grid.game_speed = delay_speed
               grid.display()
               grid.game_speed = old_speed
            else:
               break
         grid.current_tetromino = grid.next_tetromino
         grid.next_tetromino = create_tetromino()

      # render the grid
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
   tetromino_types = ['I', 'O', 'Z', 'S', 'L', 'J', 'T']
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino

def check_win_condition(current_score):
    return current_score >= 2048


def display_win_screen(grid_height, grid_width, current_score, grid):
    background_color = Color(238, 228, 218)
    button_color = Color(119, 110, 101)
    text_color = Color(238, 228, 218)

    stddraw.clear(background_color)

    canvas_total_width = grid_width + (grid_width / 3)
    center_x = canvas_total_width / 2
    center_y = grid_height / 2

    # --- You Win Başlığı ---
    stddraw.setFontSize(60)
    stddraw.setPenColor(button_color)
    stddraw.boldText(center_x, center_y + 5, "You Win!")

    # --- Skor ---
    stddraw.setFontSize(30)
    stddraw.text(center_x, center_y + 2, f"Score: {current_score}")
    stddraw.text(center_x, center_y, f"High Score: {grid.load_high_score(current_score)}")

    # --- Continue Butonu ---
    button_w, button_h = 10, 2
    button_y = center_y - 5
    button_blc_x = center_x - button_w / 2

    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_y, button_w, button_h)

    stddraw.setFontSize(30)
    stddraw.setPenColor(text_color)
    stddraw.text(center_x, button_y + button_h / 2, "Continue")

    # --- Tıklama Kontrolü ---
    while True:
        stddraw.show(50)
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if button_blc_x <= mouse_x <= button_blc_x + button_w and button_y <= mouse_y <= button_y + button_h:
                return


def display_game_over(grid_height, grid_width, current_score, grid):
   background_color = Color(238, 228, 218)
   button_color = Color(119, 110, 101)
   text_color = Color(238, 228, 218)
   
   stddraw.clear(background_color)
   
   canvas_total_width = grid_width + (grid_width / 3)
   center_x = (canvas_total_width - 1) / 2
   top_y = grid_height - 4

   # --- Game Over Başlığı ---
   stddraw.setFontSize(60)
   stddraw.setPenColor(button_color)
   stddraw.boldText(center_x - 5, top_y, "Game Over")

   # --- Skorlar ---
   stddraw.setFontSize(30)
   score_y = top_y - 3
   stddraw.text(center_x - 5, score_y, f"Score: {current_score}")
   stddraw.text(center_x - 5, score_y - 1.5, f"High Score: {grid.load_high_score(current_score)}")

   # --- Restart Butonu ---
   button_w, button_h = canvas_total_width / 3, 2
   button_y = score_y - 5
   button_blc_x = center_x - button_w / 2
   
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x - 5, button_y, button_w, button_h)
   
   stddraw.setFontSize(35)
   stddraw.setPenColor(text_color)
   stddraw.text(center_x - 5, button_y + button_h / 2, "Restart")

   while True:
      stddraw.show(50)
      if stddraw.mousePressed():
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         if button_blc_x <= mouse_x <= button_blc_x + button_w and button_y <= mouse_y <= button_y + button_h:
            return True



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
    # colors used for the menu
    background_color = Color(232,223,213)
    button_color = Color(237,194,46)
    text_color = Color(249,246,242)
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
