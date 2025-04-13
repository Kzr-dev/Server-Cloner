from os import system
import os
import psutil
import time
import sys
import discord
import asyncio
import colorama
from colorama import Fore, init
import platform
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("token")  # Create a file named `.env` in the same directory as the script and put your token in the following format: token=yourtoken

if token is None:
    print("Error, token not found in the .env")
    sys.exit(1)

class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
            for role in guild_to.roles:
                try:
                    if role.name != "@everyone":
                        await role.delete()
                        print(f"Role {role.name} deleted")
                except discord.Forbidden:
                    print(f"Error deleting role {role.name}")
                except discord.HTTPException:
                    print(f"Unable to delete role {role.name}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = []
        role: discord.Role
        for role in guild_from.roles:
            if role.name != "@everyone":
                roles.append(role)
        roles = roles[::-1]
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                print(f"Role {role.name} created")
            except discord.Forbidden:
                print(f"Error creating role {role.name}")
            except discord.HTTPException:
                print(f"Unable to create role {role.name}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print(f"Channel {channel.name} deleted")
            except discord.Forbidden:
                print(f"Error deleting channel {channel.name}")
            except discord.HTTPException:
                print(f"Unable to delete channel {channel.name}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        channels = guild_from.categories
        channel: discord.CategoryChannel
        new_channel: discord.CategoryChannel
        for channel in channels:
            try:
                overwrites_to = {}
                for key, value in channel.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                new_channel = await guild_to.create_category(
                    name=channel.name,
                    overwrites=overwrites_to)
                await new_channel.edit(position=channel.position)
                print(f"Category {channel.name} created")
            except discord.Forbidden:
                print(f"Error deleting category {channel.name}")
            except discord.HTTPException:
                print(f"Unable to delete category {channel.name}")

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        channel_text: discord.TextChannel
        channel_voice: discord.VoiceChannel
        category = None
        for channel_text in guild_from.text_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_text.category.name:
                            break
                    except AttributeError:
                        print(f"Text channel {channel_text.name} has no category")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_text.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position,
                        topic=channel_text.topic,
                        slowmode_delay=channel_text.slowmode_delay,
                        nsfw=channel_text.nsfw)
                except:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print(f"Text channel {channel_text.name} created")
            except discord.Forbidden:
                print(f"Error creating text channel {channel_text.name}")
            except discord.HTTPException:
                print(f"Unable to create text channel {channel_text.name}")
            except:
                print(f"Unable to create text channel {channel_text.name}")

        category = None
        for channel_voice in guild_from.voice_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_voice.category.name:
                            break
                    except AttributeError:
                        print(f"Voice channel {channel_voice.name} has no category")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_voice.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position,
                        bitrate=channel_voice.bitrate,
                        user_limit=channel_voice.user_limit,
                        )
                except:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print(f"Voice channel {channel_voice.name} created")
            except discord.Forbidden:
                print(f"Error deleting {channel_voice.name}")
            except discord.HTTPException:
                print(f"Unable to create voice channel {channel_voice.name}")
            except:
                print(f"Unable to create voice channel {channel_voice.name}")

    @staticmethod
    async def emojis_delete(guild_to: discord.Guild):
        for emoji in guild_to.emojis:
            try:
                await emoji.delete()
                print(f"Emoji {emoji.name} deleted")
            except discord.Forbidden:
                print(f"Error deleting emoji {emoji.name}")
            except discord.HTTPException:
                print(f"Unable to delete emoji {emoji.name}")

    @staticmethod
    async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
        emoji: discord.Emoji
        for emoji in guild_from.emojis:
            try:
                emoji_image = await emoji.url.read()
                await guild_to.create_custom_emoji(
                    name=emoji.name,
                    image=emoji_image)
                print(f"Emoji {emoji.name} created")
            except discord.Forbidden:
                print(f"Error creating emoji {emoji.name}")
            except discord.HTTPException:
                print(f"Unable to create emoji {emoji.name}")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            try:
                icon_image = await guild_from.icon_url.read()
            except discord.errors.DiscordException:
                print(f"Unable to read the icon of {guild_from.name}")
                icon_image = None
            await guild_to.edit(name=f'{guild_from.name}')
            if icon_image is not None:
                try:
                    await guild_to.edit(icon=icon_image)
                    print(f"The icon of {guild_to.name} has been changed")
                except:
                    print(f"Error changing the icon of {guild_to.name}")
        except discord.Forbidden:
            print(f"Unable to change the icon of {guild_to.name}")


client = discord.Client()
os = platform.system()
if os == "Windows":
    system("cls")
else:
    system("clear")
    print(chr(27) + "[2J")
print(f"""{Fore.RED}

                                  ░██████╗███████╗██████╗░██╗░░░██╗███████╗██████╗░ ░█████╗░██╗░░░░░░█████╗░███╗░░██╗███████╗██████╗░
                                  ██╔════╝██╔════╝██╔══██╗██║░░░██║██╔════╝██╔══██╗ ██╔══██╗██║░░░░░██╔══██╗████╗░██║██╔════╝██╔══██╗
                                  ╚█████╗░█████╗░░██████╔╝╚██╗░██╔╝█████╗░░██████╔╝ ██║░░╚═╝██║░░░░░██║░░██║██╔██╗██║█████╗░░██████╔╝ by Kzr-Dev
                                  ░╚═══██╗██╔══╝░░██╔══██╗░╚████╔╝░██╔══╝░░██╔══██╗ ██║░░██╗██║░░░░░██║░░██║██║╚████║██╔══╝░░██╔══██╗
                                  ██████╔╝███████╗██║░░██║░░╚██╔╝░░███████╗██║░░██║ ╚█████╔╝███████╗╚█████╔╝██║░╚███║███████╗██║░░██║
                                  ╚═════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝ ░╚════╝░╚══════╝░╚════╝░╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝
{Fore.RESET}""")
guild_s = input(f'[{Fore.RED}?{Fore.RESET}] Enter the server you want to clone:\n>')
guild = input(f'[{Fore.RED}?{Fore.RESET}] Enter the server where you want to clone:\n >')
input_guild_id = guild_s  
output_guild_id = guild  

print("\n")

#by Kzr-Dev, what more could you ask for?
@client.event
async def on_ready():
    try:
        print(f"Connected as: {client.user}")
        print("Cloning...")
        guild_from = client.get_guild(int(input_guild_id))
        guild_to = client.get_guild(int(output_guild_id))
        await Clone.guild_edit(guild_to, guild_from)
        await Clone.roles_delete(guild_to)
        await Clone.channels_delete(guild_to)
        await Clone.roles_create(guild_to, guild_from)
        await Clone.categories_create(guild_to, guild_from)
        await Clone.channels_create(guild_to, guild_from)
        print(f"""{Fore.GREEN}


                                                ░█████╗░██╗░░░░░░█████╗░███╗░░██╗███████╗██████╗░
                                                ██╔══██╗██║░░░░░██╔══██╗████╗░██║██╔════╝██╔══██╗
                                                ██║░░╚═╝██║░░░░░██║░░██║██╔██╗██║█████╗░░██║░░██║
                                                ██║░░██╗██║░░░░░██║░░██║██║╚████║██╔══╝░░██║░░██║
                                                ╚█████╔╝███████╗╚█████╔╝██║░╚███║███████╗██████╔╝
                                                ░╚════╝░╚══════╝░╚════╝░╚═╝░░╚══╝╚══════╝╚═════╝░

        {Fore.RESET}""")
        await asyncio.sleep(5)
        await client.close()
    except KeyboardInterrupt:
        os._exit(1)    

client.run(token, bot=False)
