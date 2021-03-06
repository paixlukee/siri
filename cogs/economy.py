import discord
from discord.ext import commands

import datetime
import requests
import random
import math
import time
from discord.ext.commands import errors, converter
from random import choice, randint
from random import choice, randint as rnd

import aiohttp
import asyncio
import json
import os

from pymongo import MongoClient
import pymongo

from .utils import patron

import config

client = MongoClient(config.mongo_client)
db = client['siri']

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.s = '§'
        self.colour = [0x37749c, 0xd84eaf, 0x45b4de, 0x42f4c5, 0xffb5f3, 0x42eef4, 0xe751ff, 0x51ffad]
        
    @commands.command(aliases=['lb'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def leaderboard(self, ctx, sort_by='money'):
        """View Siri's Economy Leaderboard"""
        msg = await ctx.send("Please wait..")
        page = 1
        choices = ['money', 'apple', 'iphone', 'house']
        start = (page - 1) * 8
        end = start + 8
        embed = discord.Embed(colour=0x37749c, description="Siri Economy Leaderboard")
        await msg.delete()
        if sort_by in choices:
            find_c = db.posts.find().sort(sort_by.lower(), -1)
            for x in find_c[start:end]:
                name = self.bot.get_user(x['user'])
                money = x['money']
                apple = x['apple']
                iphone = x['iphone']
                house = x['house']
                embed.add_field(name=f"**{name}**", value=f":moneybag:{money} :apple:{apple} :iphone:{iphone} :house:{house}", inline=False)             
            embed.set_author(name="Leaderboard", icon_url=ctx.me.avatar_url_as(format='png'))
            embed.set_footer(text=f"Sort by: {sort_by}")
            await ctx.send(embed=embed)
        
        else:
            await ctx.send("<:redtick:492800273211850767> That is not an option! You can only sort by.. `money`, `apple`, `iphone`, and `house`") 
            

    @commands.command(aliases=['setcolor'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def setcolour(self, ctx, colour):
        """Sets Profile Colour

        Colours:
        - Red
        - Orange
        - Yellow
        - Green
        - Blue
        - Violet
        - Pink
        - White

        """
        posts = db.posts.find_one({"user": ctx.author.id})
        if colour is None:
            await ctx.send("<:redtick:492800273211850767> `Incorrect Usage`\n```siri setcolour <colour-name>```")

        elif not posts is None:
            
            if colour.lower() == 'pink': # This is a reeaallly bad way of doing it. enh.
                await self.set_col(user=ctx.author.id, colour=0xff93f4)
                await ctx.send("<:greentick:492800272834494474> Set.")
            elif colour.lower() == 'blue':
                await self.set_col(user=ctx.author.id, colour=0x0000ff)
                await ctx.send("<:greentick:492800272834494474> Set.")
            elif colour.lower() == 'green':
                await self.set_col(user=ctx.author.id, colour=0x00ff00)
                await ctx.send("<:greentick:492800272834494474> Set.")
            elif colour.lower() == 'red':
                await self.set_col(user=ctx.author.id, colour=0xff0000)
                await ctx.send("<:greentick:492800272834494474> Set.")
            elif colour.lower() == 'violet' or colour.lower() == 'purple':
                await self.set_col(user=ctx.author.id, colour=0xa341f4)
                await ctx.send("<:greentick:492800272834494474> Set.")
            elif colour.lower() == 'orange':
                await self.set_col(user=ctx.author.id, colour=0xff9d00)
                await ctx.send("<:greentick:492800272834494474> Set.")
            elif colour.lower() == 'yellow':
                await self.set_col(user=ctx.author.id, colour=0xffff00)
                await ctx.send("<:greentick:492800272834494474> Set.")
            elif colour.lower() == 'white':
                await self.set_col(user=ctx.author.id, colour=0xffffff)
                await ctx.send("<:greentick:492800272834494474> Set.")
            else:
                await ctx.send("<:redtick:492800273211850767> That isn't a valid colour! View the colour list with `siri help cmd setcolour`\n```If you would like to suggest a colour, send a ticket ('siri ticket <message>') with the colour name and hex.```")
        else:
            await ctx.send("<:redtick:492800273211850767> You don't have a bank account, create one with `siri bank create`!")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def description(self, ctx, *, message):
        """Sets Profile Description"""
        posts = db.posts.find_one({"user": ctx.author.id})

        if message is None:
            await ctx.send("<:redtick:492800273211850767> `Incorrect Usage`\n```siri description <description>```")

        elif len(message) > 400:
            await ctx.send("<:redtick:492800273211850767> Description cannot be longer than 400 characters!")

        elif not posts is None:
            await ctx.send("<:greentick:492800272834494474> Set.")
            await self.set_desc(user=ctx.author.id, description=message)
        else:
            await ctx.send("<:redtick:492800273211850767> You don't have a bank account, create one with `siri bank create`!")

    @commands.command(aliases=['birthday'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bday(self, ctx, day=None, month=None, year=None):
        """Sets Profile Birthday"""
        posts = db.posts.find_one({"user": ctx.author.id})
        try:
            bday = day.split('-')
        except:
            pass
        if day is None:
            await ctx.send("<:redtick:492800273211850767> `Incorrect Usage`\n```siri birthday DD-MM-YYYY```") 
        elif int(bday[0]) > 31:
            await ctx.send("<:redtick:492800273211850767> `Incorrect Usage`\n```siri birthday DD-MM-YYYY```")
        elif int(bday[1]) > 12:
            await ctx.send("<:redtick:492800273211850767> `Incorrect Usage`\n```siri birthday DD-MM-YYYY```")
        elif int(bday[2]) < 1900:
            await ctx.send("<:redtick:492800273211850767> `Incorrect Usage`\n```siri birthday DD-MM-YYYY```")
        elif len(date) < 3:
            await ctx.send("<:redtick:492800273211850767> `Incorrect Format`\n```DD-MM-YYYY```")           
        elif not posts is None:
            await ctx.send("<:greentick:492800272834494474> Set.")
            await self.set_bday(user=ctx.author.id, date=bday)
        else:
            await ctx.send("<:redtick:492800273211850767> You don't have a bank account, create one with `siri bank create`!")

    @commands.command(aliases=['market', 'shop'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def store(self, ctx):
        """Buy an item from the Apple Store"""
        embed = discord.Embed(colour=0xa341f4, title="Welcome to the Apple Store!", description="Items:")
        embed.add_field(name=f"[1] 🍎 Apple ({self.s}2)", value=f"Get a shiny red apple.. almost as amazing as *the* Apple Company.")
        embed.add_field(name=f"[2] 📱 iPhone ({self.s}300)", value=f"Is that an iPhone 4? The best phone ever tbh")
        embed.add_field(name=f"[3] 🏠 House ({self.s}2000)", value=f"Wait.. since when can you buy homes at the Apple Store?")
        embed.set_footer(text="To buy an item, do 'siri buy <item>' or 'siri buy <item-number>'")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def eat(self, ctx):
        """Eat an apple"""
        posts = db.posts.find_one({"user": ctx.author.id})
        if not posts is None:
            if posts['apple'] > 0:
                responses = ['Yum.', 'Mmm.', 'Tasty?', 'Were you hungry?', 'How is it?']
                await ctx.send(f"You ate :apple:`1`! | {random.choice(responses)}") 
                await self.apple(user=ctx.author.id, count=-1)
            else:
                await ctx.send("<:redtick:492800273211850767> You don't have any apples!")
        else:
            await ctx.send("<:redtick:492800273211850767> You don't have a bank account, create one with `siri bank create`!")
        

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def buy(self, ctx, item = None):
        """Buy an item ('siri store' to see the items)"""
        posts = db.posts.find_one({"user": ctx.author.id})
        msg = await ctx.send("Processing..")
        if posts is None:
            await ctx.send("<:redtick:492800273211850767> You don't have a bank account, create one with `siri bank create`!")
        elif item is None:
            await ctx.send("<:redtick:492800273211850767> `Incorrect Usage`\n```siri buy <item>```")
            await msg.delete()
        elif item.lower() == 'apple' or item == '1':
            if posts['money'] < 2:
                await ctx.send("<:redtick:492800273211850767> You don't have enough to buy this item!")
                await msg.delete()
            else:
                await self.take_money(user=ctx.author.id, count=2)
                await self.apple(user=ctx.author.id, count=1)
                await msg.delete()
                await ctx.send("<:greentick:492800272834494474> You have successfully bought :apple:`1` from the Apple Store!")
        elif item.lower() == 'iphone' or item == '2':
            chance = random.randint(1, 25)
            chance_b = random.randint(1, 25)
            if posts['money'] < 300:
                await ctx.send("<:redtick:492800273211850767> You don't have enough to buy this item!")
                await msg.delete()
            elif chance == chance_b:
                await self.take_money(user=ctx.author.id, count=300)
                await msg.delete()
                await ctx.send(f"**BOGO!** You have won :iphone:`2` for the price of one!")
                await self.iphone(user=ctx.author.id, count=2)
            else:
                await self.take_money(user=ctx.author.id, count=300)
                await msg.delete()
                await ctx.send("<:greentick:492800272834494474> You have successfully bought :iphone:`1` from the Apple Store!")
                await self.iphone(user=ctx.author.id, count=1)
        elif item.lower() == 'house' or item == '3':
            await msg.delete()
            if posts['money'] < 2000:
                await ctx.send("<:redtick:492800273211850767> You don't have enough to buy this item!")
            else:
                await self.take_money(user=ctx.author.id, count=2000)
                await ctx.send("<:greentick:492800272834494474> You have successfully bought :house:`1` from the Apple Store!")
                await self.house(user=ctx.author.id, count=1)
        else:
            await ctx.send("<:redtick:492800273211850767> I couldn't find that item.. Do `siri shop` to see what we have..")

            
    @commands.command(aliases=['slot'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def slots(self, ctx, bet:int = None):
        """ Place a bet and play slots!"""
        posts = db.posts.find_one({"user": ctx.author.id})
        if bet == None:
            await ctx.send('You didn\'t specify a bet.')
        elif not int(posts['money']) > int(bet) or int(posts['money']) == int(bet):
            await ctx.send('You can\'t bet what you don\'t have.')
        elif int(bet) < 1:
            await ctx.send('Your bet must be above §0')
        else:
            emojis = [':seven:', ':cherries:', ':grapes:', ':lemon:', ':tangerine:', ':crown:', ':bell:', ':gem:', ':shell:']
            fruits = [':cherries:', ':grapes:', ':lemon:', ':tangerine:']
            a = random.choice(emojis)
            b = random.choice(emojis)
            c = random.choice(emojis)


            if a == b == c:
                if a == ':seven:':
                    won = bet*7
                    slot1 = discord.Embed(colour=random.choice(self.colour), description=f"{a}   {b}   {c}")
                    slot1.set_footer(text=f"JACKPOT! You've won §{won}!")
                elif a == ':crown:' or a == ':gem:':
                    won = bet*4
                    slot1 = discord.Embed(colour=random.choice(self.colour), description=f"{a}   {b}   {c}")
                    slot1.set_footer(text=f"Amazing! You've won §{won}!")
                else: 
                    won = bet*3
                    slot1 = discord.Embed(colour=random.choice(self.colour), description=f"{a}   {b}   {c}")
                    slot1.set_footer(text=f"Great! You've won §{won}!")
                await ctx.send(embed=slot1)
                await self.add_money(user=ctx.author.id, count=won)
            elif a == b or a == c or b == c:
                won = bet*2
                slot2 = discord.Embed(colour=random.choice(self.colour), description=f"{a}   {b}   {c}")
                slot2.set_footer(text=f"Nice! You've won §{won}!")
                await ctx.send(embed=slot2)
                await self.add_money(user=ctx.author.id, count=won)
            elif bet == None:
                await ctx.send('Please provide your bet with the command.')
            else:
                if a in fruits and b in fruits and c in fruits:
                    won = bet*3
                    slot2 = discord.Embed(colour=random.choice(self.colour), description=f"{a}   {b}   {c}")
                    slot2.set_footer(text=f"Fruit Bonanza! You've won §{won}!")
                    await ctx.send(embed=slot2)
                    await self.add_money(user=ctx.author.id, count=won)
                else:                    
                    slot3 = discord.Embed(colour=random.choice(self.colour), description=f"{a}   {b}   {c}")
                    slot3.set_footer(text=f"Aw! You didn't win anything.")
                    await ctx.send(embed=slot3)
                    await self.take_money(user=ctx.author.id, count=bet)
                    
                    
    @commands.command(aliases=['job'])
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def work(self, ctx):
        """Go to work!"""
        posts = db.utility.find_one({"utility": "responses"})
        f = 'no'
        if f == 'f':
            await ctx.send('c')
        else:
            resp = random.choice(posts['work'])
            embed = discord.Embed(colour=random.choice(self.colour), description=f"<:greentick:492800272834494474> {resp['text']} You have been paid **{self.s}{resp['money']}**.")
            embed.set_footer(text=f"Work again in 12 Hours!")
            await ctx.send(embed=embed)
            await self.add_money(user=ctx.author.id, count=resp['money'])
                    
    @commands.command(aliases=['flipacoin'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def flip(self, ctx, ht=None, bet:int=None):
        """Double your money by flipping a coin"""
        posts = db.posts.find_one({"user": ctx.author.id})
        if not ht or not bet or ht.lower() not in ['heads', 'tails']:
            await ctx.send('You need to specify heads or tails and a bet. Example: `siri flip heads 50`')
        elif not int(posts['money']) > int(bet) or int(posts['money']) == int(bet):
            await ctx.send('You can\'t bet what you don\'t have.')
        elif int(bet) < 1:
            await ctx.send('Your bet must be above §0')
        else:
            choices = ['heads', 'tails']
            win = random.choice(choices)

            if win == ht.lower():
                won = bet
                slot2 = discord.Embed(colour=random.choice(self.colour), description=f"<:coin:611327929749733386> **{win.capitalize()}**")
                slot2.set_footer(text=f"Nice! You've won §{won}!")
                await ctx.send(embed=slot2)
                await self.add_money(user=ctx.author.id, count=won)
            else:                    
                slot3 = discord.Embed(colour=random.choice(self.colour), description=f"<:coin:611327929749733386> **{win.capitalize()}**")
                slot3.set_footer(text=f"Aw! You didn't win anything.")
                await ctx.send(embed=slot3)
                await self.take_money(user=ctx.author.id, count=bet)
           
                
    @commands.command(aliases=['Profile'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def profile(self, ctx, user: discord.User=None):
        """Get user profile"""           
        if user is None:
            member = ctx.message.author

        else:
            try:
                member = user
            except:
                try:
                    member = "<@" + user + ">"
                except:
                    await ctx.send("There was an error!")
                    
        u = db.posts.find_one({"user": member.id})

        if not u is None:
            bal = u['money']
            description = u['description']
            bday = u['birthday']
            colour = u['colour']
            embed = discord.Embed(colour=colour, title=f"{member.name} #{member.discriminator}", description=f'**"**{description}**"**')
            if bday == 'BNS':
                embed.add_field(name="Birthday..", value="BIRTHDAY NOT SET: `siri birthday DD-MM-YYYY`")
            else:
                embed.add_field(name="Birthday..", value="**/**".join(bday))
            
            colour = str(colour)
            if colour == '0':
                colour = "COLOUR NOT SET: `siri setcolour <colour-name>`"
            colour = colour.replace('16749556', "<:pink:485323891317669888>").replace('255', "<:blue:485324426460528651>").replace('16776960', "<:yellow:485585695109546006>")
            colour = colour.replace('16711680', "<:red:485325173919318027>").replace('65280', "<:green:485325683594231818>").replace('10699252', "<:purple:485582995533725727>").replace('16751872', "<:orange:485585130216488975>").replace('16777215', "<:white:485587580323233827>")
            embed.add_field(name="Colour..", value=colour)
            embed.add_field(name="Level..", value=u['level'])
            embed.add_field(name="Balance..", value=f"**{self.s}**{bal}")
            embed.add_field(name="Inventory..", value=f":apple:**{u['apple']}**:iphone:**{u['iphone']}**:house:**{u['house']}**")
                   
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"<:redtick:492800273211850767> **{member.name}** doesn't have a bank account, create one with `siri bank create`!")


    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def give(self, ctx, count:int, user: discord.User=None):
        """Give your money to another user"""
        posts_user = db.posts.find_one({"user": user.id})
        posts = db.posts.find_one({"user": ctx.author.id})
                          

        if ctx.author == user:
            await ctx.send("<:redtick:492800273211850767> You cannot give money to yourself!")

        elif count < 0:
            await ctx.send(f"<:redtick:492800273211850767> You can't give under **{self.s}**1!")

        elif posts['money'] < count:
            await ctx.send(f"<:redtick:492800273211850767> You don't have **{self.s}**{count}!")

        elif posts_user is None:
            await ctx.send(f"<:redtick:492800273211850767> **{user.name}** doesn't have a bank account!")
        elif count is None:
            await ctx.send("`<:redtick:492800273211850767> Incorrect Usage`\n```siri give <@user> <count>```")

        elif not posts is None:
            await self.add_money(user=user.id, count=count)
            await self.take_money(user=ctx.author.id, count=count)
            embed = discord.Embed(colour=0x37749c, description=f"<:greentick:492800272834494474> {ctx.message.author.mention} has given {user.mention} **{self.s}**{count}!")
            await ctx.send(embed=embed)
                            
            if not 'badges' in posts:
                db.posts.update_one({"user": ctx.author.id}, {"$set":{"badges": []}})
            if not 'givemoney' in posts['badges']:
                db.posts.update_one({"user": ctx.author.id}, {"$push":{"badges": 'givemoney'}})
            else:
                pass
        else:
            await ctx.send("You don't have a bank account, create one with `siri bank create`!") 


    @commands.command(pass_context=True)
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        """Get your daily §"""
        posts = db.posts.find_one({"user": ctx.author.id})
        p = await patron.check(ctx.author.id)
        r = requests.get(f"https://discordbots.org/api/bots/481337766379126784/check?userId={ctx.author.id}", headers={"Authorization": config.dbl_token}).json()             
        count = 5
        if not posts is None:
            if r['voted'] == 1:
                am = "(**+5**, since you have upvoted!)"
                count = count + 5          
            if p == 'GOLD':
                am = "(**+75**, since you are a GOLD patron!)"
                count = count + 75
            elif p == 'SILVER':
                am = "(**+50**, since you are a SILVER patron!)"
                count = count + 50
            elif p == 'BRONZE':
                am = "(**+25**, since you are a BRONZE patron!)"
                count = count + 25
            else:
                am = "(Upvote [here](https://discordbots.org/bot/481337766379126784/vote) to earn an additional 5, tomorrow!)"
                count = 5
                
            bal = posts['money']
            await self.add_money(user=ctx.author.id, count=count)
            embed = discord.Embed(colour=0x37749c, description=f"<:greentick:492800272834494474> **{self.s}**{count} has been added to your bank account! {am} Come back in **24**hrs!")
            embed.set_footer(text=f"Balance: {self.s}{bal}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:redtick:492800273211850767> You don't have a bank account, create one with `siri bank create`!") 

    @commands.command(aliases=['bal'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def balance(self, ctx, user:discord.User=None):
        """Check your/someone's balance"""
        if user is None:
            posts = db.posts.find_one({"user": ctx.author.id})                
            if not posts is None:
                bal = posts['money']
                embed = discord.Embed(colour=0x37749c, description=f"You have **{self.s}**{bal} left in your bank account.")
                await ctx.send(embed=embed)
            else:
                await ctx.send("<:redtick:492800273211850767> You don't have a bank account, create one with `siri bank create`!")  
        else:
            posts = db.posts.find_one({"user": user.id})                         
            if not posts is None:
                bal = posts['money']
                embed = discord.Embed(colour=0x37749c, description=f"**{user.name}** has **{self.s}**{bal} left.")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"<:redtick:492800273211850767> UU{user.name}** doesn't have a bank account!") 


    @commands.group(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bank(self, ctx):
        if ctx.invoked_subcommand is None:
            user = db.posts.find_one({"user": ctx.author.id})
            if not user is None:
                await ctx.send("Check your balance with `siri balance`!")
            else:
                await ctx.send("<:redtick:492800273211850767> You don't have a bank account, create one with `siri bank create`!")

    @bank.command()
    async def create(self, ctx):
        """Create an account"""
        msg = await ctx.send("Please wait..")
        user = db.posts.find_one({"user": ctx.author.id})
        if not user is None:
            await msg.delete()
            await ctx.send("<:redtick:492800273211850767> You already have an account!")
        else:
            await self.update_data(ctx.author)
            await msg.delete()
            await ctx.send(f"<:greentick:492800272834494474> Your bank account has been created successfully. **{self.s}**20 has been added to your account as a welcome gift.")

    @commands.command()
    async def itemsuggest(self, ctx, *, message):
        await ctx.send("Thank you for the item suggestion! Please join http://discord.gg/VuvB4gt to view the results.")
        embed = discord.Embed(colour=0x37749c, description=f"**User:** `{ctx.author}`\n**User ID:** `{ctx.author.id}`\n**Suggestion**: `{message}`")
        embed.set_author(name="Incoming Suggestion", icon_url=ctx.author.avatar_url_as(format='png'))
        await self.bot.get_channel(493333785610551300).send(embed=embed) 
                            
    @commands.command()
    async def contestinfo(self, ctx):
        info = "ITEM CONTEST\n"\
            "___________\n\n"\
            "For the economy commands, there are only 3 items you can buy [Apple, iPhone, House].\n"\
            "But, I want to add 2 more items.\n\n"\
            "The one who gives me the best suggestion, will get a prize.\n\n"\
            "HOW TO ENTER:\n"\
            "1. Run the command 'siri itemsuggest' with your suggestion.\n"\
            "2. Your suggestion will be sent, wait until the contest ends.\n"\
            "3. When the contest ends, I will say the winners in https://discord.gg/CjRP2Mc\n"\
            "4. If you win, claim your prize in the support server.\n"\
            "\nPRIZES:\n"\
            "1st Place - 3 of the item you suggested, and §15,000\n"\
            "2nd Place - 2 of the item you suggested, and §10,000\n"\
            "\nContest ends when we have enough suggestions.\n"\
            "\nIf you have any questions, ask here: https://discord.gg/CjRP2Mc\n"\
            "\nGood Luck!"
        await ctx.send(f"```{info}```")
                            
    async def update_data(self, user):
        post = {
            "user": user.id,
            "money":25,
            "colour":0,
            "apple":0,
            "iphone":0,
            "house":0,
            "description":"DESCRIPTION NOT SET: `siri description <description>`",
            "birthday":"BNS"
        }
        db.posts.insert_one(post)

    async def apple(self, user:int, count=None):
        data = db.posts.find_one({"user": user})
        bal = data['apple']
        count = bal + count
        db.posts.update_one({"user": user}, {"$set":{"apple": count}})

    async def iphone(self, user:int, count=None):
        data = db.posts.find_one({"user": user})
        bal = data['iphone']
        count = bal + count
        db.posts.update_one({"user": user}, {"$set":{"iphone": count}})

    async def house(self, user:int, count=None):
        data = db.posts.find_one({"user": user})
        bal = data['house']
        count = bal + count
        db.posts.update_one({"user": user}, {"$set":{"house": count}})

    async def set_desc(self, user:int, description):
        db.posts.update_one({"user": user}, {"$set":{"description": description}})

    async def set_bday(self, user:int, date=None):
        db.posts.update_one({"user": user}, {"$set":{"birthday": date}})

    async def set_col(self, user:int, colour=None):
        db.posts.update_one({"user": user}, {"$set":{"colour": colour}})

    async def add_money(self, user:int, count):
        data = db.posts.find_one({"user": user})
        bal = data['money']
        money = int(bal) + count
        db.posts.update_one({"user": user}, {"$set":{"money": money}})

    async def take_money(self, user:int, count:int):
        data = db.posts.find_one({"user": user})
        bal = data['money']
        money = int(bal) - count
        db.posts.update_one({"user": user}, {"$set":{"money": money}})

def setup(bot):
  bot.add_cog(Economy(bot))
