import discord
from discord import client
import os
from discord.ext import commands
from discord.ext.commands import Context

class Help(commands.Cog):
    def __init__(self, blacklisted: list[int]):
        self.blacklisted = blacklisted

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"Welcome {member.mention}.")

    @commands.command()
    async def help(self, ctx: Context):
        if ctx.author.id in self.blacklisted:
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
