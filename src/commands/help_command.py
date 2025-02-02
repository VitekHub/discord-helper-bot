import discord

class HelpCommand:
    @staticmethod
    async def execute(interaction: discord.Interaction):
        """Show help information"""
        help_text = """
**Summary Bot - Pokročilé použití:**

**Základní příkazy:**
• `/sum [počet] [čas] [@uživatel] [--after datum] [--before datum]` - Shrne zprávy podle zadaných parametrů
• `/help` - Zobrazí tuto nápovědu
• `/sum-links [první_odkaz] [poslední_odkaz]` - Shrne zprávy mezi dvěma odkazy
• `/sum-ids [první_id] [poslední_id]` - Shrne zprávy mezi dvěma ID
• `/vital [možnosti]` - Extrahuje důležité informace a klíčové body
• `/find [prompt] [možnosti]` - Analyzuje zprávy podle vlastního promptu

**Pokročilé možnosti:**
1. Časové shrnutí:
• `/sum time:24h` - Posledních 24 hodin
• `/sum time:7d` - Posledních 7 dní

2. Shrnutí pro konkrétního uživatele:
• `/sum user:@uživatel` - Shrne zprávy zmiňující konkrétního uživatele

3. Shrnutí v časovém rozmezí:
• `/sum after:2024-02-01 before:2024-02-28` - Shrne zprávy mezi daty

**Příklady:**
• `/sum count:50` - Posledních 50 zpráv
• `/sum time:24h user:@uživatel` - Zmínky uživatele za posledních 24 hodin
• `/sum time:7d after:2024-01-01` - Posledních 7 dní zpráv po 1. lednu 2024
• `/find "Najdi všechny zmínky o termínech schůzek" count:100` - Najde termíny v posledních 100 zprávách
• `/find "Jaká technická rozhodnutí byla učiněna?" time:24h` - Analyzuje rozhodnutí za posledních 24 hodin
"""
        await interaction.response.send_message(help_text)