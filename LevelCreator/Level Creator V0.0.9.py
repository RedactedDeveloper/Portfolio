###Level Creator Version V.0.0.9###
#12/10/21##13/10/21#

#Saving System overhaul
#Saving should take users to a seperate view so they can choose to either overwrite a file, or create a new one.
#https://api.arcade.academy/en/latest/api/gui_widgets.html?highlight=text#arcade-gui-uiinputtext

#All variables need to be lowercase
#All classes uppercase
#Next Prototype will need this changed. Yikes.

#15/10/21 To-Do List
#Not liking the global variables [line 23 - fixed, line 95, line 122 - fixed] - Ask Mr. Leonard about this _/
#Reposition the New File Save box _/
#Add the ability to name the new file
#Add the ability to overwrite a file with saving
#   This can be done with the previous one, either can have it where it just gives you a warning if the file exists
#   Or a new button
#Add padding around the boxes for design.
#Add a way to return to the game from the save menu _/

import arcade
import arcade.gui
import os

"""
Constants
Screen Constants"""
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
        self.background = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\background.jpg")
        self.gridamount = arcade.SpriteList()

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

            #Need to change this to a level prompt in the main menu
            #Make it global?
            level = open(self.levelloadquery, "r")
            for line in level:
                line = line.split(" ")
                
                gridnumber = (int(line[0]), int(line[1]))
                grid = Grid(gridnumber)
                
                grid.position = int(line[2]), int(line[3])

                for i in range(0, len(TEXTURELIST)):
                    if find_Word_Inside_String(TEXTURELIST[i], line[4]):
                        colour = i
                        grid.set_texture(colour)
                    
                self.gridamount.append(grid)
            
            level.close()
            

    def on_key_press(self, key, modifiers):
        global current_colour
        
        if key == (arcade.key.ESCAPE):
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
            
            save_view = SavingMenuView(self.gridamount)
            self.window.show_view(save_view)

    def on_mouse_press(self, x, y, button, key_modifiers):
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

                #GridSpot = CalcGridSpot(x, y)

                grid_index = self.gridamount.index(gridspot[0])

                self.gridamount[grid_index].set_texture(current_colour)
                         
        
    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        
        self.gridamount.draw()
        

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


class MainMenuView(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_RED)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.file_Name_Box_Load = None

        new_Level_Button = arcade.gui.UIFlatButton((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT / 2) - 50, 300, 100, "New")
        new_Level_Button.on_click = self.new_Level
        self.manager.add(new_Level_Button)
        

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Main Menu", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Left click for a new level, right click to enter your level name", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE, font_size=25, anchor_x="center")

        self.manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):

        if button == arcade.MOUSE_BUTTON_RIGHT:
            
            file_Name_Box_Load = arcade.gui.UIInputText((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT / 2) - 200, 300, 100, "Hello")
            self.file_Name_Box_Load = file_Name_Box_Load
            self.manager.add(self.file_Name_Box_Load)

            load_Button = arcade.gui.UIFlatButton((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT / 2) - 50, 300, 100, "Load")
            load_Button.on_click = self.level_Load
            self.manager.add(load_Button)

    def new_Level(self, event):
        self.manager.disable()
        game_view = MyGameView(1)
        game_view.setup()
        self.window.show_view(game_view)

    def level_Load(self, event):

        file_Name_Load = self.file_Name_Box_Load.text

        if file_Name_Load[:-4] != ".txt":
            file_Name_Load = str(file_Name_Load) + ".txt"
        
        if check_Level_Exists(file_Name_Load):
            
            self.manager.disable()
            game_view = MyGameView(file_Name_Load)
            game_view.setup()
            self.window.show_view(game_view)
            
        else:
            self.file_Name_Box_Load.text = "File does not exist"
            


class SavingMenuView(arcade.View):

    def __init__(self, grid_amount):

        super().__init__()
        self.grid_amount = grid_amount
        self.file_Name_Box = None

    def on_show(self):
        
        arcade.set_background_color(arcade.color.GRAY)
        
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        #This function needs to be changed so the user is then prompted to enter a file name.
        #If it exists it should ask if the user is sure they want to overwrite it.
        #If not, just save.
        new_File_Button = arcade.gui.UIFlatButton((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT / 2) - 50, 300, 100, "NewFile")
        new_File_Button.on_click = self.on_click_save_button
        self.manager.add(new_File_Button)

        #Return back to the level, uses a temporary save file to keep the previous state.
        return_To_Game = arcade.gui.UIFlatButton(0, 0, 100, 75, "Return")
        return_To_Game.on_click = self.return_Func
        self.manager.add(return_To_Game)
        
        save(self.grid_amount, "TempSave.txt")
     
    def on_click_save_button(self, event):

        #Here show a text field where the user can enter their filename.
        #Use this to save.
        

        #Need to get it to recognise when the user has typed something into the text box
        
        file_Name_Box = arcade.gui.UIInputText((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT / 2) - 200, 300, 100, "Hello")
        
        self.file_Name_Box = file_Name_Box
        
        self.manager.add(self.file_Name_Box)
        
        save_Button = arcade.gui.UIFlatButton((SCREEN_WIDTH / 2) - 50, (SCREEN_HEIGHT / 2) - 200, 100, 75, "Save")
        
        save_Button.on_click = self.save_Func

        self.manager.add(save_Button)


    def save_Func(self, event):

        file_Name = self.file_Name_Box.text

        if file_Name[:-4] != ".txt":
            file_Name = str(file_Name) + ".txt"

        save(self.grid_amount, file_Name)

    def return_Func(self, event):

        game_view = MyGameView("TempSave.txt")
        game_view.setup()
        self.window.show_view(game_view)
        
    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_text("Save file as new, or overwrite an exisiting file?", self.window.width / 2, self.window.height - 75,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        self.manager.draw()

        
    def on_key_press(self, key, modifiers):
        if key == (arcade.key.ESCAPE):
            arcade.close_window()
            quit()


def calc_Grid_Spot(x, y):
    spot = 0
    other_Spot = 0
    while x > 20:
       x = x - 20
       spot += 1
    while y > 20:
        y = y - 20
        other_Spot += 1
    return (spot, other_Spot)

def find_Word_Inside_String(word_Wanted, string):
    word_Wanted = word_Wanted + "."
    if word_Wanted in string:
        return True
    else:
        return False

def trim_Down_Texture_Location(input):
    new_String = input[61:len(input)]
    return new_String

def save(level, level_name):

    f = open(level_name, "w")
        
    for i in range(0, len(level)):
        
        raw_Data = str(level[i].texture.name)
        new_Data = trim_Down_Texture_Location(raw_Data)
        line = str(level[i].gridnumber[0]) + " " + str(level[i].gridnumber[1]) + " " + str(level[i].position[0]) + " " + str(level[i].position[1]) + " " + new_Data + "\n"
        f.write(line)
            
    f.close()

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


