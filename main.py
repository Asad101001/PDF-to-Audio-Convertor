import pyttsx3                                  #pyttsx3: Python Text-to-Speech module. Converts text into audio using system's speech engine (offline).
from PyPDF2 import PdfReader                    #PdfReader from PyPDF2: Allows you to read .pdf files and extract text from them.
from tkinter.filedialog import askopenfilename  #askopenfilename: Opens a file dialog to let the user select a file from their system.
import os                                       #Required for checking file existence with os.path.exists("bookmark.txt"). This supports the bookmark/resume feature by managing the saved file.

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

# BOOKMARK LOAD (if exists)
if os.path.exists("bookmark.txt"):            #os.path.exists(...) checks if bookmark.txt exists.
    with open("bookmark.txt", "r") as bm:     #If it exists, opens the file and reads the last saved page number.
        last = bm.read()
        print(f"Last read page: {last}")
    resume = input("Resume from last page? (y/n): ").lower() #Asks the user if they want to resume from that page.
    start_page = int(last) if resume == 'y' else int(input(f"Enter start page (0 to {pages-1}):"))
else:
    start_page = int(input(f"Enter start page (0 to {pages-1}):")) #If not, asks for manual input of start_page.

end_page = int(input(f"Enter end page ({start_page} to {pages-1}):"))

# SEARCH MODE OPTION
search_mode = input("Search for a keyword in PDF? (y/n): ").lower()
if search_mode == 'y':
    keyword = input("Enter keyword to search: ").lower()
    for num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and keyword in text.lower():
            print(f"\n-- READING PAGE {num} (contains '{keyword}') --")
            engine.say(text)
            engine.runAndWait()
else:
    for num in range (start_page, end_page+1):     #Simple iteration ranging from 0 to pages-1
        page = reader.pages [ num ]                #Finds exact current page in the loop
        text = page.extract_text ()                #Extaction of text contents from the PDF page (not possible if PDF is image-based)
        if text:                                   #EXCEPTION HANDLING : Avoid speaking empty pages (pages without extractable text -> images)
            print(f"\n-- READING PAGE {num} --")
            engine.say (text)                      #Readies the text for speech
            engine.runAndWait ()                   #Executes speech and waits for all the readied text to finish before moving onto next page

        # BOOKMARK SAVE
        with open("bookmark.txt", "w") as bm:
            bm.write(str(num))

# OPTION TO SAVE TO MP3
save_audio = input("Do you want to save the spoken text as an MP3 file? (y/n): ").lower()
if save_audio == 'y':
    output_file = input("Enter output filename (with .mp3 extension): ")
    full_text = ""
    for num in range(start_page, end_page + 1):
        page = reader.pages[num]
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    if full_text.strip():
        engine.save_to_file(full_text, output_file)
        engine.runAndWait()
        print(f"Saved audio to: {output_file}")
    else:
        print("No text found in selected pages. Nothing saved.")
