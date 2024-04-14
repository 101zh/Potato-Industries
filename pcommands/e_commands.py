import discord, json, random
from discord.ext import commands
from discord.ext.commands import Context
from data_wrapper import UsersData, usersDataWrapper
from typing import Union, Optional

import discord.ext
import discord.ext.tasks


class EconomyCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self = self
        self.bot = bot
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
            self.shopItems = dict[str, dict[str, Union[str, int]]](json.load(sJson))

        self.hoes = ["diamond hoe", "iron hoe", "stone hoe"]

    @commands.command(aliases=["bal", "potats", "potatoes", "vault"])
    async def balance(self, ctx: Context, *, mention: discord.Member = None):
        person = ctx.author
        if mention != None:
            person = mention

        await self.createAccount(person)
        userBankData = await self.getUserBal(person)
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
        await self.createAccount(ctx.author)
        bal = await self.getUserBal(ctx.author)

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
        await self.createAccount(ctx.author)

        # Exceptions non-integer inputs
        if amount == None:
            await ctx.send(
                "You have to enter an amount to withdraw <:seriously:809518766470987799>"
            )
            return
        bal = await self.getUserBal(ctx.author)
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
        await self.createAccount(ctx.author)

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

        await self.addAmountTo(ctx.author, earnings, "wallet")

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
        await self.createAccount(ctx.author)
        userDat = await self.getUserData(ctx.author)
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

    @commands.command()
    async def use(self, ctx: Context, amount_used: int, *, item: str = None):
        pass

    async def update_user_shed(
        self, user: discord.Member, item: str, amount_used: int
    ) -> int:
        return -1

    async def use_lottery_potato(self, ctx: Context, amount: int) -> None:
        pass

    @commands.command(aliases=["cya"])
    async def sell(self, ctx: Context, amount=1, *, item):
        pass

    @commands.command()
    @commands.cooldown(1, 2700, commands.BucketType.user)
    async def dig(self, ctx: Context):
        pass

    @sell.error
    async def sell_error(self, ctx: Context, error):
        pass

    @dig.error
    async def dig_error(self, ctx: Context, error):
        pass

    @commands.command(aliases=["tools", "inventory", "inv", "shack"])
    async def shed(self, ctx: Context, *, member: discord.Member = None):
        pass

    @commands.command()
    async def buy(self, ctx: Context, amount: int, item: str):
        pass

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
                    value=f"\t id `{id}`\n\tPrice: **{price}**\n\t {desc}",
                    inline=False,
                )
                em.set_author(
                    name="Potato Industry Tools Shack",
                    icon_url="https://cdn.discordapp.com/avatars/839966871143186472/1a802ca9786c5bf56cde2ca3ed14dce6.webp?size=1024",
                )
        await ctx.send(embed=em)

    @commands.command(aliases=["gift", "gib", "send", "transfer"])
    async def give(self, ctx: Context, member: discord.Member, amount=None):
        pass

    @commands.command(aliases=["add"])
    @commands.is_owner()
    async def addpotatoes(self, ctx: Context, member: discord.Member, amount):
        pass

    @addpotatoes.error
    async def addpotatoes_error(self, ctx: Context, error):
        pass

    @commands.command(aliases=["gamble"])
    async def coinflip(self, ctx: Context, amount=None):
        pass

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def sabotage(self, ctx: Context, *, member: discord.Member):
        pass

    @sabotage.error
    async def sabotage_error(self, ctx: Context, error):
        pass

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def rob(self, ctx: Context, *, member: discord.Member):
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

    ### Helper Methods

    async def getAllUsersData(self) -> dict:
        return self.usersDataWrapper.getAllUserData()

    async def getUserData(self, user: discord.Member) -> dict:
        return self.usersDataWrapper[str(user.id)]

    async def getUserBal(self, user: discord.Member) -> dict:
        userDat = await self.getUserData(user)
        return userDat["bal"]

    async def getUserInv(self, user: discord.Member) -> dict:
        userDat = await self.getUserData(user)
        return userDat["inv"]

    async def createAccount(self, user: discord.Member) -> bool:
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

    async def addAmountTo(self, user: discord.Member, change=0, mode="wallet"):
        userBalDat = await self.getUserBal(user)
        userBalDat[mode] += change

    async def set_balance(self, user: discord.Member, wallet: int, bank: int):
        pass

    async def sell_this(self, user, item_name, amount, price=None):
        pass

    async def get_shop_item(self, item_name: str) -> dict | None:
        pass

    async def get_shop_items(self) -> dict:
        pass

    async def buy_this(self, user, item_name: str, amount: int):
        pass

    async def trueDepositAmount(self, ctx: Context, bal: dict, amount=None) -> int:
        """returns true amount to deposit\n
        A valid amount is > 0
        """
        if amount == None:
            await ctx.send(
                "You have to enter an amount to deposit <:seriously:809518766470987799>"
            )
            return 0
        elif amount == "all" or amount == "max":
            if bal["wallet"] == 0:
                await ctx.send("imagine depositing 0 potatoes amirite")
                return 0
            else:
                amount = bal["wallet"]

        amount = int(amount)
        if amount > bal["wallet"]:
            await ctx.send(
                "You're too poor to deposit potatoes <:XD:806659054721564712>"
            )
            return 0
        elif amount < 0:
            await ctx.send(
                "How the hecc u think you can deposit negative potatoes <:pepe_hehe:816898198315597834>"
            )
            return 0
        elif amount == 0:
            await ctx.send("are you *trying* to break me <:sus:809828043244961863>")
            return 0

        return amount


async def setup(bot: commands.Bot):
    await bot.add_cog(EconomyCommands(bot))
