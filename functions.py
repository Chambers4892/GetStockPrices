import constants
import bot_actions
import backend
import notifications

import discord
import os
import sys
import datetime
import time
from datetime import datetime
import traceback

#TEXT PARSING---------------------------------------------------------
async def parse_message(client, message):
    try:
        #Setup
        options = {}
        error = False
        
        options['discord_id'] = message.author.id
        options['discord_name'] = message.author.display_name

        msg_text = message.content[1:len(message.content)].lower()
        parsed_msg = msg_text.split(' ')

        #Parse and sort message pieces
        for msg in parsed_msg:
            if msg.find('=')!=-1:
                sub_msg = msg.split('=', 2)
                if sub_msg[0].strip().lower() in constants.option_choices:
                    if sub_msg[0].strip().lower() == 'stock':
                        options[sub_msg[0]] = sub_msg[1].upper()
                    elif sub_msg[0].strip().lower() == 'delay':
                        options[sub_msg[0]] = int(sub_msg[1])
                    else:
                        options[sub_msg[0]] = sub_msg[1]
            elif msg.lower() == 'all':
                options['all'] = True
          
            else:
                if msg.strip() in constants.commands:
                    options['command'] = msg.strip()
                    if options['command'] == 'help':
                        await help_text(client, message)
                        return -1
                elif msg.upper().strip() in constants.acronym_list:
                    options['stock'] = msg.upper().strip()
                elif msg.strip() in constants.directions:
                    options['direction'] = msg.strip()
                elif msg.strip() in constants.alert_types:
                    options['alert_type'] = msg.strip().Title().replace('_',' ')
                elif msg.strip() in constants.change:
                    options['change'] = msg.strip()
                elif msg.strip().find("%")!=-1:
                    try:
                        options['percent'] = float(msg.strip().replace('%',''))
                    except:
                        print("Value error in percent value.")
                elif msg.strip() in constants.extra_words:
                    pass
                else:
                    try:
                        options['value'] = float(msg)
                    except ValueError:
                        if 'note' in options.keys():
                            options['note'] = options['note'] + " " + str(msg)
                        else:
                            options['note'] = str(msg)
        #Command specific logic
        if 'command' in options.keys():
            #print(str(options))       
            if 'direction' in options.keys():
                if options['direction'] in constants.dir_up:
                    options['direction'] = 'above'
                if options['direction'] in constants.dir_down:
                    options['direction'] = 'below'
            if 'change' in options.keys():
                if options['change'] in constants.dir_up:
                    options['change'] = 'rises'
                if options['change'] in constants.dir_down:
                    options['change'] = 'drops'

            if options['command'] == 'notify':
                if options.keys() >= {'percent', 'change'}:
                    if 'stock' in options.keys():
                        options['alert_type'] = 'Percent Change'
                        if 'direction' in options.keys():
                            del options['direction']
                    else:
                        options['alert_type'] = 'Global Change'
                    if 'value' in options.keys():
                        options['duration'] = abs(round(options['value']))
                        del options['value']
                    else:
                        if 'duration' in options.keys():
                            options['duration'] = abs(round(options['duration']))
                        else:
                            options['duration'] = 1
                elif options.keys() >= {'stock', 'value', 'direction'}:
                    options['alert_type'] = 'Value Change' 
                else:
                    error = True
                    error_msg = "Bad combination of options"
            elif options['command'] == 'list':
                pass
            #Add new command combinations here
            elif options['command'] == 'remove':
                if 'all' in options.keys():
                    del options['all']
                else:
                    if message.content.lower().strip() == '!remove':
                        error = True
                        error_msg = "Please explicitly state \'!remove all\'"  
            else:
                #error = True
                #error_msg = "Command not added to rewrite yet. Legacy code may still function after this alert."   
                pass
        else:
            error = True
            error_msg = "No Command Detected"    

        if error == True:
            await message.reply(error_msg)
            return -1
        else:
            #await message.reply(str(options))
            return options  
    except:
        await error_handler(client, message.content, "parse_message")
        print("Unknown error parsing: " + message.content)
        return -1

    
#HELP TEXT---------------------------------------------------------
async def help_text(client, message):
    try:
        parsed = message.content.split(' ')
        parsed.pop(0)
        sub_path = "/help_docs"
        if len(parsed) > 0:
            for sub in parsed:
                sub_path = sub_path + "/" + str(sub.lower().strip())
        if os.path.isdir(sys.path[0]+sub_path):
            sub_path = sub_path + "/main"
        try:
            f = open(sys.path[0]+sub_path, "r")
            text = f.read()
            f.close()
        except:
            text = "That help file does not exist."
        await message.reply(sub_path + "\n" + text)
    except:
         await bot_actions.error_handler(client, message.content, "help_text")

#ERROR HANDLING----------------------------------------------------------
async def error_handler(client, message, function):
    fTime = datetime.utcnow()
    line = str(fTime) + ' ' + str(client.user) + " Error in " + function + " with: " + message + "\n" + str(traceback.print_exc()) + "\n"
    print(line)
    file = open("error.txt", "a")
    file.write(line)
    file.close
    await bot_actions.send_message(client, "226030188733923328", line)

def table_builder(line, table=""):
    output = ""
    row = "| {stock:<6s} | {dir:<10s} | {val:06.2f} | {type:<15s} |".format
    if table == "":
        table = "  Stock    Direction    Value    Type\n"
        #table = row(stock="Stock", dir="Direction", val="Value", type="Type")
    if line['alert_type'] == 'Value Change':
        output = table + row(stock=line['stock'], dir=line['direction'], val=line['value'], type=line['alert_type']) +"\n"
        #output = table + str(line['stock']) + "\t\t" + str(line['direction']) + "\t\t" + "{:.2f}".format(line['value']) + "\t" + str(line['alert_type']) + "\n"
    elif line['alert_type'] == 'Percent Change':
        output = table + row(stock=line['stock'], dir=line['change'], val=line['percent'], type=line['alert_type'])+"\n"
        #output = table + str(line['stock']) + "\t\t" + str(line['change']) + "\t\t" + "{:.2f}".format(line['percent']) + "\t" + str(line['alert_type']) + "\n"

    else:
        output = table + row(stock="---", dir=line['change'], val=line['percent'], type=line['alert_type'])+"\n"
        #output = table + "---" + "\t\t" + str(line['change']) + "\t\t" + "{:.2f}".format(line['percent']) + "\t" + str(line['alert_type']) + "\n"
        
    #print(output)
    return output
    