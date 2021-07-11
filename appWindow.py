import kivy
from kivy.app import App #this is the main app class that builds the window and handles the graphics
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.toolbar import MDToolbar
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
from kivymd.uix.list import IconRightWidget, TwoLineAvatarIconListItem, OneLineAvatarIconListItem, MDList
from kivy.clock import Clock
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.label import MDLabel

Window.clearcolor = (0.98, 0.98, 0.98, 1)

#------------------------------logic---------------------------------
import json
import random

#initialize dictionary 
mode_code = "none"
recipe_book = {}


#------------------------------kivy---------------------------------

class Grocerys(MDApp):# inherets from App
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "DeepPurple"


    def build(self): #this is the main interface of the app
        return Builder.load_file("grocery.kv") #what is inside the window?

class WindowManager(ScreenManager):
    ViewRecipe = ObjectProperty(None)

class ViewRecipe(Screen):
    pass

class RecipeList(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.generate_list)

    def generate_list(self, *args):
        with open("grocery_store.json") as f:
            recipe_book = json.load(f)
        for key in recipe_book.keys():
            self.list_item = TwoLineAvatarIconListItem(text=f"{key}",
            secondary_text= str(len(recipe_book[key])) + ' ingredients', 
            on_release = lambda x=key: self.pressed(x))
            #self.list_item = IconRightWidget('plus')   
            #add new page
            screen = NewPage(name= key)
            App.get_running_app().root.add_widget(screen)  
            self.ids.container.add_widget(self.list_item)
    
    def pressed(self, screen_name):
        App.get_running_app().root.current = screen_name.text
        App.get_running_app().root.transition.direction = "left"

class AddRecipe(Screen):
    recipename = ObjectProperty(None)
    ingredients = ObjectProperty(None)

    def add_recipe(self):
        ingredient = "none"
        recipe_name = self.recipename.text
        ingredient_list = self.ingredients.text
        ingredients = ingredient_list.splitlines()
        #load json file
        with open("grocery_store.json") as f:
            recipe_book = json.load(f)
        recipe_book [recipe_name] = {}
        for ingredient in ingredients:
            unit = 0
            recipe_book [recipe_name][ingredient] = unit
            if ingredient == " ":
                del recipe_book [recipe_name][ingredient]
        #update the json file new entry

        with open("grocery_store.json", "w") as write_file:
            json.dump(recipe_book, write_file, indent=2)
        
class NewPage(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        layout = FloatLayout()
        self.add_widget(layout)
        #add label
        recipeName = MDLabel(font_style= "Subtitle2"
            ,text =  self.name
            ,halign = "center"
            ,pos_hint = {"center_y": .95})
        layout.add_widget(recipeName)
        #add back button
        button = MDRoundFlatButton(text='<',padding= "10dp",pos_hint= {"center_x": .2, "center_y": .95}, 
        font_style= "Subtitle1", text_color= (0,0,0), line_color= (1,1,1), line_width= 1)
        layout.add_widget(button)
        button.bind(on_release = self.switch_screen)
        #add ingredient list
        with open("grocery_store.json") as f:
            recipe_book = json.load(f)
        ingredients_chosen = {}
        for name,ing in recipe_book.items():
            for key in ing:
                if (name == self.name):
                    ingredients_chosen[key] = ing[key] 
        #add ingredients list
        boxLayout = BoxLayout(orientation = 'vertical', size_hint_y= 0.93) 
        sv = ScrollView()
        ml = MDList()
        sv.add_widget(ml)
        for key in ingredients_chosen: 
            ml.add_widget(OneLineAvatarIconListItem(text = key))
        boxLayout.add_widget(sv)
        layout.add_widget(boxLayout)

    def switch_screen(self, *args):
        App.get_running_app().root.current = "RecipeList"
        App.get_running_app().root.transition.direction = "right"

if __name__ == "__main__":
    Grocerys().run() # the .run method is inhereted from the App class into MyApp