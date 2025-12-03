# Cyberpunk Terminal Dashboard

A stunning terminal-based dashboard application inspired by cyberpunk movies and hacker interfaces. Features real-time system monitoring, weather updates, and cryptocurrency/fiat currency tracking with a distinctive neon-green Matrix aesthetic.

![Cyberpunk Dashboard](https://img.shields.io/badge/style-cyberpunk-00ff00?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.10+-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-purple?style=for-the-badge)

## 📸 Preview

![Cyberpunk Dashboard Screenshot](https://github.com/user-attachments/assets/a4e80377-72da-4821-9233-73fd8814e9d5)

## ✨ Features

### 🖥️ System Monitor
- Real-time CPU usage with animated sparkline graphs
- RAM usage tracking and visualization
- CPU temperature monitoring (when available)
- Process count and system resource display
- Updates every second

### 🌍 Weather Display
- Current temperature and weather conditions
- ASCII art weather icons (☀️ ⛅ 🌧️ ❄️)
- Humidity and wind speed
- Customizable city location
- Powered by wttr.in (no API key required)

### 💰 Currency Rates
Tracks 5 major currencies:
- **₿ BTC** (Bitcoin) - BTC/USD
- **$ USD** (US Dollar) - USD/UAH
- **€ EUR** (Euro) - EUR/UAH  
- **₴ UAH** (Ukrainian Hryvnia) - base currency
- **zł PLN** (Polish Zloty) - PLN/UAH

Features:
- Live exchange rates
- 24-hour change indicators (↑/↓)
- Mini trend sparklines
- Data from CoinGecko and ExchangeRate-API

### ⏰ System Clock
- Large digital time display
- Current date and day of week
- System hostname and IP address
- System uptime tracker

### 🎨 Cyberpunk Aesthetics
- Matrix-inspired neon green color scheme
- Glitching ASCII art title
- Animated borders and indicators
- Scrolling "hacker" message log
- Distinct color coding for each panel:
  - Cyan for CPU/RAM
  - Magenta for Weather
  - Gold for Currency
  - Blue for Clock

## 🚀 Installation

### Requirements
- Python 3.10 or higher
- pip (Python package manager)
- Terminal with Unicode support

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/avtoZAZ/cyberpunk-dashboard.git
cd cyberpunk-dashboard
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure (optional):**
```bash
cp config.example.yaml config.yaml
# Edit config.yaml to set your city
```

4. **Run the dashboard:**
```bash
python main.py
```

## ⚙️ Configuration

Create a `config.yaml` file from the example:

```yaml
# City for weather display
city: Kyiv
```

You can use any city name supported by wttr.in (e.g., London, NewYork, Tokyo, Berlin, Warsaw).

## 🎮 Keyboard Controls

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `r` | Refresh all data panels |
| `h` | Show help message |

## 📦 Project Structure

```
cyberpunk-dashboard/
├── main.py                 # Entry point
├── dashboard/
│   ├── __init__.py
│   ├── app.py              # Main Textual application
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── cpu_monitor.py  # CPU/RAM monitor widget
│   │   ├── weather.py      # Weather display widget
│   │   ├── currency.py     # Currency rates widget
│   │   └── clock.py        # Clock and system info widget
│   ├── api/
│   │   ├── __init__.py
│   │   ├── weather_api.py  # wttr.in API client
│   │   └── currency_api.py # CoinGecko & ExchangeRate API client
│   └── styles/
│       ├── __init__.py
│       └── cyberpunk.tcss  # Textual CSS styles
├── requirements.txt
├── config.example.yaml
└── README.md
```

## 🎨 Color Palette

| Color | Hex Code | Usage |
|-------|----------|-------|
| Matrix Green | `#00ff00` | Primary/Title |
| Cyan | `#00ffff` | CPU Monitor |
| Magenta | `#ff00ff` | Weather |
| Gold | `#ffd700` | Currency |
| Electric Blue | `#0080ff` | Clock |
| Red | `#ff0000` | Negative changes |
| Black | `#0a0a0a` | Background |

## 🔌 APIs Used

### Weather
- **wttr.in** - Free weather API, no registration required
- Endpoint: `https://wttr.in/{city}?format=j1`

### Cryptocurrency
- **CoinGecko API** - Free crypto prices, no API key needed
- Endpoint: `https://api.coingecko.com/api/v3/simple/price`

### Fiat Currency
- **ExchangeRate-API** - Free exchange rates
- Endpoint: `https://open.er-api.com/v6/latest/UAH`

## 🛠️ Technologies

- **[Textual](https://textual.textualize.io/)** - Modern TUI framework
- **[psutil](https://github.com/giampaolo/psutil)** - System monitoring
- **[httpx](https://www.python-httpx.org/)** - Async HTTP client
- **[PyYAML](https://pyyaml.org/)** - Configuration parsing

## 💡 Usage Examples

### Basic Usage
```bash
python main.py
```

### With Custom City
Edit `config.yaml`:
```yaml
city: Tokyo
```

Then run:
```bash
python main.py
```

## 🐛 Troubleshooting

### Temperature Not Showing
CPU temperature requires appropriate sensors and may not be available on all systems (especially virtual machines or some laptops).

### Currency Data Not Loading
- Check your internet connection
- APIs may have rate limits; wait a minute and try refreshing with `r`

### Unicode Characters Not Displaying
Ensure your terminal supports Unicode. Try a modern terminal like:
- **Linux/Mac**: iTerm2, GNOME Terminal, Alacritty
- **Windows**: Windows Terminal, ConEmu

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is open source and available under the MIT License.

## 🌟 Acknowledgments

- Inspired by cyberpunk aesthetics and The Matrix
- Built with the amazing Textual framework
- Weather data from wttr.in
- Cryptocurrency data from CoinGecko
- Exchange rates from ExchangeRate-API

## 🔮 Future Enhancements

- [ ] Network traffic monitoring
- [ ] Disk usage statistics
- [ ] More cryptocurrency options
- [ ] Historical price charts
- [ ] Custom color themes
- [ ] Plugin system for additional widgets
- [ ] Matrix-style "digital rain" background effect
- [ ] Sound effects (optional)

---

Made with 💚 and lots of ☕ in the cyberpunk spirit.