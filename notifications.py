import os
import pandas as pd
import database_actions
import backend
import constants
import datetime
import bot_actions


import functions

#REGISTER NEW NOTIFICATION--------------------------------------
async def register(client, options):
    try:
        if 'command' in options:
            del options['command']
            return database_actions.add_notif(options)

    except:
        await functions.error_handler(client, str(options), "register")

async def list(client, options):
    try:
        if 'discord_name' in options:
            del options['discord_name']
        if options.keys() >= {'value', 'direction'}:
            if options['direction'] == 'above':
                options['value'] = {'$gte': options['value'] }
            if options['direction'] == 'below':
                options['value'] = {'$lte': options['value'] }
            del options['direction']
        if options.keys() >= {'percent', 'direction'}:
            if options['direction'] == 'above':
                options['percent'] = {'$gte': options['percent'] }
            if options['direction'] == 'below':
                options['percent'] = {'$lte': options['percent'] }
            del options['direction']
        #print(options)
        if 'command' in options:
            if options['command'] == 'list':
                del options['command']
                return database_actions.get_notif(options)
            elif options['command'] == 'remove':
                del options['command']
                return database_actions.delete_notif(options)
            else:
                return "Other Command"
    except:
        await functions.error_handler(client, str(options), "list")

#60 SECOND CHECK----------------------------------------
async def check_for_notifications(client, df):
  
    pd.options.mode.chained_assignment = None
    df = df.tail(360)
    df_pct = df.copy(deep=True)
    msg = ""
    for stock in constants.df_header:
        df.loc[:, stock] = pd.to_numeric(df[stock])
        df_pct.loc[:, stock] = df[stock].pct_change().multiply(100).round(decimals=constants.percent_precision)
    try:
        notifications = database_actions.check_notif()
        #Prints all stock prices
        #print(df.iloc[-1])
        for notif in notifications:
            change = 0
            if 'alert_type' in notif.keys():
                if notif['alert_type'] == 'Value Change':

                    options = {}
                    if 'delay' in notif.keys():
                        delay = notif['delay']
                    else:
                        delay = 10

                    if ('lastTrigger' not in notif.keys()) or (datetime.datetime.utcnow() - datetime.timedelta(minutes=delay) > notif['lastTrigger']):
                        id_filter = notif['_id']
                        if 'trigger' in notif.keys():
                            pass
                        else:
                            notif['trigger'] = False
                        if notif['direction'] == 'above':
                            if df[notif['stock']].iloc[-1] >= notif['value']:
                                if notif['trigger'] == False:
                                    options = {'lastTrigger': datetime.datetime.utcnow(), 'trigger': True}
                                    database_actions.update_by_id(id_filter, options)
                                    msg = notif['stock'] + " is " + notif['direction'] + " " + str(notif['value'])
                                    await bot_actions.send_message(client, notif['discord_id'], msg)
                            else:
                                if notif['trigger'] == True:
                                    options = {'trigger': False}
                                    database_actions.update_by_id(id_filter, options)
                        else:
                            if df[notif['stock']].iloc[-1] <= notif['value']:
                                if notif['trigger'] == False:
                                    options = {'lastTrigger': datetime.datetime.utcnow(), 'trigger': True}
                                    database_actions.update_by_id(id_filter, options)
                                    msg = notif['stock'] + " is " + notif['direction'] + " " + str(notif['value'])
                                    await bot_actions.send_message(client, notif['discord_id'], msg)
                            else:
                                if notif['trigger'] == True:
                                    options = {'trigger': False}
                                    database_actions.update_by_id(id_filter, options)
                elif notif['alert_type'] == 'Percent Change':
                    change = df_pct[notif['stock']].tail(notif['duration']).sum().round(decimals=constants.percent_precision)
                    print(notif['stock'] + " " + str(change) + " " + str(notif['duration']))
                    if notif['change'] == 'rises': 
                        if change >= notif['percent']:
                            msg = notif['stock'] + " has risen " + str(notif['percent']) + "% in the last " + str(notif['duration']) + " minutes."
                            await bot_actions.send_message(client, notif['discord_id'], msg)
                            pass
                    else:
                        if change <= (notif['percent']*-1):
                            msg = notif['stock'] + " has dropped " + str(notif['percent']) + "% in the last " + str(notif['duration']) + " minutes."
                            await bot_actions.send_message(client, notif['discord_id'], msg)
                            pass
                elif notif['alert_type'] == 'Global Change':
                    for stock in constants.df_header:
                        change = df_pct[stock].tail(notif['duration']).sum().round(decimals=constants.percent_precision)
                        
                        if notif['change'] == 'rises': 
                            if change >= notif['percent']:
                                msg = stock + " has risen " + str(notif['percent']) + "% in the last " + str(notif['duration']) + " minute(s)."
                                await bot_actions.send_message(client, notif['discord_id'], msg)
                                print(df_pct[stock].tail(notif['duration']))
                                print(stock + " " + str(change) + " " + str(notif['duration']))
                                
                        else:
                            if change <= (notif['percent']*-1):
                                msg = stock + " has dropped " + str(notif['percent']) + "% in the last " + str(notif['duration']) + " minute(s)."
                                await bot_actions.send_message(client, notif['discord_id'], msg)
                                print(df_pct[stock].tail(notif['duration']))
                                print(stock + " " + str(change) + " " + str(notif['duration']))
                else:
                    print('This is an error with alert_type ln 119 notifications.py')
    except:
        await functions.error_handler(client, "fix this later", "check_for_notifications")

def import_notifications():
    file = open("notify.csv", "r")
    for line in file:
        parsed_message = line.split(',')
        options = {}
        options['discord_name'] = parsed_message[1]
        options['discord_id'] = parsed_message[2]
        options['stock'] = parsed_message[3]
        options['direction'] = parsed_message[4]
        options['value'] = parsed_message[5]
        options['note'] = parsed_message[6]
        options['trigger'] = parsed_message[8].replace('\n', '')
        print(options)
        pass
    file.close
#   df = pd.read_csv(file)
    return "Successfully read notifications"

