import tkinter as tk
from PIL import Image, ImageTk
from movie import MovieApp  # Import the MovieApp class from movie.py

class AccountPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='black')

        # Set background image for the account page
        account_background_image = tk.PhotoImage(file="images/Account page.png")  # Replace with your background image path
        account_background_label = tk.Label(self, image=account_background_image)
        account_background_label.place(relwidth=1, relheight=1)  # Cover the entire window

        # Keep reference to the background image to prevent garbage collection
        self.image_ref = account_background_image

        # Example profile button
        profile_image = Image.open("images/profile.png")  # Replace with your profile image path
        
        # Convert transparent pixels to black
        profile_image = profile_image.convert("RGBA")  # Convert to RGBA to manage transparency
        data = profile_image.getdata()

        new_data = []
        for item in data:
            # If the pixel is transparent (alpha value 0), change it to black (0, 0, 0)
            if item[3] == 0:
                new_data.append((0, 0, 0, 255))  # Set to black with full opacity
            else:
                new_data.append(item)

        profile_image.putdata(new_data)  # Update the image with the new data

        # Resize image if needed
        profile_image = profile_image.resize((140, 149))  # Resize to desired size
        profile_image = ImageTk.PhotoImage(profile_image)  # Convert to Tkinter-compatible format

        # Create the profile button
        profile_button = tk.Button(self, image=profile_image, command=self.select_profile, relief="flat", borderwidth=0, highlightthickness=0)
        profile_button.place(relx=0.4, rely=0.5, anchor="center")  # Adjust the position as needed

        # Keep reference to the profile image to prevent garbage collection
        self.profile_image_ref = profile_image

    def select_profile(self):
        print("Profile Selected!")
        # Open the MovieApp window
        self.master.withdraw()  # Hide the current window
        movie_window = tk.Toplevel(self.master)  # Create a new window
        movie_app = MovieApp(movie_window)  # Initialize MovieApp in the new window

# Main application setup
if __name__ == "__main__":
    root = tk.Tk()
    root.title("PrimeFlix - Accounts")
    root.geometry("800x600")
    app = AccountPage(root)
    app.pack(fill="both", expand=True)
    root.mainloop()