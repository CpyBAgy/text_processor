from dataclasses import dataclass
from typing import Dict, List, Union


@dataclass
class Config:
    """Доменная модель конфигурации."""

    id: str
    mode: str
    path: str
    action: str = "string"


@dataclass
class FileContent:
    """Доменная модель содержимого файла."""

    file_path: str
    lines: List[str]


@dataclass
class ProcessingResult:
    """Результат обработки файлов."""

    config_file: str
    config_id: str
    config_data: Dict[str, str]
    out: Dict[str, Dict[str, Union[str, int]]]
