from os import (makedirs, getcwd)
from sys import argv
from collections import deque
from requests import (get, codes)
from bs4 import (BeautifulSoup, SoupStrainer)
from colorama import (init, deinit)


class Browser:
    args = argv
    place = ""  # Filepath
    work = getcwd()

# Only one valid argument on command line --> Path for storage
    if len(args) != 2:
        print("Only the Path for storing as an argument")
    else:
        place = args[1]
        try:
            makedirs(place)
        except FileExistsError:
            print("Directory", place, "already exists")

    def __init__(self, name, short):
        self.name = name
        self.short = short
        self.history = deque()
        self.soup = ""
        self.raw = ""

# getting input
    def user_input(self, input_):
        self.name = input_

    def find_side(self):
        # checking stored files
        try:
            with open(f"{self.work}\\{self.place}\\{self.name}.txt", "r") as saved:
                for line in saved:
                    print(line)
            self.history.append(self.name)
        # or creating a short name + leading to getting content
        except OSError:
            if ".com" or ".org" or ".de" or ".info" in self.name:
                # creating short names for history and quikaccsess
                if self.name.startswith("http://www.") or self.name.startswith("https://www."):
                    self.short = self.name.split(".", 1)[1].rsplit(".", 1)[0]
                else:
                    self.short = self.name.rsplit(".", 1)[0]
                    if self.short.startswith("www"):
                        self.short = self.short.split(".", 1)[1]
                self.store_side()
            else:
                print("error: no file or URL")

    def go_back(self):
        try:
            self.name = self.history.pop()  # 2 x --> we want the one before the current
            self.name = self.history.pop()
            with open(f"{self.work}\\{self.place}\\{self.name}.txt", "r") as saved:
                for line in saved:
                    print(line)
            self.history.append(self.name)
        except IndexError:
            pass

    # getting online content
    def store_side(self):
        if self.name.startswith("http//"):
            pass
        else:
            self.name = f"http://{self.name}"
        if self.name.endswith(".com") or self.name.endswith(".org") or self.name.endswith(".de") or self.name.endswith(".info"):
            pass
        else:
            if self.name.endswith("com"):
                self.name = self.name.replace("com", ".com")
            elif self.name.endswith("org"):
                self.name = self.name.replace("org", ".org")
            elif self.name.endswith("org"):
                self.name = self.name.replace("de", ".de")
	    elif self.name.endswith("info"):
                self.name = self.name.replace("info", ".info")
        # reachable sides are stored
        headers = {'user-agent': 'Mozilla/5.0'}
        try:
            raw_side = get(self.name, headers=headers)
            if raw_side.status_code == codes.ok:
                self.pretty_side(raw_side)
                self.history.append(self.short)
        except Exception:
            print("error: cant get site")
            return None


    # make the html readable and storing it for later
    def pretty_side(self, http):
        wanted = ['p', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        soup = BeautifulSoup(http.content, 'html.parser', parse_only=SoupStrainer(wanted))
        links = soup.find_all("a")
        for i in links:
            i.insert_before("\033[34m")
            i.insert_after("\033[39m")
        with open(f"{self.work}\\{self.place}\\{self.short}.txt", "w", encoding="utf-8") as temp_txt:
            for string in soup.stripped_strings:
                temp_txt.write(string + "\n")
                print(string)


if __name__ == "__main__":
    my_browser = Browser("", "")
    init()
    while True:
        if my_browser.user_input(input("enter a saved file, URL, back or exit: ")):
            continue
        elif my_browser.name == "exit":
            deinit()
            break
        elif my_browser.name == "back":
            my_browser.go_back()
        else:
            my_browser.find_side()
