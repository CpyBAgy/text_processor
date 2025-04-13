from unittest.mock import Mock
from application.ports import FileSystemPort
from infrastructure.adapters import ConfigFileAdapter
from domain import Config


class TestConfigFileAdapter:
    """Тесты для адаптера конфигурационного файла."""

    def setup_method(self):
        """Настройка перед каждым тестом."""
        self.file_system_port = Mock(spec=FileSystemPort)
        self.adapter = ConfigFileAdapter(self.file_system_port)

    def test_read_configs_valid_file(self):
        """Тест чтения конфигураций из валидного файла."""
        config_content = [
            "#1",
            "#mode: dir",
            "#path: ./test_files",
            "#action: string",
            "",
            "#2",
            "#mode: files",
            "#path: ./file1.txt, ./file2.txt",
            "#action: count",
        ]

        self.file_system_port.read_file.return_value = config_content

        configs = self.adapter.read_configs("config.txt")

        self.file_system_port.read_file.assert_called_once_with("config.txt")
        assert len(configs) == 2

        assert configs[0].id == "1"
        assert configs[0].mode == "dir"
        assert configs[0].path == "./test_files"
        assert configs[0].action == "string"

        assert configs[1].id == "2"
        assert configs[1].mode == "files"
        assert configs[1].path == "./file1.txt, ./file2.txt"
        assert configs[1].action == "count"

    def test_read_configs_invalid_format(self):
        """Тест обработки файла с неверным форматом."""
        config_content = [
            "Invalid format",
            "No ID here",
            "mode: dir",
            "path: ./test_files",
        ]

        self.file_system_port.read_file.return_value = config_content

        configs = self.adapter.read_configs("config.txt")

        assert len(configs) == 0

    def test_read_configs_missing_required_fields(self):
        """Тест обработки конфигурации с отсутствующими обязательными полями."""
        config_content = ["#1", "#mode: dir", "# No path here", "#action: string"]

        self.file_system_port.read_file.return_value = config_content

        configs = self.adapter.read_configs("config.txt")

        assert len(configs) == 0

    def test_get_config_by_id_found(self):
        """Тест поиска конфигурации по ID (успешный случай)."""
        configs = [
            Config(id="1", mode="dir", path="./test1"),
            Config(
                id="2", mode="files", path="./file1.txt, ./file2.txt", action="count"
            ),
        ]

        config = self.adapter.get_config_by_id(configs, "2")

        assert config is not None
        assert config.id == "2"
        assert config.mode == "files"
        assert config.path == "./file1.txt, ./file2.txt"
        assert config.action == "count"

    def test_get_config_by_id_not_found(self):
        """Тест поиска конфигурации по ID (неудачный случай)."""
        configs = [
            Config(id="1", mode="dir", path="./test1"),
            Config(
                id="2", mode="files", path="./file1.txt, ./file2.txt", action="count"
            ),
        ]

        config = self.adapter.get_config_by_id(configs, "3")

        assert config is None
