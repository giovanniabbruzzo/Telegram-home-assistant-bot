#!/usr/bin/python3
from telegram.ext import Updater, CommandHandler
from  telegram import Bot
import logging
import time
import dht22_drivers as dht
import leds
import global_settings as gs
import schedule
from threading import Thread
from private import TOKEN, ALLOWED_IDS

"""
This script needs to be run with "sudo python3"
List of commands this far:
    temperature - Used to read the current temperature
    humidity - Used to read the humidity
    leds_on - Turn the LEDs on
    leds_off - Turn the LEDs off
    leds_color - Turn on the LEDs with a specific color, send color after the command. For complete list of colors see command "/what_colors"
    what_colors - Receive the list of all the color available for the LEDs
"""

def start(update, context):
    """
        Send the welcome message
    """
    chat_id=update.effective_chat.id
    if chat_id in ALLOWED_IDS:
        msg="Welcome to the pi_control_bot, how can I help you?"
        context.bot.send_message(chat_id, text=msg)
        
def temperature(update, context):
    """
        Read the temperature
    """
    chat_id=update.effective_chat.id
    if chat_id in ALLOWED_IDS:
        temperature = dht.getTemp()
        msg = "The current temperature is {} °C".format(temperature)
        context.bot.send_message(chat_id, text=msg)  

def send_message(msg, chat_id):
	"""
        	Send a mensage to a telegram user specified on chatId
            t_id must be a number!
	"""
	bot = Bot(token=TOKEN)
	bot.sendMessage(chat_id=chat_id, text=msg)

def leds_off(update, context):
    """
       Turn the LEDs off
    """
    chat_id=update.effective_chat.id
    if chat_id in ALLOWED_IDS:
        leds.leds_off()
        msg = "The LEDs have been turned off!"
        context.bot.send_message(chat_id, text=msg)  
        
def leds_on(update, context):
    """
       Turn the LEDs off
    """
    chat_id=update.effective_chat.id
    if chat_id in ALLOWED_IDS:
        leds.leds_on()
        msg = "The LEDs have been turned on!"
        context.bot.send_message(chat_id, text=msg) 
	
    
def humidity(update, context):
    """
        Read the humidity
    """
    chat_id=update.effective_chat.id
    if chat_id in ALLOWED_IDS:
        hum = dht.getHum()          
        msg = "The current humidity is {} %".format(hum)
        context.bot.send_message(chat_id, text=msg)  

def leds_color(update, context):    
    """
        Turn on the LED using the color sent with the arguments
    """
    chat_id=update.effective_chat.id
    if chat_id in ALLOWED_IDS:
        if len(context.args) > 0 and context.args[0].lower() in list(leds.LIST_OF_COLORS.keys()):
            led_color = context.args[0].lower()
        else:
            print("Color not recognized, used default color!\n")
            led_color = "amber"
        leds.turn_on_color(led_color)
        msg = f"LED color {led_color} turned on"
        context.bot.send_message(chat_id, text=msg)  
        
def what_colors(update, context):
    """
        Send the names of all the colors available
    """
    chat_id=update.effective_chat.id
    if chat_id in ALLOWED_IDS:
        colors = "\n"
        for i in leds.LIST_OF_COLORS:
            colors+="- "+i+"\n"
        msg = f"List of colors: {colors}"
        context.bot.send_message(chat_id, text=msg)  

    
def morning_routine():
    """
        If it's time to wake up turn on LEDs and send the morning routing to the bot
    """
#    leds.leds_on()
    # Send the good morning
    msg = f"Morning, the current temperature is {dht.getTemp()}C and humidity {dht.getHum()}% !"
    # Send just to Gio
    send_message(msg, ALLOWED_IDS[0])
    
def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(30)
    
def routine_sensor_reading():
    ''' 
        Read the temperature and check if it's below the threshold
    '''
    temp = dht.getTemp()
    if temp < gs.MIN_TEMPERATURE_ALERT:
        print("Sending alert temperature!")
        msg = "ALERT: temperature under {} °C! You might wanna turn on the heating!".format(gs.MIN_TEMPERATURE_ALERT)
        # Send it to all the the IDs in the list
        for chat_id in ALLOWED_IDS:
            send_message(msg, chat_id)
            
def ledOn():
    leds.leds_on()
    
def ledOff():
    leds.leds_off()

def main():
    """
        Main bot loop
    """    
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher # Inrtoduce the dispacher locally
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO) # Set up the logging 
    # Define the different handlsers
    start_handler = CommandHandler('start', start)
    temperature_handler = CommandHandler('temperature', temperature)
    humidity_handler = CommandHandler('humidity', humidity)
    led_off_handler = CommandHandler('leds_off', leds_off)
    led_on_handler = CommandHandler('leds_on', leds_on)
    leds_color_handler = CommandHandler('leds_color', leds_color, pass_args=True)
    what_colors_handler = CommandHandler('what_colors', what_colors)
    handlers = [start_handler, temperature_handler, humidity_handler,led_off_handler,led_on_handler,leds_color_handler,what_colors_handler]
    for i in handlers:
        dispatcher.add_handler(i)
        
        # Create the job in schedule.
    schedule.every().day.at("08:45").do(morning_routine)
    schedule.every().day.at("18:30").do(ledOn)
    schedule.every().day.at("00:30").do(ledOff)

    # Spin up a thread to run the schedule check so it doesn't block your bot.
    # This will take the function schedule_checker which will check every second
    # to see if the scheduled job needs to be ran.
    Thread(target=schedule_checker).start() 
    
    # Run until Cntrl+c is typed 
    updater.start_polling()
    
    print("Bot up and running...Press Cntrl+C to power down!")
#    try:
    while True:
#            current_date = time.localtime(time.time())
#            if (current_date.tm_hour - gs.ALARM_TIME["h"]) == 0:
#                while (current_date.tm_min - gs.ALARM_TIME["m"]) != 0:
#                    time.sleep(59) # Sleep for 59 seconds
#                morning_routine()
#            else:
#                routine_sensor_reading()
#                # Sleep
#                time.sleep(60*gs.MINUTES_BETWEEN_READS)
            routine_sensor_reading()
            # Sleep
            time.sleep(60*gs.MINUTES_BETWEEN_READS)

#    except KeyboardInterrupt:
#        updater.stop()
#        print("The bot has been stopped...")
#    except Exception as e:
#        print(f"Execption: {e} catched")
        
if __name__=="__main__":
    main()
