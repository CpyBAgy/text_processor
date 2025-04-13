import re
from typing import List, Optional
from domain import Config
from application.ports import ConfigPort
from application.ports import FileSystemPort


class ConfigFileAdapter(ConfigPort):
    """Адаптер для работы с конфигурационными файлами."""

    def __init__(self, file_system_port: FileSystemPort):
        self.file_system_port = file_system_port

    def read_configs(self, config_path: str) -> List[Config]:
        """Читает конфигурации из файла."""
        content = "\n".join(self.file_system_port.read_file(config_path))

        config_blocks = re.split(r"(?=^#\d+$)", content, flags=re.MULTILINE)

        configs = []
        for block in config_blocks:
            if not block.strip():
                continue

            lines = block.strip().split("\n")

            if not lines[0].startswith("#") or not lines[0][1:].strip().isdigit():
                continue

            config_dict = {"id": lines[0][1:].strip()}

            for line in lines[1:]:
                line = line.strip()
                if not line or (line.startswith("#") and ":" not in line):
                    continue

                if ":" in line:
                    if line.startswith("#"):
                        line = line[1:]

                    key, value = line.split(":", 1)
                    config_dict[key.strip().lower()] = value.strip()

            if "mode" in config_dict and "path" in config_dict:
                configs.append(
                    Config(
                        id=config_dict["id"],
                        mode=config_dict["mode"],
                        path=config_dict["path"],
                        action=config_dict.get("action", "string"),
                    )
                )

        return configs

    def get_config_by_id(
        self, configs: List[Config], config_id: str
    ) -> Optional[Config]:
        """Находит конфигурацию по ID."""
        for config in configs:
            if config.id == config_id:
                return config
        return None
