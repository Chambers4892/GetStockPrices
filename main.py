#import prices.csv
import os
import json
import requests
import datetime
import time
from datetime import datetime
import discord
import bot_actions
import asyncio
import pandas as pd
from discord.ext import tasks

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0

        # start the task to run in the background
        self.get_stocks.start()
        
    @client.event
    async def on_message(self, message):
        
        if message.author == client.user:
            return
        if message.author.bot:
            return

        msg = message.content

        if message.content.startswith('!notify'):   #Register new notification
            await bot_actions.register(client, message)
        if message.content.startswith('!list'):     #Print list of notifications
            await bot_actions.list_notifications(client, message)
        if message.content.startswith('!help'):     #Prints help message
            await bot_actions.help_text(client, message)
        #Add context sensitive removals (e.g. by row index or an entire stock)
        if message.content.startswith('!remove'):   #Removes from list
            await bot_actions.remove(client, message)
        if message.content.startswith('!stocks'):   #Removes from list
            await bot_actions.display_stocks(client, message)


    @tasks.loop(seconds=60)
    async def get_stocks(self):
        fTime = datetime.utcnow()
        cDate = datetime.date(fTime)
        cTime = datetime.strftime(fTime, "%H:%M")
        try:
            file = open("prices.csv", "x")
            #print(file.read())
            file.write("Date, Time, TSB, TCB, SYS, LAG, IOU, GRN, THS, YAZ, TCT, CNC, MSG, TMI, TCP, IIL, FHG, SYM, LSC, PRN, EWM, TCM, ELT, HRG, TGP, WSU, IST, BAG, EVL, MCS, WLT, TCC\n")
            file.close()
        except:
            #print("Exists")
            r = requests.get("https://api.torn.com/torn/?selections=stocks&key=" + os.getenv('API'))
            print(str(cDate) + " " + str(cTime) + " " + str(r))
            prices = ""
            df = pd.DataFrame(columns = ['Index', 'Stock', 'Acronym', 'Last Value'])
            try:
                for x in r.json()["stocks"]:
                    prices = prices + ", " + str(r.json()["stocks"][x]["current_price"])
                    #try:
                    await bot_actions.check_for_notifications(client, r.json()["stocks"][x])
                    df.loc[x] = [x, str(r.json()["stocks"][x]["name"]), str(r.json()["stocks"][x]["acronym"]), "{:.2f}".format(r.json()["stocks"][x]["current_price"])]
                    #except:
                    #    print("No work :(")
            except:
                prices = "Error in prices: " + str(r)
                #print(r.json())
            df.to_csv("stocks.csv", index=False)       
            file = open("prices.csv", "a")
            file.write(str(cDate) + ", "  + str(cTime) + prices + "\n")
            
            #await bot_actions.send_message(client, prices)
            file.close()
          

    @client.event
    async def on_ready(self):
        print(f'{client.user} has connected to Discord!')  
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for !help")) 

    @get_stocks.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in
        
client = MyClient()      
client.run(os.getenv('TOKEN'))

