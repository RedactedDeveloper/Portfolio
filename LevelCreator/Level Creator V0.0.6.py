###Prototype For Level Creator Version 0.0.6###
#08/10/21#

#Final Colour Change Prototype
#Clicking on a spot will update the colour, right click will remove.
#Added textures for now


import arcade
"""
Constants
Screen Constants"""
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Level Creator Changing Colour Grid"

"""Grid Constants"""
GRID_SQUARE_SIZE = 20
global Current_Colour
Current_Colour = 1

"""GameClass"""

class MyGame(arcade.Window):
    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, True, True)
        #arcade.set_background_color(arcade.color.BLUE)
        self.GridAmount = None
        self.EmptySpace = None
        self.background = None

    def setup(self):

        self.background = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\background.jpg")
        
        self.GridAmount = arcade.SpriteList()
        self.EmptySpace = []
        START_X = 10
        START_Y = 10

        TotalNeeded = ((SCREEN_WIDTH * SCREEN_HEIGHT) / (GRID_SQUARE_SIZE * GRID_SQUARE_SIZE))
        TotalNeeded = int(TotalNeeded)

        """Forms the grid"""
        for GridSpot in range(0, TotalNeeded):
            Placement = CalcGridSpot(START_X, START_Y)
            grid = Grid(Placement)
            grid.position = START_X, START_Y
            START_X += 20

            if START_X >= SCREEN_WIDTH:
                START_X = 10
                START_Y += 20
            
            self.GridAmount.append(grid)

    def on_key_press(self, key, modifiers):
        global Current_Colour
        
        if key == (arcade.key.ESCAPE):
            arcade.close_window()
            quit()
            
        if key == (arcade.key.SPACE):
            """SPACE will cycle the colours forward."""
            if Current_Colour < 9:
                Current_Colour += 1
            

        if key == (arcade.key.ENTER):
            """Enter will cycle the colours back"""
            if Current_Colour > 1:
                Current_Colour -= 1
        

    def on_mouse_press(self, x, y, button, key_modifiers):
        gridspot = arcade.get_sprites_at_point((x, y), self.GridAmount)


        if button == arcade.MOUSE_BUTTON_RIGHT:
            """Removal upon right click"""
##            if len(gridspot) > 0:
##                GridIndex = self.GridAmount.index(gridspot[0])
##                self.EmptySpace.append(self.GridAmount[GridIndex])
##                self.GridAmount.remove(gridspot[0])

            if len(gridspot) > 0:
                GridSpot = CalcGridSpot(x, y)

                GridIndex = self.GridAmount.index(gridspot[0])

                self.GridAmount[GridIndex].set_texture(0)

        if button == arcade.MOUSE_BUTTON_LEFT:

            """Addition if the space is empty"""
            if len(gridspot) == 0:
                
                GridSpot = CalcGridSpot(x, y)
                
                for i in range(0, len(self.EmptySpace)):
                    
                    if self.EmptySpace[i].GridNumber == GridSpot:

                        UpdatedTexture = self.EmptySpace[i]
                        UpdatedTexture.set_texture(Current_Colour)
                        
                        self.GridAmount.append(UpdatedTexture)
                        break
                    
            """Change the texture"""
            if len(gridspot) > 0:

                GridSpot = CalcGridSpot(x, y)

                GridIndex = self.GridAmount.index(gridspot[0])

                self.GridAmount[GridIndex].set_texture(Current_Colour)
                
            
        
    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        
        self.GridAmount.draw()
        

class Grid(arcade.Sprite):
    def __init__(self, GridNumber, scale=1):

        self.GridNumber = GridNumber
        
        super().__init__()

        
        """Load all the textures"""
        self.White = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\Grid.PNG")
        self.Ground = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\Ground.PNG")
        self.GroundL = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\GroundL.PNG")
        self.GroundR = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\GroundR.PNG")
        self.Dirt = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\Dirt.PNG")
        self.Red = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\BigGrid_SquareRed.PNG")
        self.Coin = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\Coin.PNG")
        self.Start = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\Start.PNG")
        self.End = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\End.PNG")
        self.GreenSlime = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\GreenSlime.PNG")

        #To-do
        #Grass blocks with sides.
        #Shorten this somehow

        
        self.append_texture(self.White)
        self.append_texture(self.Ground)
        self.append_texture(self.GroundL)
        self.append_texture(self.GroundR)
        self.append_texture(self.Dirt)
        self.append_texture(self.Red)
        self.append_texture(self.Coin)
        self.append_texture(self.Start)
        self.append_texture(self.End)
        self.append_texture(self.GreenSlime)
        
        self.texture = self.White

                
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

