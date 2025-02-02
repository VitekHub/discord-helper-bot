from discord.ext import commands

class HelpCommand:
    @staticmethod
    async def execute(ctx):
        """Show help information"""
        help_text = """
**Summary Bot - Pokročilé použití:**

**Základní příkazy:**
• `!sum [počet]` - Shrne posledních [počet] zpráv (výchozí: 100)
• `!sum-help` - Zobrazí tuto nápovědu
• `!sum-links [první_odkaz] [poslední_odkaz]` - Shrne zprávy mezi dvěma odkazy
• `!sum-ids [první_id] [poslední_id]` - Shrne zprávy mezi dvěma ID
• `!vital [možnosti]` - Extrahuje důležité informace a klíčové body

**Pokročilé možnosti:**
1. Časové shrnutí:
• `!sum 24h` - Posledních 24 hodin
• `!sum 7d` - Posledních 7 dní

2. Shrnutí pro konkrétního uživatele:
• `!sum @uživatel` - Shrne zprávy zmiňující konkrétního uživatele

3. Shrnutí v časovém rozmezí:
• `!sum --after 2024-02-01 --before 2024-02-28` - Shrne zprávy mezi daty

**Příklady:**
• `!sum 50` - Posledních 50 zpráv
• `!sum 24h @uživatel` - Zmínky uživatele za posledních 24 hodin
• `!sum 7d --after 2024-01-01` - Posledních 7 dní zpráv po 1. lednu 2024
• `!sum-links [odkaz1] [odkaz2]` - Zprávy mezi dvěma odkazy
• `!sum-ids 1234567890 1234567891` - Zprávy mezi dvěma ID
"""
        await ctx.send(help_text)