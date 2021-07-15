#import prices.csv
import os  #Get env variables
import json  #Handling request results
import requests  #Requests
import datetime  #Time tagging (easier conv to utc)
import time
from datetime import datetime
import discord
import asyncio
import pandas as pd
import os
import sys

from discord.ext import tasks

#Custom imports
import bot_actions
import constants
import functions
import notifications
import database_actions

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
#bot = Bot(intents=intents, command_prefix='!')


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0
        self.last_time = ""
        #self.hourdf = pd.DataFrame()
        
        # start the task to run in the background
        self.get_stocks.start()
#@bot.event

    @client.event
    async def on_message(self, message):
        if message.author == client.user:
            return
        if message.author.bot:
            return
        if message.content.startswith('!'):
          if message.content == "!db_check" and str(message.author.id) == '226030188733923328':
              await message.reply("Executing database connection test.")
              await message.reply(database_actions.db_check())
          elif message.content == "!import_notifications" and str(message.author.id) == '226030188733923328':
              await message.reply("Importing Notifications")
              await message.reply(notifications.import_notifications())
          options = await functions.parse_message(client, message)
          msg = message.content
          if options != -1:
              if 'command' in options.keys():
                  print("Command detected: " + str(options['command']))
                  if options['command'] == 'notify':  #Register new notification
                      await message.reply(await notifications.register(client, options))
                  elif options['command'] in ['list', 'remove']:  #Register new notification
                      await message.reply(await notifications.list(client, options))
                  elif options['command'] == 'stocks':  
                      await bot_actions.display_stocks(client, message, self.full_df)
                  elif options['command'] == 'bug':  #Submit bug rpt
                      await bot_actions.bug_report(client, message)
                  else:
                      #await message.reply("Invalid command.")
                      pass


    @tasks.loop(seconds=1)
    async def get_stocks(self):
        fTime = datetime.utcnow()
        cDate = datetime.date(fTime)
        cTime = datetime.strftime(fTime, "%H:%M")
        #Checks to see if minute has changed
        if cTime != self.last_time:
            self.last_time = cTime
            #Creates file if it is missing
            if not os.path.isfile(sys.path[0]+"/prices.csv"):
                print("Prices file not found.")
                file = open("prices.csv", "x")
                file.write(constants.prices_header)
                file.close()
            r = requests.get(
                "https://api.torn.com/torn/?selections=stocks&key=" +
                os.getenv('API'))
            print(str(cDate) + " " + str(cTime) + " " + str(r))
            prices = ""
            df = pd.DataFrame(
                columns=['Index', 'Stock', 'Acronym', 'Last Value'])
            try:
                for x in r.json()["stocks"]:
                    prices = prices + ", " + str(r.json()["stocks"][x]["current_price"])
                    acr = str(r.json()["stocks"][x]["acronym"])
                    df.loc[x] = [
                        x,
                        str(r.json()["stocks"][x]["name"]),
                        str(r.json()["stocks"][x]["acronym"]),
                        "{:.2f}".format(r.json()["stocks"][x]["current_price"])
                    ]
                df.to_csv("stocks.csv", index=False)
                file = open("prices.csv", "a")
                file.write(str(cDate) + ", " + str(cTime) + prices + "\n")
                file.close()
            except:
                prices = ",Error in prices: " + str(r)
                print(r.json())
            #print(df.to_string())
            #print(self.hourdf[acr].max())

            price_row = df.transpose()
            price_row = price_row.drop(labels=['Index', 'Stock', 'Acronym'])
            price_row.set_axis(constants.df_header, axis=1, inplace=True)
            price_row['Date'] = str(cDate)
            price_row['Time'] = str(cTime)
            price_row = price_row.loc[:, constants.df_header_w_dt]
            
            self.full_df.set_axis(constants.df_header_w_dt, axis=1, inplace=True)
            price_row.set_axis(constants.df_header_w_dt, axis=1, inplace=True)
            # #self.hourdf = pd.concat([self.hourdf, price_row], copy=False, ignore_index=True)
            
            self.full_df = self.full_df.append(price_row.to_dict(orient='records'), ignore_index=True)
            await notifications.check_for_notifications(client,self.full_df)
            #if self.hourdf.shape[0] > 59:
                #self.hourdf = self.hourdf.tail(-1)
                #print("Last Row Dropped")
            #print(self.hourdf.tail())



#@bot.event

    @client.event
    async def on_ready(self):
        print(f'{client.user} has connected to Discord!')
        await client.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, name="for !help"))
        file = open("prices.csv", "r")
        df = pd.read_csv(file)
        file.close()
        self.full_df = df
        

    @get_stocks.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

client = MyClient()
client.run(os.getenv('TOKEN'))
#bot.run(os.getenv('TOKEN'))
