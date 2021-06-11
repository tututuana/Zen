import datetime
from dearpygui.core import *
from dearpygui.simple import *
import PyDictionary
import random
import re
import webbrowser
import wikipedia
from googlesearch import search
import pyperclip


dictionary = PyDictionary.PyDictionary()

def searchZen (query):

	query = query.lower()

	if query.split()[0] == "antonym":
		query = query.replace("antonym ", "", 1)
		query = query.replace(" ", "")

		antonyms = dictionary.antonym(query)
		output = ""

		for antonym in antonyms:
			output += antonym + "\n"
		
		return output

	if "define" in query:
		query = query.replace("define ", "")
		query = query.replace(" ", "")

		returnData = dictionary.meaning(query)
		output = ""

		for type, definition in returnData.items():
			for singleDefinition in definition:
				output += type + " | " + singleDefinition + "\n"

		return output

	if query.split()[0] == "synonym":
		query = query.replace("synonym ", "", 1)
		query = query.replace(" ", "")

		synonyms = dictionary.synonym(query)
		output = ""

		for synonym in synonyms:
			output += synonym + "\n"
		
		return output

	#Online

	if "wikipedia" in query:
		query = query.replace("wikipedia", "")
		
		return wikipedia.summary(query)
    
    
	if "r/" in query:
		query = re.sub(".*r\/", "", query)
		query = query.replace("_", "")
		webbrowser.open_new("https://www.reddit.com/r/" + query)
		return "Reddit page opened."


	if "google" in query:
		query = query.replace("google", "")
		for j in search(query, tld="co.in", num=10, stop=10, pause=2):
			return j

	if "browser" in query:
		query = query.replace("browser", "")
		webbrowser.open_new("https://google.com")
		return "Browser opened."
    
	#Temp

	if query == "what is the date" or query == "what's the date" or query == "date":
		date = datetime.datetime.now().strftime("%m/%d/%Y")

		return f"The date is {date}"

	if query == "what is the time" or query == "what's the time" or query == "what time is it" or query == "time":
		time = datetime.datetime.now().strftime("%H:%M:%S")

		return f"The time is {time}"

	#Misc

	if "roll a " in query and "sided dice" in query:
		query = query.replace("roll a ", "")
		query = query.replace("sided dice", "")

		return random.randint(1, int(query))

    

def searchHandle ():
	set_value("Output", "Loading...")
	set_value("Output", searchZen(get_value("Query")))

def copy():
	pyperclip.copy(get_value("Output"))

def clear():
	set_value("Output", "")
	
def openb():
	webbrowser.open_new(get_value("Output"))

set_main_window_resizable(False)
set_main_window_size(300, 575)
set_main_window_title("Zen")
set_theme("Dark 2")

set_style_window_rounding(0)

with window("Search Window", no_close = True, no_collapse = True, no_move = True, no_resize = True, width = 284, height = 268):
	add_input_text("Query", label = "", width = 267, on_enter = True, callback = searchHandle)
	add_button("Run", callback = searchHandle)
	add_button("Clear", callback = clear)
	add_button("Copy", callback = copy)
	add_button("Open", callback = openb)

with window("Results Window", no_close = True, no_collapse = True, no_move = True, no_resize = True, width = 284, height = 268):
	add_text("Output", wrap = 250)

set_window_pos("Search Window", 0, 0)
set_window_pos("Results Window", 0, 268)
set_value("Output", "Please Enter Query")

start_dearpygui()