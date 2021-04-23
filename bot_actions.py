import discord
import traceback
import datetime
import time
import pandas as pd
from datetime import datetime
import tabulate
import numpy
import constants

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
        print(user)
        await user.send(msg_txt)  
    except:
        error_handler(client, "Messaging: " + str(id), "send_message")

#HELP TEXT---------------------------------------------------------
async def help_text(client, message):
    try:
        await message.reply(constants.help_text)
    except:
        error_handler(client, message, "help_text")

#REGISTER NEW NOTIFICATION----------------------------------------
async def register(client, message):
    try:
        #Style name, id, stock, above_below, value, note, current, trigger
        id = message.author.id
        name = message.author.display_name
        parsed_msg = message.content.split(' ')
      
        if parsed_msg[1] in constants.acronym_list:
            if len(parsed_msg) > 3 and (parsed_msg[2] == "above" or parsed_msg[2] == "below") and parsed_msg[3].isnumeric():
                line = name + "," + str(id) + ","
                line = line + parsed_msg[1] + ","
                line = line + parsed_msg[2] + ","
                line = line + parsed_msg[3] + ","
                if len(parsed_msg) > 4:
                    note = parsed_msg[4]
                else:
                    note = ""
                line = line + note + ","
                line = line + ","
                line = line + "True" + "\n"
                file = open("notify.csv", "a")
                file.write(line)
                file.close
                await message.reply("Your notification has been saved.")
            else:
                await message.reply("Incorrect format use: !notify [stock] [above/below] [value] [note (optional, no spaces)]")
        else:
            await message.reply("That stock does not exist, please use the acronym found in !stocks")
    except:
        await error_handler(client, message, "register")


#LIST NOTIFICATIONS----------------------------------------  
async def list_notifications(client, message):
    #Style name, id, stock, above_below, value, note, time_notified, triggered
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    auth_id = numpy.int64(message.author.id)
    file = open("notify.csv", "r")
    df = pd.read_csv(file)
    file.close()
    df = df[df['id'] == auth_id]
    df = df[['name','stock', 'above_below', 'value', 'note']]
    #print(tabulate(df, tablefmt="grid"))
    
    await message.reply("```\n " + df.to_string() + " \n```")


#DISPLAY STOCKS.CSV----------------------------------------
async def display_stocks(client, message):
    #Style name, id, stock, above_below, value, note, time_notified, triggered
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    file = open("stocks.csv", "r")
    df = pd.read_csv(file)
    file.close()
    await message.reply("```\n " + df.to_string(index=False) + " \n```")

#REMOVE NOTIFICATIONS----------------------------------------
async def remove(client, message):
    await message.reply("This does not work yet.")
    parsed_msg = message.content.split(' ')
    print(len(parsed_msg[1]))
    auth_id = numpy.int64(message.author.id)
    file = open("notify.csv", "r")
    df = pd.read_csv(file)
    file.close()
    df = df[df['id'] != auth_id]
    print(df.to_string())
    #df.to_csv("notify.csv", index=False)


#60 SECOND CHECK----------------------------------------
async def check_for_notifications(client, stock):
    try:
        #"stock_id": 1,	"name": "Torn & Shanghai Banking", "acronym": "TSB",	"current_price": 822.39, "market_cap": 9134540776988,	"total_shares": 11107310129,	"benefit": {"frequency": 31,"requirement": 3000000,"description": "$50,000,000 every month"
        file = open("notify.csv", "r")
        df = pd.read_csv(file)
        file.close()
        temp_df = df[df['stock'] == stock['acronym']]
        #print(temp_df.to_string())
        for index, row in temp_df.iterrows():
            #print(type(stock['current_price']) + type(row['value']))
            df.loc[index, 'value']
            if stock['current_price'] > row['value']:
                row['current'] = "above"
                df.loc[index, 'current'] = "above"
                
            else:
                row['current'] = "below"
                df.loc[index, 'current'] = "below"
            
            if row['current'] == row['above_below']:
                if row['trigger'] == False:
                    msg_txt = row['stock'] + " is " + str(row['current']) + " " + str(row['value'])
                    await send_message(client, row['id'], msg_txt)
                    row['trigger'] = True
                    df.loc[index, 'trigger'] = True
            else:
                row['trigger'] = False
                df.loc[index, 'trigger'] = False
        #print(temp_df.to_string())
        
        df.to_csv("notify.csv", index=False)
        

        #print(stock['acronym'] + ": " + str(stock['current_price']))
    except:
        error_handler(client, message, "check_for_notifications")

async def error_handler(client, message, function):
    fTime = datetime.utcnow()
    line = str(fTime) + " Error in " + function + " with: " + message.content
    print(line)
    file = open("error.txt", "a")
    file.write(line)
    file.write(traceback.print_exc())
    file.close