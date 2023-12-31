import discord
from discord import client
import os
from discord.ext import commands
from discord.ext.commands import Context


class HelpCommands(commands.Cog):
    def __init__(self):
        self = self

    @commands.command()
    async def help(self, ctx: Context):
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

    @commands.command()
    async def shelp(self, ctx: Context):
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

    @commands.command()
    async def ehelp(self, ctx: Context):
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

    @commands.command()
    async def fhelp(self, ctx: Context):
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
            name=f"{prefix}bonk [user]",
            value="`[user]'s horny license`",
            inline=False,
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

    @commands.command()
    async def rhelp(self, ctx: Context):
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
