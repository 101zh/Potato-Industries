import discord, json, random
from discord.ext import commands
from discord.ext.commands import Context

import discord.ext
import discord.ext.tasks


class EconomyCommands(commands.Cog):
    def __init__(self, bot: commands.Bot, usersData: dict):
        self = self
        self.bot = bot
        self.usersData = usersData

        self.begList = [
            f"author.mention recived **earnings.money** :potato: from **nosrep** :0",
            f"author.mention found **earnings.money** :potato: while searching through a dumpster",
            f"**earnings.money** :potato: fell from the sky and landed in author.mention's arms",
            f"author.mention summoned **earnings.money** :potato:",
        ]
        self.farmListPositive = [
            f"You farmed potatoes and collected **earnings.money** :potato: :0",
            f"When farming for potatoes, a depressed potato drops **earnings.money** :potato: which you pick up",
            f"Some of your potatoes decided to get married and gives birth to **earnings.money** :potato: baby potatoes <:quackity_shy:838192314114506762>",
            f"Dank Memer gives you **earnings.money** :potato: (cursed??)",
        ]
        self.farmListNegative = [
            f"You farmed potatoes and collected **earnings.money** :potato: :0",
            f"When farming for potatoes, a depressed potato drops **earnings.money** :potato: which you pick up",
            f"Some of your potatoes decided to get married and gives birth to **earnings.money** :potato: baby potatoes <:quackity_shy:838192314114506762>",
            f"Dank Memer gives you **earnings.money** :potato: (cursed??)",
        ]
        self.personList = [
            "Donald Trump",
            "Elon Musk",
            "that one weird dude in your class",
            "Dank Memer",
            "<@698218089010954481>",
            "Eren Jeager",
            "the kid who thinks its 2018",
            "Barack Obama",
            "<@710709742791819274>",
        ]

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
        pass

    @commands.command(aliases=["gift", "gib", "send", "transfer"])
    async def give(self, ctx: Context, member: discord.Member, amount=None):
        pass

    @commands.command(aliases=["bal", "potats", "potatoes", "vault"])
    async def balance(self, ctx: Context, *, mention: discord.Member = None):
        person = ctx.author
        if mention != None:
            person = mention

        await self.create_account(person)
        userBankData = await self.getBal(person)
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
        await self.create_account(ctx.author)
        bal = await self.getBal(ctx.author)

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
        await self.create_account(ctx.author)

        # Exceptions non-integer inputs
        if amount == None:
            await ctx.send(
                "You have to enter an amount to withdraw <:seriously:809518766470987799>"
            )
            return
        bal = await self.getBal(ctx.author)
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
    # @commands.cooldown(1, 60, commands.BucketType.user)
    async def beg(self, ctx: Context):
        """By begging invoking member gains a random number of potatoes"""
        await self.create_account(ctx.author)

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
        pass

    @farm.error
    async def farm_error(self, ctx: Context, error):
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

    async def getUser(self, user: discord.Member) -> dict:
        return self.usersData[str(user.id)]

    async def getBal(self, user: discord.Member) -> dict:
        userDat = await self.getUser(user)
        return userDat["bal"]

    async def get_inv(self, user: discord.Member) -> dict:
        userDat = await self.getUser(user)
        return userDat["inv"]

    async def create_account(self, user: discord.Member) -> bool:
        """Creates user data entry, if not already present"""

        userID = str(user.id)
        if userID in self.usersData:
            return False
        else:
            self.usersData[userID] = {}
            self.usersData[userID]["bal"] = {}
            self.usersData[userID]["bal"]["wallet"] = 0
            self.usersData[userID]["bal"]["bank"] = 0
            self.usersData[userID]["inv"] = {}
        with open("database/userdata.json", "w") as f:
            json.dump(self.usersData, f)
        return True

    async def addAmountTo(self, user: discord.Member, change=0, mode="wallet"):
        userBalDat = await self.getBal(user)
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
