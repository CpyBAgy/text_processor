from unittest.mock import Mock
from application.ports import FileSystemPort
from infrastructure.repositories import FileRepository


class TestFileRepository:
    """Тесты для репозитория файлов."""

    def setup_method(self):
        """Настройка перед каждым тестом."""
        self.file_system = Mock(spec=FileSystemPort)
        self.repository = FileRepository(self.file_system)

    def test_get_file_content_without_cache(self):
        """Тест получения содержимого файла без использования кэша."""
        file_path = "test.txt"
        file_lines = ["line1", "line2"]

        self.file_system.read_file.return_value = file_lines

        result = self.repository.get_file_content(file_path, use_cache=False)

        self.file_system.read_file.assert_called_once_with(file_path)
        assert result.file_path == file_path
        assert result.lines == file_lines

    def test_get_file_content_with_cache(self):
        """Тест получения содержимого файла с использованием кэша."""
        file_path = "test.txt"
        file_lines = ["line1", "line2"]

        self.file_system.read_file.return_value = file_lines

        result1 = self.repository.get_file_content(file_path, use_cache=True)

        self.file_system.read_file.reset_mock()

        result2 = self.repository.get_file_content(file_path, use_cache=True)

        self.file_system.read_file.assert_not_called()
        assert result1.file_path == result2.file_path
        assert result1.lines == result2.lines

    def test_get_multiple_files(self):
        """Тест получения содержимого нескольких файлов."""
        file_paths = ["test1.txt", "test2.txt"]
        file_lines1 = ["file1_line1", "file1_line2"]
        file_lines2 = ["file2_line1", "file2_line2"]

        self.file_system.read_file.side_effect = [file_lines1, file_lines2]

        results = self.repository.get_multiple_files(file_paths)

        assert len(results) == 2
        assert self.file_system.read_file.call_count == 2
        assert results[0].file_path == file_paths[0]
        assert results[0].lines == file_lines1
        assert results[1].file_path == file_paths[1]
        assert results[1].lines == file_lines2

    def test_clear_cache(self):
        """Тест очистки кэша."""
        file_path = "test.txt"
        file_lines = ["line1", "line2"]

        self.file_system.read_file.return_value = file_lines

        self.repository.get_file_content(file_path)

        assert file_path in self.repository._cache

        self.repository.clear_cache()

        assert not self.repository._cache
