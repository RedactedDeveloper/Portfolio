###Level Creator Version V.0.0.8###
#12/10/21#

#Asking the user if they want to load a level, or create their own.
#Either using a different view for the main menu, or something else.

import arcade
"""
Constants
Screen Constants"""
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Level Creator Saving Test"

"""Grid Constants"""
GRID_SQUARE_SIZE = 20
global Current_Colour
Current_Colour = 1

##############################
"""GameClass"""

class MyGameView(arcade.View):
    def __init__(self, LevelLoadQuery):

        super().__init__()
        self.GridAmount = None
        self.background = None
        self.LevelLoadQuery = LevelLoadQuery

    def setup(self):
        self.background = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\background.jpg")
        self.GridAmount = arcade.SpriteList()

##        try:
##            Level = open("LevelNum1.txt")
##            LevelLoadQuery = 2
##        except:
##            a = 1

        if self.LevelLoadQuery == 1:

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
                
        if self.LevelLoadQuery == 2:

            Level = open("LevelNum1.txt", "r")
            for Line in Level:
                Line = Line.split(" ")
                
                GridNumber = (int(Line[0]), int(Line[1]))
                grid = Grid(GridNumber)
                
                grid.position = int(Line[2]), int(Line[3])
                
                #Make this either global or accessible without having to update it here
                TextureList = ["Grid", "Ground", "GroundL", "GroundR", "Dirt", "Coin", "Start", "End", "GreenSlime"]

                for i in range(0, len(TextureList)):
                    if FindWordInsideString(TextureList[i], Line[4]):
                        Colour = i
                        grid.set_texture(Colour)
                    
                
                self.GridAmount.append(grid)
            
            Level.close()
            

    def on_key_press(self, key, modifiers):
        global Current_Colour
        
        if key == (arcade.key.ESCAPE):
            arcade.close_window()
            quit()
            
        if key == (arcade.key.SPACE):
            """SPACE will cycle the colours forward."""
            if Current_Colour < 8:
                Current_Colour += 1
            

        if key == (arcade.key.ENTER):
            """Enter will cycle the colours back"""
            if Current_Colour > 1:
                Current_Colour -= 1


        if key == (arcade.key.S):
            f = open("LevelNum1.txt", "w")

            for i in range(0, len(self.GridAmount)):
                RawData = str(self.GridAmount[i].texture.name)

                NewData = TrimDownTextureLocation(RawData)
                    
                Line = str(self.GridAmount[i].GridNumber[0]) + " " + str(self.GridAmount[i].GridNumber[1]) + " " + str(self.GridAmount[i].position[0]) + " " + str(self.GridAmount[i].position[1]) + " " + NewData + "\n"
                f.write(Line)
            
            f.close()
        

    def on_mouse_press(self, x, y, button, key_modifiers):
        gridspot = arcade.get_sprites_at_point((x, y), self.GridAmount)


        if button == arcade.MOUSE_BUTTON_RIGHT:
            """Removal upon right click"""

            if len(gridspot) > 0:
                GridSpot = CalcGridSpot(x, y)

                GridIndex = self.GridAmount.index(gridspot[0])

                self.GridAmount[GridIndex].set_texture(0)


        if button == arcade.MOUSE_BUTTON_LEFT:

                    
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
        self.Coin = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\Coin.PNG")
        self.Start = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\Start.PNG")
        self.End = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\End.PNG")
        self.GreenSlime = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\GreenSlime.PNG")

        self.append_texture(self.White)
        self.append_texture(self.Ground)
        self.append_texture(self.GroundL)
        self.append_texture(self.GroundR)
        self.append_texture(self.Dirt)
        self.append_texture(self.Coin)
        self.append_texture(self.Start)
        self.append_texture(self.End)
        self.append_texture(self.GreenSlime)
        
        self.texture = self.White

class MainMenuView(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_RED)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Main Menu", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Left click for a new level, right click to load level 1", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE, font_size=25, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            game_view = MyGameView(1)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            game_view = MyGameView(2)
        game_view.setup()
        self.window.show_view(game_view)

                
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

def FindWordInsideString(WordWanted, String):
    WordWanted = WordWanted + "."
    if WordWanted in String:
        return True
    else:
        return False

def TrimDownTextureLocation(input):
    
    NewString = input[61:len(input)]
    return NewString
    


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, True, True)
    start_view = MainMenuView()
    window.show_view(start_view)
    arcade.run()


main()

