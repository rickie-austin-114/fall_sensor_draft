import tkinter as tk

def execute_function():
    arg1 = str(entry1.get())
    arg2 = str(entry2.get())

    print(len(arg1))
    print(len(arg2))
    
    print(f"Executing function with arguments: {arg1} and {arg2}")
    # Call your function here with arg1 and arg2 as arguments

# Create the main application window
root = tk.Tk()
root.title("Function Executor")

# Create input fields

label1 = tk.Label(root, text="wifi")
label1.pack()
entry1 = tk.Entry(root)
entry1.pack()

label2 = tk.Label(root, text="password")
label2.pack()
entry2 = tk.Entry(root)
entry2.pack()

label3 = tk.Label(root, text="devui")
label3.pack()
entry3 = tk.Entry(root)
entry3.pack()

# Create a button to execute the function
execute_button = tk.Button(root, text="Execute Function", command=execute_function)
execute_button.pack()

# Start the main event loop
root.mainloop()