"""CPU and RAM monitoring widget"""
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static
from textual.reactive import reactive
import psutil
from datetime import datetime


class CPUMonitor(Static):
    """Widget to display CPU and RAM usage with sparklines"""
    
    cpu_percent = reactive(0.0)
    ram_percent = reactive(0.0)
    cpu_history = reactive([])
    ram_history = reactive([])
    
    def __init__(self):
        super().__init__()
        self.max_history = 20
        self.cpu_history = []
        self.ram_history = []
    
    def on_mount(self) -> None:
        """Set up update interval when mounted"""
        self.update_interval = self.set_interval(1.0, self.update_stats)
        self.update_stats()
    
    def update_stats(self) -> None:
        """Update CPU and RAM statistics"""
        # Get CPU and RAM percentages
        self.cpu_percent = psutil.cpu_percent(interval=0.1)
        self.ram_percent = psutil.virtual_memory().percent
        
        # Update history for sparklines
        self.cpu_history.append(self.cpu_percent)
        self.ram_history.append(self.ram_percent)
        
        # Keep only last N items
        if len(self.cpu_history) > self.max_history:
            self.cpu_history.pop(0)
        if len(self.ram_history) > self.max_history:
            self.ram_history.pop(0)
        
        self.refresh()
    
    def render(self) -> str:
        """Render the CPU/RAM monitor display"""
        # Get system info
        cpu_count = psutil.cpu_count()
        ram = psutil.virtual_memory()
        ram_total_gb = ram.total / (1024 ** 3)
        ram_used_gb = ram.used / (1024 ** 3)
        
        # Get process count
        try:
            process_count = len(psutil.pids())
        except:
            process_count = 0
        
        # Get CPU temperature (if available)
        temp_str = "N/A"
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                # Try to get CPU temp from common sensors
                for name in ['coretemp', 'cpu_thermal', 'k10temp']:
                    if name in temps and temps[name]:
                        temp_str = f"{temps[name][0].current:.1f}°C"
                        break
        except:
            pass
        
        # Create sparkline for CPU
        cpu_spark = self._create_sparkline(self.cpu_history)
        ram_spark = self._create_sparkline(self.ram_history)
        
        # Create bars
        cpu_bar = self._create_bar(self.cpu_percent)
        ram_bar = self._create_bar(self.ram_percent)
        
        output = f"""╔═══════════════════════════════╗
║ ⚡ SYSTEM MONITOR            ║
╠═══════════════════════════════╣
║                               ║
║ CPU Usage: {self.cpu_percent:5.1f}%           ║
║ {cpu_bar} ║
║ {cpu_spark} ║
║                               ║
║ RAM Usage: {self.ram_percent:5.1f}%           ║
║ {ram_bar} ║
║ {ram_spark} ║
║                               ║
║ Cores: {cpu_count:2d}  Processes: {process_count:4d} ║
║ RAM: {ram_used_gb:4.1f}/{ram_total_gb:4.1f} GB           ║
║ Temp: {temp_str:>16s}       ║
╚═══════════════════════════════╝"""
        
        return output
    
    def _create_sparkline(self, data: list) -> str:
        """Create a sparkline from data"""
        if not data:
            return " " * 29
        
        # Sparkline characters from low to high
        chars = " ▁▂▃▄▅▆▇█"
        max_val = max(data) if data else 100
        if max_val == 0:
            max_val = 1
        
        spark = ""
        for val in data:
            index = int((val / max_val) * (len(chars) - 1))
            spark += chars[index]
        
        # Pad to width
        spark = spark[:29].ljust(29)
        return spark
    
    def _create_bar(self, percent: float) -> str:
        """Create a progress bar"""
        width = 27
        filled = int((percent / 100) * width)
        bar = "█" * filled + "░" * (width - filled)
        return bar
