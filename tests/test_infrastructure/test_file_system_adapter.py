import os
from unittest.mock import patch, mock_open
from infrastructure.adapters import LocalFileSystemAdapter


class TestLocalFileSystemAdapter:
    """Тесты для адаптера файловой системы."""

    def setup_method(self):
        """Настройка перед каждым тестом."""
        self.adapter = LocalFileSystemAdapter()

    def test_file_exists_true(self):
        """Тест проверки существования файла (файл существует)."""
        with patch("os.path.isfile", return_value=True):
            assert self.adapter.file_exists("existing_file.txt") is True

    def test_file_exists_false(self):
        """Тест проверки существования файла (файл не существует)."""
        with patch("os.path.isfile", return_value=False):
            assert self.adapter.file_exists("non_existing_file.txt") is False

    def test_dir_exists_true(self):
        """Тест проверки существования директории (директория существует)."""
        with patch("os.path.isdir", return_value=True):
            assert self.adapter.dir_exists("existing_dir") is True

    def test_dir_exists_false(self):
        """Тест проверки существования директории (директория не существует)."""
        with patch("os.path.isdir", return_value=False):
            assert self.adapter.dir_exists("non_existing_dir") is False

    def test_list_files(self):
        """Тест получения списка файлов в директории."""
        dir_content = ["file1.txt", "file2.txt", "subdir"]
        expected_files = [
            os.path.join("test_dir", "file1.txt"),
            os.path.join("test_dir", "file2.txt"),
        ]

        with patch("os.listdir", return_value=dir_content), patch(
            "os.path.isfile", side_effect=lambda path: not path.endswith("subdir")
        ):
            files = self.adapter.list_files("test_dir")

            assert files == expected_files

    def test_read_file(self):
        """Тест чтения содержимого файла."""
        file_content = "line1\nline2\nline3\n"
        expected_lines = ["line1", "line2", "line3"]

        with patch("builtins.open", mock_open(read_data=file_content)):
            lines = self.adapter.read_file("test.txt")

            assert lines == expected_lines

    def test_write_file(self):
        """Тест записи содержимого в файл."""
        file_content = "Test content"
        file_path = "test.txt"

        with patch("builtins.open", mock_open()) as mock_file:
            self.adapter.write_file(file_path, file_content)

            mock_file.assert_called_once_with(file_path, "w", encoding="utf-8")
            mock_file().write.assert_called_once_with(file_content)

    def test_get_absolute_path(self):
        """Тест получения абсолютного пути."""
        with patch("os.path.abspath", return_value="/absolute/path/to/file.txt"):
            assert (
                self.adapter.get_absolute_path("file.txt")
                == "/absolute/path/to/file.txt"
            )
