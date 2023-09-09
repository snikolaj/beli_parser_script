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
    with open(filename + "." + fileformat, mode="wb") as file:
        file.write(response.content)

# HTML handler
def handle_html(filename):
    FILE_LOCATION = filename
    reqs = open(FILE_LOCATION, "r", encoding="utf8").read()
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
        print(style.CYAN + "\n\nAll instances of " + ss)
        f = open("URLs of all " + ss + " files.txt", "w")
        counter = 0
        for url in urls:
            if ss in url:
                counter += 1
                print(style.GREEN + url)
                f.write(url + os.linesep)
                download_file(url, url.split("/")[-1].split(".")[0], "." + ss)
        if counter == 0:
            print(style.RED + "No " + ss + " files were found")
            f.write("No " + ss + " files were found")
    


    print(style.WHITE)

root = tk.Tk()
root.title("HTML Open File Dialog - Ackfee6086")
root.resizable(False, False)
root.geometry("400x200")


def select_file():
    filetypes = (("HTML files", "*.html"),("Other files", "*.*"))
    filename = fd.askopenfilename(title="Open a file", initialdir="/", filetypes=filetypes)
    showinfo(title="Selected File", message=filename)
    handle_html(filename)
    root.destroy()


# open button
open_button = ttk.Button(root, text="Open the File", command=select_file)
open_button.pack(expand=True)

root.mainloop()
