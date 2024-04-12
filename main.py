import discord, os, json, random, aiohttp
from discord.ext.commands import cooldown, BucketType, Context
from discord.ext import commands
from discord import Guild, Client
from discord.ext import *
from datetime import *
from datetime import datetime, timezone
import datetime as dt  # why the hell is there a breakpoint here
import discord.ext
import discord.ext.tasks
from keep_alive import keep_alive
import io
from pcommands.e_commands import EconomyCommands
from utils.blacklist import BlacklistCommands as botbans
import asyncio
from pcommands.help_commands import HelpCommands
from pcommands.dev_commands import StaffCommands, DeveloperCommands
from typing import Union

# feel free to change the name of the import whenever you want
# :0 ty


def get_prefix(client, message):
    with open("database/prefixes.json", "r") as f:
        prefixes = json.load(f)
    try:
        return prefixes[str(message.guild.id)]
    except:
        return "p!"


usersData = dict[str, dict[str, dict[str, Union[dict, int, str]]]]({})

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


# startup and status
@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready :D")
    if not await databaseFilesExists():
        await createDatabase()

    await fetch_all_user_data()

    # Add bot commands (in pcommands)
    await bot.add_cog(HelpCommands())
    await bot.add_cog(StaffCommands(bot))
    await bot.add_cog(DeveloperCommands(bot, launch_time))
    await bot.add_cog(EconomyCommands(bot, usersData))
    #

    if not backupData.is_running():
        backupData.start()

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


@discord.ext.tasks.loop(minutes=10)
async def backupData():
    with open("database/userdata.json", "w") as f:
        json.dump(usersData, f)


async def fetch_all_user_data():
        global usersData
        with open("database/userdata.json", "r") as f:
            usersData = json.load(f)


@bot.command(aliases=["back"])  # REMOVE THIS ON LAUNCH
async def backup(ctx: Context):
    with open("database/userdata.json", "w") as f:
        json.dump(usersData, f)


@bot.command()  # REMOVE THIS ON LAUNCH
async def fetch(ctx: Context):
    global usersData
    with open("database/userdata.json", "r") as f:
        usersData = json.load(f)


async def createDatabase():
    if not os.path.exists("database"):
        os.mkdir("database")

    if not os.path.isfile("database/userdata.json"):
        with open("database/userdata.json", "w") as file:
            file.write("{}")
    if not os.path.isfile("database/prefixes.json"):
        with open("database/prefixes.json", "w") as file:
            file.write("{}")
    if not os.path.isfile("database/channels.json"):
        with open("database/channels.json", "w") as file:
            file.write("[]")

    print("Created Database")


async def databaseFilesExists() -> bool:
    return (
        os.path.exists("database")
        and os.path.isfile("database/userdata.json")
        and os.path.isfile("database/prefixes.json")
        and os.path.isfile("database/channels.json")
    )


@bot.command(aliases=["rd", "raw"])
async def rawdata(ctx: Context):
    await ctx.send(f"```{usersData}```")


"""
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
]"""

launch_time = datetime.now(timezone.utc)


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


"""async def buy_this(user, item_name, amount):
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
    users = await get_user_data()
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
"""

# mogus


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


def checkint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


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


"""async def get_user_data() -> dict:
    with open("database/potato.json", "r") as f:
        users = json.load(f)
    return users


async def update_bank(user, change=0, mode="wallet") -> list[int]:
    users = await get_user_data()
    users[str(user.id)][mode] += change
    with open("database/potato.json", "w") as f:
        json.dump(users, f)
    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal"""


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
