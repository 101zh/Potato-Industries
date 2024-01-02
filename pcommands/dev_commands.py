import discord, json
from discord import Member
import os
from discord.ext import commands
from discord.ext.commands import Context
from datetime import datetime

"""
Untested
"""


class StaffCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self = self
        self.bot = bot
        self.roles = []
        self.jailrole = []

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nick(self, ctx: Context, member: discord.Member, *, name):
        await member.edit(nick=name)
        await ctx.send(
            f"Nickname for {member.mention} successfully changed to `{name}` :white_check_mark:"
        )

    @nick.error
    async def nick_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that (u need perms)")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nickall(self, ctx: Context, *, name):
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
                f"Nickname for {Member.mention} successfully changed to `{name}` :white_check_mark:"
            )
        else:
            await ctx.send(
                f"Nickname for {count} couldn't be changed. Check perms. Successfully changed {ctx.guild.member_count - count} to `{name}` :white_check_mark:"
            )

    @nickall.error
    async def nickall_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that (u need perms)")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unjail(self, ctx: Context, member: discord.Member):
        if member:
            if member == ctx.author:
                await ctx.send("You can't unjail yourself!")
            else:
                for i in self.jailrole:
                    try:
                        await member.remove_roles(i)
                    except Exception:
                        pass
                for i in self.roles:
                    try:
                        await member.add_roles(i)
                    except Exception:
                        pass
                for i in self.jailrole:
                    try:
                        self.jailrole.remove(i)
                    except Exception:
                        pass
                for i in self.roles:
                    try:
                        self.roles.remove(i)
                    except Exception:
                        pass
                await ctx.send(f"{member.mention} has been unjailed ✅")
        else:
            await ctx.send("You need to provide a member!")

    @unjail.error
    async def unjail_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that! (u need perms)")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def jail(
        self, ctx: Context, member: discord.Member, *, role: discord.Role = None
    ):
        if member:
            if role:
                if member == ctx.author:
                    await ctx.send("You can't jail yourself!")
                elif member.id == ctx.guild.owner_id:
                    await ctx.send("You can't jail the owner!")
                elif member.id == "698218089010954481":
                    return
                else:
                    self.jailrole.append(role)
                    for i in member.roles:
                        try:
                            await member.remove_roles(i)
                            self.roles.append(i)
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
                    self.jailrole.append(role)
                    for i in member.roles:
                        try:
                            await member.remove_roles(i)
                            self.roles.append(i)
                        except Exception:
                            pass
                    await ctx.send(f"{member.mention} has been jailed ✅")
        else:
            await ctx.send("Something went wrong.")

    @jail.error
    async def jail_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that (u need perms)")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: Context, *, prefix):
        with open("database/prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open("database/prefixes.json", "w") as f:
            json.dump(prefixes, f)
        await ctx.send(f"Prefix successfully changed to `{prefix}`")
        await self.bot.get_guild(ctx.guild.id).me.edit(
            nick=f"[ {prefix} ] Potato Industries"
        )

    @prefix.error
    async def prefix_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that! (u need perms)")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def slowmode(self, ctx: Context, seconds):
        seconds = int(seconds)
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

    @slowmode.error
    async def slowmode_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that! (u need perms)")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def role(self, ctx: Context, member: discord.Member, *, role: discord.Role):
        await member.add_roles(role)

    @role.error
    async def role_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that! (u need perms)")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def reactrole(self, ctx: Context, emoji, role: discord.Role, *, message):
        emb = discord.Embed(description=message, color=0x2ECC71)
        msg = await ctx.channel.send(embed=emb)
        await msg.add_reaction(emoji)
        with open("database/reactrole.json") as json_file:
            data = json.load(json_file)
            new_react_role = {
                "role_name": role.name,
                "role_id": role.id,
                "emoji": emoji,
                "message_id": msg.id,
            }
            data.append(new_react_role)
        with open("database/reactrole.json", "w") as f:
            json.dump(data, f, indent=4)
        await ctx.send(
            f"Successfully created a reaction role for `@{role}` :white_check_mark:"
        )

    @reactrole.error
    async def reactrole_error(self, ctx: Context, error):
        await ctx.send(error)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            pass
        else:
            with open("database/reactrole.json") as react_file:
                data = json.load(react_file)
                for x in data:
                    if x["emoji"] == payload.emoji.name:
                        role = discord.utils.get(
                            self.bot.get_guild(payload.guild_id).roles,
                            id=x["role_id"],
                        )
                        await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        with open("database/reactrole.json") as react_file:
            data = json.load(react_file)
            for x in data:
                if x["emoji"] == payload.emoji.name:
                    role = discord.utils.get(
                        self.bot.get_guild(payload.guild_id).roles, id=x["role_id"]
                    )
                    await self.bot.get_guild(payload.guild_id).get_member(
                        payload.user_id
                    ).remove_roles(role)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: Context, member: discord.Member, *, reason=None):
        if reason:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} got banned ;-;")
        else:
            reason = "No reason provided"
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} got banned ;-;")

    @ban.error
    async def ban_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that! (u need perms)")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: Context, member: discord.Member):
        await member.kick()
        await ctx.channel.send(f"{member.mention} got kicked ;-;")

    @kick.error
    async def kick_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that! (u need perms)")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def clean(self, ctx: Context, limit: int):
        await ctx.channel.purge(limit=limit + 1)
        channel = self.bot.get_channel(839682721374666783)
        await channel.send(
            f"{ctx.author.name} used the `clean` command in {ctx.channel.name} and deleted **{limit}** messages"
        )

    @clean.error
    async def clean_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that! (u need perms)")


class DeveloperCommands(commands.Cog):
    def __init__(self, bot: commands.Bot, launch_time: datetime):
        self = self
        self.bot = bot
        self.launch_time = launch_time

    # Helper method
    async def aexec(self, code):
        # Make an async function with the code and `exec` it
        exec(f"async def __ex(): " + "".join(f"\n {l}" for l in code.split("\n")))

        # Get `__ex` from local variables, call it and return the result
        # ohhhh
        return await locals()["__ex"]()

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx: Context, *, command):
        try:
            await self.aexec(command)
        except Exception as e:
            await ctx.send(f"Error: `{e}`")

    @eval.error
    async def eval_error(self, error, ctx):
        print(f"Error: `{error}`")

    @commands.command()
    async def uptime(self, ctx: Context):
        delta_uptime = datetime.utcnow() - self.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(
            f"`{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds`"
        )

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx: Context) -> None:
        quit()

    @commands.command()
    async def ping(self, ctx: Context):
        await ctx.send(f":ping_pong: Pong! `{round (self.bot.latency * 1000)} ms`")

    """
    Archived Commands
    """

    @commands.command()
    async def nuke(self, ctx: Context, code):
        await ctx.send(f"This Command is archived")
        return
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

    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx: Context, id, duration):
        await ctx.send(f"This Command is archived")
        return
        try:
            botbans.add_blacklist(id, duration)
            returned = botbans.humanize_time(duration)
            user = await self.bot.fetch_user(id)
            print(f"{user.name} was blacklisted for {returned}")
            await ctx.send(f"{user.name} was blacklisted for {returned}")
        except Exception as e:
            print(e)
            await ctx.send(f"Error: `{e}`")

    @commands.command()
    @commands.is_owner()
    async def unblacklist(self, ctx: Context, id):
        await ctx.send(f"This Command is archived")
        return
        try:
            botbans.remove_blacklist(id)
            user = await self.bot.fetch_user(id)
            print(user.name + " was unblacklisted.")
            await ctx.send(user.name + " was unblacklisted.")
        except Exception as e:
            print(e)
            await ctx.send(f"Error: `{e}`")
