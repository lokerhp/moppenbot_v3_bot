import discord
import config
import requests
import asyncio

client = discord.Client()


async def change_status():
    await client.wait_until_ready()
    while client.is_ready():
        await client.change_presence(activity=discord.Game(name=f"!mop | {len(client.guilds)} guilds", type=1))
        await asyncio.sleep(20)


@client.event
async def on_ready():
    print('MoppenBot op account: {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('!mop'):
        args = message.content.split(" ")
        params = {"likes": "true"}
        if len(args) > 1:
            if args[1] == "nsfw":
                params["nsfw"] = "true"
                r = requests.get("https://moppenbot.nl/api/random/", params=params)
            else:
                params["q"] = args
                r = requests.get("https://moppenbot.nl/api/search/", params=params)
        else:
            r = requests.get("https://moppenbot.nl/api/random/", params=params)
        if r.status_code == 200:
            data = r.json()
            if data["success"]:
                embed = discord.Embed(title="Mop " + str(data["joke"]["id"]), description=data["joke"]["joke"], color=0xffff00)
                embed.set_footer(text="Van " + str(data["joke"]["author"]) + " | " + str(data["joke"]["likes"]) + " 👍")
                msg = await message.channel.send(embed=embed)
                await msg.add_reaction("👍")
                return
        embed = discord.Embed(title="Error", description="Er is een error opgetreden. Meld dit.")
        await message.channel.send(embed=embed)
    
    if message.content.lower().startswith('!help'):
        args = message.content.split(" ")
        if len(args) > 1:
            if args[1] == "api":
                embed=discord.Embed(title="Moppenbot Api Informatie", description="Help Commando van de Moppenbot")
                embed.add_field(name="Main endpoint: /api/random/", value="Krijg een random mop", inline=False)
                embed.add_field(name="Mogelijke Param: nsfw=true", value="Krijg een mop die NSFW kan zijn", inline=True)
                embed.add_field(name="Mogelijke Param: likes=true ", value="Krijg ook hoeveel likes de bot heeft", inline=True)
                embed.add_field(name="Zoek endpoint: /api/search/", value="Zoek een mop met param q=<zoekwoord>", inline=True)
                embed.set_footer(text="Door: Jens de Router 💻 Jederu #5961")
                await message.channel.send(embed=embed)
        else:
            embed=discord.Embed(title="Moppenbot Help", description="Help Commando van de Moppenbot")
            embed.add_field(name="!mop", value="Krijg een random mop", inline=False)
            embed.add_field(name="!mop nsfw", value="Krijg een mop die NSFW kan zijn", inline=True)
            embed.add_field(name="!mop <zoekwoord>", value="Zoek een mop op zoekwoord", inline=True)
            embed.set_footer(text="Door: Jens de Router 💻 Jederu #5961")
            await message.channel.send(embed=embed)

    
    


@client.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        if reaction.emoji == "👍":
            params = {
                "api_key": config.API_KEY,
                "user": user.id,
                "joke": int(reaction.message.embeds[0].title.replace("Mop ", "")),
            }
            requests.get("https://moppenbot.nl/api/like/", params=params)

client.loop.create_task(change_status())
#client.run(config.TOKEN)
