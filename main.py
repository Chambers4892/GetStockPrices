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
from discord.ext import tasks

#Custom imports
import bot_actions
import constants
import help_func

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
#bot = Bot(intents=intents, command_prefix='!')


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0
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
        msg = message.content
        if message.content.startswith('!'):
          if message.content.find(' ') == -1:
            length = len(message.content)
          else:
            length =  message.content.find(' ')
          command = message.content[1:length].lower()
          print("Command: " + command)
          if command == 'notify':  #Register new notification
              await bot_actions.register(client, message)
          elif command == 'list':  #Print list of notifications
              await bot_actions.list_notifications(client, message)
          elif command == 'help':  #Prints help message
              await bot_actions.help_text(client, message)
#Add context sensitive removals (e.g. by row index or an entire stock)
          elif command == 'remove':  #Removes from list
              await bot_actions.remove(client, message)
          elif command == 'stocks':  #Removes from list
              await bot_actions.display_stocks(client, message)
          elif command == 'bug':  #Submit bug rpt
              await bot_actions.bug_report(client, message)
          else:
              #await message.reply("Invalid command.")
              pass

    @tasks.loop(seconds=60)
    async def get_stocks(self):
        fTime = datetime.utcnow()
        cDate = datetime.date(fTime)
        cTime = datetime.strftime(fTime, "%H:%M")
        
        try:
            file = open("prices.csv", "x")
            #print(file.read())
            file.write(constants.prices_header)
            file.close()
        except:
            #print("Exists")
            r = requests.get(
                "https://api.torn.com/torn/?selections=stocks&key=" +
                os.getenv('API'))
            print(str(cDate) + " " + str(cTime) + " " + str(r))
            prices = ""
            df = pd.DataFrame(
                columns=['Index', 'Stock', 'Acronym', 'Last Value'])
            try:
                for x in r.json()["stocks"]:
                    prices = prices + ", " + str(
                        r.json()["stocks"][x]["current_price"])
                    #try:
                    await bot_actions.check_for_notifications(
                        client,
                        r.json()["stocks"][x])
                    acr = str(r.json()["stocks"][x]["acronym"])
                    df.loc[x] = [
                        x,
                        str(r.json()["stocks"][x]["name"]),
                        str(r.json()["stocks"][x]["acronym"]),
                        "{:.2f}".format(r.json()["stocks"][x]["current_price"])
                    ]

                    #except:
                    #

                df.to_csv("stocks.csv", index=False)
                file = open("prices.csv", "a")
                file.write(str(cDate) + ", " + str(cTime) + prices + "\n")
                file.close()
            except:
                prices = "Error in prices: " + str(r)
                print(r.json())
            #print(df.to_string())
            #print(self.hourdf[acr].max())
            price_row = df.transpose()
            
            price_row = price_row.drop(labels=['Index', 'Stock', 'Acronym'])
            price_row.set_axis(constants.df_header, axis=1, inplace=True)
            price_row['Date'] = str(cDate)
            price_row['Time'] = str(cTime)
            price_row = price_row.loc[:, constants.df_header_w_dt]
            
            self.hourdf.set_axis(constants.df_header_w_dt, axis=1, inplace=True)
            price_row.set_axis(constants.df_header_w_dt, axis=1, inplace=True)
            #self.hourdf = pd.concat([self.hourdf, price_row], copy=False, ignore_index=True)
            
            self.hourdf = self.hourdf.append(price_row.to_dict(orient='records'), ignore_index=True)

            if self.hourdf.shape[0] > 59:
                self.hourdf = self.hourdf.tail(-1)
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
        self.hourdf = df.tail(60)
        

    @get_stocks.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

client = MyClient()
client.run(os.getenv('TOKEN'))
#bot.run(os.getenv('TOKEN'))
