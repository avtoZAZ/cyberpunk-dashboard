"""Digital clock and system info widget"""
from textual.widgets import Static
from textual.reactive import reactive
from datetime import datetime
import platform
import socket
import psutil


class ClockWidget(Static):
    """Widget to display digital clock and system information"""
    
    current_time = reactive(datetime.now())
    
    def on_mount(self) -> None:
        """Set up update interval when mounted"""
        self.update_interval = self.set_interval(1.0, self.update_time)
        self.update_time()
    
    def update_time(self) -> None:
        """Update current time"""
        self.current_time = datetime.now()
        self.refresh()
    
    def render(self) -> str:
        """Render the clock display"""
        now = self.current_time
        
        # Format time components
        hour = now.strftime("%H")
        minute = now.strftime("%M")
        second = now.strftime("%S")
        date_str = now.strftime("%Y-%m-%d")
        day_name = now.strftime("%A")
        
        # Get system info
        hostname = socket.gethostname()
        if len(hostname) > 25:
            hostname = hostname[:22] + "..."
        
        # Get uptime
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = now - boot_time
            days = uptime.days
            hours = uptime.seconds // 3600
            minutes = (uptime.seconds % 3600) // 60
            uptime_str = f"{days}d {hours}h {minutes}m"
        except:
            uptime_str = "N/A"
        
        # Get IP address (try to get local IP)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_addr = s.getsockname()[0]
            s.close()
        except:
            ip_addr = "127.0.0.1"
        
        if len(ip_addr) > 15:
            ip_addr = ip_addr[:15]
        
        # Create ASCII digital clock digits
        output = f"""╔═══════════════════════════════╗
║ ⏰ SYSTEM TIME                ║
╠═══════════════════════════════╣
║                               ║
║        {hour}:{minute}:{second}              ║
║                               ║
║      {date_str}              ║
║      {day_name:^23s}      ║
║                               ║
║ Host: {hostname:23s} ║
║ IP:   {ip_addr:23s} ║
║ Up:   {uptime_str:23s} ║
║                               ║
╚═══════════════════════════════╝"""
        
        return output
