import discord
from discord.ext import commands
import requests
import os

# Configuración inicial
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Variables de entorno
APPSHEET_URL = os.getenv("APPSHEET_URL")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # ID del canal #crear-ticket

# Opciones predefinidas
UNIDADES = ["ECOVALLAS", "VIAVERDE", "BIOBOX", "BBOXXO"]
DEPARTAMENTOS = [
    "Analista de Operaciones", "Monitoreo Digital", "Operación Digital",
    "Soporte Remoto Digital", "Programación de Pauta Digital", "Directivo",
    "Marketing y Diseño"
]
CATEGORIAS = [
    "HARDWARE", "SOFTWARE Y CONFIGURACIÓN", "CONECTIVIDAD Y RED",
    "CONTENIDO / ARTE", "PROCESOS Y GESTIÓN",
    "FACTORES EXTERNOS Y SEGURIDAD", "MANTENIMIENTO Y SOLICITUDES"
]
CANALES = ["Llamada", "Correo", "WhatsApp", "Aplicación"]

# Al iniciar el bot
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.purge(limit=5)
        view = TicketButton()
        await channel.send(
            "📝 *Crear Ticket de Incidencia*\nPresiona el botón para comenzar.",
            view=view
        )

# Botón principal
class TicketButton(discord.ui.View):
    @discord.ui.button(label="Crear Ticket", style=discord.ButtonStyle.primary)
    async def crear_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Selecciona la Unidad de Negocio:",
            view=UnidadSelect(interaction.user),
            ephemeral=True
        )

# Selección: Unidad de Negocio
class UnidadSelect(discord.ui.View):
    def _init_(self, user):
        super()._init_()
        self.user = user
        self.add_item(UnidadDropdown())

class UnidadDropdown(discord.ui.Select):
    def _init_(self):
        options = [discord.SelectOption(label=u) for u in UNIDADES]
        super()._init_(placeholder="Selecciona una unidad...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Selecciona el Departamento que reporta:",
            view=DepartamentoSelect(),
            ephemeral=True
        )

# Selección: Departamento
class DepartamentoSelect(discord.ui.View):
    def _init_(self):
        super()._init_()
        self.add_item(DepartamentoDropdown())

class DepartamentoDropdown(discord.ui.Select):
    def _init_(self):
        options = [discord.SelectOption(label=d) for d in DEPARTAMENTOS]
        super()._init_(placeholder="Selecciona un departamento...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Selecciona la Categoría Principal:",
            view=CategoriaSelect(),
            ephemeral=True
        )

# Selección: Categoría
class CategoriaSelect(discord.ui.View):
    def _init_(self):
        super()._init_()
        self.add_item(CategoriaDropdown())

class CategoriaDropdown(discord.ui.Select):
    def _init_(self):
        options = [discord.SelectOption(label=c) for c in CATEGORIAS]
        super()._init_(placeholder="Selecciona una categoría...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Selecciona el Canal de reporte:",
            view=CanalSelect(),
            ephemeral=True
        )

# Selección: Canal
class CanalSelect(discord.ui.View):
    def _init_(self):
        super()._init_()
        self.add_item(CanalDropdown())

class CanalDropdown(discord.ui.Select):
    def _init_(self):
        options = [discord.SelectOption(label=c) for c in CANALES]
        super()._init_(placeholder="Selecciona un canal de reporte...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Por favor sube las imágenes requeridas (Testigo incidencia, Solución, Detalles de equipo, Puntaje de riesgo):",
            ephemeral=True
        )

# Envío de datos
def enviar_a_appsheet(data):
    try:
        requests.post(APPSHEET_URL, json=data)
    except Exception as e:
        print("❌ Error enviando a AppSheet:", e)

bot.run(DISCORD_TOKEN)
