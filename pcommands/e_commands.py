import discord, json, random
from discord.ext import commands
from discord.ext.commands import Context


class EconomyCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self = self
        self.bot = bot

    @commands.command()
    async def use(self, ctx: Context, amount_used: int, *, item: str = None):
        if not item:
            await ctx.send(
                "try formatting it like this: `p!use {amount} {item}` \nExample: `p!use 1 lottery potato`"
            )
            return
        elif amount_used < 0:
            await ctx.send("You can't use a negative amount")
            return
        elif amount_used == 0:
            await ctx.send("What are you trying to do here?")
            return

        item = item.lower()

        # Uses the item; returns a negative # if the item isn't found
        error = await self.update_user_shed(ctx.author, item, amount_used)
        if error == -1:
            await ctx.send("You don't have that item")
            return
        elif error == -2:
            await ctx.send("You can't use more than you have")
            return

        if item == "lottery potato":
            await self.use_lottery_potato(ctx=ctx, amount=amount_used)
        else:
            await ctx.send(
                "please use a valid item or try formatting it like this: `p!use {amount} {item}` \nExample: `p!use 1 lottery potato`"
            )

    @commands.command(aliases=["gift", "gib", "send", "transfer"])
    async def give(self, ctx: Context, member: discord.Member, amount=None):
        if ctx.author.id in self.bot.ids:
            await ctx.send(
                "You cant give people potatoes, your in passive <:potato_angry:814539600235986964>"
            )
        elif member.id in self.bot.ids:
            await ctx.send(
                "Leave that passive potato alone <:potato_angry:814539600235986964>"
            )
        else:
            await self.open_account(ctx.author)
            await self.open_account(member)
            if amount == None:
                await ctx.send(
                    "You have to enter an amount to deposit <:seriously:809518766470987799>"
                )
                return
            bal = await self.update_bank(ctx.author)
            if amount == "all":
                if bal[0] == 0:
                    await ctx.send(
                        "ah yes, im sure {member.name} would love 0 potatoes <:noice:809518758262603786>"
                    )
                elif bal[0] < 0:
                    await ctx.send("You can't send someone negative :potato: kek")
                else:
                    amount = bal[0]
            amount = int(amount)
            if amount > bal[0]:
                await ctx.send(
                    f"You're too poor to give {amount} potatoes <:XD:806659054721564712>"
                )
                return
            if amount < 0:
                await ctx.send(
                    "How the hecc u think you can give negative potatoes <:pepe_hehe:816898198315597834>"
                )
                return
            if amount == 0:
                await ctx.send(
                    f"ah yes, im sure {member.name} would love 0 potatoes <:noice:809518758262603786>"
                )
                return
            await self.update_bank(ctx.author, -1 * amount, "wallet")
            await self.update_bank(member, amount, "wallet")
            await ctx.send(f"You gave **{amount}** :potato: to {member.mention}!")

    async def open_account(self, user):
        users = await self.get_user_data()
        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 0
            users[str(user.id)]["bank"] = 0
        with open("database/potato.json", "w") as f:
            json.dump(users, f)
        return True

    async def update_bank(
        self, user: discord.Member, change=0, mode="wallet"
    ) -> list[int]:
        users = await self.get_user_data()
        users[str(user.id)][mode] += change
        with open("database/potato.json", "w") as f:
            json.dump(users, f)
        bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
        return bal

    async def update_user_shed(
        self, user: discord.Member, item: str, amount_used: int
    ) -> int:
        item = item.lower()
        users = await self.get_user_data()
        usershed = users[str(user.id)]["shed"]

        # Getting the index that x item is stored at
        index = -1
        for i in range(len(usershed)):
            if usershed[i]["item"] == item:
                index = i

        # Checking if the item is found
        if index != -1:
            updated_amount = usershed[index]["amount"] - amount_used

            # Checking that the new amount isn't negative
            if updated_amount < 0:
                return -2

            # Actually using the item
            if updated_amount == 0:
                del usershed[index]
            else:
                usershed[index]["amount"] = updated_amount

            users[str(user.id)]["shed"] = usershed
            with open("database/potato.json", "w") as f:
                json.dump(users, f)

            return index
        else:
            return -1

        # -2 if amount_used makes amount < 0
        # -1 is for not found
        # any other # means that it's successful

    async def get_user_data(self) -> dict:
        with open("database/potato.json", "r") as f:
            users = json.load(f)
        return users

    async def use_lottery_potato(self, ctx: Context, amount: int) -> None:
        times_won = 0
        for i in range(amount):
            chance = random.randint(0, 100)
            if chance <= 5:
                times_won += 1

        if times_won > 0:
            amount_won = times_won * 42069
            await self.update_bank(ctx.author, amount_won)
            await ctx.send(f"You won {amount_won} congratulations!")
        else:
            await ctx.send("Sorry, you didn't win anything")

    @commands.command(aliases=["cya"])
    async def sell(self, ctx: Context, amount=1, *, item):
        try:
            await self.open_account(ctx.author)

            res = await self.sell_this(ctx.author, item, amount)

            if not res[0]:
                if res[1] == 1:
                    await ctx.send(
                        "That item isnt there <:seriously:809518766470987799>"
                    )
                    return
                if res[1] == 2:
                    await ctx.send(f"You don't have {amount} {item} in your shed.")
                    return
                if res[1] == 3:
                    await ctx.send(f"You don't have {item} in your shed.")
                    return

            await ctx.send(f"You just sold **{amount} {item}**")
        except:
            await ctx.send(
                "try formatting it like this: `p!sell {amount} {item}` \nExample: `p!sell 1 iron hoe`"
            )

    @commands.command()
    @commands.cooldown(1, 2700, commands.BucketType.user)
    async def dig(self, ctx: Context):
        items = [
            "golden potato",
            "dirty potato",
            "dirty potato",
            "dirty potato",
            "dirty potato",
            "dirty potato",
            "dirty potato",
            "dirty potato",
            "dirty potato",
            "dirty potato",
            "invisible potato",
            "invisible potato",
            "potato chip",
            "potato chip",
            "potato chip",
            "potato chip",
            "potato chip",
        ]

        await self.open_account(ctx.author)
        item = random.choice(items)
        await self.buy_this(ctx.author, item, 1)
        # help
        # ok? what's the goal

        embed = discord.Embed(
            description=f"You dug up **1 {item}** :0", color=discord.Colour.blue()
        )
        await ctx.send(embed=embed)

    @sell.error
    async def sell_error(self, ctx: Context, error):
        await ctx.send(
            "try formatting it like this: p!buy {amount} {item}\n Example: p!sell 1 iron hoe"
        )

    @dig.error
    async def dig_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 1hr)".format(
                error.retry_after
            )
            await ctx.send(msg)
        else:
            raise error

    async def sell_this(self, user, item_name, amount, price=None):
        item_name = item_name.lower()
        name_ = None
        for item in mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                if price == None:
                    price = 0.9 * item["price"]
                break

        if name_ == None:
            return [False, 1]

        cost = price * amount

        users = await self.get_user_data()

        bal = await self.update_bank(user)

        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["shed"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt - amount
                    if new_amt < 0:
                        return [False, 2]
                    users[str(user.id)]["shed"][index]["amount"] = new_amt
                    t = 1
                    break
                index += 1
            if t == None:
                return [False, 3]
        except:
            return [False, 3]

        with open("database/potato.json", "w") as f:
            json.dump(users, f)

        await self.update_bank(user, abs(cost), "wallet")

        return [True, "Worked"]

    async def get_shop_item(self, item_name: str) -> dict | None:
        shop_items = await self.get_shop_items()
        try:
            return shop_items[item_name]
        except KeyError:
            return None

    async def get_shop_items(self) -> dict:
        with open("assets/shopitems.json", "r") as f:
            shop_items = json.load(f)
        return shop_items

    async def buy_this(self, user, item_name: str, amount: int):
        item_name = item_name.lower()
        item_data = await self.get_shop_item(item_name)

        if item_data == None:
            return [False, 1]
        cost = item_data["price"] * amount
        users = await self.get_user_data()
        bal = await self.update_bank(user)
        if bal[0] < cost:
            return [False, 2]
        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["shed"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt + amount
                    users[str(user.id)]["shed"][index]["amount"] = new_amt
                    t = 1
                    break
                index += 1
            if t == None:
                obj = {"item": item_name, "amount": amount}
                users[str(user.id)]["shed"].append(obj)
        except:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["shed"] = [obj]
        with open("database/potato.json", "w") as f:
            json.dump(users, f)
        await self.update_bank(user, cost * -1, "wallet")
        return [True, "Worked"]

    @commands.command(aliases=["tools", "inventory", "inv", "shack"])
    async def shed(self, ctx: Context, *, member: discord.Member = None):
        if member:
            await self.open_account(member)
            user = member
            users = await self.get_user_data()
            try:
                shed = users[str(user.id)]["shed"]
            except:
                shed = []
            em = discord.Embed(title=f"{member.name}'s Shed", color=0x7289DA)
            for item in shed:
                name = item["item"]
                amount = item["amount"]
                if amount == 0:
                    continue
                else:
                    em.add_field(name=name, value=f"Amount: {amount}", inline=False)
            await ctx.send(embed=em)
        else:
            await self.open_account(ctx.author)
            user = ctx.author
            users = await self.get_user_data()
            try:
                shed = users[str(user.id)]["shed"]
            except:
                shed = []
            em = discord.Embed(title=f"{ctx.author.name}'s Shed", color=0x7289DA)
            for item in shed:
                name = item["item"]
                amount = item["amount"]
                if amount == 0:
                    continue
                else:
                    em.add_field(name=name, value=f"Amount: {amount}", inline=False)
            await ctx.send(embed=em)

    @commands.command()
    async def buy(self, ctx: Context, amount: int, item: str):
        if amount < 0:
            await ctx.send("hey, are you trying to break me?")
        else:
            try:
                amount = int(amount)
                await self.open_account(ctx.author)
                res = await self.buy_this(ctx.author, item, amount)
                if not res[0]:
                    if res[1] == 1:
                        await ctx.send("The tool isn't in the shop")
                        return
                    if res[1] == 2:
                        if amount == 1:
                            await ctx.send(
                                f"You don't have enough potatoes in your pocket to purchase a **{item}** <:XD:806659054721564712>"
                            )
                            return
                        else:
                            await ctx.send(
                                f"You don't have enough potatoes in your pocket to purchase **{amount} {item}s** <:XD:806659054721564712>"
                            )
                            return
                await ctx.send(f"You just bought **{amount} {item}** :0")
            except:
                await ctx.send(
                    "try formatting it like this: `p!buy {amount} {item}` \nExample: `p!buy 1 iron hoe`"
                )

    @commands.command(aliases=["store", "market"])
    async def shop(self, ctx: Context):
        em = discord.Embed(color=0x2ECC71)
        for item in mainshop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            name = "**" + name + "**"
            if name == "**golden potato**" or name == "**test item**":
                pass
                print("hi")
            else:
                em.add_field(name=name, value=f"**{price}** {desc}", inline=False)
                em.set_author(
                    name="Potato Industry Tools Shack",
                    icon_url="https://cdn.discordapp.com/avatars/839966871143186472/1a802ca9786c5bf56cde2ca3ed14dce6.webp?size=1024",
                )
        await ctx.send(embed=em)

    @commands.command(aliases=["bal", "potats", "potatoes", "vault"])
    async def balance(self, ctx: Context, *, mention: discord.Member = None):
        if mention:
            await self.open_account(mention)
            user = mention
            users = await self.get_user_data()
            wallet_amt = users[str(mention.id)]["wallet"]
            bank_amt = users[str(mention.id)]["bank"]
            if wallet_amt < 0:
                await self.update_bank(mention, -1 * wallet_amt)
            else:
                pass
            embed = discord.Embed(
                title=f"{mention.name}'s potatoes", color=discord.Colour.green()
            )
            embed.add_field(name="Pocket", value=f"{wallet_amt} :potato:")
            embed.add_field(name="Vault", value=f"{bank_amt} :potato:")
            embed.set_footer(text="Made by DepressedPotato")
            embed.set_thumbnail(url=mention.avatar)
            await ctx.send(embed=embed)
        else:
            await self.open_account(ctx.author)
            user = ctx.author
            users = await self.get_user_data()
            wallet_amt = users[str(user.id)]["wallet"]
            bank_amt = users[str(user.id)]["bank"]
            if wallet_amt < 0:
                await self.update_bank(ctx.author, -1 * wallet_amt)
            else:
                pass
            embed = discord.Embed(
                title=f"{ctx.author.name}'s potatoes", color=discord.Colour.green()
            )
            embed.add_field(name="Pocket", value=f"{wallet_amt} :potato:")
            embed.add_field(name="Vault", value=f"{bank_amt} :potato:")
            embed.set_footer(text="Made by DepressedPotato")
            embed.set_thumbnail(url=ctx.author.avatar)
            await ctx.send(embed=embed)

    @commands.command(aliases=["search"])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def beg(self, ctx: Context):
        await self.open_account(ctx.author)
        person_list = [
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
        users = await self.get_user_data()
        user = ctx.author
        earnings = random.randint(1000, 2000)
        person = random.choice(person_list)
        beg_list = [
            f"{ctx.author.mention} recived **{earnings}** :potato: from **{person}** :0",
            f"{ctx.author.mention} found **{earnings}** :potato: while searching through a dumpster",
            f"**{earnings}** :potato: fell from the sky and landed in {ctx.author.mention}'s arms",
            f"{ctx.author.mention} summoned **{earnings}** :potato:",
        ]
        embed = discord.Embed(description=random.choice(beg_list), color=0x2ECC71)
        await ctx.send(embed=embed)
        users[str(user.id)]["wallet"] += earnings
        with open("database/potato.json", "w") as f:
            json.dump(users, f)

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
        await ctx.send("start farm command")
        await self.open_account(ctx.author)
        users = await self.get_user_data()
        user = ctx.author
        earnings = random.randrange(-50, 50)
        try:
            shed = users[str(user.id)]["shed"]
        except:
            shed = []
        test = []
        for i in shed:
            name = i["item"]
            test.append(name)
        if "stone hoe" in test:
            earnings = random.randrange(-50, 75)
            if "iron hoe" in test:
                earnings = random.randrange(-25, 75)
                if "diamond hoe" in test:
                    earnings = random.randrange(-25, 100)
                else:
                    earnings = random.randrange(-25, 75)
            else:
                earnings = random.randrange(-50, 75)
                if "diamond hoe" in test:
                    earnings = random.randrange(-25, 100)
                else:
                    earnings = random.randrange(-50, 75)
        else:
            if "iron hoe" in test:
                earnings = random.randrange(-25, 75)
                if "diamond hoe" in test:
                    earnings = random.randrange(-25, 100)
                else:
                    earnings = random.randrange(-25, 75)
            else:
                if "diamond hoe" in test:
                    earnings = random.randrange(-25, 100)
                else:
                    earnings = random.randrange(-50, 51)
        if earnings < 0:
            sentences = [
                f"When collecting the potatoes you've farmed, you trip and lose **{earnings}** :potato:",
                f"Technoblade decides to steal **{earnings}** :potato: from you",
                f"A nuclear air strike blows up your warehouse and you lose **{earnings}** :potato:",
                f"You mom catches you farming potatoes when you're supposed to be doing homework and she takes **{earnings}** :potato:",
            ]
            embed = discord.Embed(description=random.choice(sentences), color=0x2ECC71)
        elif earnings > 0:
            sentences = [
                f"You farmed potatoes and collected **{earnings}** :potato: :0",
                f"When farming for potatoes, a depressed potato drops **{earnings}** :potato: which you pick up",
                f"Some of your potatoes decided to get married and gives birth to **{earnings}** :potato: baby potatoes <:quackity_shy:838192314114506762>",
                f"Dank Memer gives you **{earnings}** :potato: (cursed??)",
            ]
            embed = discord.Embed(description=random.choice(sentences), color=0x2ECC71)
        else:
            embed = discord.Embed(
                description="wow i cant believe youve actually farmed **0 :potato:** ill give u **696969 :potato:** cuz i feel kinda bad..."
            )
            earnings = 696969
        users[str(user.id)]["wallet"] += earnings
        with open("database/potato.json", "w") as f:
            json.dump(users, f)
        await ctx.send(embed=embed)

    @farm.error
    async def farm_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 1s)".format(
                error.retry_after
            )
            await ctx.send(msg)
        else:
            raise error

    @commands.command(aliases=["add"])
    @commands.is_owner()
    async def addpotatoes(self, ctx: Context, member: discord.Member, amount):
        await self.open_account(member)
        users = await self.get_user_data()
        user = member
        users[str(user.id)]["wallet"] += int(amount)
        with open("database/potato.json", "w") as f:
            json.dump(users, f)
        await ctx.send(f"Added **{amount}** :potato: to {member.mention}")

    @addpotatoes.error
    async def addpotatoes_error(self, ctx: Context, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("You cant do that!")

    @commands.command(aliases=["dep"])
    async def deposit(self, ctx: Context, amount=None):
        await self.open_account(ctx.author)
        if amount == None:
            await ctx.send(
                "You have to enter an amount to deposit <:seriously:809518766470987799>"
            )
            return
        bal = await self.update_bank(ctx.author)
        if amount == "all" or amount == "max":
            if bal[0] == "0":
                await ctx.send("imagine depositing 0 potatoes amirite")
            else:
                amount = bal[0]
        amount = int(amount)
        if amount > bal[0]:
            await ctx.send(
                "You're too poor to deposit potatoes <:XD:806659054721564712>"
            )
            return
        if amount < 0:
            await ctx.send(
                "How the hecc u think you can deposit negative potatoes <:pepe_hehe:816898198315597834>"
            )
            return
        if amount == 0:
            await ctx.send("are you *trying* to break me <:sus:809828043244961863>")
            return
        await self.update_bank(ctx.author, -1 * amount)
        await self.update_bank(ctx.author, amount, "bank")
        await ctx.send(f"You deposited **{amount}** :potato: :0")

    @commands.command(aliases=["gamble"])
    async def coinflip(self, ctx: Context, amount=None):
        # Exceptions
        if amount == None:
            await ctx.send(
                "You have to enter an amount to play <:seriously:809518766470987799>"
            )
            return

        await self.open_account(ctx.author)
        bal = await self.update_bank(ctx.author)
        gamble_amount = 0

        if amount == "all":
            gamble_amount = bal[0]
        else:
            gamble_amount = int(amount)

        # More Exceptions
        if gamble_amount > bal[0]:
            await ctx.send(
                f"You're too poor to play with {gamble_amount} potatoes <:XD:806659054721564712>"
            )
            return
        elif gamble_amount < 0:
            await ctx.send(
                "How the hecc u think you can play with negative potatoes <:pepe_hehe:816898198315597834>"
            )
            return
        elif gamble_amount > 100000:
            await ctx.send(
                "youre gambling too much the economy will collapse :potato_angry:"
            )
            return
        elif gamble_amount == 0:
            await ctx.send(
                "what are you doing trying to gamble 0 potatoes <:sus:809828043244961863>"
            )
            return

        # The actual coinlfip
        coin = random.randint(1, 10)
        if coin < 6:
            await self.update_bank(ctx.author, +1 * gamble_amount)
            embed = discord.Embed(
                title=f"You won **{gamble_amount}** :potato: \:D", color=0x3498DB
            )
            embed.set_footer(text="thats pretty pog ngl")
            await ctx.send(embed=embed)
        else:
            await self.update_bank(ctx.author, -1 * gamble_amount)
            embed = discord.Embed(
                title=f"You lost **{gamble_amount}** :potato: ;-;", color=0xE74C3C
            )
            embed.set_footer(text="lol imagine losing in a coin flip")
            await ctx.send(embed=embed)

    @commands.command(aliases=["with"])
    async def withdraw(self, ctx: Context, amount=None):
        await self.open_account(ctx.author)
        if amount == None:
            await ctx.send(
                "You have to enter an amount to withdraw <:seriously:809518766470987799>"
            )
            return
        bal = await self.update_bank(ctx.author)
        if amount == "all" or amount == "max":
            amount = bal[1]
        amount = int(amount)
        if amount > bal[1]:
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
        await self.update_bank(ctx.author, amount)
        await self.update_bank(ctx.author, -1 * amount, "bank")
        await ctx.send(f"You withdrew **{amount}** :potato:  :0")

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def sabotage(self, ctx: Context, *, member: discord.Member):
        if ctx.author.id in self.bot.ids:
            await ctx.send(
                "You cant sabotage people, your in passive <:potato_angry:814539600235986964>"
            )
        elif member.id in self.bot.ids:
            await ctx.send(
                "Leave that passive potato alone <:potato_angry:814539600235986964>"
            )
        else:
            if member == ctx.author:
                await ctx.send("you cant sabotage yourself lmao")
                self.sabotage.reset_cooldown(ctx)
                return
            elif member == self.bot.user:
                await ctx.send("hecc u dont try to sabotage me")
                self.sabotage.reset_cooldown(ctx)
                return
            else:
                pass
            await self.open_account(ctx.author)
            await self.open_account(member)
            bal = await self.update_bank(member)
            bal2 = await self.update_bank(ctx.author)
            if bal2[0] < 100000:
                await ctx.send(
                    "u need at least **100000** :potato: to sabotage someone <:potato_angry:814539600235986964>"
                )
                self.sabotage.reset_cooldown(ctx)
                return
            elif bal[1] < 10000:
                await ctx.send(
                    "dang bro this dude tryna sabotage a dude with less than **10000** :potato: in their vault <:ban_hammer:806216052426014751>"
                )
                self.sabotage.reset_cooldown(ctx)
                return
            earnings = random.randrange(-1 * bal[1], 0)
            await self.update_bank(member, earnings, "bank")
            await self.update_bank(ctx.author, -100000)
            e = [
                f"{ctx.author.mention} sabotaged {member.mention} and {member.mention} lost **{earnings} :potato:**",
                f"{ctx.author.mention} planted bombs under {member.mention}'s storage and they lost **{earnings} :potato:**",
                f"{ctx.author.mention} snuck into {member.mention}'s potato stack and went on a farting spree, instantly making **{earnings} :potato:** unedible",
            ]
            embed = discord.Embed(description=random.choice(e), color=0x2ECC71)
            await ctx.send(embed=embed)
            embed2 = discord.Embed(
                description=f"{ctx.author.mention} sabotage you and you lost **{earnings} :potato:**  \nhttps://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}",
                color=0x2ECC71,
            )
            try:
                await member.send(embed=embed2)
            except Exception as e:
                print(e)

    @sabotage.error
    async def sabotage_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 1hr)".format(
                error.retry_after
            )
            await ctx.send(msg)
        elif isinstance(error, commands.MemberNotFound):
            msg = (
                f"Sorry, I couldnt find that user. Try sabotaging someone in ur server"
            )
            await ctx.send(msg)
            self.sabotage.reset_cooldown(ctx)
        else:
            print(error)
            self.sabotage.reset_cooldown(ctx)

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def rob(self, ctx: Context, *, member: discord.Member):
        if ctx.author.id in self.bot.ids:
            await ctx.send(
                "You cant rob people, your in passive <:potato_angry:814539600235986964>"
            )
            self.rob.reset_cooldown(ctx)
        elif member.id in self.bot.ids:
            await ctx.send(
                "Leave that passive potato alone <:potato_angry:814539600235986964>"
            )
            self.rob.reset_cooldown(ctx)
        else:
            if member == ctx.author:
                await ctx.send("you cant rob yourself lmao")
                self.rob.reset_cooldown(ctx)
                return
            elif member == self.bot.user:
                await ctx.send("hecc u dont try to rob me")
                self.rob.reset_cooldown(ctx)
                return
            else:
                pass
            await self.open_account(member)
            await self.open_account(ctx.author)
            users = await self.get_user_data()
            user = ctx.author
            try:
                shed = users[str(user.id)]["shed"]
            except:
                shed = []
            test = []
            for i in shed:
                name = i["item"]
                test.append(name)
            bal = await self.update_bank(member)
            bal2 = await self.update_bank(ctx.author)
            if bal2[0] < 10000:
                await ctx.send(
                    "u need at least **10000** :potato: to rob someone <:potato_angry:814539600235986964>"
                )
                self.rob.reset_cooldown(ctx)
                return
            elif bal[0] < 1000:
                await ctx.send(
                    "dang bro this dude tryna rob a dude with less than 1000 :potato: <:ban_hammer:806216052426014751>"
                )
                self.rob.reset_cooldown(ctx)
                return
            earnings = random.randrange(-1 * bal2[0], bal[0])
            # test 1: check if custom rob items work --> hopefully we can make rob prevention items soon, that would be nice
            if "Potato Cannon" in test:
                earnings = bal[0]
            await self.update_bank(ctx.author, earnings)
            await self.update_bank(member, -1 * earnings)
            if earnings < 0:
                neg_reply = [
                    f'You try to rob {member.mention} but had to poop and during ur "break" got robbed by {member.mention}, losing **{earnings} :potato:**',
                    f"You trip and fall, scattering some potatoes all over the ground, and {member.mention} picks it up. You come home, depressed, with **{earnings} :potato:**",
                ]
                embed = discord.Embed(
                    description=random.choice(neg_reply), color=0xE67E22
                )
                await ctx.send(embed=embed)
                earnings = earnings * -1
                embed = discord.Embed(
                    description=f"{ctx.author.mention} got caught trying to rob you and you earn **{earnings} :potato:** <:XD:806659054721564712> \nhttps://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}",
                    color=0x2ECC71,
                )
                try:
                    await member.send(embed=embed)
                except Exception as e:
                    print(e)
            elif earnings > 0:
                pos_reply = [
                    f"{member.mention} was bragging about their pile of potatoes and you took **{earnings} :potato:** from {member.mention}",
                    f"You broke into {member.mention}'s secret vault and stole **{earnings} :potato:**:0",
                ]
                # test 1: check if custom rob items work --> hopefully we can make rob prevention items soon, that would be nice
                if "Potato Cannon" in test:
                    pos_reply = [
                        f"You pulled out a **Potato Cannon** and murdered {member.mention} in cold blood. You took all their potatoes, making {earnings} :potato:."
                    ]
                embed = discord.Embed(
                    description=random.choice(pos_reply), color=0x2ECC71
                )
                await ctx.send(embed=embed)
                embed = discord.Embed(
                    description=f"{ctx.author.mention} robbed you and you lost **-{earnings} :potato:** <:potato_ummmm:819025209428410388>  \nhttps://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}",
                    color=0x2ECC71,
                )
                try:
                    await member.send(embed=embed)
                except Exception as e:
                    print(e)
            else:
                await ctx.send(
                    f"dang u robbed {member.mention} and got literally nothing <:pepe_l:816898198315597834> \nhttps://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}",
                    color=0x2ECC71,
                )

    @rob.error
    async def rob_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 5m)".format(
                error.retry_after
            )
            await ctx.send(msg)
        elif isinstance(error, commands.MemberNotFound):
            msg = f"Sorry, I couldnt find that user. Try robbing someone in ur server"
            await ctx.send(msg)
            self.rob.reset_cooldown(ctx)
        else:
            print(error)
            self.rob.reset_cooldown(ctx)


    @commands.command(aliases=["lb", "rich"])
    async def leaderboard(self, ctx: Context):
        x = 10
        users = await self.get_user_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)
        total = sorted(total, reverse=True)
        em = discord.Embed(
            title=f"Top {x} Richest People",
            description="This is decided on the basis of potatoes in **POCKET AND VAULT**",
            color=discord.Color(0xFA43EE),
        )
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = self.bot.get_user(id_)
            name = member
            em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
            if index == x:
                break
            else:
                index += 1
        await ctx.send(embed=em)

    @commands.command(aliases=["lbreverse", "richreverse"])
    async def leaderboardreverse(self, ctx: Context):
        x = 10
        users = await self.get_user_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)
        total = sorted(total, reverse=False)
        em = discord.Embed(
            title=f"Top {x} Richest People",
            description="This is decided on the basis of potatoes in **POCKET AND VAULT**",
            color=discord.Color(0xFA43EE),
        )
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = self.bot.get_user(id_)
            name = member
            em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
            if index == x:
                break
            else:
                index += 1
        await ctx.send(embed=em)
