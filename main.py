import discord, os, json, random, aiohttp
from discord.ext.commands import cooldown, BucketType, Context
from discord.ext import commands
from discord import Guild, Client
from discord.ext import *
from datetime import *
from datetime import datetime
import datetime as dt  # why the hell is there a breakpoint here
from keep_alive import keep_alive
import io
from pcommands.e_commands import EconomyCommands
import utils.blacklist as botbans
import asyncio
from pcommands.help_commands import HelpCommands
from pcommands.dev_commands import StaffCommands, DeveloperCommands

# feel free to change the name of the import whenever you want
# :0 ty


def get_prefix(client, message):
    with open("database/prefixes.json", "r") as f:
        prefixes = json.load(f)
    try:
        return prefixes[str(message.guild.id)]
    except:
        return "p!"


# code setup
bot = commands.Bot(
    command_prefix=get_prefix, intents=discord.Intents.all(), case_insensitive=True
)
bot.remove_command("help")
WEBHOOK_URL = "<redacted>"
redditlist = [
    "https://www.reddit.com/r/memes/new.json",
    "https://www.reddit.com/r/dankmemes/new.json",
    "https://www.reddit.com/r/meme/new.json",
]

# get rid of this later, check assets/shopitems.json and assets/readme.md
# ok

mainshop = [
    {
        f"name": "Stone hoe",
        "price": 5000,
        "description": "`p!buy 1 stone hoe` Slightly better than the wooden hoe, but still has room for improvement. Range is changed from *-50, 50* to *-50, 75*",
    },
    {
        f"name": "Iron hoe",
        "price": 25000,
        "description": "`p!buy 1 iron hoe` A fast, reliable farming tool. You feel energised when wielding it. Range is changed from *-50, 50* to *-25, 75*",
    },
    {
        f"name": "Diamond hoe",
        "price": 100000,
        "description": "`p!buy 1 diamond hoe` The shimmering blue blade increases your potato farming abilities. Range is changed from *-50, 50* to *-25, 100*",
    },
    {
        f"name": "Potato trophy",
        "price": 5000000,
        "description": "`p!buy 1 potato trophy` Flex your 5mil potatoes with this trophy. Only the rich can afford this.",
    },
    {
        f"name": "Lottery Potato",
        "price": 5000,
        "description": "`p!buy 1 lottery potato` When used, offers a 5% chance of earning 42069 :potato:. Can also be collected through digging.",
    },
    {
        f"name": "Golden Potato",
        "price": 50000,
        "description": "`p!buy 1 golden potato` The holy golden potato. Can also be collected through digging.",
    },
    {
        f"name": "Invisible Potato",
        "price": 5000,
        "description": "`p!buy 1 invisible potato` Basically Lay's chips. Can also be collected through digging.",
    },
    {
        f"name": "Rotten Potato",
        "price": 10,
        "description": "`p!buy 1 dirty potato` Why would you buy this. Can also be collected through digging.",
    },
    {
        f"name": "Potato Chip",
        "price": 10,
        "description": "`p!buy 1 potato chip` A single potato chip. Can also be collected through digging.",
    },
    {
        f"name": "Potato Cannon",
        "price": 1e500,
        "description": "Test item for a future code project. When robbing someone automatically take all their potatoes from their pocket because they'll die from the impact of an explosive potato on their back... (unless they're passive). Watch your back!",
    },
]

launch_time = datetime.utcnow()


blacklisted = []
# for fun yay thunderredstar
# bruh

@bot.event
async def on_message(message: discord.Message):
    # Implementing botban check.
    # ok
    if message.content.startswith("p!") and message.author != bot.user:
        try:
            print(f"{message.content} | {message.author.name} | {message.guild.name}")
            botbanned = botbans.check_blacklist(message.author.id)
            if botbanned:
                duration = botbans.get_duration(message.author.id, True)
                await message.channel.send(
                    "You are blacklisted for " + duration + ". Please try again later."
                )
                return
        except Exception:
            print("ono something went wrong ;-;")
    if message.channel.id in bot.ids and message.author != bot.user:
        if message.content != "e":
            await message.delete()
        else:
            await message.channel.send("e")
    try:
        if message.mentions[0] == bot.user:
            with open("database/prefixes.json", "r") as f:
                prefixes = json.load(f)
            pre = prefixes[str(message.guild.id)]
            try:
                await message.channel.send(f"My prefix for this server is `{pre}`")
            except Exception as e:
                await message.channel.send(f"`{e}`")
    except:
        pass
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    await bot.process_commands(message)


@bot.command()
async def poll(ctx: Context, *, message=None):
    if message == None:
        await ctx.send(f"Cannot create a poll with no message!")
        return

    questions = [f"Which channel should your poll be sent to?", f"emojies?"]
    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
        await ctx.send(i)

        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)

        except asyncio.TimeoutError:
            await ctx.send("Setup timed out, please be quicker next time!")
            return
        else:
            answers.append(msg.content)

    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(
            f"You didn't mention a channel properly, please format like {ctx.channel.mention} next time."
        )
        return

    channel = bot.get_channel(c_id)

    embed = discord.Embed(
        title="Poll", description=f"{message}", colour=discord.Color.blue()
    )
    message = await channel.send(embed=embed)

    await message.add_reaction("<:upvote:809518752353878036>")
    await message.add_reaction("<:downvote:809598448684630036>")
    await message.add_reaction("<:what:807056747951947776>")
    await message.add_reaction("<:cringe:807062463383863336>")


@bot.command(aliases=["cya"])
async def sell(ctx: Context, amount=1, *, item):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        try:
            await open_account(ctx.author)

            res = await sell_this(ctx.author, item, amount)

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


@bot.command()
@commands.cooldown(1, 2700, commands.BucketType.user)
async def dig(ctx: Context):
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

    await open_account(ctx.author)
    item = random.choice(items)
    await buy_this(ctx.author, item, 1)
    # help
    # ok? what's the goal

    embed = discord.Embed(
        description=f"You dug up **1 {item}** :0", color=discord.Colour.blue()
    )
    await ctx.send(embed=embed)


@sell.error
async def sell_error(ctx: Context, error):
    await ctx.send(
        "try formatting it like this: p!buy {amount} {item}\n Example: p!sell 1 iron hoe"
    )


@dig.error
async def dig_error(ctx: Context, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 1hr)".format(
            error.retry_after
        )
        await ctx.send(msg)
    else:
        raise error


async def sell_this(user, item_name, amount, price=None):
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

    users = await get_bank_data()

    bal = await update_bank(user)

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

    await update_bank(user, abs(cost), "wallet")

    return [True, "Worked"]


@bot.command()
async def profile(ctx: Context, *, member: discord.Member = None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if member:
            userNAME = member.name
            if not member.bot:
                bot = "Not a bot"
            else:
                bot = "Is a bot"
            embed = discord.Embed(
                title=f"{userNAME}'s profile card", description="", color=0xE91E63
            )
            embed.add_field(
                name="Account name:", value=f"`{member.name}`", inline=False
            )
            embed.add_field(
                name="Creation date:", value=f"`{member.created_at}`", inline=False
            )
            embed.add_field(name="ID:", value=f"`{member.id}`", inline=False)
            embed.add_field(name="Account type:", value=f"`{bot}`", inline=False)
            embed.set_footer(text="Made by DepressedPotato")
            embed.set_thumbnail(url=member.avatar)
            await ctx.send(embed=embed)
        else:
            if not ctx.author.bot:
                bot = "Not a bot"
            else:
                bot = "Is a bot"
            embed = discord.Embed(
                title=f"{ctx.author.name}'s profile card",
                description="",
                color=0xE91E63,
            )
            embed.add_field(
                name="Account name:", value=f"`{ctx.author.name}`", inline=False
            )
            embed.add_field(
                name="Creation date:", value=f"`{ctx.author.created_at}`", inline=False
            )
            embed.add_field(name="ID:", value=f"`{ctx.author.id}`", inline=False)
            embed.add_field(name="Account type:", value=f"`{bot}`", inline=False)
            embed.set_footer(text="Made by DepressedPotato")
            embed.set_thumbnail(url=ctx.author.avatar)
            await ctx.send(embed=embed)


try:
    with open("database/channels.json") as f:
        bot.ids = set(json.load(f))
    print("Loaded channels file")
except Exception as e:
    bot.ids = set()
    print(e)


@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def passive(ctx: Context, mode=None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if mode == None:
            await ctx.send("You need to pick either `true` or `false`")
            passive.reset_cooldown(ctx)
        else:
            if mode == "true" or mode == "on" or mode == "yuh":
                if ctx.author.id in bot.ids:
                    await ctx.channel.send("You're already passive.")
                    return
                bot.ids.add(ctx.author.id)
                with open("database/channels.json", "w") as f:
                    json.dump(list(bot.ids), f)
                await ctx.channel.send("You're passive now.")
            elif mode == "false" or mode == "off" or mode == "nuh":
                if ctx.author.id in bot.ids:
                    bot.ids.remove(ctx.author.id)
                    with open("database/channels.json", "w") as f:
                        json.dump(list(bot.ids), f)
                    await ctx.channel.send("You're now impassive.")
                else:
                    await ctx.send("You're already impassive.")
            else:
                await ctx.send(
                    "You need to pick from one of these: `true/false, on/off, yuh/nuh`"
                )
                passive.reset_cooldown(ctx)


@passive.error
async def passive_error(ctx: Context, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 1min)".format(
            error.retry_after
        )
        await ctx.send(msg)
    else:
        raise error


async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break
    if name_ == None:
        return [False, 1]
    cost = price * amount
    users = await get_bank_data()
    bal = await update_bank(user)
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
    await update_bank(user, cost * -1, "wallet")
    return [True, "Worked"]


@bot.command()
async def sudo(ctx: Context, member: discord.Member, *, message=None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await ctx.message.delete()
        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()
        webhook = await ctx.channel.create_webhook(name=member.name)
        await webhook.send(str(message), username=member.name, avatar_url=member.avatar)


@bot.command(aliases=["tools", "inventory", "inv", "shack"])
async def shed(ctx: Context, *, member: discord.Member = None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if member:
            await open_account(member)
            user = member
            users = await get_bank_data()
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
            await open_account(ctx.author)
            user = ctx.author
            users = await get_bank_data()
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


def checkint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


@bot.command()
async def buy(ctx: Context, amount, *, item):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if amount < 0:
            await ctx.send("hey, are you trying to break me?")
        else:
            try:
                amount = int(amount)
                await open_account(ctx.author)
                res = await buy_this(ctx.author, item, amount)
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

@bot.command(aliases=["store", "market"])
async def shop(ctx: Context):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
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


@bot.command(aliases=["bal", "potats", "potatoes", "vault"])
async def balance(ctx: Context, *, mention: discord.Member = None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if mention:
            await open_account(mention)
            user = mention
            users = await get_bank_data()
            wallet_amt = users[str(mention.id)]["wallet"]
            bank_amt = users[str(mention.id)]["bank"]
            if wallet_amt < 0:
                await update_bank(mention, -1 * wallet_amt)
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
            await open_account(ctx.author)
            user = ctx.author
            users = await get_bank_data()
            wallet_amt = users[str(user.id)]["wallet"]
            bank_amt = users[str(user.id)]["bank"]
            if wallet_amt < 0:
                await update_bank(ctx.author, -1 * wallet_amt)
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


@bot.command(aliases=["search"])
@commands.cooldown(1, 1800, commands.BucketType.user)
async def beg(ctx: Context):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await open_account(ctx.author)
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
        users = await get_bank_data()
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
async def beg_error(ctx: Context, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 1min)".format(
            error.retry_after
        )
        await ctx.send(msg)
    else:
        raise error


@bot.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def sabotage(ctx: Context, *, member: discord.Member):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if ctx.author.id in bot.ids:
            await ctx.send(
                "You cant sabotage people, your in passive <:potato_angry:814539600235986964>"
            )
        elif member.id in bot.ids:
            await ctx.send(
                "Leave that passive potato alone <:potato_angry:814539600235986964>"
            )
        else:
            if member == ctx.author:
                await ctx.send("you cant sabotage yourself lmao")
                sabotage.reset_cooldown(ctx)
                return
            elif member == bot.user:
                await ctx.send("hecc u dont try to sabotage me")
                sabotage.reset_cooldown(ctx)
                return
            else:
                pass
            await open_account(ctx.author)
            await open_account(member)
            bal = await update_bank(member)
            bal2 = await update_bank(ctx.author)
            if bal2[0] < 100000:
                await ctx.send(
                    "u need at least **100000** :potato: to sabotage someone <:potato_angry:814539600235986964>"
                )
                sabotage.reset_cooldown(ctx)
                return
            elif bal[1] < 10000:
                await ctx.send(
                    "dang bro this dude tryna sabotage a dude with less than **10000** :potato: in their vault <:ban_hammer:806216052426014751>"
                )
                sabotage.reset_cooldown(ctx)
                return
            earnings = random.randrange(-1 * bal[1], 0)
            await update_bank(member, earnings, "bank")
            await update_bank(ctx.author, -100000)
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
                await member.send(embed=embe2)
            except Exception as e:
                print(e)


@sabotage.error
async def sabotage_error(ctx: Context, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 1hr)".format(
            error.retry_after
        )
        await ctx.send(msg)
    elif isinstance(error, commands.MemberNotFound):
        msg = f"Sorry, I couldnt find that user. Try sabotaging someone in ur server"
        await ctx.send(msg)
        sabotage.reset_cooldown(ctx)
    else:
        print(error)
        sabotage.reset_cooldown(ctx)


@bot.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def rob(ctx: Context, *, member: discord.Member):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if ctx.author.id in bot.ids:
            await ctx.send(
                "You cant rob people, your in passive <:potato_angry:814539600235986964>"
            )
            rob.reset_cooldown(ctx)
        elif member.id in bot.ids:
            await ctx.send(
                "Leave that passive potato alone <:potato_angry:814539600235986964>"
            )
            rob.reset_cooldown(ctx)
        else:
            if member == ctx.author:
                await ctx.send("you cant rob yourself lmao")
                rob.reset_cooldown(ctx)
                return
            elif member == bot.user:
                await ctx.send("hecc u dont try to rob me")
                rob.reset_cooldown(ctx)
                return
            else:
                pass
            await open_account(member)
            await open_account(ctx.author)
            users = await get_bank_data()
            user = ctx.author
            try:
                shed = users[str(user.id)]["shed"]
            except:
                shed = []
            test = []
            for i in shed:
                name = i["item"]
                test.append(name)
            bal = await update_bank(member)
            bal2 = await update_bank(ctx.author)
            if bal2[0] < 10000:
                await ctx.send(
                    "u need at least **10000** :potato: to rob someone <:potato_angry:814539600235986964>"
                )
                rob.reset_cooldown(ctx)
                return
            elif bal[0] < 1000:
                await ctx.send(
                    "dang bro this dude tryna rob a dude with less than 1000 :potato: <:ban_hammer:806216052426014751>"
                )
                rob.reset_cooldown(ctx)
                return
            earnings = random.randrange(-1 * bal2[0], bal[0])
            # test 1: check if custom rob items work --> hopefully we can make rob prevention items soon, that would be nice
            if "Potato Cannon" in test:
                earnings = bal[0]
            await update_bank(ctx.author, earnings)
            await update_bank(member, -1 * earnings)
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
async def rob_error(ctx: Context, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 5m)".format(
            error.retry_after
        )
        await ctx.send(msg)
    elif isinstance(error, commands.MemberNotFound):
        msg = f"Sorry, I couldnt find that user. Try robbing someone in ur server"
        await ctx.send(msg)
        rob.reset_cooldown(ctx)
    else:
        print(error)
        rob.reset_cooldown(ctx)


@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def farm(ctx: Context):
    ctx.send("start farm command")
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await open_account(ctx.author)
        users = await get_bank_data()
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
async def farm_error(ctx: Context, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 1s)".format(
            error.retry_after
        )
        await ctx.send(msg)
    else:
        raise error


@bot.command()
@commands.is_owner()
async def serverlist(ctx: Context):
    a = 0
    e = []
    for i in bot.guilds:
        a += 1
        e.append(i.name)
    await ctx.send(e)
    await ctx.send(a)


@bot.command(aliases=["add"])
@commands.is_owner()
async def addpotatoes(ctx: Context, member: discord.Member, amount):
    await open_account(member)
    users = await get_bank_data()
    user = member
    users[str(user.id)]["wallet"] += int(amount)
    with open("database/potato.json", "w") as f:
        json.dump(users, f)
    await ctx.send(f"Added **{amount}** :potato: to {member.mention}")


@addpotatoes.error
async def addpotatoes_error(ctx: Context, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("You cant do that!")


@bot.command(aliases=["dep"])
async def deposit(ctx: Context, amount=None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await open_account(ctx.author)
        if amount == None:
            await ctx.send(
                "You have to enter an amount to deposit <:seriously:809518766470987799>"
            )
            return
        bal = await update_bank(ctx.author)
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
        await update_bank(ctx.author, -1 * amount)
        await update_bank(ctx.author, amount, "bank")
        await ctx.send(f"You deposited **{amount}** :potato: :0")


@bot.command(aliases=["gift", "gib", "send", "transfer"])
async def give(ctx: Context, member: discord.Member, amount=None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if ctx.author.id in bot.ids:
            await ctx.send(
                "You cant give people potatoes, your in passive <:potato_angry:814539600235986964>"
            )
        elif member.id in bot.ids:
            await ctx.send(
                "Leave that passive potato alone <:potato_angry:814539600235986964>"
            )
        else:
            await open_account(ctx.author)
            await open_account(member)
            if amount == None:
                await ctx.send(
                    "You have to enter an amount to deposit <:seriously:809518766470987799>"
                )
                return
            bal = await update_bank(ctx.author)
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
            await update_bank(ctx.author, -1 * amount, "wallet")
            await update_bank(member, amount, "wallet")
            await ctx.send(f"You gave **{amount}** :potato: to {member.mention}!")


@bot.command(aliases=["gamble"])
async def coinflip(ctx: Context, amount=None):
    # Exceptions
    if amount == None:
        await ctx.send(
            "You have to enter an amount to play <:seriously:809518766470987799>"
        )
        return

    await open_account(ctx.author)
    bal = await update_bank(ctx.author)
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
        await update_bank(ctx.author, +1 * gamble_amount)
        embed = discord.Embed(
            title=f"You won **{gamble_amount}** :potato: \:D", color=0x3498DB
        )
        embed.set_footer(text="thats pretty pog ngl")
        await ctx.send(embed=embed)
    else:
        await update_bank(ctx.author, -1 * gamble_amount)
        embed = discord.Embed(
            title=f"You lost **{gamble_amount}** :potato: ;-;", color=0xe74c3c
        )
        embed.set_footer(text="lol imagine losing in a coin flip")
        await ctx.send(embed=embed)


@bot.command(aliases=["with"])
async def withdraw(ctx: Context, amount=None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await open_account(ctx.author)
        if amount == None:
            await ctx.send(
                "You have to enter an amount to withdraw <:seriously:809518766470987799>"
            )
            return
        bal = await update_bank(ctx.author)
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
        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1 * amount, "bank")
        await ctx.send(f"You withdrew **{amount}** :potato:  :0")


async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
    with open("database/potato.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data() -> dict:
    with open("database/potato.json", "r") as f:
        users = json.load(f)
    return users


async def update_bank(user, change=0, mode="wallet") -> list[int]:
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("database/potato.json", "w") as f:
        json.dump(users, f)
    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal


@bot.command(aliases=["lb", "rich"])
async def leaderboard(ctx: Context):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        x = 10
        users = await get_bank_data()
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
            member = bot.get_user(id_)
            name = member
            em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
            if index == x:
                break
            else:
                index += 1
        await ctx.send(embed=em)


@bot.command(aliases=["lbreverse", "richreverse"])
async def leaderboardreverse(ctx: Context):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        x = 10
        users = await get_bank_data()
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
            member = bot.get_user(id_)
            name = member
            em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
            if index == x:
                break
            else:
                index += 1
        await ctx.send(embed=em)


@bot.command()
async def botpic(ctx: Context):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await ctx.send(bot.user.avatar)


@bot.command()
async def avatar(ctx: Context, *, member: discord.Member = None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if member:
            await ctx.send(str(member.avatar))
        else:
            await ctx.send(str(ctx.author.avatar))


@bot.command()
async def customembed(ctx: Context, color: discord.Colour, title, *, description):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        embed = discord.Embed(
            title=f"""{title}""", description=f"""{description}""", color=color
        )
        await ctx.channel.send(embed=embed)


@bot.command(pass_context=True)
@commands.cooldown(1, 2, commands.BucketType.user)
async def meme(ctx: Context):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        embed = discord.Embed(
            title="Fresh meme from reddit", description="", color=0xF1C40F
        )
        async with aiohttp.ClientSession() as cs:
            async with cs.get(random.choice(redditlist)) as r:
                res = await r.json()
                embed.set_image(
                    url=res["data"]["children"][random.randint(0, 25)]["data"]["url"]
                )
                embed.set_footer(text="Meme from r/memes")
                message = await ctx.send(embed=embed)


@meme.error
async def meme_error(ctx: Context, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 2s)".format(
            error.retry_after
        )
        await ctx.send(msg)
    else:
        raise error


@bot.event
async def on_guild_join(guild):
    with open("database/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "p!"
    with open("database/prefixes.json", "w") as f:
        json.dump(prefixes, f)
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(
                "<a:tysm:805858522578812930> Thanks for inviting me to your server! Say `p!help` for help! <:shibalove:805858519958028349>"
            )
        break


# startup and status
@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready :D")

    # Add bot commands (in pcommands)
    await bot.add_cog(HelpCommands())
    await bot.add_cog(StaffCommands(bot))
    await bot.add_cog(DeveloperCommands(bot, launch_time))
    await bot.add_cog(EconomyCommands())
    #

    servers = len(bot.guilds)
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{members} users | {servers} servers | p!help",
        ),
    )


@bot.command()
@commands.has_permissions(administrator=True)
async def addrole(ctx: Context, member: discord.Member, role: discord.Role):
    await ctx.send("Role added")
    await member.add_roles(role)
    await ctx.send("as been unjailed :white_check_mark:")


@addrole.error
async def addrole_error(ctx: Context, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that! (u need perms)")


@bot.command()
async def guild(ctx: Context):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        name = ctx.guild.name
        description = ctx.guild.description

        owner = ctx.author.guild.owner.mention
        id = ctx.guild.id
        memberCount = ctx.guild.member_count

        icon = "https://minecraft.fandom.com/wiki/File:Missing_Texture_(anisotropic_filtering)_JE3.png"
        try:
            icon = ctx.guild.icon.url
        except AttributeError:
            pass

        link = await ctx.channel.create_invite()

        embed = discord.Embed(
            title=name + " Server Information", description=description, color=0x206694
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Invite", value=link, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)
        embed.set_footer(text="Made by DepressedPotato")
        await ctx.channel.send(embed=embed)


@bot.command()
async def fact(ctx: Context):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        with open("assets/random_facts", "r") as f:
            read = f.read()
            array = read.split("\n")
            fact = random.choice(array)
            embed = discord.Embed(description=fact, color=0xE67E22)
            await ctx.send(embed=embed)


@bot.command()
async def invite(ctx: Context):
    embed = discord.Embed(
        title="Click here invite",
        url="https://discord.com/api/oauth2/authorize?client_id=839966871143186472&permissions=1007021303&scope=bot",
        color=0xF1C40F,
    )
    embed.add_field(
        name="Raw url link:",
        value="`https://discord.com/api/oauth2/authorize?client_id=839966871143186472&permissions=1007021303&scope=bot`",
        inline=False,
    )
    embed.set_footer(text="Made by DepressedPotato")
    await ctx.send(embed=embed)


@bot.command()
async def vote(ctx: Context):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        embed = discord.Embed(
            title="Click here vote",
            url="https://top.gg/bot/839966871143186472/vote",
            color=0xF1C40F,
        )
        embed.set_footer(text="pls?")
        await ctx.send(embed=embed)


@bot.command()
async def about(ctx: Context):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        embed = discord.Embed(title="`About:`", color=0x3498DB)
        embed.add_field(
            name="Bot version", value="Version 1.54.0 | discord.py", inline=False
        )
        embed.add_field(
            name="Bot creators",
            value="<@698218089010954481> <@701554023337033808> <@691009964570968144>",
            inline=False,
        )
        embed.add_field(
            name="Support server", value="https://discord.gg/vX2JgPQC7W", inline=False
        )
        embed.add_field(
            name="Top.gg voting page",
            value="https://top.gg/bot/839966871143186472/vote",
            inline=False,
        )
        embed.add_field(
            name="YouTube channel",
            value="https://www.youtube.com/channel/UCqiV-VjdA7Iydx3Y8Y1z0TQ",
        )
        embed.set_footer(text="Made by DepressedPotato")
        await ctx.send(embed=embed)


keep_alive()
bot.run(os.getenv("password"))
