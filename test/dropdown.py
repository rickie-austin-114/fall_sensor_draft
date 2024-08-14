import tkinter as tk

selected_option = ""

value = 5

def on_selection_change(*args):
    selected_option = var.get()
    print(f"Selected option: {selected_option}")
    # options.append(f"Option {value}")
    # value += 1
    # Perform actions based on the selected option

def print_value():
    print(selected_option)

# List of options
options = ['Option 1', 'Option 2', 'Option 3', 'Option 4']

# Create the main application window
root = tk.Tk()
root.title("Dropdown List Example")

# Create a variable to store the selected option
var = tk.StringVar(root)
var.set(options[0])  # Set the default selected option

# Create the dropdown list
option_menu = tk.OptionMenu(root, var, *options, command=on_selection_change)
option_menu.pack()

button = tk.Button(root, text="print value", command=print_value)
button.pack()


# Start the main event loop
root.mainloop()