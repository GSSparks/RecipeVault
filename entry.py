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
    # Remove leading/trailing whitespace and remove potentially harmful characters
    rx = re.compile(r"[^a-zA-Z0-9,!.'\s]+")
    sanitized = rx.sub(' ', text).strip()
    return sanitized

# Function to save the recipe in markdown format
def save_recipe(recipe_name, category, ingredients, instructions, parent_window):
    recipe_name = recipe_name.strip()

    # Sanitize name, ingredients, and instructions
    sanitized_recipe_name = sanitize_text(recipe_name)
    sanitized_ingredients = sanitize_text(ingredients)
    sanitized_instructions = sanitize_text(instructions)

    # Validate that recipe_name, ingredients, and instructions are not empty
    if not sanitized_recipe_name:
        messagebox.showerror("Input Error", "Recipe name cannot be empty.", parent=parent_window)
        return False # Stop if the name is invalid

    if not sanitized_ingredients:
        messagebox.showerror("Input Error", "Ingredients cannot be empty.", parent=parent_window)
        return False # Stop if ingredients are empty

    if not sanitized_instructions:
        messagebox.showerror("Input Error", "Instructions cannot be empty.", parent=parent_window)
        return False # Stop if instructions are empty

    # Create a valid filename and path for the recipe
    filename = sanitized_recipe_name.lower().replace(" ", "_") + ".md"
    file_path = os.path.join(RECIPES_DIR, filename)

    # Check if the file already exists
    if os.path.exists(file_path):
        # Ask the user if they want to overwrite the existing file
        overwrite = messagebox.askyesno(
            "Overwrite Confirmation",
            f"The recipe '{sanitized_recipe_name}' already exists. Do you want to overwrite it?",
            parent=parent_window
        )
        if not overwrite:
            return False  # Stop if the user does not want to overwrite

    # Save the recipe to the file
    with open(file_path, 'w') as f:
        f.write(f"# {sanitized_recipe_name}\n\n## {category}\n\n## Ingredients\n")
        f.write(sanitized_ingredients + "\n\n## Instructions\n")
        f.write(sanitized_instructions)

    return True

# Function to open the recipe entry screen
def open_recipe_entry(existing_file_path=None):
    entry_window = tk.Toplevel()

    # Set the window title based on whether an existing file is being edited or a new recipe is being entered
    # And set the image and the alternative text to use for the window
    if existing_file_path:
        entry_window.title("Edit Recipe")
        image = "./images/recipe_edit.png"
        alt_text = "Edit Recipe"
    else:
        entry_window.title("New Recipe Entry")
        image = "./images/recipe_add.png"
        alt_text = "Add Recipe"

    entry_window.configure(bg=bg_color)
    entry_window.resizable(False, False)

    # Labels and Entry Fields
    recipe_name_frame = tk.LabelFrame(entry_window, text="Recipe Name:", bg=bg_color, font=font)
    recipe_name_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")
    recipe_name_entry = tk.Entry(recipe_name_frame, width=49, font=font_title)
    recipe_name_entry.grid(padx=10, pady=10)

    # Category dropdown box
    category_frame = tk.Frame(entry_window, bg=bg_color)
    category_frame.grid(row=3, column=0, sticky="e", padx=10)
    tk.Label(category_frame, text="Select Category:", bg=bg_color, font=font).grid(row=0, column=0, padx=10, pady=10)
    category_var = tk.StringVar(value="All")  # Set default value to All
    category_combobox = ttk.Combobox(category_frame, textvariable=category_var, font=font, state="readonly")
    category_combobox['values'] = categories
    category_combobox.grid(row=0, column=1)

    # Ingredients Frame
    ingredients_frame = tk.LabelFrame(entry_window, text="Ingredients", bg=bg_color, font=font)
    ingredients_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    ingredients_text = tk.Text(ingredients_frame, width=70, height=7, font=font, wrap="word", spacing1=5, spacing2=2, spacing3=5)
    ingredients_text.grid(padx=10, pady=20)

    # Instructions Frame
    instructions_frame = tk.LabelFrame(entry_window, bg=bg_color, text="Instructions", font=font)
    instructions_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    instructions_text = tk.Text(instructions_frame, width=70, height=7, font=font, wrap="word", spacing1=5, spacing2=2, spacing3=5)
    instructions_text.grid(padx=10, pady=20)

    # Button frame
    button_frame = tk.Frame(entry_window, bg=bg_color)
    button_frame.grid(row=4, column=0, sticky='nsw')

    # Add logo or alternative text
    try:
        logo_image = tk.PhotoImage(file=image, width=200, height=60)
        logo = tk.Label(button_frame, image=logo_image, bg=bg_color).grid(row=0, column=0)
    except tk.TclError:
        log = tk.Label(button_frame, text=alt_text, bg=bg_color, font=font_title, padx=30).grid(row=0, column=0)

    # Save button
    def save_and_exit():
        recipe_name = recipe_name_entry.get()
        category = category_combobox.get()
        ingredients = ingredients_text.get("1.0", tk.END).strip()
        instructions = instructions_text.get("1.0", tk.END).strip()

        if save_recipe(recipe_name, category, ingredients, instructions, entry_window):
            entry_window.after(200, entry_window.destroy)  # Close the entry window

    save_button = tk.Button(button_frame, text="Save Recipe", bg=bt_color, font=bt_font, height=button_height, width=button_width, command=save_and_exit)
    save_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")

    # Cancel button
    cancel_button = tk.Button(button_frame, text="Cancel", bg=bt_color, font=bt_font, height=button_height, width=button_width, command=entry_window.destroy)
    cancel_button.grid(row=0, column=3, padx=10, pady=5, sticky="e")

    # If an existing file is passed, load its contents
    if existing_file_path:
        with open(existing_file_path, 'r') as f:
            lines = f.readlines()
            recipe_name_entry.insert(0, lines[0][2:].strip())  # Recipe Name
            category_var.set(lines[2][2:].strip())
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
