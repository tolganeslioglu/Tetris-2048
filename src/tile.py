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
   def __init__(self, number=2, number_color=None, background_color=None):
      self.number = number
      
      # Determine the foreground (number) color
      if number_color is None:
         if number in (2, 4):
               self.foreground_color = color.BOUNDRY_COLOR
         else:
               self.foreground_color = color.WHITE
      else:
         self.foreground_color = number_color

      # Determine the background color
      if background_color is None:
         background_color_name = "TILE_" + str(number)
         try:
            self.background_color = getattr(color, background_color_name)
         except AttributeError:
            print(f"Warning: Color {background_color_name} not found. Using default TILE_2.")
            self.background_color = color.TILE_2
      else:
         self.background_color = background_color

      # Box (boundary) color
      self.box_color = color.LINE_COLOR


   # A method for drawing this tile at a given position with a given length
   def draw(self, position, length=1):  # length defaults to 1
      # draw the tile as a filled square
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(position.x, position.y, length / 2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length / 2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.text(position.x, position.y, str(self.number))
