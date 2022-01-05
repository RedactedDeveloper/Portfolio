###Prototype For Level Creator Version 0.0.5###
#07/10/21#

#Adding in a new colour.
#User should be able to press space to cycle between white and green blocks.
#The existing blocks should not change.


import arcade

#Constants
#Screen Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Level Creator Changing Colour Grid"

#Grid Constants
GRID_SQUARE_SIZE = 20
global Current_Colour
Current_Colour = 1

#GameClass

class MyGame(arcade.Window):
    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, True, True)
        arcade.set_background_color(arcade.color.BLUE)
        self.GridAmount = None
        self.EmptySpace = None

    def setup(self):
        self.GridAmount = arcade.SpriteList()
        self.EmptySpace = []
        START_X = 10
        START_Y = 10

        TotalNeeded = ((SCREEN_WIDTH * SCREEN_HEIGHT) / (GRID_SQUARE_SIZE * GRID_SQUARE_SIZE))
        TotalNeeded = int(TotalNeeded)
        
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
            #For this prototype, SPACE will cycle colours forward.
            if Current_Colour < 4:
                Current_Colour += 1
                

        #How i tested to get the colour changing working
##            Sprite0 = self.GridAmount[0]
##            #print(Sprite0.textures)
##            self.GridAmount.remove(Sprite0)
##            Sprite0.set_texture(0)
##            self.GridAmount.append(Sprite0)

            

        if key == (arcade.key.ENTER):
            #Enter will cycle back
            if Current_Colour > -1:
                Current_Colour -= 1
            
##            Sprite0 = self.GridAmount[0]
##            #print(Sprite0.textures)
##            self.GridAmount.remove(Sprite0)
##            Sprite0.set_texture(1)
##            self.GridAmount.append(Sprite0)
##            #pass
        

    def on_mouse_press(self, x, y, button, key_modifiers):
        gridspot = arcade.get_sprites_at_point((x, y), self.GridAmount)


        """Removal"""
        if len(gridspot) > 0:
            GridIndex = self.GridAmount.index(gridspot[0])
            self.EmptySpace.append(self.GridAmount[GridIndex])
            self.GridAmount.remove(gridspot[0])
           

        """Addition"""
        if len(gridspot) == 0:
            
            GridSpot = CalcGridSpot(x, y)
            
            for i in range(0, len(self.EmptySpace)):
                
                if self.EmptySpace[i].GridNumber == GridSpot:

                    UpdatedTexture = self.EmptySpace[i]
                    UpdatedTexture.set_texture(Current_Colour)
                    
                    self.GridAmount.append(UpdatedTexture)
                    break
                
            
        
    def on_draw(self):
        arcade.start_render()
        
        self.GridAmount.draw()
        

class Grid(arcade.Sprite):
    def __init__(self, GridNumber, scale=1):
        
        ###Colour cannot be changed here, this is the init function
##        if Current_Colour == "Green":
##            self.image_file_name = r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\BigGrid_SquareGreen.PNG"
##        else:
##            self.image_file_name = r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\BigGrid_Square.PNG"

        self.GridNumber = GridNumber
        
        super().__init__()

        self.White = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\BigGrid_Square.PNG")
        self.Green = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\BigGrid_SquareGreen.PNG")
        self.Red = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\BigGrid_SquareRed.PNG")

        
        self.append_texture(self.White)
        self.append_texture(self.Green)
        self.append_texture(self.Red)
        
        

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


##def Button(a=2):
##    if a == 1:
##        a = 0
##        return a
##    if a == 0:
##        a = 1
##        return a

def Update_Colour(Current_Colour):
    if Current_Colour == "White":
        Current_Colour = "Green"
    if Current_Colour == "Green":
        Current_Colour = "White"

def main():
    window = MyGame()
    window.setup()
    arcade.run()


main()  

