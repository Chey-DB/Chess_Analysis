import requests
import logging

class ChessDataExtractor:
    def __init__(self, username: str, email: str) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": f"username:{username}, email:{email}"})
        self.url = f"https://api.chess.com/pub/player/{username}/games/archives"
        self.all_games_cache = None  # Cache for storing all games data

    def safe_request(self, url: str) -> dict:
        """Make a safe HTTP GET request and return the JSON data."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Failed to get data from {url}: {str(e)}")
            return {}

    def get_monthly_archive_urls(self) -> list[str]:
        """Fetch all monthly archive URLs for the user."""
        data = self.safe_request(self.url)
        return data.get("archives", [])

    def get_games_from_monthly_archive(self, monthly_archive_url: str) -> list[dict[str, any]]:
        """Fetch games from a specified monthly archive URL."""
        data = self.safe_request(monthly_archive_url)
        return data.get("games", [])

    def get_all_games(self) -> list[dict[str, any]]:
        """Aggregate all games from all available archives."""
        if self.all_games_cache is None:
            self.all_games_cache = []
            monthly_archive_urls = self.get_monthly_archive_urls()
            for url in monthly_archive_urls:
                games = self.get_games_from_monthly_archive(url)
                self.all_games_cache.extend(games)
        return self.all_games_cache
    
    def extract_games_by_type(self, game_type: str) -> list[dict[str, any]]:
        """Extract games filtered by type ('live' or 'daily')."""
        all_games = self.get_all_games()
        filtered_games = [game for game in all_games if game["url"].split("/")[-2] == game_type]
        return filtered_games

    def extract_pgn(self) -> list[str]:
        """Extract the PGNs of all games."""
        all_games = self.get_all_games()
        pgns = [game["pgn"] for game in all_games]
        return pgns
