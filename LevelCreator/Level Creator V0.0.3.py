###ProtoType For Level Creator Version 0.0.3###
###24/09/2021 - Still again###
#Replacing Clicked Tiles#
import arcade

#Constants
#Screen Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Level Creator First Prototype"

#Grid Constants
GRID_SQUARE = 20

#Setting Up the Game class - This will be changed to game view later when the menu
#is implemented - probably not this prototype

class MyGame(arcade.Window):
    def __init__(self):
        #Set up the window and the grid system
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, True, True)
        arcade.set_background_color(arcade.color.AMAZON)
        self.GridAmount = None
        self.ReplacementGrid = None
        
    #Sets up the grid
    def setup(self):
        self.GridAmount = arcade.SpriteList()
        self.ReplacementGrid =arcade.SpriteList()
        START_X = 10
        START_Y = 10

        TotalNeeded = ((SCREEN_WIDTH * SCREEN_HEIGHT) / (GRID_SQUARE * GRID_SQUARE))
        TotalNeeded = int(TotalNeeded)
        
        for GridSpot in range(0, TotalNeeded):
            #Draw the amount of grid spots needed, and assign their correct positioning
            grid = Grid(GridSpot, 1)
            grid.position = START_X, START_Y
            START_X += 20
            if START_X >= SCREEN_WIDTH:
                START_X = 10
                START_Y += 20
            self.GridAmount.append(grid)
            
        rgrid = SecondGrid(0, 1)
        rgrid.position = 1290, 730
        self.ReplacementGrid.append(rgrid)
            
    def on_key_press(self, key, modifiers):
        if key == (arcade.key.ESCAPE) or (arcade.key.ENTER):
            arcade.close_window()
            
    def on_mouse_press(self, x, y, button, key_modifiers):
        gridspot = arcade.get_sprites_at_point((x, y), self.GridAmount)

        if len(gridspot) > 0:
            
            self.GridAmount.remove(gridspot[0])
            AmountReplaced = 0
            NewSpot = SecondGrid(AmountReplaced, 1)
            NewX, NewY = NewCoord(x, y)
            NewSpot.position = NewX, NewY
            
            self.ReplacementGrid.append(NewSpot)
            AmountReplaced += 1
        

    def on_draw(self):
        arcade.start_render()

        self.GridAmount.draw()
        self.ReplacementGrid.draw()

class Grid(arcade.Sprite):
    def __init__(self, GridNumber, scale=1):
        self.image_file_name = r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\BigGrid_Square.PNG"

        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")
        
class SecondGrid(arcade.Sprite):
    def __init__(self, GridNumber, scale=1):
        self.image_file_name = r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Replacement.PNG"
        
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")
        
def NewCoord(x, y):
    base = 10
    NearestTen = 10 * round(x/base)
    if (NearestTen % 20) == 1:
        NearestTen - 10
    NearestTenY = 10 * round(y/base)
    if (NearestTenY % 20) == 1:
        NearestTenY - 10
    return NearestTen, NearestTenY

def main():
    window = MyGame()
    window.setup()
    arcade.run()

main()
