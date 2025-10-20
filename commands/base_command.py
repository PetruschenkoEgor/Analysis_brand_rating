from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseCommand(ABC):
    """Абстрактный базовый класс для всех команд обработки CSV."""

    @abstractmethod
    def execute(self) -> List[Dict[str, Any]]:
        pass
