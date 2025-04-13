import os
from typing import List
from application.ports import FileSystemPort


class LocalFileSystemAdapter(FileSystemPort):
    """Адаптер для работы с локальной файловой системой."""

    def file_exists(self, path: str) -> bool:
        """Проверяет существование файла."""
        return os.path.isfile(path)

    def dir_exists(self, path: str) -> bool:
        """Проверяет существование директории."""
        return os.path.isdir(path)

    def list_files(self, dir_path: str) -> List[str]:
        """Возвращает список файлов в директории."""
        file_paths = []
        for file_name in sorted(os.listdir(dir_path)):
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                file_paths.append(file_path)
        return file_paths

    def read_file(self, file_path: str) -> List[str]:
        """Читает содержимое файла и возвращает список строк."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return [line.rstrip("\n") for line in file.readlines()]
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {str(e)}")
            return []

    def write_file(self, file_path: str, content: str) -> None:
        """Записывает содержимое в файл."""
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    def get_absolute_path(self, path: str) -> str:
        """Возвращает абсолютный путь к файлу."""
        return os.path.abspath(path)
