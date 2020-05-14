"""
Responsible for running the entire display. Also handles some voice assistant features.
"""

import tkinter
import datetime

from time import strftime
from tkcalendar import Calendar
from PIL import Image, ImageTk
from _io import BytesIO
import speech_recognition

import maps
import animation
import sensor
import scraper
import threading
import speak
import config

myfont = "Shree Devanagari 714" # edit this to change font

window = tkinter.Tk()
window.attributes("-fullscreen", True)
window.option_add("*Background", "black")
window.option_add("*Foreground", "white")
window.config(bg="black")

style = tkinter.ttk.Style(window)
style.theme_use("clam") 

# define everything that will be constantly updated, so that new ones don't have to be created
fscores = tkinter.Frame(window)
fnews = tkinter.Frame(window)
fcal = tkinter.Frame(window)
fweather = tkinter.Frame(window)

timelabel = tkinter.Label(window, font=(myfont, 50), text=strftime(("%I:%M:%S %p")))
scoreslabel = tkinter.Label(fscores, font=(myfont, 15))
newslabel = tkinter.Label(fnews, font=(myfont, 15), wraplength=300, justify="right", text="")
daylabel = tkinter.Label(fcal, font=(myfont, 25))
datelabel = tkinter.Label(fcal, font=(myfont, 25))
cal = Calendar(fcal, font=(myfont, 15), locale="en_US", showweeknumbers=False, showothermonthdays=False, foreground="black", background="black", bordercolor="black", headersbackground="black", headersforeground="white", normalbackground="black", weekendbackground="black", normalforeground="white", weekendforeground="white", selectbackground="black", selectforeground="pink")
weatherarray = []

for i in range(0, 8):
    weatherarray.append(tkinter.Label(fweather, compound=tkinter.CENTER, font=(myfont, 25), fg="white", bg="black"))
    
maplabel = tkinter.Label(window)

# load gif
giflabel = animation.ImageLabel(window)
giflabel.load("mygif.gif")

check_gif = True  # True if the gif is currently being played
no_games = False  # True if there are no NBA games today

map_string = ["none"] 

zoom_level = 8  # initial zoom level for the Google Maps Static API. 

ai_off = None 


def time():
    
    timelabel.config(text=strftime(("%I:%M:%S %p")))
    
    # update calendar only at midnight
    if(strftime(("%I:%M:%S %p")) == "12:00:00 AM"):
        calendar()
        
    timelabel.after(1000, time)


def scores():
    
    # scraping web data takes some time, so use multithreading to avoid freezing the main thread
    scoresthread = threading.Thread(target=scraper.basketball)
    scoresthread.start()
    
    winners = config.winners
    losers = config.losers
    
    if len(winners) == 0:
        
        scoreslabel.config(text="No games today", font=(myfont, 30))
        scoreslabel.pack()
        
        global no_games
        if no_games == False:
            scoreslabel.after(1000, scores)  # check one more time after a short delay (in case of bad wifi)
            no_games = True
    else:
        
        teams = config.teams
        text = ""
        
        for i in range(0, len(winners)):
            
            for j in winners[i]:
                if j in teams:
                    text = text + teams[j] + "\t" 
                else:
                    text = text + j + "\t" 
            text = text + "\n"
            for k in losers[i]:
                if k in teams:
                    text = text + teams[k] + "\t"
                else:
                    text = text + k + "\t"
            text = text + "\n" + "\n"
        
        text = text.strip('\n')
        
        scoreslabel.config(text=text, font=(myfont, 15))
        scoreslabel.pack()
        scoreslabel.after(60000, scores)  # update scores every minute


def news():
    
    # scraping web data takes some time, so use multithreading to avoid freezing the main thread
    newsthread = threading.Thread(target=scraper.headlines)
    newsthread.start()
    newslist = config.news_list
    
    if len(newslist) == 0:
        newslabel.after(1000, news)  # check one more time after a short delay

    bigtext = ""
    
    for i in newslist:
        bigtext = bigtext + i + "\n" + "\n"
        
    bigtext = bigtext.strip()
    
    newslabel.config(text=bigtext)
    newslabel.pack(anchor="e")
    
    newslabel.after(600000, news)  # update every 10 minutes
    

def weather():
    degree_sign = u'\N{DEGREE SIGN}'
    
    # scraping web data takes some time, so use multithreading to avoid freezing the main thread
    weatherthread = threading.Thread(target=scraper.weather)
    weatherthread.start()
    
    if len(config.weather_list) == 0:
        window.after(1000, weather)
    
    counter = 0
    
    for i in config.weather_list:
        wtext = i[0].strip() + "\t" + str(i[1]) + degree_sign 
        
        # put day of week, weather image, and temperature on one line
        day = weatherarray[counter]
        img = ImageTk.PhotoImage(Image.open("weathericons/" + i[2] + "@2x.png").resize((30, 30), Image.ANTIALIAS))
        day.config(text=wtext, image=img)
        day.grid(column=0, row=counter)
        day.img = img
        counter = counter + 1
    
    window.after(3600000, weather)  # update every hour

    
def calendar():
    
    # day of week
    today = datetime.date.today()
    dtext = today.strftime("%A").strip()
    daylabel.config(text=dtext)
    
    # date
    daylabel.grid(column=0, row=0, sticky="w")
    ttext = today.strftime("%B %d, %Y")
    datelabel.config(text=ttext)
    datelabel.grid(column=0, row=1, sticky="w")
    
    # calendar
    cal.selection_set(datetime.date.today())
    cal.config(background="black")
    cal.grid(column=0, row=2)


def input(recognizer, audio):
    
    result = ""
    try:
        myspeech = recognizer.recognize_google(audio)
        result = myspeech
    except speech_recognition.UnknownValueError:
        result = []
    
    global map_string
    global zoom_level
    
    if "how are you" in result:
        speak.output("i am good.")  # used for testing audio
    
    elif "where" in result:
        
        map_string = maps.edit_result(result)  # get just the location string
        maps.get_map(map_string, zoom_level)  # get map image
        speak.output("showing where " + map_string + " is")
        show_map()
        
    # zoom in on displayed location
    elif "zoom in" in result:
        if map_string == ["none"]:
            speak.output("nothing to zoom in on")
            
        else:
            
            if zoom_level == 20 or zoom_level == 18:
                speak.output("can't zoom in any further")
                return
            
            if "completely" in result or "all the way" in result or "max" in result or "maximum" in result:
                speak.output("zooming in all the way")
                zoom_level = 18
            else:
                speak.output("zooming in on location")
                if zoom_level == 1:
                    zoom_level = 0
                zoom_level = zoom_level + 4
            
            maps.get_map(map_string, zoom_level)
            show_map()
            
    # zoom out on map
    elif "zoom out" in result:
        if map_string == ["none"]:
            speak.output("nothing to zoom out on")
            
        else:
            
            if zoom_level == 0 or zoom_level == 1:
                speak.output("can't zoom out any further")
                return
            
            if "completely" in result or "all the way" in result or "max" in result or "maximum" in result:
                speak.output("zooming out all the way")
                zoom_level = 1
            else:
                
                speak.output("zooming out")
                if zoom_level == 18:
                    zoom_level = 20
                zoom_level = zoom_level - 4
                
            maps.get_map(map_string, zoom_level)
            show_map()
            
    # hide map, show GIF
    elif "clear" in result or "hide" in result:
        speak.output("clearing screen")
        maplabel.place_forget()
        giflabel.place(relx=.5, rely=.5, anchor="center")
        global check_gif
        check_gif = True
        
        
def show_map():
    f = open("map.png", "rb")
    
    img = ImageTk.PhotoImage(Image.open(BytesIO(f.read())))
    maplabel.config(image=img)
    maplabel.img = img
        
    maplabel.place(x=window.winfo_width() / 2  , y=window.winfo_height() / 2, anchor="center")
    giflabel.place_forget()
    global check_gif
    check_gif = False  # GIF is no longer being played

    
def ai_on():
    
    """ from https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py"""
    r = speech_recognition.Recognizer()
    m = speech_recognition.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)  

    global ai_off
    ai_off = r.listen_in_background(m, input)  # call this method to shut down the voice assistant


def show():
    fscores.place(anchor="sw", relx=0, rely=1.0)
    fnews.place(anchor="se", relx=1, rely=1)
    fcal.place(anchor="nw", relx=0, rely=0)
    fweather.place(anchor="ne", relx=1.0, rely=0)
    timelabel.place(x=window.winfo_width() / 2  , anchor="n")
    
    if check_gif:
        giflabel.place(relx=.5, rely=.5, anchor="center")
    else:
        show_map()
    ai_on()

    
def hide():
    # make screen blank, turn off voice assistant
    ai_off(wait_for_stop=False)
    fscores.place_forget()
    fnews.place_forget()
    fcal.place_forget()
    fweather.place_forget()
    timelabel.place_forget()
    maplabel.place_forget()
    giflabel.place_forget()

    
def on_detect():

    if sensor.detect():
        show()
        start_loop()
        

def start_loop():
    window.after(60000, hide)  # after a minute, sleep
    window.after(60100, on_detect)  # turn on camera for detection

    
def init():

    scores()
    calendar()
    time()
    weather()
    news()
    

init()

window.after(1000, on_detect)
window.mainloop()
