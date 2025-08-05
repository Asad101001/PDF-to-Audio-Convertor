import pyttsx3                                  #pyttsx3: Python Text-to-Speech module. Converts text into audio using system's speech engine (offline).
from PyPDF2 import PdfReader                    #PdfReader from PyPDF2: Allows you to read .pdf files and extract text from them.
from tkinter.filedialog import askopenfilename  #askopenfilename: Opens a file dialog to let the user select a file from their system.
import os

pdf = askopenfilename ()                       #Opens a file selection windows and stores file path of the PDF in 'pdf' variable
reader = PdfReader (pdf)                       #Initializes PdfReader as 'reader' and loads the file into memory for access
pages = len (reader.pages)                     # reader.pages -> list so len() just gives total number of messages

engine = pyttsx3.init ()                       #Initialzes text-to-speech engine as object 'engine' which controls speech functionality

#VOICE SELECTION
voices = engine.getProperty('voices')
print("Available voices:")
for i , voice in enumerate(voices):
    print(f"{i}: {voice.name} ({voice.languages})")
choice =   int(input("Select voice number:"))
engine.setProperty('voice',voices[choice].id)  # 0 -> Male , 1 -> Female

#RATE AND VOLUME CONTROL
rate = int(input("Enter speech rate (default is ~200): "))
volume = float(input("Enter volume (0.0 to 1.0): "))
engine.setProperty('volume', volume)           #Volume level
engine.setProperty('rate', rate)               #Rate of Speech

start_page = int(input(f"Enter start page (0 to {pages-1}):"))
end_page = int(input(f"Enter end page ({start_page} to {pages-1}):"))


for num in range (start_page, end_page+1):     #Simple iteration ranging from 0 to pages-1
    page = reader.pages [ num ]                #Finds exact current page in the loop
    text = page.extract_text ()                #Extaction of text contents from the PDF page (not possible if PDF is image-based)
    if text:                                   #EXCEPTION HANDLING : Avoid speaking empty pages (pages without extractable text -> images)
            print(f"\n-- READING PAGE {num} --")
            engine.say (text)                  #Readies the text for speech
            engine.runAndWait ()               #Executes speech and waits for all the readied text to finish before moving onto next page
