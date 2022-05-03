#!/usr/bin/env python3
# Author: Elise Swepston (eswepston@gmail.com)
#
# Made to be paired with an adressable LED light strip of 16 lights and a RPi
#
# This version of the program goes from 50 to 100 degrees so that it looks better durin warmer temps



import time
import datetime
from rpi_ws281x import PixelStrip, Color
import argparse
import requests
import json

# LED strip configuration:
LED_COUNT = 156        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def demo(strip, wait_ms=50, iterations=10):
    # Set the top to a 100
    for j in range(iterations):
        for q in range(3):
            for i in range(105, 156, 1): #(start, stop, step)
                strip.setPixelColor(i + q, Color(216, 9, 0))
            strip.show()
            
    # Set low to 50 
    for j in range(iterations):
        for q in range(3):
            for i in range(0, 52, 1): #(start, stop, step)
                strip.setPixelColor(i + q, Color(45, 0, 59))
            strip.show()
    
    time.sleep(1)
    c=50
    # Raise current color
    while c < 100:
        for j in range(iterations):
            for q in range(3):
                for i in range(54, 104, 1): #(start, stop, step)
                    
                    # Get the color values as a sting in form 'red green blue'
                    str = setTempColor(c)
                    str = str.split( ) # Split the sting into an array by the spaces
    
                    # Seperate it into the color values and store. Have to convert the string to an int.
                    red = int(str[0])
                    green = int(str[1])
                    blue = int(str[2])
                    
                    strip.setPixelColor(i + q, Color(red, green, blue))
                strip.show()
        c = c+1
        
        c=100
        
    # Lower current color
    while c > 50:
        for j in range(iterations):
            for q in range(3):
                for i in range(54, 104, 1): #(start, stop, step)
                    
                    # Get the color values as a sting in form 'red green blue'
                    str = setTempColor(c)
                    str = str.split( ) # Split the sting into an array by the spaces
    
                    # Seperate it into the color values and store. Have to convert the string to an int.
                    red = int(str[0])
                    green = int(str[1])
                    blue = int(str[2])
                    
                    strip.setPixelColor(i + q, Color(red, green, blue))
                strip.show()
        c = c-1
                   
        
# Whipes the color to whatever the passed in color is
def colorWipe(strip, color, wait_ms=30):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

# Changes the section color to a passed in color Color(R,G,B) and a start and stop node on the LED
def setSectionColor(strip, color, start, stop, wait_ms=50, iterations=10):

    for j in range(iterations):
        for q in range(3):
            for i in range(start, stop, 1): #(start, stop, step)
                strip.setPixelColor(i + q, color)
            strip.show()
            

# Sets the color of the max temp for the day (the top 3rd of the light)            
def setMaxColor(strip):
    # Call the API and get the weather data for Charlotte NC
    response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=35.2271&lon=-80.8431&exclude=minutely,hourly,alerts&appid=acfb681bde372f01b30270ea86ad61ca&units=imperial")
    
        # FOR DEV AND PROBLEMS: this allows you to get the API returned with a nice layout so you can adjust it later
    #text = json.dumps(response.json(), sort_keys=True, indent=4)
    #print(text)
    
    # Get the max tempeutres for the day and round to the nearest whole number - each [] is a layer in the json
    max = round(response.json()['daily'][0]['temp']['max'])
    
    # Get the color values as a sting in form 'red green blue'
    str = setTempColor(max)
    str = str.split( ) # Split the sting into an array by the spaces
    
    # Seperate it into the color values and store. Have to convert the string to an int.
    red = int(str[0])
    green = int(str[1])
    blue = int(str[2])
    
    
    if max > 100:
        # If temp is over 100, set to really red
        setSectionColor(strip, Color(166, 0, 0), 105, 156)
    elif max < 50:
        # If temp is under 10, set to really purple
        setSectionColor(strip, Color(78, 0, 101), 105, 156)
    else:
        # Call setSectionColor and pass in the RGB values from above plus the top section of lights
        setSectionColor(strip, Color(red, green, blue), 105, 156)


# sets the color of the min temp for the day (the bottom 3rd of the light)
def setMinColor(strip):
    # Call the API and get the weathe data for Charlotte NC
    response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=35.2271&lon=-80.8431&exclude=minutely,hourly,alerts&appid=acfb681bde372f01b30270ea86ad61ca&units=imperial")
    
        #FOR DEV AND PROBLEMS: this allows you to get the API returned with a nice layout so you can adjust it later
    #text = json.dumps(response.json(), sort_keys=True, indent=4)
    #print(text)
    
    # Get the min tempeutres for the day and round to the nearest whole number
    min = round(response.json()['daily'][0]['temp']['min'])
    
    # Get the color values as a sting in form 'red green blue'#Get the color values
    str = setTempColor(min)
    str = str.split( ) # Split the sting into an array by the spaces
    
    # Seperate it into the color values and store. Have to convert the string to an int.
    red = int(str[0])
    green = int(str[1])
    blue = int(str[2])
    
    
    if min > 100:
        # If temp is over 100, set to really red
        setSectionColor(strip, Color(166, 0, 0), 0, 52)
    elif min < 50:
        # If temp is under 10, set to really purple
        setSectionColor(strip, Color(78, 0, 101), 0, 52)
    else:
        # Call setSectionColor and pass in the RGB values from above plus the top section of lights
        setSectionColor(strip, Color(red, green, blue), 0, 52)


# Sets the color of the current temp (the middle 3rd of the light)
def setCurrentColor(strip):
    # Call the API and get the weathe data for Charlotte NC
    response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=35.2271&lon=-80.8431&exclude=minutely,hourly,alerts&appid=acfb681bde372f01b30270ea86ad61ca&units=imperial")#call the API and get the info then set it
    
    # Get the min tempeutres for the day and round to the nearest whole number
    current = round(response.json()['current']['temp'])
    
    # Get the color values as a sting in form 'red green blue'#Get the color values
    str = setTempColor(current)
    str = str.split( ) # Split the sting into an array by the spaces
    
    # Print out so that it can actually be seen working in the terminal
    print("This is the Currect Temp")
    print(current)
    
    # Seperate it into the color values and store. Have to convert the string to an int.
    red = int(str[0])
    green = int(str[1])
    blue = int(str[2])
    
    
    if current > 100:
        # If temp is over 100, set to really red
        setSectionColor(strip, Color(166, 0, 0), 54, 104)
    elif current < 50:
        # If temp is under 10, set to really purple
        setSectionColor(strip, Color(78, 0, 101), 54, 104)
    else:
        # Call setSectionColor and pass in the RGB values from above plus the top section of lights
        setSectionColor(strip, Color(red, green, blue), 54, 104)

  
# Full switch - sets the color based on the rounded temp. Anything from 10 to 100 degrees
switcher = {
        50: '45 0 59',
        51: '96 10 140',
        52: '88 24 148',
        53: '80 37 156',
        54: '72 51 165',
        55: '65 64 173',
        56: '57 77 181',
        57: '49 90 179',
        58: '42 104 197',
        59: '33 118 205',
        60: '26 131 213',
        61: '18 145 221',
        62: '10 158 229',
        63: '3 171 237',
        64: '1 180 229',
        65: '3 187 213',
        66: '5 193 198',
        67: '7 199 182',
        68: '9 205 165',
        69: '10 211 150',
        70: '12 218 134',
        71: '14 224 118',
        72: '16 230 102',
        73: '18 236 86',
        74: '19 243 74',
        75: '21 249 55',
        76: '25 255 39',
        77: '45 255 36',
        78: '69 255 31',
        79: '92 255 28',
        80: '115 255 24',
        81: '138 255 20',
        82: '160 255 16',
        83: '184 255 12',
        84: '207 255 8',
        85: '230 255 4',
        86: '253 255 0',
        87: '255 242 0',
        88: '254 227 0',
        89: '254 212 0',
        90: '254 198 0',
        91: '253 183 0',
        92: '253 169 0',
        93: '252 155 0',
        94: '252 141 0',
        95: '246 118 0',
        96: '240 96 0',
        97: '234 73 0',
        98: '228 50 0',
        99: '221 28 0',
        100: '216 9 0'
        
        }

def setTempColor(temp):
    return switcher.get(temp, '255, 255, 255')


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
    
    try:
        
        # Turn on and set everything to white then hold for 3 seconds
        colorWipe(strip, Color(255, 255, 255))
        time.sleep(3)
        
        # Set up on start
        setMaxColor(strip)
        setCurrentColor(strip)
        setMinColor(strip)
        
        while True: # This will run until the ctrl + c command is given
            
            # Get the current time
            now = datetime.datetime.now()
            
            # Check if new day and reset colors if it is
            if now.hour == 0: #0 is 1 am
                #Clear the whole thing and reset max and min
                colorWipe(strip, Color(255, 255, 255))
                time.sleep(1)
                setMaxColor(strip)
                setMinColor(strip)
                
            # Set the middle 3rd to the current temp then loop after 5 minutes 
            setCurrentColor(strip)
            time.sleep(300)
            
            #demo
            #colorWipe(strip, Color(255, 255, 255), 10)
            #time.sleep(3)
            #demo(strip)
            #time.sleep(3)
            #colorWipe(strip, Color(255, 255, 255), 10)
            #time.sleep(10)
            #colorWipe(strip, Color(0, 0, 0), 10)
            #time.sleep(10)
            

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
