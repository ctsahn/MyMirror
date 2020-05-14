# MyMirror

This is a smart mirror software written entirely in Python!

Features include:

* Current date and time
* Calendar
* Latest news headlines (from https://news.google.com/)
* Latest NBA scores (from https://www.basketball-reference.com/). Note: I haven't been able to completely test this feature yet because the NBA season is currently suspended :(
* Current weather and weather forecast for the week (from https://openweathermap.org/)
* Automatically turns on display when a person is detected by the webcam
* Voice assistant that can show map images and zoom in/out(still a work in progress)
* Also plays a futuristic GIF, because why not

## Installation
Install dependencies with `sudo apt-get install libjasper-dev libqtgui4 libqt4-test libatlas-base-dev python3-pyaudio flac mpg321`. Then `cd` into this repo and run `pip3 install -r requirements.txt`. 

## Usage

**You will need enter your OpenWeatherMap API key and your location's latitude and longitude into `scraper.py`, and enter your Google Maps Static API key into `maps.py`.** The API keys can be acquired at https://home.openweathermap.org/users/sign_up and https://developers.google.com/maps/documentation/maps-static/get-api-key (for the map feature, you will need to sign up for Google Cloud, but I believe you get 100,000 free Maps Static API call per month). 

Run the smart mirror with `python3 gui.py`. (On the Raspberry Pi, you need to run `LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1 python3 gui.py`. More information about this here: https://github.com/piwheels/packages/issues/59)



<p float="left">
  <img src="https://i.imgur.com/6roGNox.jpg" width="400" />
  <img src="https://i.imgur.com/5UOKiA0.jpg" width="400" /> 
</p>

Please feel free to contribute to this project! This is my first time writing a decent-sized program in Python and working with multiple threads, so please let me know about any potential improvements I can make.
