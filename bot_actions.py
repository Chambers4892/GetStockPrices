import discord
import traceback
import datetime
import time
import pandas as pd
from datetime import datetime
import tabulate
import numpy
import constants
import backend
import analytics
import functions
import database_actions
import os
import sys
import json

#SEND_ALERT---------------------------------------------------------
async def send_alert(client, msg_txt):
    print("Attempting alert: " + id + ", " + msg_txt)
    file = open("mail_list.txt", "r")
    ids = file.read().split("/n")
    for id in ids:
        print(id)
        try:
            user = await client.fetch_user(id)
            print(user)
            await user.send(msg_txt)  
        except:
            print("Error with user: " + id)
            #traceback.print_exc()

#SEND_MESSAGE---------------------------------------------------------
async def send_message(client, id, msg_txt):
    print("Attempting message: " + str(id) + ", " + msg_txt)
    try:
        user = await client.fetch_user(id)
        await user.send(msg_txt)  
        print("Success: " + str(user))
    except:
        functions.error_handler(client, "Messaging: " + str(id), "send_message")





#DISPLAY STOCKS.CSV----------------------------------------
async def display_stocks(client, message, full_df):
    #Style name, id, stock, above_below, value, note, time_notified, triggered
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    parsed = message.content.split(' ')
    parsed.pop(0)
    if len(parsed) == 2:
        if parsed[0].upper() in constants.acronym_list and parsed[1].isnumeric():
            ranges = analytics.get_stock_range(full_df, parsed[0].upper(), int(parsed[1]))
            await message.reply("```\n " 
              + json.dumps(ranges) + 
              " \n```")
        else:
            ranges = analytics.get_ranges(full_df, int(parsed[1]))
            await message.reply("Stock Ranges:\n```\n" + ranges.to_string(index=False) + "\n```")
    else:   
        file = open("stocks.csv", "r")
        df = pd.read_csv(file)
        file.close()
        await message.reply("```\n " + df.to_string(index=False) + " \n```")



async def bug_report(client, message, function):
    fTime = datetime.utcnow()
    line = str(fTime) + message.content + "\n"
    print(line)
    file = open("error.txt", "a")
    file.write(line)
    file.close
    send_message(client, "226030188733923328", message.content)
    
