from dataclasses import dataclass
from typing import Optional

@dataclass
class Card:
    rank: str
    value: int
    image_path: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.rank}"

    @property
    def is_ace(self) -> bool:
        return self.rank == "A" 