import pymongo
import tkinter as tk
from tkinter import PhotoImage, Label, Entry, Button, Toplevel, Text
from tkinter import simpledialog



client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb = client['Reachandling']
information = mydb['Reach']


current_mode = 0
current_search_mode = 0  


entered_info = {
    "Name": "",
    "Content": "",
    "Instagram": {"Followers": None, "Username": ""},
    "Twitter": {"Followers": None, "Username": ""},
    "YouTube": {"Subscribers": None, "Channel": ""},
}

input_frame = None


def enter_info_mode():
    global current_mode
    current_mode = 1
    clear_widgets()
    show_info_entry_widgets()
     

def find_info_mode():
    global current_mode
    global current_search_mode
    current_mode = 2
    clear_widgets()
    show_search_options()
    current_search_mode = 0 


def search_data(search_mode):
    results = []

    def get_min_max_values():
        min_value = simpledialog.askfloat("Enter Minimum Value", f"Enter minimum {search_mode} value:")
        max_value = simpledialog.askfloat("Enter Maximum Value", f"Enter maximum {search_mode} value:")

        if min_value is not None and max_value is not None:
            for data in information.find({}):
                if search_mode == "Instagram":
                    if 'Instagram' in data and 'Followers' in data['Instagram']:
                        followers = data['Instagram']['Followers']
                        if min_value <= followers <= max_value:
                            results.append(data)
                elif search_mode == "Twitter":
                    if 'Twitter' in data and 'Followers' in data['Twitter'] and data['Twitter']['Followers'] is not None:
                        followers = data['Twitter']['Followers']
                        if min_value <= followers <= max_value:
                            results.append(data)
                elif search_mode == "YouTube":
                    if 'YouTube' in data and 'Subscribers' in data['YouTube'] and data['YouTube']['Subscribers'] is not None and data['YouTube']['Subscribers'] != '':
                        subscribers = data['YouTube']['Subscribers']
                        if min_value <= subscribers <= max_value:
                            results.append(data)

            display_search_results(results)

    get_min_max_values()

    
    
def show_search_options():
    find_info_button.grid_forget()

    instagram_button = tk.Button(input_frame, text="Search by Instagram Followers", command=lambda: search_data("Instagram"))
    youtube_button = tk.Button(input_frame, text="Search by YouTube Subscribers", command=lambda: search_data("YouTube"))
    twitter_button = tk.Button(input_frame, text="Search by Twitter Followers", command=lambda: search_data("Twitter"))
   
    instagram_button.grid(row=4, column=3, padx=5, pady=5)
    youtube_button.grid(row=5, column=3, padx=5, pady=5)
    twitter_button.grid(row=6, column=3, padx=5, pady=5)
    
    find_info_button.config(state=tk.DISABLED)


min_max_window = None

def search_min_max_window(search_criteria):
    clear_widgets()
    show_min_max_window(search_criteria)

def show_min_max_window(search_criteria):
    global min_max_window  
    min_max_window = Toplevel(root)
    min_max_window.title(f"Enter Min and Max {search_criteria}")

    min_label = Label(min_max_window, text="Min:")
    min_label.pack()
    min_entry = Entry(min_max_window)
    min_entry.pack()

    max_label = Label(min_max_window, text="Max:")
    max_label.pack()
    max_entry = Entry(min_max_window)
    max_entry.pack()

    submit_button = Button(min_max_window, text="Submit", command=lambda: search_data(search_criteria, min_entry.get(), max_entry.get()))
    submit_button.pack()

results_window = None

def show_results_window():
    global results_window
    results_window = Toplevel(root)
    results_window.title("Search Results")
    results_window.geometry("400x300")
    
    go_back_button = tk.Button(results_window, text="Go Back to Main Menu", command=go_back_to_initial)
    go_back_button.pack(pady=5)

def display_search_results(results):
    show_results_window()
    result_text = Text(results_window)
    result_text.pack(fill=tk.BOTH, expand=True)
    result_text.insert(tk.END, "Search Results:\n\n")

    if not results:
        result_text.insert(tk.END, "No results found.")
    else:
        for data in results:
            result_text.insert(tk.END, f"Name: {data['Name']}\n")
            result_text.insert(tk.END, f"Content: {data['Content']}\n")

            if 'Instagram' in data:
                result_text.insert(tk.END, f"Instagram Username: {data['Instagram']['Username']}\n")
                result_text.insert(tk.END, f"Instagram Followers: {data['Instagram']['Followers']}\n")

            if 'Twitter' in data:
                result_text.insert(tk.END, f"Twitter Username: {data['Twitter']['Username']}\n")
                result_text.insert(tk.END, f"Twitter Followers: {data['Twitter']['Followers']}\n")

            if 'YouTube' in data:
                result_text.insert(tk.END, f"YouTube Channel: {data['YouTube']['Channel']}\n")
                result_text.insert(tk.END, f"YouTube Subscribers: {data['YouTube']['Subscribers']}\n")

            result_text.insert(tk.END, "\n")

def submit_info():
    for key, value in entered_info.items():
        if not value:
            entered_info[key] = None  

    insert_data()
    clear_widgets()
    show_initial_widgets()


def go_back_to_initial():
    clear_widgets()
    show_initial_widgets()


def show_info_entry_widgets():
    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)
    content_label.grid(row=1, column=0)
    content_entry.grid(row=1, column=1)
    ig_followers_label.grid(row=2, column=0)
    ig_followers_entry.grid(row=2, column=1)
    ig_username_label.grid(row=3, column=0)
    ig_username_entry.grid(row=3, column=1)
    tt_followers_label.grid(row=4, column=0)
    tt_followers_entry.grid(row=4, column=1)
    tt_username_label.grid(row=5, column=0)
    tt_username_entry.grid(row=5, column=1)
    yt_channel_label.grid(row=7, column=0)
    yt_channel_entry.grid(row=7, column=1)
    yt_subscribers_label.grid(row=8, column=0)
    yt_subscribers_entry.grid(row=8, column=1)
    submit_button.grid(row=9, column=0, columnspan=2)

def clear_widgets():
    for widget in input_frame.winfo_children():
        widget.pack_forget()

def insert_data():
    entered_info["Name"] = name_entry.get()
    entered_info["Content"] = content_entry.get()
    entered_info["Instagram"]["Username"] = ig_username_entry.get()
    entered_info["Instagram"]["Followers"] = float(ig_followers_entry.get()) if ig_followers_entry.get() else None
    entered_info["Twitter"]["Username"] = tt_username_entry.get()
    entered_info["Twitter"]["Followers"] = float(tt_followers_entry.get()) if tt_followers_entry.get() else None
    entered_info["YouTube"]["Channel"] = yt_channel_entry.get()
    entered_info["YouTube"]["Subscribers"] = float(yt_subscribers_entry.get()) if yt_subscribers_entry.get() else None

    if not entered_info["Name"]:
        result_label.config(text="Name is required.")
        return

    information.insert_one(entered_info)
    result_label.config(text="Data inserted successfully!")
    
    

def show_initial_widgets():
    clear_widgets()
    enter_info_button.config(state=tk.NORMAL)
    find_info_button.config(state=tk.NORMAL)

root = tk.Tk()
root.title("Reach Handling")
root.maxsize(600, 800)

logo = PhotoImage(file="logo.gif")
logo = logo.subsample(2)

logo_label = tk.Label(root, image=logo, borderwidth="9px", relief="raised")
logo_label.pack(padx=10, pady=10)

input_frame = tk.Frame(root)
input_frame.pack()

name_label = tk.Label(input_frame, text="Name:")
name_entry = tk.Entry(input_frame)

content_label = tk.Label(input_frame, text="Content:")
content_entry = tk.Entry(input_frame)

ig_followers_label = tk.Label(input_frame, text="Instagram Followers(in M):")
ig_followers_entry = tk.Entry(input_frame)

ig_username_label = tk.Label(input_frame, text="Instagram Username:")
ig_username_entry = tk.Entry(input_frame)

tt_followers_label = tk.Label(input_frame, text="Twitter Followers(in M):")
tt_followers_entry = tk.Entry(input_frame)

tt_username_label = tk.Label(input_frame, text="Twitter Username:")
tt_username_entry = tk.Entry(input_frame)

yt_channel_label = tk.Label(input_frame, text="YouTube Channel:")
yt_channel_entry = tk.Entry(input_frame)

yt_subscribers_label = tk.Label(input_frame, text="YouTube Subscribers(in M):")
yt_subscribers_entry = tk.Entry(input_frame)

submit_button = tk.Button(input_frame, text="Submit", command=submit_info)


result_label = tk.Label(root, text="")
result_label.pack()

enter_info_button = tk.Button(root, text="Enter New Info", command=enter_info_mode, fg="Green", relief="raised",
                             border="2px", borderwidth="4px")
enter_info_button.pack(pady=5)

find_info_button = tk.Button(root, text="Find Info", command=find_info_mode, fg="red", relief="ridge",
                            border="2px", borderwidth="4px")
find_info_button.pack(pady=5)

root.mainloop()
