#!/usr/bin/env python

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import re

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

def sanitize_text(text):
    # Remove leading/trailing whitespace and escape potentially harmful characters
    sanitized = text.strip()  # Trim whitespace from both ends
    sanitized = re.sub(r'[<>]', '', sanitized)  # Remove any unwanted characters (e.g., <, >)
    return sanitized

# Function to save the recipe in markdown format
def save_recipe(recipe_name, category, ingredients, instructions, parent_window):
    recipe_name = recipe_name.strip()

    # Check if the recipe name is empty
    if not recipe_name:
        messagebox.showerror("Input Error", "Recipe name cannot be empty.", parent=parent_window)
        return False # Stop if the name is invalid

    # Sanitize ingredients and instructions
    sanitized_ingredients = sanitize_text(ingredients)
    sanitized_instructions = sanitize_text(instructions)

    # Validate that ingredients and instructions are not empty
    if not sanitized_ingredients:
        messagebox.showerror("Input Error", "Ingredients cannot be empty.", parent=parent_window)
        return False # Stop if ingredients are empty

    if not sanitized_instructions:
        messagebox.showerror("Input Error", "Instructions cannot be empty.", parent=parent_window)
        return False # Stop if instructions are empty

    # Create a valid filename and path for the recipe
    filename = recipe_name.lower().replace(" ", "_") + ".md"
    file_path = os.path.join(RECIPES_DIR, filename)

    # Check if the file already exists
    if os.path.exists(file_path):
        # Ask the user if they want to overwrite the existing file
        overwrite = messagebox.askyesno(
            "Overwrite Confirmation",
            f"The recipe '{recipe_name}' already exists. Do you want to overwrite it?",
            parent=parent_window
        )
        if not overwrite:
            return False  # Stop if the user does not want to overwrite

    # Save the recipe to the file
    with open(file_path, 'w') as f:
        f.write(f"# {recipe_name}\n\n## {category}\n\n## Ingredients\n")
        f.write(sanitized_ingredients + "\n\n## Instructions\n")
        f.write(sanitized_instructions)

    return True

# Function to open the recipe entry screen
def open_recipe_entry(existing_file_path=None):
    entry_window = tk.Toplevel()
    entry_window.title("Recipe Entry")
    entry_window.configure(bg=bg_color)

    # Labels and Entry Fields
    tk.Label(entry_window, text="Recipe Name:", bg=bg_color).grid(row=0, column=0, padx=10, pady=10)
    recipe_name_entry = tk.Entry(entry_window, width=40)
    recipe_name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Category dropdown box
    # Category selection
    tk.Label(entry_window, text="Select Category:", bg=bg_color).grid(row=1, column=0, padx=10, pady=10)
    category_var = tk.StringVar()
    category_combobox = ttk.Combobox(entry_window, textvariable=category_var, state="readonly")
    category_combobox['values'] = categories
    category_combobox.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(entry_window, text="Ingredients:", bg=bg_color).grid(row=2, column=0, padx=10, pady=10)
    ingredients_text = tk.Text(entry_window, width=40, height=10)
    ingredients_text.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(entry_window, text="Instructions:", bg=bg_color).grid(row=3, column=0, padx=10, pady=10)
    instructions_text = tk.Text(entry_window, width=40, height=10)
    instructions_text.grid(row=3, column=1, padx=10, pady=10)

    # Save button
    def save_and_exit():
        recipe_name = recipe_name_entry.get()
        category = category_combobox.get()
        ingredients = ingredients_text.get("1.0", tk.END).strip()
        instructions = instructions_text.get("1.0", tk.END).strip()

        if save_recipe(recipe_name, category, ingredients, instructions, entry_window):
            entry_window.after(200, entry_window.destroy)  # Close the entry window

    save_button = tk.Button(entry_window, text="Save Recipe", bg=bt_color, command=save_and_exit)
    save_button.grid(row=4, column=1, padx=10, pady=10)

    # Cancel button
    cancel_button = tk.Button(entry_window, text="Cancel", bg=bt_color, command=entry_window.destroy)
    cancel_button.grid(row=4, column=0, padx=10, pady=10)

    # If an existing file is passed, load its contents
    if existing_file_path:
        with open(existing_file_path, 'r') as f:
            lines = f.readlines()
            recipe_name_entry.insert(0, lines[0][2:].strip())  # Recipe Name
            category_var.set(lines[2].strip()[2:])
            ingredients = []
            instructions = []
            is_ingredients = False
            for line in lines[4:]:
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
