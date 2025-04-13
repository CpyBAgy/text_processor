from abc import ABC, abstractmethod
from typing import List


class FileSystemPort(ABC):
    """Интерфейс для работы с файловой системой."""

    @abstractmethod
    def file_exists(self, path: str) -> bool:
        """Проверяет существование файла."""
        pass

    @abstractmethod
    def dir_exists(self, path: str) -> bool:
        """Проверяет существование директории."""
        pass

    @abstractmethod
    def list_files(self, dir_path: str) -> List[str]:
        """Возвращает список файлов в директории."""
        pass

    @abstractmethod
    def read_file(self, file_path: str) -> List[str]:
        """Читает содержимое файла и возвращает список строк."""
        pass

    @abstractmethod
    def write_file(self, file_path: str, content: str) -> None:
        """Записывает содержимое в файл."""
        pass

    @abstractmethod
    def get_absolute_path(self, path: str) -> str:
        """Возвращает абсолютный путь к файлу."""
        pass
