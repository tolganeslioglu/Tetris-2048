import lib.stddraw as stddraw  # used for drawing the tiles to display them
import lib.color as color

# A class for modeling numbered tiles as in 2048
class Tile:
   # Class variables shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.004
   # font family and font size used for displaying the tile number
   font_family, font_size = "Arial", 14

   # A constructor that creates a tile with 2 as the number on it
   def __init__(self, number=2):
      self.number = number
      # set color based on number
      self.update_color()

   def update_color(self):
      # Foreground color: dark border for 2 & 4, white for everything else
      if self.number in (2, 4):
         self.foreground_color = color.BOUNDRY_COLOR
      else:
         self.foreground_color = color.WHITE

      # Background color: use TILE_<number> if it exists, otherwise TILE_2048
      background_name = f"TILE_{self.number}"
      if hasattr(color, background_name):
         self.background_color = getattr(color, background_name)
      else:
         # Any tile >2048 uses the 2048 color
         self.background_color = color.TILE_2048

      # Box (boundary) color is always the grid line color
      self.box_color = color.LINE_COLOR


   # A method for drawing this tile at a given position with a given length
   def draw(self, position, length=1, is_next=False, is_pred=False):
      # draw the tile as a filled square
      if is_pred:
         stddraw.setPenColor(color.DARK_GRAY)

      else:
         stddraw.setPenColor(self.background_color)

      stddraw.filledSquare(position.x, position.y, length / 2)

      # draw the bounding box around the tile as a square
      if is_pred:
         stddraw.setPenColor(color.LIGHT_GRAY)
         
      else:
         stddraw.setPenColor(self.box_color)

      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length / 2)
      stddraw.setPenRadius()  # reset the pen radius to its default value

      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)

      if is_next:
         stddraw.setFontSize(self.font_size - 3)
      else:
         stddraw.setFontSize(self.font_size)
      
      stddraw.text(position.x, position.y, str(self.number))
      stddraw.setPenRadius()  # reset the pen radius to its default value