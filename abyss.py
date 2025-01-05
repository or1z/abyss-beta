import os
import sys
import discord
from discord.ext import commands
from cryptography.fernet import Fernet
import time
import json
import asyncio

os.system(f'title Abyss [BETA] - Home') 

APPDATA_PATH = os.path.join(os.getenv('LOCALAPPDATA'), 'abyss-beta')
KEY_FILE = os.path.join(APPDATA_PATH, 'key.key')
DATA_FILE = os.path.join(APPDATA_PATH, 'data.abyss')

if not os.path.exists(APPDATA_PATH):
    os.makedirs(APPDATA_PATH)

if not os.path.exists(KEY_FILE):
    key = generate_key()
    save_key(key)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "wb") as file:
        empty_data = encrypt_data(json.dumps({}), load_key())
        file.write(empty_data)

def generate_key():
    return Fernet.generate_key()

def load_key():
    return open(KEY_FILE, "rb").read()

def save_key(key):
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def encrypt_data(data, key):
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return encrypted

def decrypt_data(data, key):
    f = Fernet(key)
    decrypted = f.decrypt(data).decode()
    return decrypted

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_token_and_prefix():
    profiles = {}
    ascii_art = """
        _                   
       | |                  
   __ _| |__  _   _ ___ ___ 
  / _` | '_ \| | | / __/ __|
 | (_| | |_) | |_| \__ \__ \
  \__,_|_.__/ \__, |___/___/
               __/ |        
              |___/         
   
    """
    with open(DATA_FILE, "rb") as file:
        key = load_key()
        encrypted_data = file.read()
        data = decrypt_data(encrypted_data, key)
        profiles = json.loads(data)

    print(ascii_art)
    print("\nLoad - 1\n")
    print("Login - 2\n")
    choice = input("\nabyss@self~$: ").strip()
    if choice == '1':
        clear_terminal()
        print(ascii_art)
        print("\nAvailable Profile's\n")
        for name in profiles:
            print(f"- {name}\n")
        profile_name = input("\nabyss@profile~$: ").strip()
        if profile_name in profiles:
            token = profiles[profile_name]["token"]
            prefix = profiles[profile_name]["prefix"]
        else:
            print("Profile not found. Please restart and create a new profile.")
            sys.exit()
    elif choice == '2':
        profile_name = input("Enter profile name: ").strip()
        if profile_name in profiles:
            token = profiles[profile_name]["token"]
            prefix = profiles[profile_name]["prefix"]
        else:
            token = input("Token: ")
            prefix = input("Prefix: ")
            profiles[profile_name] = {"token": token, "prefix": prefix}
            save_profile_data(profiles, key)
    
    clear_terminal()
    return token, prefix

def save_profile_data(profiles, key):
    data = json.dumps(profiles)
    encrypted_data = encrypt_data(data, key)
    with open(DATA_FILE, "wb") as file:
        file.write(encrypted_data)

TOKEN, PREFIX = get_token_and_prefix()

ascii_art = """
        _                   
       | |                  
   __ _| |__  _   _ ___ ___ 
  / _` | '_ \| | | / __/ __|
 | (_| | |_) | |_| \__ \__ \
  \__,_|_.__/ \__, |___/___/
               __/ |        
              |___/         

"""

bot = commands.Bot(command_prefix=PREFIX, self_bot=True)
deleted_messages = {}
current_emoji = None

@bot.event
async def on_ready():
    clear_terminal()

    if os.name == 'nt':
        os.system(f'title Abyss [BETA] - Welcome, {bot.user.name}')
    else:
        print(f"\033]0;Abyss [BETA | Welcome, {bot.user.name}]\a")

    guild_count = len(bot.guilds)
    print(ascii_art)
    print(f"Welcome to Abyss [BETA] By: @z2de | Prefix: {PREFIX} | Logged in as: {bot.user} | Servers: {guild_count}")
    
    bot.loop.create_task(react_to_messages())

async def react_to_messages():
    global current_emoji
    missed_messages = []

    while True:
        if current_emoji:
            def check(msg):
                return msg.author == bot.user

            try:
                message = await bot.wait_for('message', check=check, timeout=30.0)
                
                if not any(reaction.emoji == current_emoji for reaction in message.reactions):
                    await message.add_reaction(current_emoji)
                    print(f"[+] Reacted to message with {current_emoji}")
                else:
                    print("[!] Message already reacted to.")

            except asyncio.TimeoutError:
                if missed_messages:
                    print("[+] Reacting to missed messages...")
                    for msg in missed_messages:
                        try:
                            if not any(reaction.emoji == current_emoji for reaction in msg.reactions):
                                await msg.add_reaction(current_emoji)
                                print(f"[+] Reacted to missed message with {current_emoji}")
                        except Exception as e:
                            print(f"[!] Error reacting to missed message: {str(e)}")
                    missed_messages.clear()
                continue
            except discord.Forbidden:
                print("[!] Missing permissions to add reactions.")
            except discord.HTTPException:
                print("[!] An error occurred while adding the reaction.")
            except Exception as e:
                print(f"[!] Unexpected error: {str(e)}")

            if message and not any(reaction.emoji == current_emoji for reaction in message.reactions):
                missed_messages.append(message)
        else:
            await asyncio.sleep(1)

@bot.command()
async def react(ctx, emoji: str):
    global current_emoji
    current_emoji = emoji
    await ctx.message.delete()
    await ctx.send(f"Reaction emoji set to {emoji}")

@bot.command()
async def snipe(ctx):
    try:
        await ctx.message.delete()
        if ctx.channel.id in deleted_messages:
            content, author, server_name, server_id = deleted_messages[ctx.channel.id]
            await ctx.send(f"**{author}**: {content}")
            print(f"[+] Sniped message from {author}:{content} | Server: {server_name} | Server ID: {server_id}")
        else:
            await ctx.send("There's no recently deleted message to snipe.")
            print("[!] No recently deleted message to snipe.")
    except Exception as e:
        print(f"[!] Error: {str(e)}")

@bot.command()
async def purge(ctx, limit: int):
    try:
        await ctx.message.delete()
        if not ctx.guild:
            print("[!] This command can only be used in a server, not in DMs.")
            return

        deleted = await ctx.channel.purge(limit=limit, check=lambda m: m.author == ctx.author)
        print(f"[-] Purged {len(deleted)} messages. | Server: {ctx.guild.name} | Server ID: {ctx.guild.id}")
    except discord.Forbidden:
        print("[!] Missing permissions to delete messages.")
    except Exception as e:
        print(f"[!] Error: {str(e)}")

@bot.command()
async def stream(ctx, *, name: str):
    try:
        await ctx.message.delete()
        activity = discord.Streaming(name=name, url="https://twitch.tv/ninja")
        await bot.change_presence(activity=activity)
        print(f"[+] Streaming: {name}")
    except Exception as e:
        print(f"[!] Error: {str(e)}")

@bot.command(name="commands")
async def commands_list(ctx):
    try:
        await ctx.message.delete()
        help_message = """
        ## Available Commands:
        - react [emoji]`: Reacts to your messages with the specified emoji.
        - snipe`: Snipes the last deleted message in the channel.
        - purge [amount]`: Deletes a specified number of your messages in the channel.
        - stream [name]`: Sets your status to streaming with the specified name.

### Abyss [beta]
        """
        await ctx.send(help_message)
        print("[+] Commands command executed")
    except Exception as e:
        print(f"[!] Error: {str(e)}")

if __name__ == "__main__":
    try:
        bot.run(TOKEN, bot=False)
    except Exception as e:
        print(f"[!] Failed to start with token: {str(e)}")
