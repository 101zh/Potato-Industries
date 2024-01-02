import discord, json, random
from discord.ext import commands
from discord.ext.commands import Context


class EconomyCommands(commands.Cog):
    def __init__(self):
        self = self

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
        if(amount_used<0):
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
            
            
