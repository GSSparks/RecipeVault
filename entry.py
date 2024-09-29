#!/usr/bin/env python

import tkinter as tk
from tkinter import messagebox
import os

# Function to save recipe to a markdown file in the same folder as the executable
def save_recipe():
    recipe_name = name_entry.get().strip()
    ingredients = ingredients_text.get("1.0", tk.END).strip()
    instructions = instructions_text.get("1.0", tk.END).strip()

    if not recipe_name or not ingredients or not instructions:
        messagebox.showwarning("Input Error", "All fields must be filled out.")
        return

    # Format the recipe name for the filename (lowercase, replace spaces with underscores)
    formatted_name = recipe_name.lower().replace(" ", "_")
    file_name = f"{formatted_name}.md"

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    # Create the markdown content
    markdown_content = f"# {recipe_name}\n\n## Ingredients:\n{ingredients}\n\n## Instructions:\n{instructions}\n"

    try:
        with open(file_path, 'w') as file:
            file.write(markdown_content)
        messagebox.showinfo("Success", f"Recipe saved successfully as {file_name}")
    except Exception as e:
        messagebox.showerror("File Error", f"An error occurred while saving the recipe: {e}")

# Set up the tkinter window
root = tk.Tk()
root.title("RecipeVault - Recipe Entry")

# Recipe Name Entry
tk.Label(root, text="Recipe Name:").grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(root, width=40)
name_entry.grid(row=0, column=1, padx=10, pady=10)

# Ingredients Entry
tk.Label(root, text="Ingredients:").grid(row=1, column=0, padx=10, pady=10)
ingredients_text = tk.Text(root, height=10, width=40)
ingredients_text.grid(row=1, column=1, padx=10, pady=10)

# Preparation Instructions Entry
tk.Label(root, text="Instructions:").grid(row=2, column=0, padx=10, pady=10)
instructions_text = tk.Text(root, height=10, width=40)
instructions_text.grid(row=2, column=1, padx=10, pady=10)

# Save Button
save_button = tk.Button(root, text="Save Recipe", command=save_recipe)
save_button.grid(row=3, column=1, padx=10, pady=10, sticky="e")

# Run the tkinter loop
root.mainloop()
