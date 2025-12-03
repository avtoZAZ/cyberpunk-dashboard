"""Currency API client for crypto and fiat currencies"""
import httpx
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


class CurrencyAPI:
    """Fetches currency rates from CoinGecko and ExchangeRate-API"""
    
    def __init__(self):
        self.coingecko_url = "https://api.coingecko.com/api/v3"
        self.exchange_url = "https://open.er-api.com/v6/latest"
        self._cache = {}
        self._cache_time = {}
        self._cache_duration = timedelta(minutes=5)
    
    async def get_btc_price(self) -> Optional[Dict[str, Any]]:
        """
        Fetch Bitcoin price from CoinGecko
        
        Returns:
            Dict with BTC/USD price and 24h change
        """
        cache_key = "btc"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.coingecko_url}/simple/price",
                    params={
                        "ids": "bitcoin",
                        "vs_currencies": "usd",
                        "include_24hr_change": "true"
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                result = {
                    "symbol": "BTC",
                    "price": data["bitcoin"]["usd"],
                    "change_24h": data["bitcoin"].get("usd_24h_change", 0),
                    "base": "USD"
                }
                
                self._cache[cache_key] = result
                self._cache_time[cache_key] = datetime.now()
                return result
                
        except Exception as e:
            return {
                "symbol": "BTC",
                "price": 0,
                "change_24h": 0,
                "base": "USD",
                "error": str(e)[:30]
            }
    
    async def get_fiat_rates(self) -> Optional[Dict[str, Any]]:
        """
        Fetch fiat currency rates (USD, EUR, PLN to UAH)
        
        Returns:
            Dict with exchange rates
        """
        cache_key = "fiat"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Get rates with UAH as base
                response = await client.get(f"{self.exchange_url}/UAH")
                response.raise_for_status()
                data = response.json()
                
                rates = data.get("rates", {})
                
                # Convert to show how much UAH you get for 1 unit of foreign currency
                result = {
                    "USD": {
                        "symbol": "USD",
                        "price": 1 / rates.get("USD", 1) if rates.get("USD") else 0,
                        "change_24h": 0,  # ExchangeRate-API doesn't provide change
                        "base": "UAH"
                    },
                    "EUR": {
                        "symbol": "EUR",
                        "price": 1 / rates.get("EUR", 1) if rates.get("EUR") else 0,
                        "change_24h": 0,
                        "base": "UAH"
                    },
                    "PLN": {
                        "symbol": "PLN",
                        "price": 1 / rates.get("PLN", 1) if rates.get("PLN") else 0,
                        "change_24h": 0,
                        "base": "UAH"
                    },
                    "UAH": {
                        "symbol": "UAH",
                        "price": 1.0,
                        "change_24h": 0,
                        "base": "UAH"
                    }
                }
                
                self._cache[cache_key] = result
                self._cache_time[cache_key] = datetime.now()
                return result
                
        except Exception as e:
            return {
                "USD": {"symbol": "USD", "price": 0, "change_24h": 0, "base": "UAH", "error": str(e)[:30]},
                "EUR": {"symbol": "EUR", "price": 0, "change_24h": 0, "base": "UAH", "error": str(e)[:30]},
                "PLN": {"symbol": "PLN", "price": 0, "change_24h": 0, "base": "UAH", "error": str(e)[:30]},
                "UAH": {"symbol": "UAH", "price": 1.0, "change_24h": 0, "base": "UAH"},
            }
    
    async def get_all_rates(self) -> Dict[str, Dict[str, Any]]:
        """
        Fetch all currency rates (BTC + fiat)
        
        Returns:
            Dict with all currency data
        """
        btc_data = await self.get_btc_price()
        fiat_data = await self.get_fiat_rates()
        
        result = {
            "BTC": btc_data,
            **fiat_data
        }
        
        return result
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cache is still valid"""
        if key not in self._cache or key not in self._cache_time:
            return False
        
        return datetime.now() - self._cache_time[key] < self._cache_duration
