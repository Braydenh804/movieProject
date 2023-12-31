from tkinter import *
import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO
from search_content import *
from double_linked_list import *
from stack import *
from merge_sort import *


class Screen(Frame):

    def __init__(self, master, name):
        Frame.__init__(self, master)
        # Attributes
        self.master = master
        self.name = name
        # Initialise with master
        self.master.add_screen(self)

    def show(self):
        """
        Method will show screen
        """
        self.master.show_screen(self.name)


class ScreenController(Frame):
    """
    Screen Controller
    will manage screens
    in the program
    """

    def __init__(self, parent):
        Frame.__init__(self, parent)
        # Configure
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Attributes
        self.allScreens = {}
        self.currentScreen = None

    def add_screen(self, screen_object):
        """
        Adds a Screen object to the screenController
        """
        # Place the screen
        screen_object.grid(row=0, column=0, sticky="nsew")
        # Add to dictionary
        self.allScreens[screen_object.name] = screen_object

    def show_screen(self, screen_name):
        if screen_name in self.allScreens:
            # Display
            self.allScreens[screen_name].tkraise()
            # Update variable
            self.currentScreen = screen_name


# Create a Tkinter Log In Window
start_window = Tk()
start_window.title("Entertainment Hub")
start_window.geometry(f'{1035}x{1080}+{-10}+{0}')
start_window.columnconfigure(0, weight=1)
start_window.rowconfigure(1, weight=1)
start_window.configure(bg='#333333')
# Create a Controller for the screens
screen_master = ScreenController(start_window)
screen_master.grid(row=1, column=0, sticky='n')

# Create a navigation bar
nav_bar = Frame(start_window)
nav_bar.grid(row=0, column=0)
nav_bar.config(bg="#333333")
search_movies_button = Button(nav_bar, text='Search For Movies', bg="#0c2b59", fg='#FFFFFF', font=("Arial", 16),
                              command=lambda: movie_search_page.show())
search_tv_button = Button(nav_bar, text='Search For TV Shows', bg="#0c2b59", fg='#FFFFFF', font=("Arial", 16),
                          command=lambda: tv_search_page.show())
movie_watchlist_button = Button(nav_bar, text='Movie Watchlist', bg="#0c2b59", fg='#FFFFFF',
                                font=("Arial", 16), command=lambda: (
    update_movie_watchlist(movie_watchlist_dict), movie_watchlist_page.show()))
tv_watchlist_button = Button(nav_bar, text='TV Show Watchlist', bg="#0c2b59", fg='#FFFFFF', font=("Arial", 16),
                             command=lambda: (update_tv_watchlist(tv_watchlist_dict), tv_watchlist_page.show()))
your_ratings_button = Button(nav_bar, text='Your Ratings', bg="#0c2b59", fg='#FFFFFF', font=("Arial", 16),
                             command=lambda: (update_button_img(), rate_content_page.show()))
sign_out_button = Button(nav_bar, text='Close App', bg="#0c2b59", fg='#FFFFFF', font=("Arial", 16), command=quit)

# Placing toolbar widget
search_movies_button.grid(row=0, column=0)
search_tv_button.grid(row=0, column=1)
movie_watchlist_button.grid(row=0, column=2)
tv_watchlist_button.grid(row=0, column=3)
your_ratings_button.grid(row=0, column=4)
sign_out_button.grid(row=0, column=5)

# Search For Movies Page
movie_search_page = Screen(screen_master, "Movie Search Page")
movie_search_page.config(bg="#333333")
header_label = Label(movie_search_page, text="Search For A Movie", bg='#333333', fg="#0c2b59", font=("Arial", 30))
search_label = Label(movie_search_page, text="Enter Movie Title", bg='#333333', fg="#FFFFFF", font=("Arial", 16))

search_button = Button(movie_search_page, text="Search", bg="#0c2b59", fg="#FFFFFF", font=("Arial", 16),
                       command=lambda: display_search(search_movie_file(search_entry.get(), 1), 1))
search_entry = Entry(movie_search_page, font=("Arial", 16))
filter_label = Label(movie_search_page, text="Filter For A Movie", bg='#333333', fg="#0c2b59", font=("Arial", 30))
year_label = Label(movie_search_page, text="Movie Release Year", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
year_entry = Entry(movie_search_page, font=("Arial", 16), width=4)
rating_label = Label(movie_search_page, text="Minium Rating (0-10)", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
rating_entry = Entry(movie_search_page, font=("Arial", 16), width=4)
genre_label = Label(movie_search_page, text="              Select Up To 3 Genres Below", bg='#333333', fg="#FFFFFF",
                    font=("Arial", 16))
filter_button = Button(movie_search_page, text="Search", bg="#0c2b59", fg="#FFFFFF", font=("Arial", 16))
# Defining a Variable To Dynamically Change the Label Based On The Selected Checkboxes
current_genres_text = tk.StringVar()
current_genres_text.set("None Currently Selected")
current_genres_label = Label(movie_search_page, textvariable=current_genres_text, bg='#333333', fg="#FFFFFF",
                             font=("Arial", 10))

# Placing widgets on the movie_search_page
header_label.grid(row=0, column=0, pady=5, padx=60)
search_label.grid(row=1, column=0)
search_entry.grid(row=2, column=0)
search_button.grid(row=3, column=0)
filter_label.grid(row=0, column=1, pady=5, padx=60)
year_label.grid(row=1, column=1)
year_entry.grid(row=1, column=1, sticky="e", padx=60)
rating_label.grid(row=2, column=1)
rating_entry.grid(row=2, column=1, sticky="e", padx=60)
genre_label.grid(row=3, column=1)
current_genres_label.grid(row=4, column=1)
filter_button.grid(row=5, column=1, sticky="e", padx=80)


def create_movie_checkboxes():
    #  List of Movie Genres
    movie_genres = [
        "Adventure", "Fantasy", "Action", "Biography", "Documentary", "News",
        "Sport", "Romance", "Drama", "Family", "History", "Mystery", "Crime",
        "Comedy", "Musical", "Thriller", "Adult", "Western", "War", "Horror",
        "Animation", "Sci-Fi", "Film-Noir", "Talk-Show", "Reality-TV", "Game-Show"
    ]

    # Sort values alphabetically
    movie_genres.sort()

    # Create a dictionary to hold checkbox variables
    checkbox_vars = {}

    # Initialize row counter
    row_num = 5
    # Functions for Movie Search Page

    # Create checkboxes for each value in the sorted list
    for value in movie_genres:
        checkbox_vars[value] = tk.BooleanVar()
        current_genres_selected = []
        checkbox = tk.Checkbutton(movie_search_page, text=value, fg="#FFFFFF", font=("Arial", 13), bg="#333333",
                                  variable=checkbox_vars[value],
                                  command=lambda v=value: on_checkbox_toggle(v))
        checkbox.grid(row=row_num, column=1, sticky="W", padx=115)
        row_num += 1

    def on_checkbox_toggle(genre):
        # This function will be called whenever a genre checkbox is toggled

        # Checks if there is already 3 genres.py selected
        if len(current_genres_selected) == 3 and genre not in current_genres_selected:
            return  # Exit Function Early
        else:
            # Removes the value is it already exists
            if genre in current_genres_selected:
                current_genres_selected.remove(genre)
                new_text = ', '.join(str(element) for element in current_genres_selected)
                current_genres_text.set(new_text)
                # If No Genres Selected Add Text Stating That
                if not current_genres_selected:
                    current_genres_text.set("None Currently Selected")
            else:
                # Add The New Genre To The Label
                current_genres_selected.append(genre)
                new_text = ', '.join(str(element) for element in current_genres_selected)
                current_genres_text.set(new_text)


create_movie_checkboxes()

# Search For TV Shows Page
tv_search_page = Screen(screen_master, "TV Search Page")
tv_search_page.config(bg="#333333")
tv_header_label = Label(tv_search_page, text="Search For A Show", bg='#333333', fg="#0c2b59",
                        font=("Arial", 30))
tv_search_label = Label(tv_search_page, text="Enter Show Title", bg='#333333', fg="#FFFFFF",
                        font=("Arial", 16))
tv_search_entry = Entry(tv_search_page, font=("Arial", 16))
tv_search_button = Button(tv_search_page, text="Search", bg="#0c2b59", fg="#FFFFFF", font=("Arial", 16),
                          command=lambda: display_search(search_movie_file(tv_search_entry.get(), 2), 2))
tv_filter_label = Label(tv_search_page, text="Filter For A Show", bg='#333333', fg="#0c2b59",
                        font=("Arial", 30))
tv_year_label = Label(tv_search_page, text="Show Release Year", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
tv_year_entry = Entry(tv_search_page, font=("Arial", 16), width=4)
tv_rating_label = Label(tv_search_page, text="Minium Rating (0-10)", bg='#333333', fg="#FFFFFF",
                        font=("Arial", 16))
tv_rating_entry = Entry(tv_search_page, font=("Arial", 16), width=4)
tv_genre_label = Label(tv_search_page, text="              Select Up To 3 Genres Below", bg='#333333',
                       fg="#FFFFFF", font=("Arial", 16))
tv_filter_button = Button(tv_search_page, text="Search", bg="#0c2b59", fg="#FFFFFF", font=("Arial", 16))
# Defining a Variable To Dynamically Change the Label Based On The Selected Checkboxes
tv_current_genres_text = tk.StringVar()
tv_current_genres_text.set("None Currently Selected")
tv_current_genres_label = Label(tv_search_page, textvariable=tv_current_genres_text, bg='#333333', fg="#FFFFFF",
                                font=("Arial", 10))

# Placing widgets on the start_screen
tv_header_label.grid(row=0, column=0, pady=5, padx=60)
tv_search_label.grid(row=1, column=0)
tv_search_entry.grid(row=2, column=0)
tv_search_button.grid(row=3, column=0)
tv_filter_label.grid(row=0, column=1, pady=5, padx=60)
tv_year_label.grid(row=1, column=1)
tv_year_entry.grid(row=1, column=1, sticky="e", padx=63)
tv_rating_label.grid(row=2, column=1)
tv_rating_entry.grid(row=2, column=1, sticky="e", padx=63)
tv_genre_label.grid(row=3, column=1)
tv_current_genres_label.grid(row=4, column=1)
tv_filter_button.grid(row=5, column=1, sticky="e", padx=90)


def create_tv_checkboxes():
    #  List of TV_show Genres
    tv_genres = [
        "Adventure", "Fantasy", "Action", "Biography", "Documentary", "News",
        "Sport", "Romance", "Drama", "Family", "History", "Mystery", "Crime",
        "Comedy", "Musical", "Thriller", "Adult", "Western", "War", "Horror",
        "Animation", "Sci-Fi", "Film-Noir", "Talk-Show", "Reality-TV", "Game-Show"
    ]

    # Sort values alphabetically
    tv_genres.sort()

    # Create a dictionary to hold checkbox variables
    tv_checkbox_vars = {}

    # Initialize row counter
    row_num = 5

    # Create checkboxes for each value in the sorted list
    for value in tv_genres:
        tv_checkbox_vars[value] = tk.BooleanVar()
        current_genres_selected = []
        checkbox = tk.Checkbutton(tv_search_page, text=value, fg="#FFFFFF", font=("Arial", 13), bg="#333333",
                                  variable=tv_checkbox_vars[value],
                                  command=lambda v=value: on_checkbox_toggle(v))
        checkbox.grid(row=row_num, column=1, sticky="W", padx=114)
        row_num += 1

    def on_checkbox_toggle(genre):
        # This function will be called whenever a genre checkbox is toggled

        # Checks if there is already 3 genres.py selected
        if len(current_genres_selected) == 3 and genre not in current_genres_selected:
            return  # Exit Function Early
        else:
            # Removes the value is it already exists
            if genre in current_genres_selected:
                current_genres_selected.remove(genre)
                new_text = ', '.join(str(element) for element in current_genres_selected)
                tv_current_genres_text.set(new_text)
                # If No Genres Selected Add Text Stating That
                if not current_genres_selected:
                    tv_current_genres_text.set("None Currently Selected")
            else:
                # Add The New Genre To The Label
                current_genres_selected.append(genre)
                new_text = ', '.join(str(element) for element in current_genres_selected)
                tv_current_genres_text.set(new_text)


create_tv_checkboxes()


# Function That Converts An Image Link Into Picture Usable In The GUI
def resize_and_display_image_from_url(image_url, image_button):
    # Download the image from the URL
    Image.MAX_IMAGE_PIXELS = None
    response = requests.get(image_url)
    img_data = BytesIO(response.content)

    # Open the image from the downloaded data
    original_img = Image.open(img_data)

    # Resize the image
    new_size = (216, 336)  # Replace with the desired dimensions
    resized_img = original_img.resize(new_size)

    # Convert the resized image to Tkinter PhotoImage
    tk_img = ImageTk.PhotoImage(resized_img)

    # Update the label with the resized image
    image_button.configure(image=tk_img)
    image_button.image = tk_img


def display_search(search_results, content_type):
    # Search Results Window
    search_result_page = Screen(screen_master, "Movie Search Results")
    search_result_page.config(bg="#333333")

    sr_label = Label(search_result_page, text="Your Search Results", bg='#333333', fg="#FFFFFF",
                     font=("Arial", 36))
    sr_label.grid(row=0, column=0, columnspan=2, pady=10, padx=300, sticky='w')

    sr_image_button1 = Button(search_result_page, image=None, compound=TOP, bg='#333333', borderwidth=0, fg='#FFFFFF',
                              font=("Arial", 16), command=lambda: update_content_info(current_node, current_key))
    sr_image_button1.grid(row=1, column=0, sticky='w', padx=225)

    sr_image_button2 = Button(search_result_page, image=None, compound=TOP, bg='#333333', borderwidth=0, fg='#FFFFFF',
                              font=("Arial", 16),
                              command=lambda: update_content_info(current_node.next_node, current_key + 1))
    sr_image_button2.grid(row=1, column=0, sticky='w', padx=600)
    sr_back_button = Button(search_result_page, text="Reload Last",
                            image=None, compound=TOP, bg='#0c2b59', borderwidth=0, fg='#FFFFFF', font=("Arial", 16),
                            command=lambda: last_button_pressed())
    sr_next_button = Button(search_result_page, text="Load Next",
                            image=None, compound=TOP, bg='#0c2b59', borderwidth=0, fg='#FFFFFF',
                            font=("Arial", 16), command=lambda: next_button_pressed())
    sr_back_button.grid(row=2, column=0, sticky='w', padx=270)
    sr_next_button.grid(row=2, column=0, sticky='w', padx=655)
    sr_number_of_pages_label = Label(search_result_page, text="1/2 pages", bg="#333333", fg="#FFFFFF",
                                     font=("Arial", 16), width=86)
    sr_number_of_pages_label.grid(row=3, column=0, sticky='w')

    # Search Results Functions
    global current_node
    if search_results == {}:
        if content_type == 1:
            search_entry.delete(0, tk.END)
            movie_search_page.show()
            print('There Are No Matching Movies')
        elif content_type == 2:
            tv_search_entry.delete(0, tk.END)
            tv_search_page.show()
            print('There Are No Matching Tv Series')
        return

    l_list = DoublyLinkedList()
    if type(search_results) is dict:
        search_result_page.show()
        for key, values in reversed(search_results.items()):
            l_list.add(key, values)
    global num_of_result
    num_of_result = len(search_results)

    def if_odd_add1(num):
        if num % 2 != 0:
            num = num + 1
        return num

    sr_number_of_pages_label.config(text=f"1/{int(if_odd_add1(num_of_result) / 2)} pages")

    # Function to update the GUI based on the current node
    def update_button1(node, x):
        # Extract values from the dictionary in the current node
        key = node.data[x]
        # Create a formatted string from the values
        if len(key[0][2]) > 20:
            if key[0][2][20] != "\n":
                insert_position = 20
                key[0][2] = key[0][2][:insert_position] + "\n" + key[0][2][insert_position:]

        if len(key[0][2]) > 40:
            if key[0][2][40] != "\n":
                insert_2nd_position = 40
                key[0][2] = key[0][2][:insert_2nd_position] + "\n" + key[0][2][insert_2nd_position:]

        formatted_string = f"{key[0][2]}\nYear: {key[0][3]}\nRating: {key[0][5]}/10\nVotes: {key[0][6]}"

        sr_image_button1.config(text=formatted_string)
        url = key[0][7]
        resize_and_display_image_from_url(url, sr_image_button1)

    def update_button2(node, x):
        # Extract values from the dictionary in the current node
        sr_image_button2.grid(row=1, column=0, sticky='w', padx=600)
        try:
            key = node.data[x]
        except AttributeError:
            sr_image_button2.grid_forget()
            return

        if len(key[0][2]) > 20:
            if key[0][2][20] != "\n":
                insert_position = 20
                key[0][2] = key[0][2][:insert_position] + "\n" + key[0][2][insert_position:]

        if len(key[0][2]) > 40:
            if key[0][2][40] != "\n":
                insert_2nd_position = 40
                key[0][2] = key[0][2][:insert_2nd_position] + "\n" + key[0][2][insert_2nd_position:]
        # Create a formatted string from the values
        formatted_string = f"{key[0][2]}\nYear: {key[0][3]}\nRating: {key[0][5]}/10\nVotes: {key[0][6]}"

        sr_image_button2.config(text=formatted_string)
        url = key[0][7]
        resize_and_display_image_from_url(url, sr_image_button2)

    global current_key
    current_key = 0

    def next_button_pressed():
        global current_node
        global current_key
        global num_of_result

        # Check if there is a next node
        if current_node and current_node.next_node:
            # Set current node to the 2nd next node
            current_node = current_node.next_node
        if current_node and current_node.next_node:
            current_node = current_node.next_node

            sr_number_of_pages_label.config(
                text=f"{int((if_odd_add1(current_key) + 4) / 2)}/{int(if_odd_add1(num_of_result) / 2)} pages")
            # Update the GUI with values from the next node and the node after that
            current_key = current_key + 2
            update_button1(current_node, current_key)
            update_button2(current_node.next_node, current_key + 1)

    def last_button_pressed():
        global current_node
        global current_key
        global num_of_result

        # Check if there is a next node
        if current_node and current_node.prev_node:
            # Set current node to the 2nd prev node
            current_node = current_node.prev_node
        if current_node and current_node.prev_node:
            current_node = current_node.prev_node

            sr_number_of_pages_label.config(
                text=f"{int((if_odd_add1(current_key)) / 2)}/{int(if_odd_add1(num_of_result) / 2)} pages")

            # Update the GUI with values from the next node and the node after that
            current_key = current_key - 2
            update_button1(current_node, current_key)
            update_button2(current_node.next_node, current_key + 1)

    current_node = l_list.head
    update_button1(current_node, 0)
    update_button2(current_node.next_node, 1)


def update_content_info(node, x):
    # Content Info Page
    content_info_page = Screen(screen_master, "Content Details")
    content_info_page.config(bg="#333333")
    url = "https://m.media-amazon.com/images/M/MV5BYTU3NWI5OGMtZmZhNy00MjVmLTk1YzAtZjA3ZDA3NzcyNDUxXkEyXkFqcGdeQXVyODY5Njk4Njc@._V1_FMjpg_UX1000_.jpg"
    content_details_img = Button(content_info_page, text="TV Series 2008-2013\n9.5/10 2.1M", compound=TOP, img=None,
                                 borderwidth=0, bg='#333333', fg='#FFFFFF', font=("Arial", 16), )
    resize_and_display_image_from_url(url, content_details_img)
    content_details_img.grid(row=1, column=0, sticky="nw")
    content_title = Label(content_info_page, text="Breaking Bad", bg='#333333', fg="#FFFFFF", font=("Arial", 19))
    content_title.grid(row=1, column=0, padx=225, pady=5, sticky="nw")
    description_title = Label(content_info_page,
                              text="A chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing\nand selling methamphetamine with a former student in order to secure his family's\nfuture",
                              bg='#333333', fg="#FFFFFF", font=("Arial", 16), borderwidth=0, pady=10, justify='left')
    description_title.grid(row=1, column=0, padx=225, pady=80, sticky="nw")
    content_genre_tag1 = Button(content_info_page, text="Documentary", font=("Arial", 14), bg='#0c2b59', fg='#FFFFFF',
                                width=11, height=1)
    content_genre_tag2 = Button(content_info_page, text="Action", font=("Arial", 14), bg='#0c2b59', fg='#FFFFFF',
                                width=11, height=1)
    content_genre_tag3 = Button(content_info_page, text="Documentary", font=("Arial", 14), bg='#0c2b59', fg='#FFFFFF',
                                width=11, height=1)
    content_genre_tag1.grid(row=1, column=0, padx=217, pady=45, sticky="nw")
    content_genre_tag2.grid(row=1, column=0, padx=344, pady=45, sticky="nw")
    content_genre_tag3.grid(row=1, column=0, padx=471, pady=45, sticky="nw")
    add_watchlist = Button(content_info_page, text="Add to\nWatchlist", font=("Arial", 14), bg='#0c2b59',
                           fg='#FFFFFF', width=11, command=lambda: add_to_watchlist(node, x))
    add_watchlist.grid(row=2, column=0, sticky='nw', padx=45)
    mark_as_watched = Button(content_info_page, text="Mark As\nWatched", font=("Arial", 14), bg='#0c2b59', fg='#FFFFFF',
                             width=11, command=lambda: add_to_watched_stack(node, x))
    mark_as_watched.grid(row=3, column=0, sticky='nw', padx=45)

    if node.data[x][0][0] in watched_dict:
        mark_as_watched.config(text="Marked As\nWatched")

    if node.data[x][0][0] in movie_watchlist_dict:
        add_watchlist.config(text="Added to\nWatchlist")

    if node.data[x][0][0] in tv_watchlist_dict:
        add_watchlist.config(text="Added to\nWatchlist")

    # Pages Button Functions
    def add_to_watchlist(node, x):
        if add_watchlist.cget("text") == "Add to\nWatchlist":
            add_watchlist.config(text="Added to\nWatchlist")
            info = node.data[x]
            if info[0][1] == "movie":
                movie_watchlist_dict[info[0][0]] = info[0]
            elif info[0][1] == "tvSeries":
                tv_watchlist_dict[info[0][0]] = info[0]

    def add_to_watched_stack(node, x):
        if mark_as_watched.cget("text") == "Mark As\nWatched":
            info = node.data[x]
            watched_stack.push(info[0])
            watched_dict[info[0][0]] = info[0]
            mark_as_watched.config(text="Marked As\nWatched")

    key = node.data[x]

    content_data = f"Year: {key[0][3]}\nRating: {key[0][5]}/10\nVotes: {key[0][6]}"
    content_details_img.config(text=content_data)
    url = key[0][7]
    resize_and_display_image_from_url(url, content_details_img)

    input_string = key[0][2]
    # Remove newline characters
    no_new_line = input_string.replace('\n', '')
    content_title.config(text=no_new_line)

    if len(key[0][8]) >= 75:
        if key[0][8][75] != "\n":
            insert_position = 75
            key[0][8] = key[0][8][:insert_position] + "\n" + key[0][8][insert_position:]

    if len(key[0][8]) >= 150:
        if key[0][8][150] != "\n":
            insert_2nd_position = 150
            key[0][8] = key[0][8][:insert_2nd_position] + "\n" + key[0][8][insert_2nd_position:]

    if len(key[0][8]) >= 225:
        if key[0][8][225] != "\n":
            insert_3nd_position = 225
            key[0][8] = key[0][8][:insert_3nd_position] + "\n" + key[0][8][insert_3nd_position:]

    description_title.config(text=key[0][8])

    input_string1 = key[0][8]
    # Replace &apos with an actual apostrophe
    no_apos = input_string1.replace('&apos;', "'")
    description_title.config(text=no_apos)

    input_string2 = no_apos
    # Replace &quot with actual quotes
    no_quotes = input_string2.replace('&quot;', '"')
    description_title.config(text=no_quotes)

    genres = key[0][4]
    input_string = genres

    # Split the string by commas
    values = input_string.split(',')

    # Initialize variables
    var1 = var2 = var3 = None

    # Assign each value to a separate variable
    if len(values) >= 1:
        var1 = values[0]
    if len(values) >= 2:
        var2 = values[1]
    if len(values) >= 3:
        var3 = values[2]
    if var1:
        content_genre_tag1.config(text=var1)
    if var2:
        content_genre_tag2.config(text=var2)
    else:
        content_genre_tag2.grid_forget()
    if var3:
        content_genre_tag3.config(text=var3)
    else:
        content_genre_tag3.grid_forget()

    content_info_page.show()


#  Rate Content Page
global watched_stack
global watched_dict
watched_stack = Stack()
watched_dict = {}
rate_content_page = Screen(screen_master, "Content Ratings")
rate_content_page.config(bg="#333333")
rate_content = Button(rate_content_page, text="Mark Something As\nWatched To Rate It", compound=TOP, img=None,
                      borderwidth=0, bg='#333333', fg='#FFFFFF', font=("Arial", 16))
rate_content.grid(row=0, column=0, sticky='nw')
rating_entry = Entry(rate_content_page, font=("Arial", 21), justify='center', width=4, )
rating_entry.grid(row=1, column=0, sticky='e', padx=0)
enter_rating = Button(rate_content_page, text='Enter Rating', bg="#0c2b59", fg='#FFFFFF', font=("Arial", 16),
                      command=lambda: enter_rating())
enter_rating.grid(row=1, column=0, sticky='w', padx=10)
skip_button = Button(rate_content_page, text='Skip', width=10, bg="#0c2b59", fg='#FFFFFF', font=("Arial", 16),
                     command=lambda: skip_button())
skip_button.grid(row=2, column=0, pady=5, stick="w", padx=11)
movie_rating_label = Label(rate_content_page, text="Top Movie Ratings:", bg='#333333', fg="#FFFFFF",
                           font=("Arial", 21))
movie_rating_label.grid(row=0, column=1, padx=35, sticky='nw', pady=10)

tv_rating_label = Label(rate_content_page, text="Top Tv Show Ratings:", bg='#333333', fg="#FFFFFF",
                        font=("Arial", 21))
tv_rating_label.grid(row=0, column=1, padx=425, sticky='ne', pady=10)
top_movie_rating_button = Button(rate_content_page, text='Display', bg="#0c2b59", fg='#FFFFFF', font=("Arial", 16))
top_movie_rating_button.grid(row=0, column=1, sticky='nw', pady=10, padx=290)
top_tv_rating_button = Button(rate_content_page, text='Display', bg="#0c2b59", fg='#FFFFFF', font=("Arial", 16))
top_tv_rating_button.grid(row=0, column=1, sticky='ne', pady=10, padx=330)


def update_button_img():
    if not watched_stack.is_empty():
        top = watched_stack.peek()
        url = top[7]
        resize_and_display_image_from_url(url, rate_content)
        rate_content.config(text=f'{top[3]}\n{top[5]}/10: {top[6]}')


def skip_button():
    if not watched_stack.is_empty():
        watched_stack.pop()
        if not watched_stack.is_empty():
            top = watched_stack.peek()
            url = top[7]
            resize_and_display_image_from_url(url, rate_content)
            rate_content.config(text=f'{top[3]}\n{top[5]}/10: {top[6]}')
        else:
            rate_content.config(image='')
            rate_content.config(text='Mark Something As\nWatched To Rate It')
    else:
        rate_content.config(image='')
        rate_content.config(text='Mark Something As\nWatched To Rate It')


def enter_rating():
    try:
        # Attempt to convert the value to a float
        float_value = float(rating_entry.get())

        # Check if the float is within the specified range
        if 1.0 <= float_value <= 10.0 and float_value == round(float_value, 1):
            top = watched_stack.peek()
            watched_dict[top[0]].append(float_value)
            rating_entry.config(text='')
            if not watched_stack.is_empty():
                watched_stack.pop()
                if not watched_stack.is_empty():
                    top = watched_stack.peek()
                    url = top[7]
                    resize_and_display_image_from_url(url, rate_content)
                    rate_content.config(text=f'{top[3]}\n{top[5]}/10: {top[6]}')
                    rating_entry.delete(0, tk.END)
                else:
                    rate_content.config(image='')
                    rate_content.config(text='Mark Something As\nWatched To Rate It')
                    rating_entry.delete(0, tk.END)
            else:
                rate_content.config(image='')
                rate_content.config(text='Mark Something As\nWatched To Rate It')
                rating_entry.delete(0, tk.END)
        else:
            rating_entry.delete(0, tk.END)
            print('Please enter a value between 1.0 and 10')

    except ValueError:
        # ValueError will be raised if the conversion to float fails
        print('Please enter a number')
        rating_entry.delete(0, tk.END)


# Movie watchlist page
global movie_watchlist_dict
movie_watchlist_dict = {}
global movie_watchlist_image_button1
global movie_watchlist_image_button2
global movie_wlist_back_button
global movie_wlist_next_button
global movie_wlist_number_of_pages_label
global movie_dict_index
movie_dict_index = 0
movie_watchlist_page = Screen(screen_master, "Movie Watchlist")
movie_watchlist_page.config(bg="#333333")
movie_watchlist_label = Label(movie_watchlist_page, text="Your Movie Watchlist", bg='#333333', fg="#FFFFFF",
                              font=("Arial", 36))
movie_watchlist_label.grid(row=0, column=0, columnspan=2, pady=10, padx=300, sticky='w')
movie_watchlist_image_button1 = Button(movie_watchlist_page, compound=TOP, bg='#333333', borderwidth=0, fg='#FFFFFF',
                                       font=("Arial", 16))
movie_watchlist_image_button1.grid(row=1, column=0, sticky='w', padx=225)
movie_watchlist_image_button2 = Button(movie_watchlist_page, compound=TOP, bg='#333333', borderwidth=0, fg='#FFFFFF',
                                       font=("Arial", 16))
movie_watchlist_image_button2.grid(row=1, column=0, sticky='w', padx=600)
movie_wlist_number_of_pages_label = Label(movie_watchlist_page, text="1/2 pages", bg="#333333", fg="#FFFFFF",
                                          font=("Arial", 16), width=86)
movie_wlist_number_of_pages_label.grid(row=3, column=0, sticky='w')

movie_wlist_sorting = Button(movie_watchlist_page, text="Sorting Options", borderwidth=0, bg="#0c2b59", fg="#FFFFFF",
                             font=("Arial", 20), command=lambda: merge_sort_dict(0))
movie_wlist_sorting.grid(row=0, column=0, sticky="nw", pady=20, padx=20)


def update_movie_watchlist(dict):
    movie_wlist_back_button = Button(movie_watchlist_page, text="Reload Last",
                                     image=None, compound=TOP, bg='#0c2b59', borderwidth=0, fg='#FFFFFF',
                                     font=("Arial", 16), command=lambda: last_button())
    movie_wlist_next_button = Button(movie_watchlist_page, text="Load Next",
                                     image=None, compound=TOP, bg='#0c2b59', borderwidth=0, fg='#FFFFFF',
                                     font=("Arial", 16), command=lambda: next_button())
    movie_wlist_back_button.grid(row=2, column=0, sticky='w', padx=270)
    movie_wlist_next_button.grid(row=2, column=0, sticky='w', padx=655)

    # Function to update the GUI
    def update_button1(key):
        data = dict[key]
        if len(data[2]) > 20:
            if data[2][20] != "\n":
                insert_position = 20
                data[2] = data[2][:insert_position] + "\n" + data[2][insert_position:]

        if len(data[2]) > 40:
            if data[2][40] != "\n":
                insert_2nd_position = 40
                data[2] = data[2][:insert_2nd_position] + "\n" + data[2][insert_2nd_position:]
        movie_watchlist_image_button1.config(text=f'{data[2]}\nYear: {data[3]}\nRating: {data[5]}/10\nVotes: {data[6]}')
        resize_and_display_image_from_url(data[7], movie_watchlist_image_button1)
        movie_watchlist_image_button1.grid(row=1, column=0, sticky='w', padx=225)

    def update_button2(key):
        data = dict[key]
        if len(data[2]) > 20:
            if data[2][20] != "\n":
                insert_position = 20
                data[2] = data[2][:insert_position] + "\n" + data[2][insert_position:]

        if len(data[2]) > 40:
            if data[2][40] != "\n":
                insert_2nd_position = 40
                data[2] = data[2][:insert_2nd_position] + "\n" + data[2][insert_2nd_position:]
        movie_watchlist_image_button2.config(text=f'{data[2]}\nYear: {data[3]}\nRating: {data[5]}/10\nVotes: {data[6]}')
        resize_and_display_image_from_url(data[7], movie_watchlist_image_button2)
        movie_watchlist_image_button2.grid(row=1, column=0, sticky='w', padx=600)

    def if_odd_add1(num):
        if num % 2 != 0:
            num = num + 1
        return num

    if int(len(dict.keys())) == 0:
        movie_watchlist_image_button1.grid_forget()
        movie_watchlist_image_button2.grid_forget()
        movie_wlist_next_button.grid_forget()
        movie_wlist_back_button.grid_forget()
        movie_wlist_number_of_pages_label.grid_forget()
    elif int(len(dict.keys())) == 1:
        movie_watchlist_image_button2.grid_forget()
        keys_list = list(dict.keys())
        update_button1(keys_list[0])
        movie_wlist_number_of_pages_label.config(text="1/1 Pages")
        movie_wlist_number_of_pages_label.grid(row=3, column=0, sticky='w')
        movie_wlist_back_button.grid(row=2, column=0, sticky='w', padx=270)
        movie_wlist_next_button.grid(row=2, column=0, sticky='w', padx=655)
    elif int(len(dict.keys())) == 2:
        keys_list = list(dict.keys())
        update_button1(keys_list[0])
        update_button2(keys_list[1])
        movie_wlist_number_of_pages_label.config(text="1/1 Pages")
        movie_wlist_number_of_pages_label.grid(row=3, column=0, sticky='w')
        movie_wlist_back_button.grid(row=2, column=0, sticky='w', padx=270)
        movie_wlist_next_button.grid(row=2, column=0, sticky='w', padx=655)
    else:
        keys_list = list(dict.keys())
        update_button1(keys_list[movie_dict_index])
        if len(keys_list) - movie_dict_index >= 2:
            update_button2(keys_list[movie_dict_index + 1])
        num = len(keys_list)
        number_of_pages = int(if_odd_add1(num) / 2)
        movie_wlist_number_of_pages_label.config(text=f"{(movie_dict_index + 2) // 2}/{number_of_pages} Pages")
        movie_wlist_number_of_pages_label.grid(row=3, column=0, sticky='w')
        movie_wlist_back_button.grid(row=2, column=0, sticky='w', padx=270)
        movie_wlist_next_button.grid(row=2, column=0, sticky='w', padx=655)

    def next_button():
        global movie_dict_index
        if len(list(dict.keys())) - movie_dict_index > 2:
            keys_list = list(dict.keys())
            num = len(keys_list)
            movie_dict_index += 2
            movie_wlist_number_of_pages_label.config(
                text=f"{((movie_dict_index + 2) // 2)}/{if_odd_add1(num) // 2} Pages")

            if num - movie_dict_index >= 2:
                update_button1(keys_list[movie_dict_index])
                update_button2(keys_list[movie_dict_index + 1])
                movie_watchlist_image_button2.grid(row=1, column=0, sticky='w', padx=600)
            else:
                update_button1(keys_list[movie_dict_index])
                movie_watchlist_image_button2.grid_forget()

    def last_button():
        global movie_dict_index
        if movie_dict_index != 0:
            keys_list = list(dict.keys())
            num = len(keys_list)
            movie_dict_index -= 2
            movie_wlist_number_of_pages_label.config(
                text=f"{((movie_dict_index + 2) // 2)}/{if_odd_add1(num) // 2} Pages")

            if num - movie_dict_index >= 2:
                update_button1(keys_list[movie_dict_index])
                update_button2(keys_list[movie_dict_index + 1])
                movie_watchlist_image_button2.grid(row=1, column=0, sticky='w', padx=600)
            else:
                update_button1(keys_list[movie_dict_index])
                movie_watchlist_image_button2.grid_forget()


# Tv Watchlist Page
global tv_watchlist_dict
tv_watchlist_dict = {}
global tv_watchlist_image_button1
global tv_watchlist_image_button2
global tv_wlist_back_button
global tv_wlist_next_button
global tv_wlist_number_of_pages_label
global tv_dict_index
tv_dict_index = 0
tv_watchlist_page = Screen(screen_master, " Tv Watchlist")
tv_watchlist_page.config(bg="#333333")
watchlist_label = Label(tv_watchlist_page, text="Your Tv-Show Watchlist", bg='#333333', fg="#FFFFFF",
                        font=("Arial", 36))
watchlist_label.grid(row=0, column=0, columnspan=2, pady=10, padx=258, sticky='w')
tv_watchlist_image_button1 = Button(tv_watchlist_page, compound=TOP, bg='#333333', borderwidth=0, fg='#FFFFFF',
                                    font=("Arial", 16))
tv_watchlist_image_button1.grid(row=1, column=0, sticky='w', padx=225)
tv_watchlist_image_button2 = Button(tv_watchlist_page, compound=TOP, bg='#333333', borderwidth=0, fg='#FFFFFF',
                                    font=("Arial", 16))
tv_watchlist_image_button2.grid(row=1, column=0, sticky='w', padx=600)
tv_wlist_number_of_pages_label = Label(tv_watchlist_page, text="1/2 pages", bg="#333333", fg="#FFFFFF",
                                       font=("Arial", 16), width=86)
tv_wlist_number_of_pages_label.grid(row=3, column=0, sticky='w')
tv_wlist_sorting = Button(tv_watchlist_page, text="Sorting Options", borderwidth=0, bg="#0c2b59", fg="#FFFFFF",
                          font=("Arial", 20), command=lambda: merge_sort_dict(1))
tv_wlist_sorting.grid(row=0, column=0, sticky="nw", pady=20, padx=20)


def update_tv_watchlist(dict):
    tv_wlist_back_button = Button(tv_watchlist_page, text="Reload Last",
                                  image=None, compound=TOP, bg='#0c2b59', borderwidth=0, fg='#FFFFFF',
                                  font=("Arial", 16), command=lambda: last_button())
    tv_wlist_next_button = Button(tv_watchlist_page, text="Load Next",
                                  image=None, compound=TOP, bg='#0c2b59', borderwidth=0, fg='#FFFFFF',
                                  font=("Arial", 16), command=lambda: next_button())
    tv_wlist_back_button.grid(row=2, column=0, sticky='w', padx=270)
    tv_wlist_next_button.grid(row=2, column=0, sticky='w', padx=655)

    def update_button1(key):
        data = dict[key]
        if len(data[2]) > 20:
            if data[2][20] != "\n":
                insert_position = 20
                data[2] = data[2][:insert_position] + "\n" + data[2][insert_position:]

        if len(data[2]) > 40:
            if data[2][40] != "\n":
                insert_2nd_position = 40
                data[2] = data[2][:insert_2nd_position] + "\n" + data[2][insert_2nd_position:]
        tv_watchlist_image_button1.config(text=f'{data[2]}\nYear: {data[3]}\nRating: {data[5]}/10\nVotes: {data[6]}')
        resize_and_display_image_from_url(data[7], tv_watchlist_image_button1)
        tv_watchlist_image_button1.grid(row=1, column=0, sticky='w', padx=225)

    def update_button2(key):
        data = dict[key]
        if len(data[2]) > 20:
            if data[2][20] != "\n":
                insert_position = 20
                data[2] = data[2][:insert_position] + "\n" + data[2][insert_position:]

        if len(data[2]) > 40:
            if data[2][40] != "\n":
                insert_2nd_position = 40
                data[2] = data[2][:insert_2nd_position] + "\n" + data[2][insert_2nd_position:]
        tv_watchlist_image_button2.config(text=f'{data[2]}\nYear: {data[3]}\nRating: {data[5]}/10\nVotes: {data[6]}')
        resize_and_display_image_from_url(data[7], tv_watchlist_image_button2)
        tv_watchlist_image_button2.grid(row=1, column=0, sticky='w', padx=600)

    def if_odd_add1(num):
        if num % 2 != 0:
            num = num + 1
        return num

    if int(len(dict.keys())) == 0:
        tv_watchlist_image_button1.grid_forget()
        tv_watchlist_image_button2.grid_forget()
        tv_wlist_next_button.grid_forget()
        tv_wlist_back_button.grid_forget()
        tv_wlist_number_of_pages_label.grid_forget()
    elif int(len(dict.keys())) == 1:
        tv_watchlist_image_button2.grid_forget()
        keys_list = list(dict.keys())
        update_button1(keys_list[0])
        tv_wlist_number_of_pages_label.config(text="1/1 Pages")
        tv_wlist_number_of_pages_label.grid(row=3, column=0, sticky='w')
        tv_wlist_back_button.grid(row=2, column=0, sticky='w', padx=270)
        tv_wlist_next_button.grid(row=2, column=0, sticky='w', padx=655)
    elif int(len(dict.keys())) == 2:
        keys_list = list(dict.keys())
        update_button1(keys_list[0])
        update_button2(keys_list[1])
        tv_wlist_number_of_pages_label.config(text="1/1 Pages")
        tv_wlist_number_of_pages_label.grid(row=3, column=0, sticky='w')
        tv_wlist_back_button.grid(row=2, column=0, sticky='w', padx=270)
        tv_wlist_next_button.grid(row=2, column=0, sticky='w', padx=655)
    else:
        keys_list = list(dict.keys())
        update_button1(keys_list[tv_dict_index])
        if len(keys_list) - tv_dict_index >= 2:
            update_button2(keys_list[tv_dict_index + 1])
        num = len(keys_list)
        number_of_pages = int(if_odd_add1(num) / 2)
        tv_wlist_number_of_pages_label.config(text=f"{(tv_dict_index + 2) // 2}/{number_of_pages} Pages")
        tv_wlist_number_of_pages_label.grid(row=3, column=0, sticky='w')
        tv_wlist_back_button.grid(row=2, column=0, sticky='w', padx=270)
        tv_wlist_next_button.grid(row=2, column=0, sticky='w', padx=655)

    def next_button():
        global tv_dict_index
        if len(list(dict.keys())) - tv_dict_index > 2:
            keys_list = list(dict.keys())
            num = len(keys_list)
            tv_dict_index += 2
            tv_wlist_number_of_pages_label.config(
                text=f"{((tv_dict_index + 2) // 2)}/{if_odd_add1(num) // 2} Pages")

            if num - tv_dict_index >= 2:
                update_button1(keys_list[tv_dict_index])
                update_button2(keys_list[tv_dict_index + 1])
                tv_watchlist_image_button2.grid(row=1, column=0, sticky='w', padx=600)
            else:
                update_button1(keys_list[tv_dict_index])
                tv_watchlist_image_button2.grid_forget()

    def last_button():
        global tv_dict_index
        if tv_dict_index != 0:
            keys_list = list(dict.keys())
            num = len(keys_list)
            tv_dict_index -= 2
            tv_wlist_number_of_pages_label.config(
                text=f"{((tv_dict_index + 2) // 2)}/{if_odd_add1(num) // 2} Pages")

            if num - tv_dict_index >= 2:
                update_button1(keys_list[tv_dict_index])
                update_button2(keys_list[tv_dict_index + 1])
                tv_watchlist_image_button2.grid(row=1, column=0, sticky='w', padx=600)
            else:
                update_button1(keys_list[tv_dict_index])
                tv_watchlist_image_button2.grid_forget()


# Sorting Options Page
def merge_sort_dict(identifer):
    sorting_options_page = Screen(screen_master, "Sorting Options")
    sorting_options_page.config(bg="#333333")
    ascending_label = Label(sorting_options_page, text="Sort One Of The Below Values\nFrom Highest To Lowest",
                            fg='#FFFFFF',
                            font=("Arial", 28), bg='#333333')
    descending_label = Label(sorting_options_page, text="Sort One Of The Below Values\nFrom Lowest To Highest",
                             fg='#FFFFFF',
                             font=("Arial", 28), bg='#333333')
    year_ascend_cb = Checkbutton(sorting_options_page, text="Release Year", fg='#FFFFFF',
                                 font=("Arial", 20), bg='#333333', command=lambda: highlight_checkbox(1))
    rating_ascend_cb = Checkbutton(sorting_options_page, text="Rating", fg='#FFFFFF',
                                   font=("Arial", 20), bg='#333333', command=lambda: highlight_checkbox(2))
    votes_ascend_cb = Checkbutton(sorting_options_page, text="Number Of Votes", fg='#FFFFFF',
                                  font=("Arial", 20), bg='#333333', command=lambda: highlight_checkbox(3))
    year_descend_cb = Checkbutton(sorting_options_page, text="Release Year", fg='#FFFFFF',
                                  font=("Arial", 20), bg='#333333', command=lambda: highlight_checkbox(4))
    rating_descend_cb = Checkbutton(sorting_options_page, text="Rating", fg='#FFFFFF',
                                    font=("Arial", 20), bg='#333333', command=lambda: highlight_checkbox(5))
    votes_descend_cb = Checkbutton(sorting_options_page, text="Number Of Votes", fg='#FFFFFF',
                                   font=("Arial", 20), bg='#333333', command=lambda: highlight_checkbox(6))
    confirm_button = Button(sorting_options_page, text="Confirm", fg='#FFFFFF',
                            font=("Arial", 20), bg="#0c2b59", command=lambda: confirm_button(identifer))
    cancel_button = Button(sorting_options_page, text="Cancel", fg='#FFFFFF',
                           font=("Arial", 20), bg="#0c2b59", command=lambda: cancel_button(identifer))
    ascending_label.grid(row=0, column=0, sticky='w')
    descending_label.grid(row=0, column=1, sticky='w', padx=20)
    year_ascend_cb.grid(row=1, column=0)
    rating_ascend_cb.grid(row=2, column=0)
    votes_ascend_cb.grid(row=3, column=0)
    year_descend_cb.grid(row=1, column=1)
    rating_descend_cb.grid(row=2, column=1)
    votes_descend_cb.grid(row=3, column=1)
    confirm_button.grid(row=4, column=1, sticky='w', pady=100, padx=75)
    cancel_button.grid(row=4, column=0, sticky='e', pady=100, padx=75)

    def highlight_checkbox(box):
        if box == 1:
            year_ascend_cb.config(bg='#0c2b59')
            rating_ascend_cb.config(bg='#333333')
            votes_ascend_cb.config(bg='#333333')
            year_descend_cb.config(bg='#333333')
            rating_descend_cb.config(bg='#333333')
            votes_descend_cb.config(bg='#333333')
        elif box == 2:
            year_ascend_cb.config(bg='#333333')
            rating_ascend_cb.config(bg='#0c2b59')
            votes_ascend_cb.config(bg='#333333')
            year_descend_cb.config(bg='#333333')
            rating_descend_cb.config(bg='#333333')
            votes_descend_cb.config(bg='#333333')
        elif box == 3:
            year_ascend_cb.config(bg='#333333')
            rating_ascend_cb.config(bg='#333333')
            votes_ascend_cb.config(bg='#0c2b59')
            year_descend_cb.config(bg='#333333')
            rating_descend_cb.config(bg='#333333')
            votes_descend_cb.config(bg='#333333')
        elif box == 4:
            year_ascend_cb.config(bg='#333333')
            rating_ascend_cb.config(bg='#333333')
            votes_ascend_cb.config(bg='#333333')
            year_descend_cb.config(bg='#0c2b59')
            rating_descend_cb.config(bg='#333333')
            votes_descend_cb.config(bg='#333333')
        elif box == 5:
            year_ascend_cb.config(bg='#333333')
            rating_ascend_cb.config(bg='#333333')
            votes_ascend_cb.config(bg='#333333')
            year_descend_cb.config(bg='#333333')
            rating_descend_cb.config(bg='#0c2b59')
            votes_descend_cb.config(bg='#333333')
        elif box == 6:
            year_ascend_cb.config(bg='#333333')
            rating_ascend_cb.config(bg='#333333')
            votes_ascend_cb.config(bg='#333333')
            year_descend_cb.config(bg='#333333')
            rating_descend_cb.config(bg='#333333')
            votes_descend_cb.config(bg='#0c2b59')

    def cancel_button(identifer):
        if identifer == 0:
            movie_watchlist_page.show()
        elif identifer == 1:
            tv_watchlist_page.show()

    def confirm_button(identifer):
        if year_ascend_cb.cget("background") == '#0c2b59':
            if identifer == 0:
                mergesort_dict = MergeSortDict(movie_watchlist_dict)
                sorted_dict = mergesort_dict.merge_sort(by_key=False, ascending=False, value_index=3)
                update_movie_watchlist(sorted_dict)
                movie_watchlist_page.show()
            elif identifer == 1:
                mergesort_dict = MergeSortDict(tv_watchlist_dict)
                sorted_dict = mergesort_dict.merge_sort(by_key=False, ascending=False, value_index=3)
                update_tv_watchlist(sorted_dict)
                tv_watchlist_page.show()
        if rating_ascend_cb.cget("background") == '#0c2b59':
            if identifer == 0:
                mergesort_dict = MergeSortDict(movie_watchlist_dict)
                sorted_dict = mergesort_dict.merge_sort(by_key=False, ascending=False, value_index=5)
                update_movie_watchlist(sorted_dict)
                movie_watchlist_page.show()
            elif identifer == 1:
                mergesort_dict = MergeSortDict(tv_watchlist_dict)
                sorted_dict = mergesort_dict.merge_sort(by_key=False, ascending=False, value_index=5)
                update_tv_watchlist(sorted_dict)
                tv_watchlist_page.show()
        if votes_ascend_cb.cget("background") == '#0c2b59':
            if identifer == 0:
                mergesort_dict = MergeSortDict(movie_watchlist_dict)
                sorted_dict = mergesort_dict.merge_sort(by_key=False, ascending=False, value_index=6)
                update_movie_watchlist(sorted_dict)
                movie_watchlist_page.show()
            elif identifer == 1:
                mergesort_dict = MergeSortDict(tv_watchlist_dict)
                sorted_dict = mergesort_dict.merge_sort(by_key=False, ascending=False, value_index=6)
                update_tv_watchlist(sorted_dict)
                tv_watchlist_page.show()
        if year_descend_cb.cget("background") == '#0c2b59':
            if identifer == 0:
                mergesort_dict = MergeSortDict(movie_watchlist_dict)
                sorted_dict = mergesort_dict.merge_sort(by_key=False, ascending=True, value_index=3)
                update_movie_watchlist(sorted_dict)
                movie_watchlist_page.show()
            elif identifer == 1:
                mergesort_dict = MergeSortDict(tv_watchlist_dict)
                sorted_dict = mergesort_dict.merge_sort(by_key=False, ascending=True, value_index=3)
                update_tv_watchlist(sorted_dict)
                tv_watchlist_page.show()
        if rating_descend_cb.cget("background") == '#0c2b59':
            if identifer == 0:
                mergesort_dict = MergeSortDict(movie_watchlist_dict)
                sorted_dict = mergesort_dict.merge_sort(by_key=False, ascending=True, value_index=5)
                update_movie_watchlist(sorted_dict)
                movie_watchlist_page.show()
            elif identifer == 1:
                mergesort_dict = MergeSortDict(tv_watchlist_dict)
                sorted_dict = mergesort_dict.merge_sort(by_key=False, ascending=True, value_index=5)
                update_tv_watchlist(sorted_dict)
                tv_watchlist_page.show()
        if votes_descend_cb.cget("background") == '#0c2b59':
            if identifer == 0:
                mergesort_dict = MergeSortDict(movie_watchlist_dict)
                sorted_dict = mergesort_dict.merge_sort(by_key=False, ascending=True, value_index=6)
                update_movie_watchlist(sorted_dict)
                movie_watchlist_page.show()
            elif identifer == 1:
                mergesort_dict = MergeSortDict(tv_watchlist_dict)
                sorted_dict = mergesort_dict.merge_sort(by_key=False, ascending=True, value_index=6)
                update_tv_watchlist(sorted_dict)
                tv_watchlist_page.show()


movie_search_page.show()
start_window.mainloop()
