import discord
from discord import app_commands
from discord.ext import commands
import os

# Intents necesarios
intents = discord.Intents.default()
intents.message_content = True

# Bot principal
bot = commands.Bot(command_prefix="/", intents=intents)

# Evento al iniciar
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔗 Comandos sincronizados ({len(synced)})")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")

# Comando principal para crear ticket
@bot.tree.command(name="ticket", description="Crear un nuevo ticket de incidencia")
async def ticket(interaction: discord.Interaction):
    # Crear vista con botón
    view = discord.ui.View()
    view.add_item(discord.ui.Button(
        label="Crear Ticket",
        style=discord.ButtonStyle.green,
        custom_id="crear_ticket_btn"
    ))
    await interaction.response.send_message(
        "Presiona el botón para crear un ticket:",
        view=view,
        ephemeral=True
    )

# Evento cuando alguien presiona un botón
@bot.event
async def on_interaction(interaction: discord.Interaction):
    try:
        if interaction.type == discord.InteractionType.component:
            if interaction.data.get("custom_id") == "crear_ticket_btn":
                await interaction.response.send_message(
                    "Formulario de ticket en construcción... 🚧",
                    ephemeral=True
                )
    except Exception as e:
        print(f"Error en interacción: {e}")

# Ejecutar bot usando token seguro desde variables de entorno
bot.run(os.getenv("DISCORD_TOKEN"))
