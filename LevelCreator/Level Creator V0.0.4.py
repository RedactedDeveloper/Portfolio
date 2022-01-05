###Prototype For Level Creator Version 0.0.4###
#27/09/21, 01/10/21, 06/10/21#
#Changing how the grid works#

##Changed the grid number to a coordinate instead. Bottom left tile is now (0, 0) rather than 0.
##This means I can do a simple function for finding the gridspot. (CalcGridSpot())



import arcade

#Constants
#Screen Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Level Creator Different Grid"

#Grid Constants
GRID_SQUARE_SIZE = 20

#GameClass

class MyGame(arcade.Window):
    def __init__(self):
        #Open the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, True, True)
        arcade.set_background_color(arcade.color.BLUE)
        #Open the Grid section
        self.GridAmount = None
        self.EmptySpace = None

    def setup(self):
        self.GridAmount = arcade.SpriteList()
        self.EmptySpace = []
        START_X = 10
        START_Y = 10

        TotalNeeded = ((SCREEN_WIDTH * SCREEN_HEIGHT) / (GRID_SQUARE_SIZE * GRID_SQUARE_SIZE))
        TotalNeeded = int(TotalNeeded)
        #print(TotalNeeded)

        
        for GridSpot in range(0, TotalNeeded):
            Placement = CalcGridSpot(START_X, START_Y)
            grid = Grid(Placement, (START_X, START_Y), True)
            grid.position = START_X, START_Y
            START_X += 20
            
            #print(Placement)
            if START_X >= SCREEN_WIDTH:
                #print(GridSpot)
                START_X = 10
                START_Y += 20
            
            self.GridAmount.append(grid)

    def on_key_press(self, key, modifiers):
        if key == (arcade.key.ESCAPE) or (arcade.key.ENTER):
            arcade.close_window()
            quit()

    def on_mouse_press(self, x, y, button, key_modifiers):
        gridspot = arcade.get_sprites_at_point((x, y), self.GridAmount)

        #Decide to either remove or add a sprite

        #Removal
        if len(gridspot) > 0:
            GridIndex = self.GridAmount.index(gridspot[0])
            self.EmptySpace.append(self.GridAmount[GridIndex])
            #print(self.GridAmount[GridIndex])
            self.GridAmount.remove(gridspot[0])
            #print(self.GridAmount[GridIndex])
           
            
        #Addition
        ###Need to try fix the mouse giving the exact X, Y.
        ###Need it to give the centre of the square so the grid can be selected
        
        if len(gridspot) == 0:
            
            GridSpot = CalcGridSpot(x, y)
            #print(gridspot)
            for i in range(0, len(self.EmptySpace)):
                
                #print(self.EmptySpace[i].GridNumber)
                if self.EmptySpace[i].GridNumber == GridSpot:
                    self.GridAmount.append(self.EmptySpace[i])
                    break
            
        
    def on_draw(self):
        arcade.start_render()
        
        self.GridAmount.draw()
        #self.GridAmount.draw_hit_boxes((255, 0, 0, 255), 2)

class Grid(arcade.Sprite):
    def __init__(self, GridNumber, Position, Visiblity, scale=1):
        self.image_file_name = r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\BigGrid_Square.PNG"
        self.Position = Position
        self.GridNumber = GridNumber
        self.Visiblity = Visiblity
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")


def CalcGridSpot(x, y):
    Spot = 0
    OtherSpot = 0
    while x > 20:
       x = x - 20
       Spot += 1
    while y > 20:
        y = y - 20
        OtherSpot += 1
    return (Spot, OtherSpot)

def main():
    window = MyGame()
    window.setup()
    arcade.run()


main()  

