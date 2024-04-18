import discord
import json
import random
import asyncio
from discord import User, Member, Message
from discord.ext import commands
from discord.ext.commands import Context, errors
from data_wrapper import UsersData, usersDataWrapper
from typing import Union, Optional

import discord.ext
import discord.ext.tasks


class EconomyCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self = self
        self.client = bot
        self.usersDataWrapper = usersDataWrapper

        with open("assets/dialogue.json", "r") as dJson:
            dialogue = json.load(dJson)
            self.begList = list[str](dialogue["begList"])
            self.farmDialoguePositive = list[str](dialogue["farmListPositive"])
            self.farmDialogueNegative = list[str](dialogue["farmListNegative"])
            self.personList = list[str](dialogue["personList"])
            del dialogue
            del dJson

        with open("assets/shopitems.json", "r") as sJson:
            self.shopItems = dict[str, dict[str, Union[str, int]]](
                json.load(sJson))

        self.hoes = ["diamond hoe", "iron hoe", "stone hoe"]

    @commands.command(aliases=["bal", "potats", "potatoes", "vault"])
    async def balance(
        self, ctx: Context, *, mention: Optional[Union[User, Member]] = None
    ):
        person = ctx.author
        if mention != None:
            person = mention

        self.createAccount(person)
        userBankData = self.getUserBal(person)
        wallet_amt = userBankData["wallet"]
        bank_amt = userBankData["bank"]
        embed = discord.Embed(
            title=f"{person.name}'s potatoes", color=discord.Colour.green()
        )
        embed.add_field(name="Pocket", value=f"{wallet_amt} :potato:")
        embed.add_field(name="Vault", value=f"{bank_amt} :potato:")
        embed.set_footer(text="Made by DepressedPotato")
        embed.set_thumbnail(url=person.avatar)
        await ctx.send(embed=embed)

    @commands.command(aliases=["dep"])
    async def deposit(self, ctx: Context, amount=None):
        """Deposits an amount into invoking user's bank"""
        self.createAccount(ctx.author)
        bal = self.getUserBal(ctx.author)

        # Exceptions non-integer inputs
        if amount == None:
            await ctx.send(
                "You have to enter an amount to deposit <:seriously:809518766470987799>"
            )
            return
        elif amount == "all" or amount == "max":
            if bal["wallet"] == 0:
                await ctx.send("imagine depositing 0 potatoes amirite")
                return

            amount = bal["wallet"]

        # Exceptions to integer inputs
        amount = int(amount)
        if amount > bal["wallet"]:
            await ctx.send(
                "You're too poor to deposit potatoes <:XD:806659054721564712>"
            )
            return
        elif amount < 0:
            await ctx.send(
                "How the hecc u think you can deposit negative potatoes <:pepe_hehe:816898198315597834>"
            )
            return
        elif amount == 0:
            await ctx.send("are you *trying* to break me <:sus:809828043244961863>")
            return

        await ctx.send(f"You deposited **{amount}** :potato: :0")
        bal["wallet"] -= amount
        bal["bank"] += amount

    @commands.command(aliases=["with"])
    async def withdraw(self, ctx: Context, amount=None):
        """Withdraws an amount into invoking user's wallet"""
        self.createAccount(ctx.author)

        # Exceptions non-integer inputs
        if amount == None:
            await ctx.send(
                "You have to enter an amount to withdraw <:seriously:809518766470987799>"
            )
            return
        bal = self.getUserBal(ctx.author)
        if amount == "all" or amount == "max":
            if bal["bank"] == 0:
                await ctx.send("imagine withdrawing 0 potatoes amirite")
                return
            amount = bal["bank"]

        # Exceptions to integer inputs
        amount = int(amount)
        if amount > bal["bank"]:
            await ctx.send(
                "You're too poor to withdraw that much potatoes <:XD:806659054721564712>"
            )
            return
        if amount < 0:
            await ctx.send(
                "How the hecc u think you can withdraw negative potatoes  <:pepe_hehe:816898198315597834>"
            )
            return
        if amount == 0:
            await ctx.send("are you *trying* to break me <:sus:809828043244961863>")
            return

        bal["bank"] -= amount
        bal["wallet"] += amount
        await ctx.send(f"You withdrew **{amount}** :potato:  :0")

    @commands.command(aliases=["search"])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def beg(self, ctx: Context):
        """By begging invoking member gains a random number of potatoes"""
        self.createAccount(ctx.author)

        user = ctx.author
        earnings = random.randint(1000, 2000)
        person = random.choice(self.personList)
        descrip = (
            random.choice(self.begList)
            .replace("nosrep", person)
            .replace("author.mention", user.mention)
            .replace("earnings.money", str(earnings))
        )
        embed = discord.Embed(description=descrip, color=0x2ECC71)
        await ctx.send(embed=embed)

        self.addAmountTo(ctx.author, earnings, "wallet")

    @beg.error
    async def beg_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 1min)".format(
                error.retry_after
            )
            await ctx.send(msg)
        else:
            raise error

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def farm(self, ctx: Context):
        self.createAccount(ctx.author)
        userDat = self.getUserData(ctx.author)
        earnings = random.randrange(-50, 50)

        for hoeName in self.hoes:
            if hoeName in userDat["inv"].keys():
                print(hoeName)
                print(userDat)
                if hoeName == "diamond hoe":
                    earnings = random.randrange(-25, 100)
                    print("dia")
                elif hoeName == "iron hoe":
                    earnings = random.randrange(-25, 75)
                    print("iron")
                elif hoeName == "stone hoe":
                    earnings = random.randrange(-50, 75)
                    print("stone")
                break
        del hoeName

        descrip = ""
        if earnings < 0:
            descrip = random.choice(self.farmDialogueNegative).replace(
                "earnings.money", str(earnings)
            )
        elif earnings > 0:
            descrip = random.choice(self.farmDialoguePositive).replace(
                "earnings.money", str(earnings)
            )
        else:
            descrip = "wow i cant believe youve actually farmed **0 :potato:** ill give u **69 :potato:** cuz i feel kinda bad..."
            earnings = 69

        userDat["bal"]["wallet"] += earnings
        embed = discord.Embed(description=descrip, color=0x2ECC71)
        await ctx.send(embed=embed)
        del userDat

    @farm.error
    async def farm_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 1s)".format(
                error.retry_after
            )
            await ctx.send(msg)
        else:
            raise error

    @commands.command(aliases=["store", "market"])
    async def shop(self, ctx: Context):
        em = discord.Embed(color=0x2ECC71)
        for k, v in self.shopItems.items():
            name = "**" + str(v["name"]) + "**"
            id = k
            price = v["cost"]
            desc = v["description"]
            if name == "**Test Item**":
                pass
            else:
                em.add_field(
                    name=name,
                    value=f"\t ID: `{id}`\n\tPrice: **{price}**\n\t {desc}",
                    inline=False,
                )
                em.set_author(
                    name="Potato Industry Tools Shack",
                    icon_url="https://cdn.discordapp.com/avatars/839966871143186472/1a802ca9786c5bf56cde2ca3ed14dce6.webp?size=1024",
                )
        await ctx.send(embed=em)

    @commands.command(aliases=["tools", "inventory", "inv", "shack"])
    async def shed(self, ctx: Context, *, member: Optional[Member] = None):
        # await ctx.send("test")
        user = ctx.author
        if member != None:
            user = member

        self.createAccount(user)
        inv = self.getUserInv(user)
        em = discord.Embed(title=f"{user.name}'s Shed", color=0x7289DA)
        for k, v in inv.items():
            name = self.getItemName(k)
            sell = self.shopItems[k]["sell"]
            amount = v
            em.add_field(
                name=name + " - " + str(v),
                value=f":1412-reply:Sells for: `"
                + str(sell)
                + "`",  # TODO: Change emoji
                inline=False,
            )
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 2700, commands.BucketType.user)
    async def dig(self, ctx: Context):
        rng = random.random() * 100 + 1  # [1,100]
        itemID = ""
        if rng <= 2.5:
            itemID = "goldenpotato"  # 2.5% chance
        elif rng <= 20:
            itemID = "invisiblepotato"  # 17.5% chance
        elif rng <= 50:
            itemID = "potatochip"  # 30% chance
        else:
            itemID = "rottenpotato"  # 50% chance

        await self.addToInv(ctx.author, itemID, 1)
        embed = discord.Embed(
            description=f"You dug up **1 {self.getItemName(itemID)}** :0",
            color=discord.Colour.blue(),
        )
        await ctx.send(embed=embed)

    @dig.error
    async def dig_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 1hr)".format(
                error.retry_after
            )
            await ctx.send(msg)
        else:
            raise error

    @commands.command()
    async def buy(self, ctx: Context, amount: int = 1, *, itemID: str):
        self.createAccount(ctx.author)
        itemID = self.formatToItemID(itemID)

        ### Exceptions ###
        if amount <= 0:
            await ctx.send("hey, are you trying to break me?")
            return
        if not self.isItemInShop(itemID):
            await ctx.send("That isn't in the shop")
            return

        userBalDat = self.getUserBal(ctx.author)
        item = self.getItem(itemID)
        cost = item["cost"] * amount

        itemMsg = item["name"]
        if amount == 1:
            itemMsg = f"a **{itemMsg}**"
        else:
            itemMsg = f"**{amount} {itemMsg}s**"

        if cost > userBalDat["wallet"]:
            await ctx.send(
                f"You don't have enough potatoes in your pocket to purchase {
                    itemMsg} <:XD:806659054721564712>"
            )
            return

        userBalDat["wallet"] -= cost
        await ctx.send(f"You just bought {itemMsg} :0")
        await self.addToInv(ctx.author, itemID, amount)
        del itemID
        del itemMsg
        del cost

    @buy.error
    async def buy_error(self, ctx: Context, error):
        await ctx.send(
            "try formatting it like this: p!buy [amount] [item]"
        )

    @commands.command(aliases=["cya"])
    async def sell(self, ctx: Context, amount: int, *, itemID: str):
        self.createAccount(ctx.author)
        itemID = self.formatToItemID(itemID)

        ### Exceptions ##
        if amount <= 0:
            await ctx.send("hey, are you trying to break me?")
            return
        elif not self.isItemInShop(itemID):
            await ctx.send("r u trying to sell nothing?")
            return

        userInvDat = self.getUserInv(ctx.author)
        item = self.getItem(itemID)

        if itemID not in userInvDat.keys():
            await ctx.send(f"You don't have a {item["name"]} in your shed.")
            return
        elif userInvDat[itemID] < amount:
            await ctx.send(f"You don't have {amount} {item["name"]} in your shed.")
            return

        itemName = item["name"]

        commission = item["sell"] * amount
        try:
            await ctx.send(f"Sell **{amount} {itemName}** for {commission} :potato:? (y/n)")
            # Waits for 7.5 seconds
            response: Message = await self.client.wait_for("message", timeout=7.5)
        except asyncio.TimeoutError:
            return

        if response.content.lower() not in ("yes", "y"):
            await ctx.send("Sale cancelled")
            return

        await ctx.send(f"You just sold **{amount} {itemName}** for {commission} :potato:")
        self.addAmountTo(ctx.author, commission, "wallet")

    @sell.error
    async def sell_error(self, ctx: Context, error):
        await ctx.send(
            "try formatting it like this: p!sell [amount] [item]"
        )

    @commands.command()
    async def use(self, ctx: Context, amount: int, *, itemID: str):
        self.createAccount(ctx.author)
        itemID = self.formatToItemID(itemID)

        ### Exceptions ##
        if amount <= 0:
            await ctx.send("hey, are you trying to break me?")
            return
        elif not self.isItemInShop(itemID):
            await ctx.send("r u trying to use nothing?")
            return

        userInvDat = self.getUserInv(ctx.author)
        item = self.getItem(itemID)

        if itemID not in userInvDat.keys():
            await ctx.send(f"You don't have a {item["name"]} in your shed.")
            return
        elif userInvDat[itemID] < amount:
            await ctx.send(f"You don't have {amount} {item["name"]} in your shed.")
            return

        try:
            getattr(self, "use_" + itemID)()
        except errors.CommandInvokeError:
            await ctx.send("u can't use this item")

    @use.error
    async def use_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("try formatting it like this: `p!use [amount] [item]`")
        else:
            raise error

    @commands.command(aliases=["gift", "gib", "send", "transfer"])
    async def give(self, ctx: Context, member: Union[User, Member], amount=None):
        pass

    @commands.command(aliases=["add"])
    @commands.is_owner()
    async def addpotatoes(self, ctx: Context, member: Union[User, Member], amount):
        pass

    @addpotatoes.error
    async def addpotatoes_error(self, ctx: Context, error):
        pass

    @commands.command(aliases=["gamble"])
    async def coinflip(self, ctx: Context, amount=None):
        pass

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def sabotage(self, ctx: Context, *, member: Union[User, Member]):
        pass

    @sabotage.error
    async def sabotage_error(self, ctx: Context, error):
        pass

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def rob(self, ctx: Context, *, member: Union[User, Member]):
        pass

    @rob.error
    async def rob_error(self, ctx: Context, error):
        pass

    @commands.command(aliases=["lb", "rich"])
    async def leaderboard(self, ctx: Context):
        pass

    @commands.command(aliases=["lbreverse", "richreverse"])
    async def leaderboardreverse(self, ctx: Context):
        pass

    ### Use Command ###

    def use_lotterypotato(self, ctx: Context, amount: int) -> None:
        pass

    ### Helper Methods ###

    def getAllUsersData(self) -> dict:
        return self.usersDataWrapper.getAllUserData()

    def getUserData(self, user: Union[User, Member]) -> dict:
        return self.usersDataWrapper[str(user.id)]

    def getUserBal(self, user: Union[User, Member]) -> dict:
        return self.getUserData(user)["bal"]

    def getUserInv(self, user: Union[User, Member]) -> dict:
        return self.getUserData(user)["inv"]

    def createAccount(self, user: Union[User, Member]) -> bool:
        """Creates user data entry, if not already present"""

        userID = str(user.id)
        if userID in self.usersDataWrapper:
            return False
        else:
            self.usersDataWrapper[userID] = {}
            self.usersDataWrapper[userID]["bal"] = {}
            self.usersDataWrapper[userID]["bal"]["wallet"] = 0
            self.usersDataWrapper[userID]["bal"]["bank"] = 0
            self.usersDataWrapper[userID]["inv"] = {}
        with open("database/userdata.json", "w") as f:
            json.dump(usersDataWrapper.getAllUserData(), f)
        return True

    async def addToInv(
        self, user: Union[User, Member], itemID: str, amount: int
    ) -> None:
        userInvDat = self.getUserInv(user)
        try:
            userInvDat[itemID] += amount
        except KeyError:
            userInvDat[itemID] = amount

    def getItemName(self, itemID: str) -> str:
        return self.getItem(itemID)["name"]

    def getItem(self, itemID: str) -> dict:
        return self.shopItems[itemID]

    def isItemInShop(self, itemID: str) -> bool:
        """Returns true if itemID corresponds to a shop item"""
        return itemID in self.shopItems.keys()

    def formatToItemID(self, itemID: str) -> str:
        """Returns the passed in string all lowercase and without spaces"""
        return itemID.lower().replace(" ", "")

    def addAmountTo(self, user: Union[User, Member], change=0, mode="wallet"):
        self.getUserBal(user)[mode] += change


async def setup(bot: commands.Bot):
    await bot.add_cog(EconomyCommands(bot))
