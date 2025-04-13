from typing import List, Optional
from domain import Config
from application.ports import ConfigPort
from application.ports import FileSystemPort


class ConfigService:
    """Сервис для работы с конфигурациями."""

    def __init__(self, config_port: ConfigPort, file_system_port: FileSystemPort):
        self.config_port = config_port
        self.file_system_port = file_system_port

    def read_configs(self, config_path: str) -> List[Config]:
        """Читает конфигурации из файла."""
        if not self.file_system_port.file_exists(config_path):
            raise FileNotFoundError(f"Конфигурационный файл не найден: {config_path}")

        return self.config_port.read_configs(config_path)

    def get_config_by_id(
        self, configs: List[Config], config_id: str
    ) -> Optional[Config]:
        """Находит конфигурацию по ID."""
        return self.config_port.get_config_by_id(configs, config_id)

    def get_files_from_config(self, config: Config) -> List[str]:
        """Получает список файлов на основе конфигурации."""
        if config.mode == "dir":
            if not self.file_system_port.dir_exists(config.path):
                raise FileNotFoundError(f"Директория не найдена: {config.path}")

            return sorted(self.file_system_port.list_files(config.path))

        elif config.mode == "files":
            file_paths = [p.strip() for p in config.path.split(",")]
            for file_path in file_paths:
                if not self.file_system_port.file_exists(file_path):
                    raise FileNotFoundError(f"Файл не найден: {file_path}")

            return sorted(file_paths)

        else:
            raise ValueError(f"Неподдерживаемый режим: {config.mode}")
