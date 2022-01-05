###Level Creator Version V.0.1.0###
#22/10/21#


#File sizes have gone from 130KB down to 20KB
#U.I Tweaks 

import arcade
import arcade.gui
import os

"""
Constants
Screen Constants
"""
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Level Creator Saving Overhaul"

"""Grid Constants"""
GRID_SQUARE_SIZE = 20

TEXTURELIST = ["Grid", "Ground", "GroundL", "GroundR", "Dirt", "Coin", "Start", "End", "GreenSlime"]

current_colour = 1

##############################
"""GameView"""

class MyGameView(arcade.View):

    def __init__(self, levelloadquery):

        super().__init__()
        self.gridamount = None
        self.background = None
        self.levelloadquery = levelloadquery


    def setup(self):
        """Set the background"""
        self.background = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\background.jpg")
        """Create the spritelist for the grid"""
        self.gridamount = arcade.SpriteList()

        """Loading a new level"""
        if self.levelloadquery == 1:
            START_X = 10
            START_Y = 10

            totalneeded = ((SCREEN_WIDTH * SCREEN_HEIGHT) / (GRID_SQUARE_SIZE * GRID_SQUARE_SIZE))
            totalneeded = int(totalneeded)

            """Forms the grid"""
            for gridspot in range(0, totalneeded):
                placement = calc_Grid_Spot(START_X, START_Y)
                grid = Grid(placement)
                grid.position = START_X, START_Y
                START_X += 20

                if START_X >= SCREEN_WIDTH:
                    START_X = 10
                    START_Y += 20
                
                self.gridamount.append(grid)

        
        else:
            """If a level is given, it loads here"""
            """Open up the file, read it line by line"""
            level = open(self.levelloadquery, "r")
            for line in level:
                line = line.split(" ")
                """Line[0] and line[1] are the grid coordinates"""
                gridnumber = (int(line[0]), int(line[1]))
                grid = Grid(gridnumber)

                Coords = calc_XandY_From_GridSpot(int(line[0]), int(line[1]))
                grid.position = Coords[0], Coords[1]

                """Line[2] is the texture file"""
                grid.set_texture(int(line[2]))
                    
                self.gridamount.append(grid)
            
            level.close()
            
    def on_key_press(self, key, modifiers):
        global current_colour
        
        if key == (arcade.key.ESCAPE):
            """Quit button"""
            arcade.close_window()
            quit()
            
        if key == (arcade.key.SPACE):
            """SPACE will cycle the colours forward."""
            if current_colour < 8:
                current_colour += 1
            
        if key == (arcade.key.ENTER):
            """Enter will cycle the colours back"""
            if current_colour > 1:
                current_colour -= 1

        if key == (arcade.key.S):
            """Changes to the saving menu"""
            save_view = SavingMenuView(self.gridamount)
            self.window.show_view(save_view)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Get the grid that the user just pressed"""
        gridspot = arcade.get_sprites_at_point((x, y), self.gridamount)


        if button == arcade.MOUSE_BUTTON_RIGHT:
            """Removal upon right click"""

            if len(gridspot) > 0:
                #GridSpot = CalcGridSpot(x, y)

                grid_index = self.gridamount.index(gridspot[0])

                self.gridamount[grid_index].set_texture(0)


        if button == arcade.MOUSE_BUTTON_LEFT:

            """Change the texture"""
            if len(gridspot) > 0:

                grid_index = self.gridamount.index(gridspot[0])

                self.gridamount[grid_index].set_texture(current_colour)
                         
        
    def on_draw(self):
        arcade.start_render()
        """Rectangle box for the background"""
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        
        self.gridamount.draw()
        
###########################################################

"""Sprite class"""
class Grid(arcade.Sprite):
    def __init__(self, gridnumber, scale=1):

        self.gridnumber = gridnumber
        
        super().__init__()

        
        """Load all the textures"""
        #Perhaps try to shorten this somehow.
        self.white = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\Grid.PNG")
        self.ground = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\Ground.PNG")
        self.groundL = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\GroundL.PNG")
        self.groundR = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\GroundR.PNG")
        self.dirt = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\Dirt.PNG")
        self.coin = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\Coin.PNG")
        self.start = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\Start.PNG")
        self.end = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\End.PNG")
        self.greenSlime = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\GreenSlime.PNG")

        self.append_texture(self.white)
        self.append_texture(self.ground)
        self.append_texture(self.groundL)
        self.append_texture(self.groundR)
        self.append_texture(self.dirt)
        self.append_texture(self.coin)
        self.append_texture(self.start)
        self.append_texture(self.end)
        self.append_texture(self.greenSlime)
        
        self.texture = self.white

#################################################

class MainMenuView(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_RED)

        """Setup and enable the GUI Manager"""
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.file_Name_Box_Load = None
        self.new_Level_Button = None
        self.load_Button = None
        self.main_Menu_Text = None

        self.main_Menu_Text = arcade.gui.UILabel((SCREEN_WIDTH /2) - 200, SCREEN_HEIGHT - 100, 500, 400, "Main Menu", 'Arial', 64)
        self.manager.add(self.main_Menu_Text)

        """Adds the button to create a new level"""
        self.new_Level_Button = arcade.gui.UIFlatButton(150 , (SCREEN_HEIGHT / 2) - 50, 300, 100, "New")
        self.new_Level_Button.on_click = self.new_Level
        self.manager.add(self.new_Level_Button)

        """Load Button"""
        self.load_Button = arcade.gui.UIFlatButton((SCREEN_WIDTH - 450), (SCREEN_HEIGHT / 2) - 50, 300, 100, "Load")
        self.load_Button.on_click = self.level_Load_Menu
        self.manager.add(self.load_Button)
        
        

    def on_draw(self):
        arcade.start_render()
     
        #arcade.draw_text("Left click for a new level, right click to enter your level name", self.window.width / 2, self.window.height / 2 - 75,
                         #arcade.color.WHITE, font_size=25, anchor_x="center")
        self.manager.draw()

            

    """When a new level is selected disable the UIManager (Otherwise the buttons didn't
    disable correctly upon the transition, and switch the view to the level creator)"""
    def new_Level(self, event):
        self.manager.disable()
        game_view = MyGameView(1)
        game_view.setup()
        self.window.show_view(game_view)

    def level_Load_Menu(self, event):

        self.manager.remove(self.new_Level_Button)
        self.manager.remove(self.load_Button)
        self.manager.remove(self.main_Menu_Text)

        text_Input = arcade.gui.UIInputText((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT / 2) - 200, 300, 50, "Enter Level Name Here")

        file_Name_Box_Load = arcade.gui.UIPadding(
            text_Input,
            padding = (10, 10, 10, 10),
            bg_color = arcade.color.WHITE
            )
        
        self.file_Name_Box_Load = file_Name_Box_Load
        self.manager.add(self.file_Name_Box_Load)

        self.load_Button = arcade.gui.UIFlatButton((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT / 2) - 50, 300, 75, "Load")
        self.load_Button.on_click = self.level_Load
        self.manager.add(self.load_Button)
        
    """Check the level has .txt at the end, if not add it on. Then check the level exists"""
    def level_Load(self, event):

        file_Name_Load = self.file_Name_Box_Load.child.text

        if file_Name_Load[-4:] != ".txt":
            file_Name_Load = str(file_Name_Load) + ".txt"
        
        if check_Level_Exists(file_Name_Load):
            
            self.manager.disable()
            game_view = MyGameView(file_Name_Load)
            game_view.setup()
            self.window.show_view(game_view)
            
        else:
            """If it doesnt exist the tell the user"""
            self.file_Name_Box_Load.child.text = "File does not exist"

    def on_key_press(self, key, modifiers):
        if key == (arcade.key.ESCAPE):
            arcade.close_window()
            quit()
            
####################################################

class SavingMenuView(arcade.View):

    def __init__(self, grid_amount):

        super().__init__()
        self.grid_amount = grid_amount
        self.file_Name_Box = None

    def on_show(self):
        
        arcade.set_background_color(arcade.color.GRAY)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        new_File_Button = arcade.gui.UIFlatButton((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT / 2) - 50, 300, 100, "NewFile")
        new_File_Button.on_click = self.on_click_save_button
        self.manager.add(new_File_Button)

        
        return_To_Game = arcade.gui.UIFlatButton(0, 0, 100, 75, "Return")
        return_To_Game.on_click = self.return_Func
        self.manager.add(return_To_Game)

        """Save the level to a file when you enter the save menu, this will be deleted once you leave the save menu"""
        save(self.grid_amount, "TempSave.txt")
     
    def on_click_save_button(self, event):

        """Creates a text field for the user to type in their level name"""
        file_Name_Box = arcade.gui.UIInputText((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT / 2) - 200, 300, 100, "Hello")
        self.file_Name_Box = file_Name_Box
        self.manager.add(self.file_Name_Box)
        """Creates a button to save the level"""
        save_Button = arcade.gui.UIFlatButton((SCREEN_WIDTH / 2) - 50, (SCREEN_HEIGHT / 2) - 200, 100, 75, "Save")
        save_Button.on_click = self.save_Func
        self.manager.add(save_Button)
        


    def save_Func(self, event):
        """Check for the .txt extension, then go to the save function to save"""
        file_Name = self.file_Name_Box.text

        if file_Name[-4:] != ".txt":
            file_Name = str(file_Name) + ".txt"
            
        #print(self.grid_amount[0].gridnumber[0])
        save(self.grid_amount, file_Name)
        self.file_Name_Box.text = "File Successfully Saved"

    def return_Func(self, event):
        """Return the creator view by using the temp save"""
        game_view = MyGameView("TempSave.txt")
        game_view.setup()
        os.remove("TempSave.txt")
        self.manager.disable()
        self.window.show_view(game_view)
        
    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_text("Save file as new, or overwrite an exisiting file?", self.window.width / 2, self.window.height - 75,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        self.manager.draw()

        
    def on_key_press(self, key, modifiers):
        if key == (arcade.key.ESCAPE):
            os.remove("TempSave.txt")
            arcade.close_window()
            quit()

###########################################################  

def calc_Grid_Spot(x, y):
    """Find the coordinates of the gridspot by using the x and y values.
    Each square is 20 pixels wide, so keep diving the x and y value by 20 until you find where it should be"""
    spot = 0
    other_Spot = 0
    while x > GRID_SQUARE_SIZE:
       x = x - GRID_SQUARE_SIZE
       spot += 1
    while y > GRID_SQUARE_SIZE:
        y = y - GRID_SQUARE_SIZE
        other_Spot += 1
    return (spot, other_Spot)

def calc_XandY_From_GridSpot(CoordX, CoordY):
    x = 0
    y = 0

    x = (20 * CoordX) + 10
    y = (20 * CoordY) + 10
    
    return(x, y)
    
"""Find if a file is inside of a string, this is used to find the correct texture inside
the texture directory"""
def find_Word_Inside_String(word_Wanted, string):
    word_Wanted = word_Wanted + "."
    if word_Wanted in string:
        return True
    else:
        return False

"""Trim down the texture by over half"""
#Unused
def trim_Down_Texture_Location(input):
    new_String = input[61:len(input)]
    return new_String

"""The save function.
Opens a file, deletes its contents, then begins saving"""

def save(level, level_name):

    f = open(level_name, "w")
        
    for i in range(0, len(level)):
        
        raw_Data = str(level[i].texture.name)
        
        for j in range(0, len(TEXTURELIST)):
            if find_Word_Inside_String(TEXTURELIST[j], raw_Data):
                colour = j
                colour = str(colour)
        
        """GridNumber[0 and 1] are the grid coordinates, position[0 and 1] and the x and y,
        and the new_Data is the texture data"""
        line = str(level[i].gridnumber[0]) + " " + str(level[i].gridnumber[1]) + " " + colour + "\n"
        f.write(line)
            
    f.close()

"""Check the level exists by searching the chosen directory"""
def check_Level_Exists(level_Name):
    all_Levels = os.listdir(r'C:\Users\AToll\OneDrive\Desktop\LevelCreator')
    for i in range(0, len(all_Levels)):
        if level_Name == all_Levels[i]:
            return True
    return False

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, True, True)
    start_view = MainMenuView()
    window.show_view(start_view)
    arcade.run()

main()


