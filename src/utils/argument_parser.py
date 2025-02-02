from dataclasses import dataclass
from datetime import datetime
from ..utils.time_parser import parse_time

@dataclass
class FilterOptions:
    limit: int = 100
    after: datetime = None
    before: datetime = None
    mentioned_user: str = None

class ArgumentParser:
    def __init__(self, args):
        self.args = args

    def parse(self) -> FilterOptions:
        """Parse command arguments into filter options"""
        options = FilterOptions()
        i = 0
        
        while i < len(self.args):
            arg = self.args[i]
            
            if arg.endswith(('h', 'd')):
                options.after = parse_time(arg)
                if options.after:
                    options.limit = None
            elif arg.isdigit():
                options.limit = int(arg)
            elif arg.startswith('<@') and arg.endswith('>'):
                options.mentioned_user = arg
            elif arg == '--after' and i + 1 < len(self.args):
                try:
                    options.after = datetime.strptime(self.args[i + 1], '%Y-%m-%d')
                    i += 1
                except ValueError:
                    raise ValueError("Invalid date format for --after. Use YYYY-MM-DD")
            elif arg == '--before' and i + 1 < len(self.args):
                try:
                    options.before = datetime.strptime(self.args[i + 1], '%Y-%m-%d')
                    i += 1
                except ValueError:
                    raise ValueError("Invalid date format for --before. Use YYYY-MM-DD")
            i += 1
            
        return options