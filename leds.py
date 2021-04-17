import board
import neopixel
import time

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
PIXEL_PIN = board.D18

# The number of NeoPixels
NUM_PIXELS = 20

BRIGHTNESS = 0.1
# Color palette
LIST_OF_COLORS = {
        "amber":(255,126,0), "white":(255, 255, 255), "almond":(239,222,205), "blue":(0, 0, 255), 
        "red":(255, 0, 0), "green":(0, 255, 0), "violet":(149,0,179), "moonshine_blue":(114,160,193),
        "rainbow":(0, 0, 0), "light_brown":(196,98,16), "sea_green":(59,122,87)
        }

pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS)

def leds_off():
    pixels.fill((0, 0, 0)) 
    
def leds_on():
    pixels.fill(LIST_OF_COLORS["amber"]) 
    
def turn_on_color(led_color):
    if led_color != "rainbow":
        pixels.fill(LIST_OF_COLORS[led_color])
    else:
        rainbow()

    
def rainbow():
    for i in range(NUM_PIXELS):
        pixel_index = (i * 256 // NUM_PIXELS)
        pixels[i] = wheel(pixel_index & 255)
    pixels.show()
        
        
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) 
        