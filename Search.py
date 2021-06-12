import datetime
from dearpygui.core import *
from dearpygui.simple import *
import json
import os
import PyDictionary
import pyperclip
import random
import re
import requests
import subprocess
import time
import webbrowser
import wikipedia
import win10toast
import wolframalpha
from googlesearch import search

functionalityData = json.load(open("data/functionalityData.json"))
preprocessingData = json.load(open("data/preprocessingData.json"))

dictionary = PyDictionary.PyDictionary()
wolfram = wolframalpha.Client(functionalityData["wolfram_key"])

def searchZen (query):
	# Query Pre-processing

	query = query.lower()

	for contraction, expansion in preprocessingData["contractions"].items():
		query = query.replace(contraction, expansion)

	query = re.sub(r'[^\w\s]','', query)

	# Antonyms, Definitions, Synonyms, and Translations

	if query.split()[0] == "antonym":
		query = query.replace("antonym ", "", 1)
		query = query.replace(" ", "")

		antonyms = dictionary.antonym(query)
		output = ""

		for antonym in antonyms:
			output += antonym + "\n"
		
		return output

	if query.split()[0] == "define":
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

	# Online Connections

	if "wikipedia" in query:
		query = query.replace("wikipedia", "")
		
		return wikipedia.summary(query)

	if "wolfram" in query:
		query = query.replace("wolfram alpha", "")
		query = query.replace("wolfram", "")

		response = wolfram.query(query)

		return next(response.results).text

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

	# Temporal

	if query == "what is the date" or query == "what's the date" or query == "date":
		date = datetime.datetime.now().strftime("%m/%d/%Y")

		return f"The date is {date} (MM/DD/YYYY)"

	if query == "what is the time" or query == "what's the time" or query == "what time is it" or query == "time":
		time = datetime.datetime.now().strftime("%H:%M:%S")

		return f"The time is {time}"

	# Miscellanous

	if "roll a " in query and "sided dice" in query:
		query = query.replace("roll a ", "")
		query = query.replace("sided dice", "")

		return random.randint(1, int(query))
	
	# Easter Eggs

	if query == "what is your name":
		return "Zen"
	
	if query == "who made you":
		return "Brian Nguyen"

	if query == "what gender are you":
		return "Animals and Spanish words have genders. I do not."

	if query == "answer to life" or query == "answer to the universe" or query == "answer to everything":
		return "42 - The Hitchhiker's Guide to the Galaxy"

	if query == "i am sad" or query == "i am so sad":
		if random.randint(0, 1) == 0:
			return "I prescribe hot chocolate and Netflix."
		else:
			return "Instant cure for sadness: look up pictures of cats while eating ice cream."

def searchHandle ():
	set_value("Output", "Loading...")
	set_value("Output", searchZen(get_value("Query")))

def copyOutput ():
	pyperclip.copy(get_value("Output"))

def clear():
	set_value("Output", "Please Enter Query")

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
	add_button("Copy Result", callback = copyOutput)
	add_button("Clear Result", callback = clear)
	add_button("Open Result", callback = openb)

with window("Results Window", no_close = True, no_collapse = True, no_move = True, no_resize = True, width = 284, height = 268):
	add_text("Output", wrap = 250)

set_window_pos("Search Window", 0, 0)
set_window_pos("Results Window", 0, 268)
set_value("Output", "Please Enter Query")

start_dearpygui()