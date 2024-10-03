#!/usr/bin/env python

import tkinter as tk
import json
import os

# Function to read the configuration from the config file
def read_config():
    with open('config.json', 'r') as f:
        return json.load(f)

# Load the configuration
config = read_config()

# Set variables in the local scope
for key, value in config.items():
    locals()[key] = value if not isinstance(value, list) else tuple(value)  # Convert lists to tuples

# Ensure the recipes directory exists
RECIPES_DIR = os.path.abspath(recipe_directory)
os.makedirs(RECIPES_DIR, exist_ok=True)

# Function to save the recipe in markdown format
def save_recipe(recipe_name, ingredients, instructions):
    filename = recipe_name.lower().replace(" ", "_") + ".md"
    file_path = os.path.join(RECIPES_DIR, filename)

    with open(file_path, 'w') as f:
        f.write(f"# {recipe_name}\n\n## Ingredients\n")
        f.write(ingredients + "\n\n## Instructions\n")
        f.write(instructions)

# Function to open the recipe entry screen
def open_recipe_entry(existing_file_path=None):
    entry_window = tk.Toplevel()
    entry_window.title("Recipe Entry")
    entry_window.configure(bg=bg_color)

    # Labels and Entry Fields
    tk.Label(entry_window, text="Recipe Name:", bg=bg_color).grid(row=0, column=0, padx=10, pady=10)
    recipe_name_entry = tk.Entry(entry_window, width=40)
    recipe_name_entry.grid(row=0, column=1, padx=10, pady=10)

    #

    tk.Label(entry_window, text="Ingredients:", bg=bg_color).grid(row=1, column=0, padx=10, pady=10)
    ingredients_text = tk.Text(entry_window, width=40, height=10)
    ingredients_text.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(entry_window, text="Instructions:", bg=bg_color).grid(row=2, column=0, padx=10, pady=10)
    instructions_text = tk.Text(entry_window, width=40, height=10)
    instructions_text.grid(row=2, column=1, padx=10, pady=10)

    # Save button
    def save_and_exit():
        recipe_name = recipe_name_entry.get()
        ingredients = ingredients_text.get("1.0", tk.END).strip()
        instructions = instructions_text.get("1.0", tk.END).strip()

        save_recipe(recipe_name, ingredients, instructions)
        entry_window.destroy()  # Close the entry window

    save_button = tk.Button(entry_window, text="Save Recipe", bg=bt_color, command=save_and_exit)
    save_button.grid(row=3, column=1, padx=10, pady=10)

    # Cancel button
    cancel_button = tk.Button(entry_window, text="Cancel", bg=bt_color, command=entry_window.destroy)
    cancel_button.grid(row=3, column=0, padx=10, pady=10)

    # If an existing file is passed, load its contents
    if existing_file_path:
        with open(existing_file_path, 'r') as f:
            lines = f.readlines()
            recipe_name_entry.insert(0, lines[0][2:].strip())  # Recipe Name
            ingredients = []
            instructions = []
            is_ingredients = False
            for line in lines[2:]:
                if line.startswith("## Ingredients"):
                    is_ingredients = False
                    continue
                if is_ingredients:
                    instructions.append(line.strip())
                else:
                    if line.startswith("## Instructions"):
                        is_ingredients = True
                        continue
                    ingredients.append(line.strip())

            ingredients_text.insert(tk.END, "\n".join(ingredients))
            instructions_text.insert(tk.END, "\n".join(instructions))

    entry_window.mainloop()
