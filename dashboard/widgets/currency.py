"""Currency rates display widget"""
from textual.widgets import Static
from textual.reactive import reactive
from dashboard.api.currency_api import CurrencyAPI
from typing import Dict, Any
import random


class CurrencyWidget(Static):
    """Widget to display cryptocurrency and fiat currency rates"""
    
    currency_data = reactive({})
    
    def __init__(self):
        super().__init__()
        self.api = CurrencyAPI()
        self.trend_history = {
            "BTC": [],
            "USD": [],
            "EUR": [],
            "PLN": [],
            "UAH": []
        }
        self.max_trend = 10
    
    def on_mount(self) -> None:
        """Set up update interval when mounted"""
        self.update_interval = self.set_interval(60.0, self.update_rates)  # Update every minute
        self.call_later(self.update_rates)  # Immediate first update
    
    async def update_rates(self) -> None:
        """Fetch and update currency rates"""
        self.currency_data = await self.api.get_all_rates()
        
        # Update trend history
        for symbol in self.trend_history:
            if symbol in self.currency_data:
                price = self.currency_data[symbol].get("price", 0)
                self.trend_history[symbol].append(price)
                if len(self.trend_history[symbol]) > self.max_trend:
                    self.trend_history[symbol].pop(0)
        
        self.refresh()
    
    def render(self) -> str:
        """Render the currency display"""
        if not self.currency_data:
            return self._render_loading()
        
        # Currency symbols
        symbols_map = {
            "BTC": "₿",
            "USD": "$",
            "EUR": "€",
            "UAH": "₴",
            "PLN": "zł"
        }
        
        # Display order
        display_order = ["BTC", "USD", "EUR", "UAH", "PLN"]
        
        lines = []
        lines.append("╔═══════════════════════════════╗")
        lines.append("║ 💰 CURRENCY RATES             ║")
        lines.append("╠═══════════════════════════════╣")
        lines.append("║                               ║")
        
        for symbol in display_order:
            if symbol not in self.currency_data:
                continue
            
            data = self.currency_data[symbol]
            price = data.get("price", 0)
            change = data.get("change_24h", 0)
            base = data.get("base", "")
            sym = symbols_map.get(symbol, symbol)
            
            # Format price based on currency
            if symbol == "BTC":
                price_str = f"${price:,.2f}" if price > 0 else "N/A"
                pair = f"{symbol}/{base}"
            elif symbol == "UAH":
                price_str = "1.00"
                pair = "UAH"
            else:
                price_str = f"{price:.2f}" if price > 0 else "N/A"
                pair = f"{symbol}/{base}"
            
            # Change indicator
            if change > 0:
                change_str = f"↑ {change:+.2f}%"
                change_color = "+"
            elif change < 0:
                change_str = f"↓ {change:+.2f}%"
                change_color = "-"
            else:
                change_str = "  0.00%"
                change_color = " "
            
            # Trend sparkline
            trend = self._create_trend(symbol)
            
            # Format line (adjusted to fit)
            lines.append(f"║ {sym} {symbol:3s} {price_str:>12s}        ║")
            lines.append(f"║     {pair:8s} {change_str:>12s} ║")
            lines.append(f"║     {trend:23s} ║")
        
        lines.append("║                               ║")
        lines.append("╚═══════════════════════════════╝")
        
        return "\n".join(lines)
    
    def _create_trend(self, symbol: str) -> str:
        """Create a mini trend sparkline"""
        if symbol not in self.trend_history or not self.trend_history[symbol]:
            return " " * 23
        
        data = self.trend_history[symbol]
        if len(data) < 2:
            return "━" * 23
        
        # Sparkline characters
        chars = " ▁▂▃▄▅▆▇█"
        
        min_val = min(data)
        max_val = max(data)
        range_val = max_val - min_val
        
        if range_val == 0:
            return "━" * 23
        
        spark = ""
        for val in data:
            normalized = (val - min_val) / range_val
            index = int(normalized * (len(chars) - 1))
            spark += chars[index]
        
        return spark[:23].ljust(23)
    
    def _render_loading(self) -> str:
        """Render loading state"""
        return """╔═══════════════════════════════╗
║ 💰 CURRENCY RATES             ║
╠═══════════════════════════════╣
║                               ║
║   Loading currency data...    ║
║                               ║
║                               ║
║                               ║
║                               ║
║                               ║
║                               ║
║                               ║
║                               ║
║                               ║
║                               ║
║                               ║
╚═══════════════════════════════╝"""
