import requests
import json
from typing import List, Dict

class WebSearch:
    def __init__(self):
        self.brave_api_key = None  # Obter em: https://brave.com/search/api/
        self.google_api_key = None  # Opcional
        
    def search(self, query: str, num_results: int = 5, provider: str = "brave") -> List[Dict]:
        """Pesquisa na web"""
        
        if provider == "brave" and self.brave_api_key:
            return self._brave_search(query, num_results)
        else:
            # Fallback para Google Custom Search ou DuckDuckGo
            return self._duckduckgo_search(query, num_results)
    
    def _brave_search(self, query: str, num_results: int) -> List[Dict]:
        """Usa API Brave Search"""
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.brave_api_key
        }
        params = {
            "q": query,
            "count": num_results,
            "safesearch": "moderate"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            results = []
            if 'web' in data and 'results' in data['web']:
                for item in data['web']['results'][:num_results]:
                    results.append({
                        'title': item.get('title', ''),
                        'link': item.get('url', ''),
                        'snippet': item.get('description', ''),
                        'source': 'Brave Search'
                    })
            return results
        except Exception as e:
            print(f"Erro Brave Search: {e}")
            return []
    
    def _duckduckgo_search(self, query: str, num_results: int) -> List[Dict]:
        """Fallback para DuckDuckGo (sem API key)"""
        try:
            # Simulação - na prática você usaria uma biblioteca como duckduckgo-search
            return [{
                'title': f"Resultado para: {query}",
                'link': f"https://duckduckgo.com/?q={query}",
                'snippet': 'Configure Brave Search API para resultados melhores.',
                'source': 'DuckDuckGo'
            }]
        except:
            return []
    
    def set_api_key(self, api_key: str, provider: str = "brave"):
        """Configurar API Key"""
        if provider == "brave":
            self.brave_api_key = api_key
            return True
        return False
