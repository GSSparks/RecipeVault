#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
import os
import entry  # Import the entry module
from tkinter import messagebox  # Import messagebox for confirmation dialogs

# Function to read the configuration from the config file
def read_config():
    config = {}
    with open('config.txt', 'r') as f:
        for line in f:
            key, value = line.strip().split(' = ')
            config[key] = value.strip('"')  # Remove quotes if any
    return config

# Load the configuration
config = read_config()
RECIPES_DIR = os.path.abspath(config.get('recipe_directory', './recipes'))

# Ensure the recipes directory exists
os.makedirs(RECIPES_DIR, exist_ok=True)

# Function to refresh the recipe list in the text box based on the selected category
def refresh_recipes(recipe_listbox, recipe_map, category_var):
    recipe_listbox.delete(0, tk.END)  # Clear the listbox
    recipe_map.clear()  # Clear the previous mapping

    # Get the selected category
    selected_category = category_var.get()
    category_filter = selected_category if selected_category != "All" else None

    # Find all .md files in the recipes directory
    for file in os.listdir(RECIPES_DIR):
        if file.endswith('.md'):
            file_path = os.path.join(RECIPES_DIR, file)
            with open(file_path, 'r') as f:
                title = f.readline().strip()[2:]  # Read the first line and remove the "# " prefix
                category = f.readline().strip()[2:]  # Read the second line for the category

                # Filter recipes by category if selected
                if category_filter is None or category == category_filter:
                    recipe_listbox.insert(tk.END, title)  # Add title to the listbox
                    recipe_map[title] = file  # Map title to filename

# Function to open a selected recipe
def open_selected_recipe(recipe_listbox, recipe_map):
    selected = recipe_listbox.curselection()
    if selected:
        title = recipe_listbox.get(selected[0])  # Get the title
        filename = recipe_map.get(title)  # Get the corresponding filename
        if filename:
            entry.open_recipe_entry(os.path.join(RECIPES_DIR, filename))  # Open the recipe using the entry module

# Function to open the recipe entry screen to add a new recipe
def add_new_recipe():
    entry.open_recipe_entry()

# Function to delete a selected recipe
def delete_selected_recipe(recipe_listbox, recipe_map):
    selected = recipe_listbox.curselection()
    if selected:
        title = recipe_listbox.get(selected[0])  # Get the title
        filename = recipe_map.get(title)  # Get the corresponding filename
        if filename:
            file_path = os.path.join(RECIPES_DIR, filename)

            # Confirm deletion
            if messagebox.askyesno("Delete Recipe", f"Are you sure you want to delete '{title}'?"):
                os.remove(file_path)  # Delete the file
                refresh_recipes(recipe_listbox, recipe_map)  # Refresh the list after deletion

# Main function for the GUI
def main_screen():
    root = tk.Tk()
    root.title("RecipeVault - Main Screen")

    # Recipe Listbox
    tk.Label(root, text="Available Recipes:").grid(row=0, column=0, padx=10, pady=10, columnspan=2)
    recipe_listbox = tk.Listbox(root, width=30, height=15)
    recipe_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Recipe map to store title to filename mapping
    recipe_map = {}

    # Drop-down for categories
    tk.Label(root, text="Select Category:").grid(row=0, column=3, padx=10, pady=10)
    category_var = tk.StringVar(value="All")  # Default value
    category_combobox = ttk.Combobox(root, textvariable=category_var, state="readonly")
    category_combobox['values'] = ["All", "Dessert", "Main Course", "Appetizer"]  # Update with your actual categories
    category_combobox.grid(row=0, column=4, padx=10, pady=10)
    category_combobox.bind("<<ComboboxSelected>>", lambda event: refresh_recipes(recipe_listbox, recipe_map, category_var))  # Refresh on selection change

    # Set button size
    button_width = 10

    # Buttons in a grid layout
    open_button = tk.Button(root, text="Open", command=lambda: open_selected_recipe(recipe_listbox, recipe_map), width=button_width)
    open_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    add_button = tk.Button(root, text="Add", command=add_new_recipe, width=button_width)
    add_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    # Delete button styled with red color
    delete_button = tk.Button(root, text="Delete", command=lambda: delete_selected_recipe(recipe_listbox, recipe_map), bg="red", fg="white", width=button_width)
    delete_button.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

    quit_button = tk.Button(root, text="Quit", command=root.destroy, width=button_width)
    quit_button.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

    # Refresh the listbox whenever the main window is focused
    root.bind("<FocusIn>", lambda event: refresh_recipes(recipe_listbox, recipe_map, category_var))

    # Initial population of the recipe listbox
    refresh_recipes(recipe_listbox, recipe_map, category_var)

    root.mainloop()

# Run the main screen
if __name__ == "__main__":
    main_screen()
