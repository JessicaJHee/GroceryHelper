import json

#initialize dictionary 
mode_code = "none"
recipe_book = {}

#function to add a recipe
def add_recipe():
    recipe_name = input ("Enter the name of the recipe: ")
    ingredient = "none"
    recipe_book [recipe_name] = {}
    while (ingredient != " "):
        ingredient = input ("Enter the ingredient: ")
        unit = input ("Enter the unit: ")   
        recipe_book [recipe_name][ingredient] = unit
        if ingredient == " ":
            del recipe_book [recipe_name][ingredient]

#main application while loop
while (mode_code != "5"):
    #prompt for user input for menu selection
    mode_code = input ("What would you like to do? \n   1. Add Recipe\n   2. Print all avaliable recipes\n   3. Get list \n   4. Store/load data\n   5. Quit\n")

    #convert user input to reable application states
    if mode_code == "1": mode = "add_recipe"
    elif mode_code == "2": mode = "print_recipe"
    elif mode_code == "3": mode = "get_list"
    elif mode_code == "4": mode ="get_data"
    elif mode_code == "5": mode = "quit"
    else: mode = "none"

    #to add recipe
    if mode == "add_recipe":
        add_recipe()
    #to print all avaliable recipes
    elif mode == "print_recipe":
        for key in recipe_book.keys():
            print (key,"\n")
    #to receive the actual grocery list
    elif mode == "get_list":
        num_recipies = input ("How many meals would you like? ")
    #to interact with the json data file that holds the recipes
    elif mode == "get_data":
        option = input ("Press 1 to store, 2 to load:\n")
        if option == "1":
            with open("grocery_store.json", "w") as write_file:
                json.dump(recipe_book, write_file, indent=2)
        elif option =="2":
            with open("grocery_store.json") as f:
                recipe_book= json.load(f)
    #exit application
    elif mode == "quit":
        print("Bye!")