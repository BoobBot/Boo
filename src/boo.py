import json

import discord
import random
import asyncio
import click
import sys
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")


def get_troll():
    with open('sayings.json') as f:
        return random.choice(json.load(f)["trickortroll"])


async def haunted(bot, guild_id, role_id, interval=300):
    while bot.loop.is_running():
        home = bot.get_guild(int(guild_id))
        if not home:
            continue
        channels = [c for c in home.channels if isinstance(c, discord.TextChannel)]
        role = discord.utils.get(home.roles, id=int(role_id))
        if role:
            target = role.members
            print(f"role found using {role.name}")
        else:
            target = [m for m in home.members if not m.bot]
            target.extend([r for r in home.roles if r.mentionable and r != home.default_role])
            print(f"no role found using {len(target)} members/roles")

        try:
            random.shuffle(channels)
            random.shuffle(target)
            channel = random.SystemRandom().choice(channels)
            ping = random.SystemRandom().choice(target)
            troll = get_troll()
            await channel.send(f"{ping.mention}, {troll}", delete_after=5)
            print("({}) {}, {}".format(str(channel), str(ping), troll))

        except discord.HTTPException:
            continue
        await asyncio.sleep(interval)


class HauntedGuild(discord.Client):
    def __init__(self, guild_id, role_id, interval=300, **options):
        super().__init__(**options)
        self.guild_id = guild_id
        self.role_id = role_id
        self.interval = interval

    async def on_ready(self):
        print('Logged in as {}({}) on {} servers'.format(self.user.name, self.user.id, len(self.guilds)))
        if not self.get_guild(int(self.guild_id)):
            print("error no guild with id of {} found did you add the bot?".format(self.guild_id))
            exit(-1)
        await haunted(self, self.guild_id, self.role_id, interval=self.interval)


@click.command()
@click.option('--token', prompt="Bot Token?", help="Discord bot token")
@click.option('--guild_id', prompt="Guild id", help="id of your discord server")
@click.option('--role_id', prompt="Role id", help="id of the role")
@click.option('--interval', default=300, prompt="Spook interval",
              help="Duration between spooky sayings")
def start(token, guild_id, role_id, interval=300):
    bot = HauntedGuild(guild_id, role_id, interval=interval, intents=discord.Intents().all())
    bot.run(token)


if __name__ == '__main__':
    start()
