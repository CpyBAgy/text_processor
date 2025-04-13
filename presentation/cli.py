import os
import sys
import json
from typing import List, Optional, Tuple
from domain import ProcessingResult


class CLI:
    """Интерфейс командной строки."""

    @staticmethod
    def parse_args() -> Tuple[str, Optional[str]]:
        """Разбор аргументов командной строки."""
        if len(sys.argv) == 1 or (
            len(sys.argv) == 2 and sys.argv[1].lower() in ["help", "-h", "--help", "/?"]
        ):
            CLI.show_help()
            sys.exit(0)

        if len(sys.argv) == 2:
            return sys.argv[1], None

        if len(sys.argv) != 3:
            print(
                "Неверные аргументы\nВоспользуйтесь командой 'python script.py' для справки"
            )
            sys.exit(1)

        return sys.argv[1], sys.argv[2]

    @staticmethod
    def show_help() -> None:
        """Вывод справочной информации о программе."""
        help_text = """
Программа для обработки текстовых файлов согласно заданной конфигурации.

ИСПОЛЬЗОВАНИЕ:
    python script.py <config_file> <config_id>
    python script.py <config_file>
    python script.py help

АРГУМЕНТЫ:
    <config_file>    Путь к конфигурационному файлу
    <config_id>      ID конфигурации для использования
    help             Показать эту справку

ФОРМАТЫ КОНФИГУРАЦИИ:
    Каждая конфигурация должна содержать:
    - ID (например, #1)
    - mode: dir или files
    - path: путь к директории или список файлов через запятую
    - action: string, count или replace (необязательно, по умолчанию string)

ПРИМЕРЫ:
    python script.py config.txt 1      # Использовать конфигурацию #1 из файла config.txt
    python script.py config.txt        # Показать конфигурации из файла
    python script.py help              # Показать эту справку
    """
        print(help_text)

    @staticmethod
    def display_configs(configs: List) -> None:
        """Вывод списка всех доступных конфигураций в файле."""
        print(f"\nДоступные конфигурации в файле {sys.argv[1]}:")
        print("-" * 70)
        print(f"{'ID':^5} | {'Режим':^6} | {'Действие':^10} | {'Путь':<20}")
        print("-" * 70)

        for cfg in configs:
            path = cfg.path
            if len(path) > 40:
                path = path[:37] + "..."

            print(f"{cfg.id:^5} | {cfg.mode:^6} | {cfg.action:^10} | {path:<40}")

        print("-" * 70)

    @staticmethod
    def save_result(result: ProcessingResult) -> None:
        """Сохранение результата в JSON файл."""
        result_dict = {
            "configFile": result.config_file,
            "configurationID": result.config_id,
            "configurationData": result.config_data,
            "out": result.out,
        }

        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        output_path = os.path.join(
            results_dir, f"result_config_{result.config_id}.json"
        )
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)

        print(f"Результат сохранен в: {output_path}")
