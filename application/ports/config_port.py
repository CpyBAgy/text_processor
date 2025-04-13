from abc import ABC, abstractmethod
from typing import List, Optional
from domain import Config


class ConfigPort(ABC):
    """Интерфейс для работы с конфигурациями."""

    @abstractmethod
    def read_configs(self, config_path: str) -> List[Config]:
        """Читает конфигурации из файла."""
        pass

    @abstractmethod
    def get_config_by_id(
        self, configs: List[Config], config_id: str
    ) -> Optional[Config]:
        """Находит конфигурацию по ID."""
        pass
