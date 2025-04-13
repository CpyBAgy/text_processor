from typing import List, Dict, Optional
from domain.models import FileContent
from application.ports import FileSystemPort


class FileRepository:
    """Репозиторий для работы с файлами."""

    def __init__(self, file_system: FileSystemPort):
        self.file_system = file_system
        self._cache: Dict[str, FileContent] = {}

    def get_file_content(self, file_path: str, use_cache: bool = True) -> FileContent:
        """Получает содержимое файла."""
        if use_cache and file_path in self._cache:
            return self._cache[file_path]

        lines = self.file_system.read_file(file_path)
        file_content = FileContent(file_path=file_path, lines=lines)

        self._cache[file_path] = file_content

        return file_content

    def get_multiple_files(
        self, file_paths: List[str], use_cache: bool = True
    ) -> List[FileContent]:
        """Получает содержимое нескольких файлов."""
        result = []
        for path in file_paths:
            result.append(self.get_file_content(path, use_cache))
        return result

    def clear_cache(self) -> None:
        """Очищает кэш файлов."""
        self._cache.clear()
