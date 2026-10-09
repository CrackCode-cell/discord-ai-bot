import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DISCORD_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("Add both keys to your .env file.")

ai = AsyncOpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is online as {bot.user}!")


@bot.tree.command(
    name="ask",
    description="Ask the AI a question"
)
@app_commands.describe(question="What do you want to ask?")
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer(thinking=True)

    try:
        response = await ai.responses.create(
            model="gpt-5.5",
            instructions=(
                "You are a friendly Discord AI bot. "
                "Give helpful, clear, concise answers."
            ),
            input=question,
            max_output_tokens=250,
        )

        answer = response.output_text.strip()

        if not answer:
            answer = "I couldn't generate an answer this time."

        await interaction.followup.send(answer[:1900])

    except Exception:
        print("An AI request failed. Check the terminal for details.")
        await interaction.followup.send(
            "Sorry, I couldn't answer that right now. "
            "Please try again later."
        )


bot.run(DISCORD_TOKEN)
