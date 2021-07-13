import datetime
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
import dearpygui.dearpygui as dpg

functionalityData = json.load(open("data/functionalityData.json"))
preprocessingData = json.load(open("data/preprocessingData.json"))

dictionary = PyDictionary.PyDictionary()
wolfram = wolframalpha.Client(functionalityData["wolfram_key"])

# generate uuids (just to go with your existing code)
query_id = dpg.generate_uuid()
output_id = dpg.generate_uuid()


def searchZen(query):
    # Query Pre-processing

    query = query.lower()

    for contraction, expansion in preprocessingData["contractions"].items():
        query = query.replace(contraction, expansion)

    query = re.sub(r'[^\w\s]', '', query)

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


def searchHandle():
    dpg.set_value(output_id, "Loading...")
    dpg.set_value(output_id, searchZen(dpg.get_value(query_id)))


def copyOutput():
    pyperclip.copy(dpg.get_value(output_id))


def clear():
    dpg.set_value(output_id, "Please Enter Query")


def openb():
    webbrowser.open_new(dpg.get_value(output_id))


with dpg.window(label="Search Window", pos=[0, 0], no_close=True, no_collapse=True, no_move=True, no_resize=True, width=284, height=268):
    dpg.add_input_text(label="", width=267, on_enter=True, callback=searchHandle, id=query_id)
    dpg.add_button(label="Run", callback=searchHandle)
    dpg.add_button(label="Copy Result", callback=copyOutput)
    dpg.add_button(label="Clear Result", callback=clear)
    dpg.add_button(label="Open Result", callback=openb)

with dpg.window(label="Results Window", pos=[0, 268], no_close=True, no_collapse=True, no_move=True, no_resize=True, width=284, height=268):
    dpg.add_text("Output", wrap=250 , id=output_id)

dpg.set_value(output_id, "Please Enter Query")

dpg.setup_viewport()
dpg.set_viewport_resizable(False)
dpg.set_viewport_width(300)
dpg.set_viewport_height(575)
dpg.set_viewport_title("Zen")
dpg.start_dearpygui()