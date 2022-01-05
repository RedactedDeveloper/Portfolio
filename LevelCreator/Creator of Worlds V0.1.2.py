###Creator of Worlds V.0.1.2###
#05/11/21#

#Add a camera - for the platformer
#Add gameover/win screen
#Adjust controls slightly
#Jumppads!

#To-Do Either in this prototype or another.
#When you put a grass block on top of another, the bottom should turn to dirt. -Done
#Saving should warn the user about overwriting -Function is already made, add it to the saving.
#Improve how the U.I looks in general. - This will need designing, leave to the end.
#Level creator needs U.I to tell the user what block theyre using. -Done

#Will be easier to learn how the camera works with the platformer before implementing the camera for the level creator.

#When a jump platform is placed. Place a 'jump' tile above it which controls the increase in jump height. - Done
#When placing a jump pad in creation mode, if a tile is above the jumppad/it is at the top of the screen, don't place and warn the user

import arcade
import arcade.gui
import os

"""
Constants
Screen Constants
"""
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Platformer Tweaks and Improvements"

"""Grid Constants"""
GRID_SQUARE_SIZE = 20

TEXTURELIST = ["Grid", "Ground", "GroundL", "GroundR", "Dirt", "Coin", "Start", "End", "Jumppad"]

"""Player Constants"""

PLAYER_SPEED = 3
GRAVITY = 0.75
PLAYER_JUMP_SPEED = 10

##############################
"""GameView"""

class LevelCreatorView(arcade.View):

    def __init__(self, levelloadquery):

        super().__init__()
        self.gridamount = None
        self.background = None
        self.levelloadquery = levelloadquery
        self.current_colour = 1
        self.gui_camera = None

        self.hud_Sprite = None
        
        self.manager = arcade.gui.UIManager()
        self.manager.enable()


    def setup(self):
        """Set the background"""
        self.background = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\background.jpg")
        """Create the spritelist for the grid"""
        self.gridamount = arcade.SpriteList()

        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

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


        self.hud_Sprite = Grid(63, 36)
        self.hud_Sprite.set_texture(1)
        sprite_Widget = arcade.gui.UISpriteWidget(x=1230, y=670, width=40, height=40, sprite=self.hud_Sprite)
        
        self.manager.add(sprite_Widget)
        
    def on_key_press(self, key, modifiers):
        
        if key == (arcade.key.ESCAPE):
            """Quit button"""
            arcade.close_window()
            quit()
            
        if key == (arcade.key.SPACE):
            """SPACE will cycle the colours forward."""
            if self.current_colour < 8:
                self.current_colour += 1

                #self.manager.remove(self.hud_Sprite)
                self.hud_Sprite.set_texture(self.current_colour)
                #self.manager.add(self.hud_Sprite)
            
        if key == (arcade.key.ENTER):
            """Enter will cycle the colours back"""
            if self.current_colour > 1:
                self.current_colour -= 1
                
                #self.manager.remove(self.hud_Sprite)
                self.hud_Sprite.set_texture(self.current_colour)
                #self.manager.add(self.hud_Sprite)

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

                grid_index = self.gridamount.index(gridspot[0])

                self.gridamount[grid_index].set_texture(0)


        if button == arcade.MOUSE_BUTTON_LEFT:

            """Change the texture"""
            if len(gridspot) > 0:

                updateColour = True

                grid_index = self.gridamount.index(gridspot[0])

                

                """If the spot underneath is grassy, turn it to dirt"""

                #underneath_X, underneath_Y = calc_XandY_From_GridSpot(self.gridamount[grid_index].gridnumber[0], (self.gridamount[grid_index].gridnumber[1]) - 1)

                overhead_X, overhead_Y = calc_XandY_From_GridSpot(self.gridamount[grid_index].gridnumber[0], (self.gridamount[grid_index].gridnumber[1]) + 1)
                
                #spot_Underneath = arcade.get_sprites_at_point((underneath_X, underneath_Y), self.gridamount)

                spot_Overhead = arcade.get_sprites_at_point((overhead_X, overhead_Y), self.gridamount)

                #print(len(spot_Overhead))

                try:
                    underneath_X, underneath_Y = calc_XandY_From_GridSpot(self.gridamount[grid_index].gridnumber[0], (self.gridamount[grid_index].gridnumber[1]) - 1)

                    spot_Underneath = arcade.get_sprites_at_point((underneath_X, underneath_Y), self.gridamount)
                    
                    if find_Word_Inside_String("Ground", spot_Underneath[0].texture.name) and self.current_colour == 1:

                        underneath_Index = self.gridamount.index(spot_Underneath[0])

                        self.gridamount[underneath_Index].set_texture(4)
                except:
                    
                    pass
                    
                try:    
                    if ((find_Word_Inside_String("Ground", spot_Overhead[0].texture.name)) or (find_Word_Inside_String("Dirt", spot_Overhead[0].texture.name))) and self.current_colour == 1:

                        #overhead_Index = self.gridamount.index(spot_Overhead[0])
    
                        self.gridamount[grid_index].set_texture(4)
                        updateColour = False
                        
                except:
                    pass

                
                if self.current_colour == 8:

                    try:
                        
                        if len(spot_Overhead) == 0:
                            print("oi")
                            ###PUT THE USER WARN STATEMENTS HERE
                            pass

                        elif ((len(spot_Overhead) == 1) and not(find_Word_Inside_String("Grid", spot_Overhead[0].texture.name))):
                            print("double oi")
                            pass
                        
                        else:
                            self.gridamount[grid_index].set_texture(self.current_colour)
                    except:
                        pass
                    
                if self.current_colour != 8 and updateColour:
                    self.gridamount[grid_index].set_texture(self.current_colour)
            
    def on_draw(self):
        arcade.start_render()
        """Rectangle box for the background"""
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        
        self.gridamount.draw()

        self.gui_camera.use()
        self.manager.draw()
        
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
        self.jumpPad = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\Jumppad.PNG")
        self.blank = arcade.load_texture(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\BlankGrid.PNG")

        self.append_texture(self.white)
        self.append_texture(self.ground)
        self.append_texture(self.groundL)
        self.append_texture(self.groundR)
        self.append_texture(self.dirt)
        self.append_texture(self.coin)
        self.append_texture(self.start)
        self.append_texture(self.end)
        self.append_texture(self.jumpPad)
        self.append_texture(self.blank)
        
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
        self.load_type = None

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

        self.play_Button = arcade.gui.UIFlatButton(((SCREEN_WIDTH /2)- 150), (SCREEN_HEIGHT / 2) - 150, 300, 100, "Play")
        self.play_Button.on_click = self.play_Menu
        self.manager.add(self.play_Button)        
        

    def on_draw(self):
        arcade.start_render()
 
        self.manager.draw()

            

    """When a new level is selected disable the UIManager (Otherwise the buttons didn't
    disable correctly upon the transition, and switch the view to the level creator)"""
    def play_Menu(self, event):

        self.manager.remove(self.new_Level_Button)
        self.manager.remove(self.load_Button)
        self.manager.remove(self.main_Menu_Text)
        self.manager.remove(self.play_Button)

        text_Input = arcade.gui.UIInputText((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT / 2) - 200, 300, 50, "Enter Level Name Here")

        file_Name_Box_Play = arcade.gui.UIPadding(
            text_Input,
            padding = (10, 10, 10, 10),
            bg_color = arcade.color.WHITE
            )

        self.file_Name_Box_Play = file_Name_Box_Play
        self.manager.add(self.file_Name_Box_Play)

        self.Playing_Button = arcade.gui.UIFlatButton((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT / 2) - 50, 300, 75, "Load")
        self.Playing_Button.on_click = self.level_Play
        self.manager.add(self.Playing_Button)
        
    
    def new_Level(self, event):
        self.manager.disable()
        creator_view = LevelCreatorView(1)
        creator_view.setup()
        self.window.show_view(creator_view)

    def level_Load_Menu(self, event):

        self.manager.remove(self.new_Level_Button)
        self.manager.remove(self.load_Button)
        self.manager.remove(self.main_Menu_Text)
        self.manager.remove(self.play_Button)

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
            creator_view = LevelCreatorView(file_Name_Load)
            creator_view.setup()
            self.window.show_view(creator_view)
            
        else:
            """If it doesnt exist the tell the user"""
            self.file_Name_Box_Load.child.text = "File does not exist"

    def level_Play(self, event):

        file_Name_Play = self.file_Name_Box_Play.child.text

        if file_Name_Play[-4:] != ".txt":
            file_Name_Play = str(file_Name_Play) + ".txt"

        if check_Level_Exists(file_Name_Play):

            self.manager.disable()
            game_view = PlatformerView(file_Name_Play)
            game_view.setup()
            self.window.show_view(game_view)

        else:
            self.file_Name_Box_Play.child.text = "File does not exist"
        

        
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
            
        save(self.grid_amount, file_Name)
        self.file_Name_Box.text = "File Successfully Saved"

    def return_Func(self, event):
        """Return the creator view by using the temp save"""
        creator_view = LevelCreatorView("TempSave.txt")
        creator_view.setup()
        os.remove("TempSave.txt")
        self.manager.disable()
        self.window.show_view(creator_view)
        
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

class PlatformerView(arcade.View):

    def __init__(self, level):
         super().__init__()

         self.scene = None

         self.player_Sprite_List = None
         self.player_Sprite = None
         self.walls = None
         self.level = level
         self.coins = None

         
         self.gui_camera = None
         self.score = None

         arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)


         self.player_Speed = None
         self.gravity = None
         self.player_Jump_Speed = None

    def setup(self):

        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Coins", use_spatial_hash=True)
        self.scene.add_sprite_list("End", use_spatial_hash=True)
        self.scene.add_sprite_list("JumpPads", use_spatial_hash=True)
        
        self.player_Sprite_List = arcade.SpriteList()
        self.walls = arcade.SpriteList(use_spatial_hash=True)
        self.coins = arcade.SpriteList(use_spatial_hash=True)
        self.end = arcade.SpriteList(use_spatial_hash=True)
        
        self.player_Sprite = arcade.Sprite(r"C:\Users\AToll\OneDrive\Desktop\LevelCreator\Assets\Textures\stick-man.PNG", 1)
        self.player_Sprite.position = 70, 40
        
        self.scene.add_sprite("Player", self.player_Sprite)

        self.gui_Camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.score = 0

        self.player_Speed = 3
        self.gravity = 0.75
        self.player_Jump_Speed = 10

        
        """Open up the file, read it line by line"""
        file = open(self.level, "r")
        for line in file:
            line = line.split(" ")

            if int(line[2]) == 0:
                pass

            elif int(line[2]) == 5:
                gridnumber = (int(line[0]), int(line[1]))
                grid = Grid(gridnumber)

                Coords = calc_XandY_From_GridSpot(int(line[0]), int(line[1]))
                grid.position = Coords[0], Coords[1]

                """Line[2] is the texture file"""
                grid.set_texture(int(line[2]))
                    
                self.scene.add_sprite("Coins", grid)

            elif int(line[2]) == 7:
                
                gridnumber = (int(line[0]), int(line[1]))
                grid = Grid(gridnumber)

                Coords = calc_XandY_From_GridSpot(int(line[0]), int(line[1]))
                grid.position = Coords[0], Coords[1]

                
                grid.set_texture(0)
                    
                self.scene.add_sprite("End", grid)

            elif int(line[2]) == 8:
                
                gridnumber = (int(line[0]), int(line[1]))
                grid = Grid(gridnumber)

                Coords = calc_XandY_From_GridSpot(int(line[0]), int(line[1]))
                grid.position = Coords[0], Coords[1]
                
                grid.set_texture(8)

                self.scene.add_sprite("Walls", grid)
                

                gridnumber = (int(line[0]), (int(line[1]) + 1))
                grid = Grid(gridnumber)

                Coords = calc_XandY_From_GridSpot(int(line[0]), (int(line[1]) + 1))
                grid.position = Coords[0], Coords[1]

                grid.set_texture(9)
                self.scene.add_sprite("JumpPads", grid)

                
                
                
            else:
                """Line[0] and line[1] are the grid coordinates"""
                gridnumber = (int(line[0]), int(line[1]))
                grid = Grid(gridnumber)

                Coords = calc_XandY_From_GridSpot(int(line[0]), int(line[1]))
                grid.position = Coords[0], Coords[1]

                """Line[2] is the texture file"""
                grid.set_texture(int(line[2]))
                    
                self.scene.add_sprite("Walls", grid)
        
        file.close()

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_Sprite,
                                                             self.scene.get_sprite_list("Walls"),
                                                             gravity_constant=GRAVITY
                                                             )

    def on_draw(self):

        arcade.start_render()

        self.scene.draw()

        self.gui_Camera.use()

        score_Text = ("Score:" + str(self.score))
        arcade.draw_text(score_Text, 300, 300, arcade.color.WHITE, 18)

   

    def on_key_press(self, key, modifiers):

       
        
        if key == (arcade.key.ESCAPE):
            arcade.close_window()
            quit()

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_Sprite.change_y = self.player_Jump_Speed
                print(self.player_Jump_Speed)

        elif (key == arcade.key.LEFT or key == arcade.key.A):
            self.player_Sprite.change_x = -self.player_Speed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_Sprite.change_x = self.player_Speed

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_Sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_Sprite.change_x = 0

    def on_update(self, delta_time):

        higherJump = False

        coin_Hit_List = arcade.check_for_collision_with_list(self.player_Sprite, self.scene.get_sprite_list("Coins"))

        for coin_Hit in coin_Hit_List:
            coin_Hit.remove_from_sprite_lists()
            self.score += 1

        end_Hit = arcade.check_for_collision_with_list(self.player_Sprite, self.scene.get_sprite_list("End"))

        for end_Has_Hit in end_Hit:
            Coins_Left = self.scene.get_sprite_list("Coins")

            if len(Coins_Left) == 0:
                arcade.close_window()
                quit()

        
                
        jumpPad_Hit = arcade.check_for_collision_with_list(self.player_Sprite, self.scene.get_sprite_list("JumpPads"))
        
        for jumpPad_Is_Hit in jumpPad_Hit:
            higherJump = True

        if higherJump:
            self.player_Jump_Speed = 15
        else:
            self.player_Jump_Speed = 10

        self.physics_engine.update()

        #self.player_Jump_Speed = 10
            
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
        and the colour is the texture data"""
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
