"""Main Cyberpunk Dashboard Application"""
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Static
from textual.binding import Binding
from dashboard.widgets.cpu_monitor import CPUMonitor
from dashboard.widgets.weather import WeatherWidget
from dashboard.widgets.currency import CurrencyWidget
from dashboard.widgets.clock import ClockWidget
import random
import yaml
from pathlib import Path


class CyberpunkTitle(Static):
    """Animated cyberpunk title"""
    
    def on_mount(self) -> None:
        """Set up glitch effect interval"""
        self.glitch_interval = self.set_interval(2.0, self.apply_glitch)
        self.normal_title = True
    
    def apply_glitch(self) -> None:
        """Apply glitch effect to title"""
        self.normal_title = not self.normal_title
        self.refresh()
    
    def render(self) -> str:
        """Render the title with optional glitch effect"""
        if self.normal_title:
            return """
 ▄████▄▓██   ██▓ ▄▄▄▄   ▓█████  ██▀███   ██▓███   █    ██  ███▄    █  ██ ▄█▀
▒██▀ ▀█ ▒██  ██▒▓█████▄ ▓█   ▀ ▓██ ▒ ██▒▓██░  ██▒ ██  ▓██▒ ██ ▀█   █  ██▄█▒ 
▒▓█    ▄ ▒██ ██░▒██▒ ▄██▒███   ▓██ ░▄█ ▒▓██░ ██▓▒▓██  ▒██░▓██  ▀█ ██▒▓███▄░ 
▒▓▓▄ ▄██▒░ ▐██▓░▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄  ▒██▄█▓▒ ▒▓▓█  ░██░▓██▒  ▐▌██▒▓██ █▄ 
▒ ▓███▀ ░░ ██▒▓░░▓█  ▀█▓░▒████▒░██▓ ▒██▒▒██▒ ░  ░▒▒█████▓ ▒██░   ▓██░▒██▒ █▄
░ ░▒ ▒  ░ ██▒▒▒ ░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░▒▓▒░ ░  ░░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒ ▒ ▒▒ ▓▒
"""
        else:
            # Glitch effect - slightly offset/corrupted version
            return """
 ▄█##▄▓██ # ██▓ ▄▄#▄   ▓█#▓█  ██▀███   ██▓███   █    ██  ███▄    █  ██ ▄█▀
▒██▀#▀█ ▒██  ██▒▓█#▓█▄ ▓█   ▀ ▓██ ▒ ██▒▓██░  ██▒ ██  ▓██▒ ██ ▀█   █  ██▄█▒ 
▒▓█  # ▄ ▒██ ██░▒██▒ ▄##▒███   ▓██ ░▄█ ▒▓██░ ██▓▒▓██  ▒██░▓██  ▀█ ██▒▓███▄░ 
▒▓▓▄#▄██▒░ ▐██▓░▒██░#▀  ▒▓█  ▄ ▒██▀▀█▄  ▒██▄█▓▒ ▒▓▓█  ░██░▓██▒  ▐▌██▒▓██ █▄ 
▒ ▓███▀#░░ ██▒▓░░▓█  ▀#▓░▒████▒░██▓ ▒██▒▒██▒ ░  ░▒▒█████▓ ▒██░   ▓██░▒██▒ █▄
░ ░▒#▒  ░ ██▒▒▒ ░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░▒▓▒░ ░  ░░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒ ▒ ▒▒ ▓▒
"""


class HackerLog(Static):
    """Scrolling hacker messages log"""
    
    messages = [
        ">>> INITIALIZING NEURAL INTERFACE...",
        ">>> ACCESS GRANTED: LEVEL 9",
        ">>> DECRYPTING BLOCKCHAIN DATA...",
        ">>> SCANNING NETWORK NODES...",
        ">>> QUANTUM ENCRYPTION ACTIVE",
        ">>> FIREWALL STATUS: OPTIMAL",
        ">>> SYNCING WITH SATELLITE...",
        ">>> MATRIX CONNECTION STABLE",
        ">>> AI ASSISTANT ONLINE",
        ">>> CYBER DEFENSE: ENABLED",
        ">>> MONITORING CRYPTO MARKETS...",
        ">>> DATA STREAM: ACTIVE",
        ">>> ANOMALY DETECTION: ON",
        ">>> SYSTEM INTEGRITY: 100%",
    ]
    
    def on_mount(self) -> None:
        """Set up message rotation"""
        self.message_interval = self.set_interval(3.0, self.rotate_message)
        self.current_message = random.choice(self.messages)
    
    def rotate_message(self) -> None:
        """Rotate to next random message"""
        self.current_message = random.choice(self.messages)
        self.refresh()
    
    def render(self) -> str:
        """Render current message"""
        return f" {self.current_message}"


class CyberpunkDashboard(App):
    """Main Cyberpunk Dashboard Application"""
    
    CSS_PATH = Path(__file__).parent / "styles" / "cyberpunk.tcss"
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("r", "refresh_data", "Refresh"),
        ("h", "toggle_help", "Help"),
    ]
    
    def __init__(self, city: str = "Kyiv"):
        super().__init__()
        self.city = city
        self.title = "CYBERPUNK DASHBOARD"
        self.sub_title = "[ NEURAL INTERFACE v1.0 ]"
    
    def compose(self) -> ComposeResult:
        """Create child widgets"""
        yield CyberpunkTitle(id="title")
        
        with Container(id="main-grid"):
            yield CPUMonitor()
            yield WeatherWidget(self.city)
            yield CurrencyWidget()
            yield ClockWidget()
        
        yield HackerLog(id="footer")
    
    def action_refresh_data(self) -> None:
        """Refresh all data widgets"""
        # Get all widgets and trigger their update methods
        for widget in self.query(CPUMonitor):
            widget.update_stats()
        
        for widget in self.query(WeatherWidget):
            widget.call_later(widget.update_weather)
        
        for widget in self.query(CurrencyWidget):
            widget.call_later(widget.update_rates)
    
    def action_toggle_help(self) -> None:
        """Show help message"""
        # For now, just rotate the footer message
        log = self.query_one(HackerLog)
        log.current_message = ">>> HOTKEYS: Q=Quit | R=Refresh | H=Help"
        log.refresh()


def load_config() -> dict:
    """Load configuration from config.yaml if it exists"""
    config_path = Path("config.yaml")
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {}


def run():
    """Run the dashboard application"""
    config = load_config()
    city = config.get("city", "Kyiv")
    
    app = CyberpunkDashboard(city=city)
    app.run()
