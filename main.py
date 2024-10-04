#!/usr/bin/env python

"""
Author:         Gary Sparks
Date written:   10/13/24
Assignment:     SDEV140 Final Project
Short Desc:     This is a recipe storage, organize, and retrieve program.
                It is writen in Python using the Tkinter toolkit.
"""

import tkinter as tk
from tkinter import filedialog, ttk
import os
import json
import entry  # Import the entry module
from tkinter import messagebox  # Import messagebox for confirmation dialogs

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
                nothing = f.readline()  # FIXME Hacky way to skip a line :/
                category = f.readline().strip()[3:]  # Read the third line for the category

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
def delete_selected_recipe(recipe_listbox, recipe_map, category_var):
    selected = recipe_listbox.curselection()
    if selected:
        title = recipe_listbox.get(selected[0])  # Get the title
        filename = recipe_map.get(title)  # Get the corresponding filename
        if filename:
            file_path = os.path.join(RECIPES_DIR, filename)

            # Confirm deletion
            if messagebox.askyesno("Delete Recipe", f"Are you sure you want to delete '{title}'?"):
                os.remove(file_path)  # Delete the file
                refresh_recipes(recipe_listbox, recipe_map, category_var)  # Refresh the list after deletion

# Function to display the recipe preview
def display_recipe_preview(recipe_listbox, recipe_map, preview_text):
    selected = recipe_listbox.curselection()
    if selected:
        title = recipe_listbox.get(selected[0])  # Get the selected title
        filename = recipe_map.get(title)  # Get the corresponding filename
        if filename:
            file_path = os.path.join(RECIPES_DIR, filename)
            with open(file_path, 'r') as f:
                content = f.readlines()  # Read the entire file content line by line
                preview_text.delete(1.0, tk.END)  # Clear previous content

                # Initialize tags for formatting
                preview_text.tag_configure("title", font=("Helvetica", 16, "bold"))
                preview_text.tag_configure("subtitle", font=("Helvetica", 14, "bold"))
                preview_text.tag_configure("normal", font=font)

                for line in content:
                    line = line.strip()
                    if line.startswith("# "):  # Title
                        preview_text.insert(tk.END, line[2:] + "\n", "title")  # Skip the "# "
                    elif line.startswith("## "):  # Subtitle
                        preview_text.insert(tk.END, line[3:] + "\n", "subtitle")  # Skip the "## "
                    else:
                        preview_text.insert(tk.END, line + "\n", "normal")  # Normal text

# Main function for the GUI
def main_screen():
    root = tk.Tk()
    root.title("RecipeVault")
    root.configure(bg=bg_color)
    root.resizable(False, False)

    # Recipe Listbox
    tk.Label(root, text="Available Recipes:", bg=bg_color, font=font).grid(row=0, column=0, columnspan=2, padx=10, sticky="w")
    recipe_listbox = tk.Listbox(root, justify='left', borderwidth=10, selectbackground='#f0f0f0' , bd=1, font=font, bg='#ffffff', fg="#333333")
    recipe_listbox.grid(row=1, column=0, columnspan=2, padx=10, sticky="nsew")

    # Recipe map to store title to filename mapping
    recipe_map = {}

    # Drop-down for categories
    category_frame = tk.Frame(root, bg=bg_color)
    category_frame.grid(row=0, column=3, columnspan=3, padx=10, pady=10)
    tk.Label(category_frame, text="Select Category:", bg=bg_color, font=font).grid(row=0, column=0, padx=5, sticky="nsew")
    category_var = tk.StringVar(value="All")  # Default value
    category_combobox = ttk.Combobox(category_frame, textvariable=category_var, state="readonly")
    category_combobox['values'] = categories
    category_combobox.grid(row=0, column=1, columnspan=2)
    category_combobox.bind("<<ComboboxSelected>>", lambda event: refresh_recipes(recipe_listbox, recipe_map, category_var))  # Refresh on selection change

    # Create a frame for the buttons
    button_frame = tk.Frame(root, bg=bg_color)
    button_frame.grid(row=2, column=0, columnspan=5, pady=10)

    # Buttons in a grid layout
    open_button = tk.Button(button_frame, text="Open", command=lambda: open_selected_recipe(recipe_listbox, recipe_map), width=button_width, bg=bt_color, font=bt_font)
    open_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    add_button = tk.Button(button_frame, text="Add", command=add_new_recipe, width=button_width, bg=bt_color, font=bt_font)
    add_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    # Delete button styled with red color
    delete_button = tk.Button(button_frame, text="Delete", command=lambda: delete_selected_recipe(recipe_listbox, recipe_map, category_var), bg="red", fg="white", activebackground="darkred", activeforeground="white", width=button_width, font=bt_font)
    delete_button.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

    quit_button = tk.Button(button_frame, text="Quit", command=root.destroy, width=button_width, bg=bt_color, font=bt_font)
    quit_button.grid(row=2, column=4, padx=5, pady=5, sticky="ew")

    # Add logo
    logo_image = tk.PhotoImage(file="./images/vault.png", width=200, height=60)
    logo = tk.Label(button_frame, image=logo_image, bg=bg_color).grid(row=2, column=5)

    # Add a Text widget for previewing recipe content
    preview_text = tk.Text(root, wrap='word', width=50, height=15, padx=10, pady=10, bg=preview_color)
    preview_text.grid(row=1, column=2, columnspan=3, padx=10)

    # Bind double-click to display recipe preview
    recipe_listbox.bind("<Double-Button-1>", lambda event: display_recipe_preview(recipe_listbox, recipe_map, preview_text))

    # Refresh the listbox whenever the main window is focused
    root.bind("<FocusIn>", lambda event: refresh_recipes(recipe_listbox, recipe_map, category_var))

    # Initial population of the recipe listbox
    refresh_recipes(recipe_listbox, recipe_map, category_var)

    root.mainloop()

# Run the main screen
if __name__ == "__main__":
    main_screen()
