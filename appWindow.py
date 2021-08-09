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
from kivymd.uix.list import TwoLineAvatarIconListItem, OneLineAvatarIconListItem, MDList
from kivy.clock import Clock
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.checkbox import CheckBox
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.button import Button
from kivymd.uix.menu import MDDropdownMenu
import requests
from kivy.uix.image import AsyncImage

Window.clearcolor = (0.98, 0.98, 0.98, 1)

#------------------------------logic---------------------------------
import json
import random

#initialize dictionary 
rand_recipe_count = "none"
recipe_book = {}
ingredients_chosen ={}


#------------------------------kivy---------------------------------

class Grocerys(MDApp):# inherets from App
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "DeepPurple"


    def build(self): #this is the main interface of the app
        return Builder.load_file("grocery.kv") #what is inside the window?

class WindowManager(ScreenManager):
    GenerateList = ObjectProperty(None)

class ViewRecipe(Screen):
    pass
class GenerateList(Screen):
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
            #add new page
            screen = NewPage(name= key)
            App.get_running_app().root.add_widget(screen)  
            self.ids.container.add_widget(self.list_item)
    
    def pressed(self, screen_name):
        App.get_running_app().root.current = screen_name.text
        App.get_running_app().root.transition.direction = "left"
    
class ListSelection(Screen):
    pass
class RecipeList(Screen):
    pass
class ChosenRecipe(Screen):
    pass
class RandomRecipe(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.on_enter)

    def on_enter(self, *args):
        menu = None
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "height": 56,
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_item(x),
            }
            for i in range(1,8)
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.dropdown_item,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        self.menu.bind()
    def set_item(self, text_item):
        global rand_recipe_count
        self.ids.dropdown_item.set_item(text_item)
        rand_recipe_count = text_item
        self.menu.dismiss()
        return rand_recipe_count


class FinalListRand(Screen):
    def on_enter(self, *args):
        #load ingredient list
        with open("grocery_store.json") as f:
            recipe_book = json.load(f)

        rand_list = {}
        ingredients_chosen = {}
        if rand_recipe_count != 'none':
            for x in range (0, int(rand_recipe_count)):
                rand_list[x] = random.choice(list(recipe_book.keys()))
                for name,ing in recipe_book.items():
                    for key in ing:
                        if (name == rand_list[x]):
                            ingredients_chosen[key] = ing[key]
        print(rand_list)
        print("tttttttttttttttttttttttttttttttttttt")        
        print(ingredients_chosen)
        layout = FloatLayout()
        self.add_widget(layout)
        #add ingredients list
        listLayout = GridLayout(cols=2, padding = 40, row_force_default=True, row_default_height = 45)
        for key in ingredients_chosen:
            listLayout.add_widget(MDLabel(text = key))
            checkbox = MDCheckbox(on_active = self.checkbox_clicked)
            listLayout.add_widget(checkbox)
        layout.add_widget(listLayout)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.on_enter)  

    def checkbox_clicked (self, *args): #value holds the state of the checkbox
        print ("test")
        

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
        
        #load ingredient list
        with open("grocery_store.json") as f:
            recipe_book = json.load(f)
        ingredients_chosen = {}
        for name,ing in recipe_book.items():
            for key in ing:
                if (name == self.name):
                    ingredients_chosen[key] = ing[key] 
        
        #add ingredients list
        listLayout = GridLayout(cols=2, padding = 40, row_force_default=True, row_default_height = 45) 
        for key in ingredients_chosen: 
            listLayout.add_widget(MDLabel(text = key))
            checkbox = MDCheckbox(on_active = self.checkbox_clicked)
            listLayout.add_widget(checkbox)
        #add checkboxes 
        layout.add_widget(listLayout)
        #add back button
        button = MDRoundFlatButton(text='<',padding= "10dp",pos_hint= {"center_x": .2, "center_y": .95}, 
        font_style= "Subtitle1", text_color= (0,0,0), line_color= (1,1,1), line_width= 1)
        layout.add_widget(button)
        button.bind(on_release = self.switch_screen)
    def checkbox_clicked (self, *args): #value holds the state of the checkbox
        print ("test")

    def switch_screen(self, *args):
        App.get_running_app().root.current = "GenerateList"
        App.get_running_app().root.transition.direction = "right"

def load_all(layout,self):
    #first item in row
    response1 = requests.get('https://api.spoonacular.com/recipes/random?number=1&apiKey=635fd284d78141c4b057f2faf20b02a3')
    #for x in range(0, len(response1.json()['recipes'][0]['extendedIngredients'])):
        #print(response1.json()['recipes'][0]['extendedIngredients'][x]['original'])
    layout.add_widget(AsyncImage(source = response1.json()['recipes'][0]['image']))
    #second item in row
    response2 = requests.get('https://api.spoonacular.com/recipes/random?number=1&apiKey=635fd284d78141c4b057f2faf20b02a3')
    #for x in range(0, len(response1.json()['recipes'][0]['extendedIngredients'])):
        #print(response1.json()['recipes'][0]['extendedIngredients'][x]['original'])
    layout.add_widget(AsyncImage(source = response2.json()['recipes'][0]['image']))
    #first item name
    recipeName1 = MDLabel(font_style= "Subtitle2"
        ,text = response1.json()['recipes'][0]['title']
        ,halign = "center")
    layout.add_widget(recipeName1)
    #second item name
    recipeName2 = MDLabel(font_style= "Subtitle2"
        ,text = response2.json()['recipes'][0]['title']
        ,halign = "center")
    layout.add_widget(recipeName2)

class Explore(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        layout = GridLayout(cols = 2, rows = 6, padding = [0,60,0,20])
        self.add_widget(layout)
        #for x in range (0,3):
            #load_all(layout, self)      


if __name__ == "__main__":
    Grocerys().run() # the .run method is inhereted from the App class into MyApp