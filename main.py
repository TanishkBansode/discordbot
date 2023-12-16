from interactions import slash_command, SlashContext

@slash_command(name="my_command", description="My first command :)")
async def my_command_function(ctx: SlashContext):
    await ctx.send("Hello World")

@slash_command(name="my_long_command", description="My second command :)")
async def my_long_command_function(ctx: SlashContext):
    # need to defer it, otherwise, it fails
    await ctx.defer()

    # do stuff for a bit
    await asyncio.sleep(600)

    await ctx.send("Hello World")