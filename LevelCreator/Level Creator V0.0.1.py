###ProtoType For Level Creator Version 0.0.1###
###24/09/2021###
#Getting The Grid#
import arcade

#Constants
#Screen Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Level Creator First Prototype"

#Grid Constants
GRID_SQUARE = 10


#Setting Up the Game class - This will be changed to game view later
class MyGame(arcade.Window):
    def __init__(self):
        #Set up the window and the grid system
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, True, True)
        arcade.set_background_color(arcade.color.AMAZON)
        self.GridAmount = None
    #Sets up the grid
    def setup(self):
        self.GridAmount = arcade.SpriteList()
        START_X = 5
        START_Y = 5

        TotalNeeded = ((SCREEN_WIDTH * SCREEN_HEIGHT) / (GRID_SQUARE * GRID_SQUARE))
        TotalNeeded = int(TotalNeeded)
        for GridSpot in range(0, TotalNeeded):
            #Draw the amount of grid spots needed, and assign their correct positioning
            grid = Grid(GridSpot, 1)
            grid.position = START_X, START_Y
            START_X += 10
            if START_X >= SCREEN_WIDTH:
                START_X = 5
                START_Y += 10
            self.GridAmount.append(grid)
            
    def on_key_press(self, key, modifiers):
        if key == (arcade.key.ESCAPE) or (arcade.key.ENTER):
            arcade.close_window()
            quit()

    def on_draw(self):
        arcade.start_render()

        self.GridAmount.draw()

class Grid(arcade.Sprite):
    def __init__(self, GridNumber, scale=1):
        self.image_file_name = r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Grid_Square.PNG"

        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")
    

def main():
    window = MyGame()
    window.setup()
    arcade.run()

main()
