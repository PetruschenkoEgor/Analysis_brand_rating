from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseCommand(ABC):
    """Абстрактный базовый класс для всех команд обработки CSV."""
    @abstractmethod
    def execute(self) -> List[Dict[str, Any]]:
        pass
