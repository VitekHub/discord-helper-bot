from .base import BaseSummaryCommand
from ..utils.argument_parser import ArgumentParser

class FindCommand(BaseSummaryCommand):
    async def execute(self, args):
        """Execute find command"""
        try:
            # Send initial response
            await self.interaction.response.defer(thinking=True, ephemeral=True)
            
            # Join all args to handle spaces correctly
            full_text = " ".join(args)
            
            # Find the last quoted text
            prompt = None
            other_args = []
            found_quoted = False
            
            # Try to find text in both types of quotes
            for quote_char in ['"', "'"]:
                last_quote_start = full_text.rfind(quote_char)
                
                if last_quote_start != -1:
                    # Find the matching opening quote
                    prev_quote_end = full_text.rfind(quote_char, 0, last_quote_start)
                    
                    if prev_quote_end != -1:
                        # Extract the prompt and other args
                        prompt = full_text[prev_quote_end + 1:last_quote_start].strip()
                        other_args = full_text[:prev_quote_end].strip().split()
                        found_quoted = True
                        break  # Found a valid quoted text, stop looking
            
            # If no quoted text found, try to find prompt after the options
            if not found_quoted:
                # Assume everything after numeric/time arguments is the prompt
                for i, arg in enumerate(args):
                    if not (arg.endswith(('h', 'd')) or arg.isdigit() or 
                           arg.startswith(('--after', '--before')) or 
                           arg.startswith('<@')):
                        prompt = ' '.join(args[i:])
                        other_args = list(args[:i])
                        break
            
            if not prompt or not prompt.strip():
                await self.send_status('Chybí prompt. Použijte: !find [možnosti] "váš prompt v uvozovkách" nebo \'váš prompt v uvozovkách\'')
                return
                
            await self.send_status("Analyzuji zprávy podle zadaného promptu...")
            
            # Parse remaining arguments
            parser = ArgumentParser(other_args)
            filters = parser.parse()
            
            # Get messages with filters
            messages = await self.message_service.get_channel_messages(
                self.ctx.channel,
                limit=filters.limit,
                after=filters.after,
                before=filters.before
            )
            
            if filters.mentioned_user:
                messages = [msg for msg in messages if filters.mentioned_user in msg]
                
            if not messages:
                await self.send_status("Nenalezeny žádné zprávy k analýze.")
                return
                
            # Send messages to AI with custom prompt
            conversation_text = "\n".join(messages)
            response = await self.ai_service.process_custom_prompt(conversation_text, prompt)
            
            await self.ctx.send(f"**Výsledek analýzy {len(messages)} zpráv** (bez příkazů a zpráv botů):\n\n{response}")
            
        except Exception as e:
            await self.send_status(f"Chyba při zpracování příkazu: {str(e)}")