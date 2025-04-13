from typing import Dict, List, Union
from domain import Config, FileContent, ProcessingResult
from domain import TextProcessingService
from application.ports import FileSystemPort


class FileProcessorService:
    """Сервис для обработки файлов."""

    def __init__(
        self, file_system_port: FileSystemPort, text_service: TextProcessingService
    ):
        self.file_system_port = file_system_port
        self.text_service = text_service

    def read_files(self, file_paths: List[str]) -> List[FileContent]:
        """Читает содержимое файлов."""
        result = []
        for file_path in file_paths:
            lines = self.file_system_port.read_file(file_path)
            result.append(FileContent(file_path=file_path, lines=lines))
        return result

    def process_files(
        self, files_content: List[FileContent], action: str
    ) -> Dict[str, Dict[str, Union[str, int]]]:
        """Обрабатывает файлы согласно указанному действию."""
        result = {}

        max_lines = (
            max(len(content.lines) for content in files_content) if files_content else 0
        )

        for line_num in range(1, max_lines + 1):
            line_result = {}

            for file_idx, file_content in enumerate(files_content):
                file_num = file_idx + 1

                action_map = {
                    "string": lambda line: line,
                    "count": lambda line: self.text_service.count_words(line),
                    "replace": lambda line: self.text_service.replace_letters(
                        line, file_num
                    ),
                }

                if line_num <= len(file_content.lines):
                    current_line = file_content.lines[line_num - 1]
                    line_result[str(file_num)] = action_map.get(
                        action, lambda line: ""
                    )(current_line)
                else:
                    line_result[str(file_num)] = 0 if action == "count" else ""

            result[str(line_num)] = line_result

        return result

    def create_processing_result(
        self,
        config_file: str,
        config: Config,
        processed_data: Dict[str, Dict[str, Union[str, int]]],
    ) -> ProcessingResult:
        """Создает объект с результатами обработки."""
        return ProcessingResult(
            config_file=self.file_system_port.get_absolute_path(config_file),
            config_id=config.id,
            config_data={"mode": config.mode, "path": config.path},
            out=processed_data,
        )
