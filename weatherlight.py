#!/usr/bin/env python3
# Author: Elise Swepston (eswepston@gmail.com)
#
# Made to be paired with an adressable LED light strip of 16 lights and a RPi
#
# This version of the program goes from 10 to 100 degrees

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
    elif max < 10:
        # If temp is under 10, set to really purple
        setSectionColor(strip, Color(78, 0, 101), 105, 156)
    else:
        # Call setSectionColor and pass in the RGB values from above plus the top section of lights
        setSectionColor(strip, Color(red, green, blue), 105, 156)


# Sets the color of the min temp for the day (the bottom 3rd of the light)
def setMinColor(strip):
    # Call the API and get the weathe data for Charlotte NC
    response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=35.2271&lon=-80.8431&exclude=minutely,hourly,alerts&appid=acfb681bde372f01b30270ea86ad61ca&units=imperial")
    
        # FOR DEV AND PROBLEMS: this allows you to get the API returned with a nice layout so you can adjust it later
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
    elif min < 10:
        # If temp is under 10, set to really purple
        setSectionColor(strip, Color(78, 0, 101), 0, 52)
    else:
        # Call setSectionColor and pass in the RGB values from above plus the top section of lights
        setSectionColor(strip, Color(red, green, blue), 0, 52)


# sets the color of the current temp (the middle 3rd of the light)
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
    elif current < 10:
        # If temp is under 10, set to really purple
        setSectionColor(strip, Color(78, 0, 101), 54, 104)
    else:
        # Call setSectionColor and pass in the RGB values from above plus the top section of lights
        setSectionColor(strip, Color(red, green, blue), 54, 104)

  
# Full switch - sets the color based on the rounded temp. Anything from 10 to 100 degrees
switcher = {
        10: '102 0 134',
        11: '99 4 136',
        12: '95 12 141',
        13: '91 20 146',
        14: '86 27 150',
        15: '82 34 154',
        16: '78 42 159',
        17: '73 50 164',
        18: '69 57 168',
        19: '65 64 173',
        20: '60 72 177',
        21: '55 79 182',
        22: '51 87 186',
        23: '47 94 190',
        24: '43 102 195',
        25: '38 109 199',
        26: '34 116 204',
        27: '30 123 208',
        28: '26 131 213',
        29: '22 139 218',
        30: '17 146 222',
        31: '13 153 226',
        32: '8 161 231',
        33: '4 168 235',
        34: '0 176 239',
        35: '1 179 231',
        36: '2 183 223',
        37: '3 187 213',
        38: '4 190 204',
        39: '5 193 169',
        40: '6 197 187',
        41: '7 200 179',
        42: '8 204 169',
        43: '9 207 160',
        44: '10 210 152',
        45: '11 214 143',
        46: '12 218 134',
        47: '13 221 125',
        48: '14 224 116',
        49: '15 228 108',
        50: '16 231 99',
        51: '17 235 90',
        52: '18 239 81',
        53: '19 242 73',
        54: '20 245 64',
        55: '21 249 55',
        56: '22 252 47',
        57: '25 255 39',
        58: '39 255 37',
        59: '51 255 35',
        60: '64 255 33',
        61: '76 255 31',
        62: '88 255 28',
        63: '102 255 26',
        64: '115 255 24',
        65: '128 255 22',
        66: '140 255 20',
        67: '154 255 17',
        68: '166 255 15',
        69: '179 255 13',
        70: '191 255 11',
        71: '204 255 9',
        72: '217 255 6',
        73: '230 255 4',
        74: '242 255 2',
        75: '245 254 0',
        76: '255 246 0',
        77: '255 238 0',
        78: '245 230 0',
        79: '245 222 0',
        80: '245 214 0',
        81: '245 206 0',
        82: '245 198 0',
        83: '253 190 0',
        84: '253 182 0',
        85: '253 174 0',
        86: '253 166 0',
        87: '253 159 0',
        88: '252 149 0',
        89: '252 142 0',
        90: '250 132 0',
        91: '247 119 0',
        92: '244 107 0',
        93: '240 93 0',
        94: '236 81 0',
        95: '233 68 0',
        96: '229 56 0',
        97: '225 43 0',
        98: '222 30 0',
        99: '219 18 0',
        100: '166 0 0'
        
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
                # Clear the whole thing and reset max and min
                colorWipe(strip, Color(255, 255, 255))
                time.sleep(1)
                setMaxColor(strip)
                setMinColor(strip)
                
            # Set the middle 3rd to the current temp then loop after 5 minutes 
            setCurrentColor(strip)
            time.sleep(300)
            

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
