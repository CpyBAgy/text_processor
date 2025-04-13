from unittest.mock import Mock
from domain import FileContent, Config, TextProcessingService
from application.ports import FileSystemPort
from application.services import FileProcessorService


class TestFileProcessorService:
    """Тесты для сервиса обработки файлов."""

    def setup_method(self):
        """Настройка перед каждым тестом."""
        self.file_system_port = Mock(spec=FileSystemPort)
        self.text_service = Mock(spec=TextProcessingService)
        self.service = FileProcessorService(self.file_system_port, self.text_service)

    def test_read_files(self):
        """Тест чтения содержимого файлов."""
        file_paths = ["file1.txt", "file2.txt"]
        file1_lines = ["file1_line1", "file1_line2"]
        file2_lines = ["file2_line1"]

        self.file_system_port.read_file.side_effect = [file1_lines, file2_lines]

        results = self.service.read_files(file_paths)

        assert len(results) == 2
        assert results[0].file_path == file_paths[0]
        assert results[0].lines == file1_lines
        assert results[1].file_path == file_paths[1]
        assert results[1].lines == file2_lines
        assert self.file_system_port.read_file.call_count == 2

    def test_process_files_string_action(self):
        """Тест обработки файлов с действием 'string'."""
        files_content = [
            FileContent(file_path="file1.txt", lines=["file1_line1", "file1_line2"]),
            FileContent(file_path="file2.txt", lines=["file2_line1"]),
        ]

        result = self.service.process_files(files_content, "string")

        assert "1" in result
        assert "2" in result
        assert "1" in result["1"]
        assert "2" in result["1"]
        assert result["1"]["1"] == "file1_line1"
        assert result["1"]["2"] == "file2_line1"
        assert result["2"]["1"] == "file1_line2"
        assert result["2"]["2"] == ""

    def test_process_files_count_action(self):
        """Тест обработки файлов с действием 'count'."""
        files_content = [
            FileContent(file_path="file1.txt", lines=["one two three", "four five"]),
            FileContent(file_path="file2.txt", lines=["six seven eight nine"]),
        ]

        self.text_service.count_words.side_effect = lambda text: len(text.split())

        result = self.service.process_files(files_content, "count")

        assert result["1"]["1"] == 3
        assert result["1"]["2"] == 4
        assert result["2"]["1"] == 2
        assert result["2"]["2"] == 0

    def test_process_files_replace_action(self):
        """Тест обработки файлов с действием 'replace'."""
        files_content = [
            FileContent(file_path="file1.txt", lines=["abc", "def"]),
            FileContent(file_path="file2.txt", lines=["ghi"]),
        ]

        self.text_service.replace_letters.side_effect = (
            lambda text, file_num: f"replaced_{file_num}_{text}"
        )

        result = self.service.process_files(files_content, "replace")

        assert result["1"]["1"] == "replaced_1_abc"
        assert result["1"]["2"] == "replaced_2_ghi"
        assert result["2"]["1"] == "replaced_1_def"
        assert result["2"]["2"] == ""

    def test_create_processing_result(self):
        """Тест создания объекта с результатами обработки."""
        config_file = "config.txt"
        config = Config(id="1", mode="dir", path="./test")
        processed_data = {"1": {"1": "data1", "2": "data2"}}
        abs_path = "/absolute/path/to/config.txt"

        self.file_system_port.get_absolute_path.return_value = abs_path

        result = self.service.create_processing_result(
            config_file, config, processed_data
        )

        self.file_system_port.get_absolute_path.assert_called_once_with(config_file)
        assert result.config_file == abs_path
        assert result.config_id == config.id
        assert result.config_data == {"mode": config.mode, "path": config.path}
        assert result.out == processed_data
