import discord
from discord.ext import commands

intencoes = discord.Intents.default()
intencoes.message_content = True

bot = commands.Bot(command_prefix="!", intents=intencoes)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command()
async def oi(ctx):
    await ctx.send(f'Olá, {ctx.author.name}! Tudo certo?')

@bot.command()
async def ajuda(ctx):
    comandos = "**Comandos disponíveis:**\n"
    comandos += "`!oi` - O bot te cumprimenta\n"
    comandos += "`!limpar X` - Apaga X mensagens\n"
    comandos += "`!sorteio item1 item2 item3` - Sorteia um dos itens\n"
    comandos += "`!silenciar @usuário tempo_em_minutos (opcional)` - Silencia o usuário\n"
    comandos += "`!desmutar @usuário` - Remove o silenciamento\n"
    comandos += "`!ban @usuário tempo_em_minutos (opcional) motivo (opcional)` - Bane o usuário\n"
    comandos += "`!desbanir usuário#0000` - Desbane o usuário pelo nome e tag\n"
    await ctx.send(comandos)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, quantidade: int):
    await ctx.channel.purge(limit=quantidade + 1)  # inclui o comando
    await ctx.send(f"{quantidade} mensagens apagadas!", delete_after=3)

import random

@bot.command()
async def sorteio(ctx, *itens):
    if len(itens) < 2:
        await ctx.send("Me dá pelo menos 2 itens pra sortear!")
    else:
        escolhido = random.choice(itens)
        await ctx.send(f"🎉 O sorteado foi: **{escolhido}**!")
@bot.command()
@commands.has_permissions(manage_roles=True)
async def silenciar(ctx, member: discord.Member, tempo: int = 0):
    role = discord.utils.get(ctx.guild.roles, name="Silenciado")
    if not role:
        role = await ctx.guild.create_role(name="Silenciado")

        for canal in ctx.guild.channels:
            await canal.set_permissions(role, speak=False, send_messages=False)

    await member.add_roles(role)
    await ctx.send(f"{member.mention} foi silenciado!")

    if tempo > 0:
        await asyncio.sleep(tempo * 60)  # tempo em minutos
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} foi desmutado após {tempo} minutos.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, tempo: int = 0, *, motivo=None):
    await member.ban(reason=motivo)
    await ctx.send(f"{member.mention} foi banido! Motivo: {motivo}")

    if tempo > 0:
        await asyncio.sleep(tempo * 60)
        await ctx.guild.unban(member)
        await ctx.send(f"{member.mention} foi desbanido após {tempo} minutos.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def desbanir(ctx, *, usuario):
    banned_users = await ctx.guild.bans()
    usuario_nome, usuario_tag = usuario.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (usuario_nome, usuario_tag):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} foi desbanido!")
            return

    await ctx.send("Usuário não está banido.")
@bot.command()
@commands.has_permissions(mention_everyone=True)
async def chamar_todos(ctx):
    await ctx.send("@everyone Atenção!")

    


bot.run("XXXXXX")
