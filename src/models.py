from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class Track:
    name: str
    artist: str
    playcount: Optional[int]
    listeners: Optional[int]
    genre: Optional[str] = None
    artist_genre: Optional[str] = None
    artist_country: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Música": self.name,
            "Artista": self.artist,
            "Playcount": self.playcount if self.playcount is not None else "N/A",
            "Listeners": self.listeners if self.listeners is not None else "N/A",
            "Gênero musical da música": self.genre or "N/A",
            "Gênero musical do artista": self.artist_genre or "N/A",
        }
