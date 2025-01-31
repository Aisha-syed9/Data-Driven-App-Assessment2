import tkinter as tk
from tkinter import Entry, Button, Label, Canvas, Scrollbar, Frame
import requests
from PIL import Image, ImageTk
from io import BytesIO

# API Key and URL for TMDb API
API_KEY = "1156b06dade228ec3859bdaa8ba3b146"
BASE_URL = "https://api.themoviedb.org/3/search/movie"

class MovieApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PrimeFlix - Movie Search")
        self.master.geometry("900x600")
        self.master.configure(bg="black")

        # ----------- HEADER (NAVIGATION BAR) ----------- 
        nav_bar = Frame(self.master, bg="black", height=50)
        nav_bar.pack(fill="x")

        # App Name
        Label(nav_bar, text="PrimeFlix", fg="white", bg="black", font=("Arial", 14, "bold")).pack(side="left", padx=10)

        # Navigation Buttons
        Button(nav_bar, text="Home", bg="darkgray", fg="Black", font=("Arial", 12, "bold"), relief="flat").pack(side="left", padx=5)

        # Search Entry Box inside a Frame for better padding control
        search_frame = Frame(nav_bar, bg="black")
        search_frame.pack(side="left", padx=10)

        self.search_entry = Entry(search_frame, font=("Arial", 12), width=40)
        self.search_entry.pack(side="left", padx=30)   # Adds padding for the entry box

        # Load Search Button Image
        search_img = Image.open("images/search.png")  
        search_img = search_img.resize((25, 25))
        self.search_icon = ImageTk.PhotoImage(search_img)

        # Search Button (Image)
        search_button = Button(nav_bar, image=self.search_icon, command=self.search_movie, relief="flat", bg="black", borderwidth=0)
        search_button.pack(side="left", padx=1)

        # Load User Profile Image
        user_img = Image.open("images/profile.png")  
        user_img = user_img.resize((40, 40))
        self.user_icon = ImageTk.PhotoImage(user_img)

        # User Profile Button (Image)
        user_profile = Label(nav_bar, image=self.user_icon, bg="black")
        user_profile.pack(side="right", padx=10)

        # ----------- MOVIE DISPLAY SECTION ----------- 
        self.movie_frame = Frame(self.master, bg="black")
        self.movie_frame.pack(fill="both", expand=True)

        # Movie Rating Label (Re-added)
        self.movie_rating_label = Label(self.movie_frame, text="Rating: N/A", fg="white", bg="black", font=("Arial", 12))
        self.movie_rating_label.pack()

        # Movie Poster Canvas (Gray Box)
        self.canvas = Canvas(self.movie_frame, bg="Black", width=300, height=400)
        self.canvas.pack()

        # Horizontal Scroll Bar (if needed)
        self.scroll_bar = Scrollbar(self.movie_frame, orient="horizontal", command=self.canvas.xview)
        self.scroll_bar.pack(side="bottom", fill="x")
        self.canvas.configure(xscrollcommand=self.scroll_bar.set)

        # Movie Poster Display
        self.image_label = Label(self.canvas, bg="black")
        self.canvas.create_window((150, 200), window=self.image_label)

        # Movie Title and Description
        self.movie_title_label = Label(self.movie_frame, text="MOVIE TITLE", fg="white", bg="black", font=("Times New Roman", 20, "bold"))
        self.movie_title_label.pack()

        self.movie_desc_label = Label(self.movie_frame, text="Movie description", fg="white", bg="black", font=("Times New Roman", 14), wraplength=800)
        self.movie_desc_label.pack()

        # ----------- MOVIE NAVIGATION BUTTONS ----------- 
        self.current_movie_index = 0  # Keeps track of the currently displayed movie
        self.movies_data = []  # Stores movie results

        # Left Navigation Arrow
        self.arrow_left = Label(self.master, text="◀", fg="white", bg="black", font=("Arial", 18), cursor="hand2")
        self.arrow_left.place(x=20, y=300)
        self.arrow_left.bind("<Button-1>", lambda event: self.move_backward())

        # Right Navigation Arrow
        self.arrow_right = Label(self.master, text="▶", fg="white", bg="black", font=("Arial", 18), cursor="hand2")
        self.arrow_right.place(x=860, y=300)
        self.arrow_right.bind("<Button-1>", lambda event: self.move_forward())

    def search_movie(self):
        """Fetch movie data from TMDb API based on the user's search query."""
        movie_title = self.search_entry.get()
        if movie_title:
            self.fetch_movie_data(movie_title)

    def fetch_movie_data(self, title):
        """Fetch movie data from TMDb API."""
        response = requests.get(BASE_URL, params={"api_key": API_KEY, "query": title})
        
        if response.status_code == 200:
            data = response.json()
            self.movies_data = data.get("results", [])
            if self.movies_data:
                self.current_movie_index = 0
                self.display_movie(self.movies_data[self.current_movie_index])
            else:
                self.movie_title_label.config(text="No movies found.")
                self.movie_desc_label.config(text="")
                self.canvas.delete("all")
        else:
            self.movie_title_label.config(text="Error fetching data.")
            self.movie_desc_label.config(text="")
            self.canvas.delete("all")

    def display_movie(self, movie):
        """Display the selected movie's title, description, rating, and poster."""
        self.movie_title_label.config(text=movie.get("title", "Unknown Title"))
        self.movie_desc_label.config(text=movie.get("overview", "No description available."))
        
        # Display movie rating
        rating = movie.get("vote_average")
        if rating:
            self.movie_rating_label.config(text=f"Rating: {rating}/10")
        else:
            self.movie_rating_label.config(text="Rating: N/A")
        
        # Fetch poster image from TMDb
        poster_path = movie.get("poster_path")
        if poster_path:
            image_url = f"https://image.tmdb.org/t/p/w300{poster_path}"
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                img_data = Image.open(BytesIO(image_response.content))
                img_resized = img_data.resize((300, 400))
                img_tk = ImageTk.PhotoImage(img_resized)
                self.image_label.config(image=img_tk)
                self.image_label.image = img_tk
            else:
                self.image_label.config(image="")
        else:
            self.image_label.config(image="")

    def move_backward(self):
        """Move to the previous movie in the list."""
        if self.current_movie_index > 0:
            self.current_movie_index -= 1
            self.display_movie(self.movies_data[self.current_movie_index])

    def move_forward(self):
        """Move to the next movie in the list."""
        if self.current_movie_index < len(self.movies_data) - 1:
            self.current_movie_index += 1
            self.display_movie(self.movies_data[self.current_movie_index])
