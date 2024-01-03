import discord, json, random
from discord.ext import commands
from discord.ext.commands import Context


class EconomyCommands(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self = self
        self.bot = bot

    @commands.command()
    async def use(self, ctx: Context, amount: int, *, item: str = None):
        if not item:
            await ctx.send(
                "try formatting it like this: `p!use {amount} {item}` \nExample: `p!use 1 lottery potato`"
            )
            return
        item = item.lower()

        # Uses the item; returns a negative # if the isn't found/more is used than one has
        error = await self.update_user_shed(ctx.author, item, amount)
        if error == -1:
            await ctx.send("You don't have that item")
            return
        elif error == -2:
            await ctx.send("You can't use more than you have")
            return
        elif error == -3:
            await ctx.send("What are you trying to do here?")
            return

        if item == "lottery potato":
            await self.use_lottery_potato(ctx=ctx, amount=amount)
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
        # Exception amount_used can't be negative
        if amount_used < 0:
            return -3

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
            if updated_amount < 0:
                # returns -2 if the amount used is more than acceptable
                return -2
            elif updated_amount == 0:
                del usershed[index]
            else:
                usershed[index]["amount"] -= amount_used

            users[str(user.id)]["shed"] = usershed

            with open("database/potato.json", "w") as f:
                json.dump(users, f)

            return index
        else:
            return -1

        # -3 is for when amount is a negative value
        # -2 is for negative amount value
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
