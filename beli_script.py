# OS utilities
import sys
import os

# HTML parsing
from bs4 import BeautifulSoup

# download functionality
import requests

# filename handling
import re

# GUI
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# required system call for command line colors
os.system("")
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

# download function
def download_file(url, filename, fileformat):
    query_parameters = {"downloadformat": fileformat}
    response = requests.get(url, params=query_parameters)
    filename = re.sub(r'\W+', '', filename)
    write_to_file(filename + fileformat, response.content)

def write_to_file(filename, contents):
    """
    Writes contents to a file. If the file exists, adds a number to the end of the filename.
    If the file with the number exists, increments the number until a file by that name does not exist.
    """
    # Split the filename into its base and extension
    base, ext = os.path.splitext(filename)

    # If the file doesn't exist, write to it
    if not os.path.exists(filename):
        with open(filename, 'wb') as f:
            f.write(contents)
    else:
        # If the file exists, add a number to the end of the filename
        i = 1
        while True:
            new_filename = f"{base}_{i}{ext}"
            if not os.path.exists(new_filename):
                with open(new_filename, 'wb') as f:
                    f.write(contents)
                break
            i += 1

def print_tk_and_console(text_to_print):
    print(text_to_print)
    text_widget.insert(tk.END, text_to_print + '\n')
    text_widget.update()

# HTML handler
def handle_html(filename):
    FILE_LOCATION = filename
    reqs = open(FILE_LOCATION, "r", encoding="utf8").read()
    print_tk_and_console("Successfully opened file")
    soup = BeautifulSoup(reqs, "html.parser")
    urls = []
    substrings = ["mp3", "jpg", "jpeg", "png", "svg", "fla", "mp4", "gif", "xml", "wav", "json", "webp"]
    for link in soup.find_all('a'):
        temp = link.get('href')
        for ss in substrings:
            if ("." + ss) in temp:
                urls.append(temp)
                break

    for link in soup.find_all('source'):
        temp = link.get('src')
        for ss in substrings:
            if ("." + ss) in temp:
                urls.append(temp)
                break
    
    for link in soup.find_all('img'):
        temp = link.get('src')
        for ss in substrings:
            if ("." + ss) in temp:
                urls.append(temp)
                break


    for ss in substrings:
        print_tk_and_console("\n\nAll instances of " + ss)
        f = open("URLs of all " + ss + " files.txt", "w")
        counter = 0
        for url in urls:
            if ss in url:
                counter += 1
                print_tk_and_console(url)
                f.write(url + os.linesep)
                download_file(url, url.split("/")[-1].split(".")[0], "." + ss)
        if counter == 0:
            print_tk_and_console("No " + ss + " files were found")
            f.write("No " + ss + " files were found")


root = tk.Tk()
root.title("HTML File Extractor")
root.resizable(False, False)
root.geometry("768x256")


def select_file():
    filetypes = (("HTML files", "*.html"),("Other files", "*.*"))
    filename = fd.askopenfilename(title="Open a file", initialdir="/", filetypes=filetypes)
    showinfo(title="Selected File", message=filename)
    handle_html(filename)
    root.destroy()


# open button
open_button = ttk.Button(root, text="Open the File", command=select_file)
open_button.pack(expand=True)

text_widget = tk.Text(root)
text_widget.pack()

text_widget.insert(tk.END, "To extract and download all the files embedded in an HTML file, select it with the button above.\n")

root.mainloop()
