import json
import os
from typing import List
from domain.models import Config, ProcessingResult


class ConsoleFormatter:
    """Форматирование вывода в консоль."""

    @staticmethod
    def format_configs(configs: List[Config], config_file: str) -> str:
        """Форматирует список конфигураций для вывода."""
        result = [
            f"\nДоступные конфигурации в файле {config_file}:",
            "-" * 70,
            f"{'ID':^5} | {'Режим':^6} | {'Действие':^10} | {'Путь':<20}",
            "-" * 70,
        ]

        for cfg in configs:
            path = cfg.path
            if len(path) > 40:
                path = path[:37] + "..."

            result.append(
                f"{cfg.id:^5} | {cfg.mode:^6} | {cfg.action:^10} | {path:<40}"
            )

        result.append("-" * 70)
        return "\n".join(result)

    @staticmethod
    def format_error(error_message: str) -> str:
        """Форматирует сообщение об ошибке."""
        return f"Ошибка: {error_message}"


class JsonFormatter:
    """Форматирование данных в JSON."""

    @staticmethod
    def format_result(result: ProcessingResult) -> str:
        """Преобразует результат обработки в JSON строку."""
        result_dict = {
            "configFile": result.config_file,
            "configurationID": result.config_id,
            "configurationData": result.config_data,
            "out": result.out,
        }

        return json.dumps(result_dict, indent=2, ensure_ascii=False)

    @staticmethod
    def save_to_file(result: ProcessingResult, file_path: str = None) -> str:
        """Сохраняет результат в JSON файл."""
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        if file_path is None:
            file_path = os.path.join(
                results_dir, f"result_config_{result.config_id}.json"
            )
        elif not os.path.dirname(file_path):
            file_path = os.path.join(results_dir, file_path)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(JsonFormatter.format_result(result))

        return file_path
