import difflib
import discord
import typing
from discord.ext import commands
from typing import Literal
import json
from pathlib import Path  # Importing Path from pathlib for file operations

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
asked = False
global_sub = ""
global_answer = ""
user_points = {}
global_user_points = {}
asker = str()

####################################################################
def save_user_points():
    with open('user_points.json', 'w') as file:
        json.dump(user_points, file)

def load_user_points():
    global user_points
    try:
        with open('user_points.json', 'r') as file:
            user_points = json.load(file)
    except FileNotFoundError:
        pass 

###################################################################
def save_global_user_points():
    with open('global_user_points.json', 'w') as file:
        json.dump(global_user_points, file)

def load_global_user_points():
    global global_user_points
    try:
        with open('global_user_points.json', 'r') as file:
            global_user_points = json.load(file)
    except FileNotFoundError:
        pass  
####################################################################

@bot.event
async def on_ready():
    print("Bot Ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print("error")

    # Load user_points when the bot starts
    load_user_points()
    load_global_user_points()

@bot.tree.command(name='ask')
async def ask(interaction: discord.Interaction, *, question: str, answer: str, subject: Literal['Science', 'Maths', 'English', 'Sanskrit', 'Social Science']):
    global asked
    global global_answer
    global asker
    global global_sub
    global_sub = subject
    global_answer = answer
    asker = interaction.user.name

    if asked:
        await interaction.response.send_message("There's already a question asked. Please answer it before asking a new one.", ephemeral=True)
    else:
        asked = True
        embed = discord.Embed(
            title=question,
            description=f"Subject: {subject}",
            color=discord.Color.blue()
        )
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)


@bot.tree.command(name='answer')
async def answer(interaction: discord.Interaction, *, answer: str):
    global asked
    global global_answer
    global asker 
    global global_sub
    
    similarity = difflib.SequenceMatcher(None, answer.lower(), global_answer.lower()).ratio()
    similarity_threshold = 0.65
    if asker == interaction.user.name:
        await interaction.response.send_message(f'{interaction.user.mention}, You cannot answer your own question! ')
    else:
        if not asked:
            await interaction.response.send_message("There's no question to be answered currently, you can use **/ask** to ask questions")
        else:
            user_name = interaction.user.name
            if similarity >= similarity_threshold:
                #########################################################################################################################
                if user_name not in user_points:
                    user_points[user_name] = {global_sub: 1}  # Initialize points for the user and subject if not present
                else:
                    if global_sub not in user_points[user_name]:
                        user_points[user_name][global_sub] = 1
                    else:
                        user_points[user_name][global_sub] += 1
                ##########################################################################################################################
                if user_name not in global_user_points:
                    global_user_points[user_name] = {global_sub: 1}  # Initialize points for the user and subject if not present
                else:
                    if global_sub not in global_user_points[user_name]:
                        global_user_points[user_name][global_sub] = 1
                    else:
                        global_user_points[user_name][global_sub] += 1
                #########################################################################################################################
                
                await interaction.response.send_message(f'{interaction.user.mention} answered it. He gets +1 point.')
                asked = False
                save_global_user_points()
                save_user_points()  # Save user_points after each correct answer
            else:
                await interaction.response.send_message(f'{interaction.user.mention} tried, but it was incorrect.')

@bot.tree.command(name='leaderboard')
async def leaderboard(interaction, *, leaderboard_type: Literal['Lifetime', 'Temporary'] ,subject: Literal['Total', 'Science', 'Maths', 'English', 'Sanskrit', 'Social Science']):
    global user_points
    global global_user_points

    def check_subject(a):
        if subject=='Total':
            leaderboard_message = "Leaderboard:\n```\n"
            # Sort the user_points dictionary based on total points
            sorted_leaderboard = sorted(a.items(), key=lambda x: sum(x[1].values()), reverse=True)

            for position, (user, subjects) in enumerate(sorted_leaderboard, start=1):
                total_points = sum(subjects.values())
                leaderboard_message += f"{position}. {user}: {total_points} points\n"
            
            leaderboard_message += "```"
            return leaderboard_message
        
        else:
            leaderboard_message = f"{subject} Leaderboard:\n```\n"
            
            def get_marks(user_data):
                return user_data[1].get(subject, 0)

            # Using sorted to sort users based on subject marks
            sorted_leaderboard = sorted(a.items(), key=get_marks, reverse=True)

            # Display the result
            for position, (user, _) in enumerate(sorted_leaderboard, start=1):
                points = a[user].get(subject, 0)
                leaderboard_message += f"{position}. {user}: {points} points\n"
                
            leaderboard_message += "```"
            return leaderboard_message
                
    if leaderboard_type== 'Lifetime':
        lead_msg = check_subject(global_user_points)
    elif leaderboard_type == 'Temporary':
        lead_msg = check_subject(user_points)
        
            
            
    
    await interaction.response.send_message(lead_msg)

# Run the bot
bot.run('Your API Key')
