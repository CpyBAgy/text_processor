#!/usr/bin/env python
import sys
import traceback

from domain import TextProcessingService
from application.services import ConfigService, FileProcessorService
from infrastructure.adapters import LocalFileSystemAdapter, ConfigFileAdapter
from infrastructure.repositories import FileRepository
from presentation import CLI, ConsoleFormatter, JsonFormatter


def main():
    try:
        file_system = LocalFileSystemAdapter()
        config_adapter = ConfigFileAdapter(file_system)
        file_repository = FileRepository(file_system)
        text_service = TextProcessingService()

        config_service = ConfigService(config_adapter, file_system)
        file_processor = FileProcessorService(file_system, text_service)

        config_file, config_id = CLI.parse_args()

        configs = config_service.read_configs(config_file)

        if config_id is None:
            formatted_configs = ConsoleFormatter.format_configs(configs, config_file)
            print(formatted_configs)
            sys.exit(0)

        selected_config = config_service.get_config_by_id(configs, config_id)
        if not selected_config:
            error_msg = ConsoleFormatter.format_error(
                f"Конфигурация с ID {config_id} не найдена в файле {config_file}"
            )
            print(error_msg)
            sys.exit(1)

        file_paths = config_service.get_files_from_config(selected_config)

        files_content = file_repository.get_multiple_files(file_paths)

        processed_data = file_processor.process_files(
            files_content, selected_config.action
        )

        result = file_processor.create_processing_result(
            config_file, selected_config, processed_data
        )

        output_path = JsonFormatter.save_to_file(result)
        print(f"Результат сохранен в: {output_path}")

    except Exception as e:
        print(ConsoleFormatter.format_error(str(e)))
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
