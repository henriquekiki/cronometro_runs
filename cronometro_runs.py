import discord
from discord.ext import commands, tasks
import datetime
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

timers = {
    "minato": {"tempo_fixo": datetime.timedelta(minutes=120), "tempo_customizado": None, "contagem_fixa": True},
    "mini minato": {"tempo_fixo": datetime.timedelta(minutes=60), "tempo_customizado": None, "contagem_fixa": True},
    "d reaper": {"tempo_fixo": datetime.timedelta(minutes=60), "tempo_customizado": None, "contagem_fixa": True},
}

def format_time(td):
    hours, remainder = divmod(td.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:02}H {minutes:02}M"

@bot.command()
async def minato(ctx, tempo_customizado: int = None):
    if tempo_customizado is not None:
        timers['minato']['tempo_customizado'] = datetime.timedelta(minutes=tempo_customizado)
        timers['minato']['tempo_fixo'] = datetime.timedelta(minutes=120)
        timers['minato']['contagem_fixa'] = False
        await ctx.send(f"Run de Minato iniciará em {tempo_customizado} minutos e depois seguirá o tempo fixo.")
    else:
        await ctx.send(f"Tempo aproximado para Run de Minato: {format_time(timers['minato']['tempo_customizado'] or timers['minato']['tempo_fixo'])} CH 0")

@bot.command()
async def dreaper(ctx, tempo_customizado: int = None):
    if tempo_customizado is not None:
        timers['d reaper']['tempo_customizado'] = datetime.timedelta(minutes=tempo_customizado)
        timers['d reaper']['tempo_fixo'] = datetime.timedelta(minutes=60)
        timers['d reaper']['contagem_fixa'] = False
        await ctx.send(f"Run de D-Reaper iniciará em {tempo_customizado} minutos e depois seguirá o tempo fixo.")
    else:
        await ctx.send(f"Tempo aproximado para Run D-Reaper: {format_time(timers['d reaper']['tempo_customizado'] or timers['d reaper']['tempo_fixo'])} CH 0")

@tasks.loop(seconds=1)
async def atualizar_temporizadores():
    for timer_name, timer in timers.items():
        
        if timer['tempo_customizado'] and timer['tempo_customizado'].total_seconds() > 0:
            timer['tempo_customizado'] -= datetime.timedelta(seconds=1)
            timer['contagem_fixa'] = False

        else:
            timer['contagem_fixa'] = True
            timer['tempo_fixo'] -= datetime.timedelta(seconds=1)
        
        if timer['tempo_fixo'].total_seconds() <= 0:
            timer['tempo_fixo'] = timers[timer_name]['original_tempo_fixo']


@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    for timer in timers.values():
        timer['original_tempo_customizado'] = timer['tempo_customizado']
        timer['original_tempo_fixo'] = timer['tempo_fixo']
    atualizar_temporizadores.start()


discord_token = 'TOKEN DO SEU BOT AQUI'
bot.run(discord_token)
