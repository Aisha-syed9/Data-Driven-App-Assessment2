import tkinter as tk
from accounts import AccountPage  # Import the AccountPage class from accounts.py

# Create the main Tkinter window
root = tk.Tk()
root.title("PrimeFlix - Home")
root.geometry("800x600")  # Adjust size as needed

# Function to go to the account page
def go_to_account_page():
    # Create the account page and switch to it
    account_page = AccountPage(root)
    account_page.pack(fill="both", expand=True)  # Make sure this is packed
    # Hide the home page content when switching to account page
    home_page.pack_forget()

# Frame for the home page content
home_page = tk.Frame(root, bg='black')
home_page.pack(fill="both", expand=True)

# Set background image for the home page
background_image = tk.PhotoImage(file="images\Start page.png")  #image file path
background_label = tk.Label(home_page, image=background_image)
background_label.place(relwidth=1, relheight=1)  # Cover the entire window

# Keep reference to the image to prevent it from being garbage collected
home_page.image_ref = background_image

# Start button to go to the account page
start_button_image = tk.PhotoImage(file="images\start button.png")  #start button image path
start_button = tk.Button(home_page, image=start_button_image, command=go_to_account_page, relief="flat", borderwidth=0, highlightthickness=0, bd=0)
start_button.place(relx=0.5, rely=0.7, anchor="center")  # Position the button in the center

# Keep reference to the button image to prevent it from being garbage collected
home_page.button_ref = start_button_image

# Run the Tkinter main loop
root.mainloop()
