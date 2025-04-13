import pytest
from unittest.mock import Mock
from domain import Config
from application.services import ConfigService
from application.ports import ConfigPort, FileSystemPort


class TestConfigService:
    """Тесты для сервиса конфигураций."""

    def setup_method(self):
        """Настройка перед каждым тестом."""
        self.config_port = Mock(spec=ConfigPort)
        self.file_system_port = Mock(spec=FileSystemPort)
        self.service = ConfigService(self.config_port, self.file_system_port)

    def test_read_configs_success(self):
        """Тест успешного чтения конфигураций."""
        config_path = "config.txt"
        configs = [Config(id="1", mode="dir", path="./test", action="string")]

        self.file_system_port.file_exists.return_value = True
        self.config_port.read_configs.return_value = configs

        result = self.service.read_configs(config_path)

        self.file_system_port.file_exists.assert_called_once_with(config_path)
        self.config_port.read_configs.assert_called_once_with(config_path)
        assert result == configs

    def test_read_configs_file_not_found(self):
        """Тест обработки ошибки при отсутствии файла конфигурации."""
        config_path = "non_existent.txt"

        self.file_system_port.file_exists.return_value = False

        with pytest.raises(FileNotFoundError) as exc_info:
            self.service.read_configs(config_path)

        assert f"Конфигурационный файл не найден: {config_path}" in str(exc_info.value)
        self.file_system_port.file_exists.assert_called_once_with(config_path)
        self.config_port.read_configs.assert_not_called()

    def test_get_config_by_id(self):
        """Тест получения конфигурации по ID."""
        configs = [
            Config(id="1", mode="dir", path="./test1", action="string"),
            Config(id="2", mode="files", path="./test2", action="count"),
        ]
        config_id = "2"
        expected_config = configs[1]

        self.config_port.get_config_by_id.return_value = expected_config

        result = self.service.get_config_by_id(configs, config_id)

        self.config_port.get_config_by_id.assert_called_once_with(configs, config_id)
        assert result == expected_config

    def test_get_files_from_config_dir_mode(self):
        """Тест получения файлов в режиме директории."""
        config = Config(id="1", mode="dir", path="./test", action="string")
        expected_files = ["./test/file1.txt", "./test/file2.txt"]

        self.file_system_port.dir_exists.return_value = True
        self.file_system_port.list_files.return_value = expected_files

        result = self.service.get_files_from_config(config)

        self.file_system_port.dir_exists.assert_called_once_with(config.path)
        self.file_system_port.list_files.assert_called_once_with(config.path)
        assert result == expected_files

    def test_get_files_from_config_dir_not_found(self):
        """Тест обработки ошибки при отсутствии директории."""
        config = Config(id="1", mode="dir", path="./non_existent", action="string")

        self.file_system_port.dir_exists.return_value = False

        with pytest.raises(FileNotFoundError) as exc_info:
            self.service.get_files_from_config(config)

        assert f"Директория не найдена: {config.path}" in str(exc_info.value)
        self.file_system_port.dir_exists.assert_called_once_with(config.path)
        self.file_system_port.list_files.assert_not_called()

    def test_get_files_from_config_files_mode(self):
        """Тест получения файлов в режиме списка файлов."""
        file_paths = "./test/file1.txt, ./test/file2.txt"
        expected_files = ["./test/file1.txt", "./test/file2.txt"]
        config = Config(id="1", mode="files", path=file_paths, action="string")

        self.file_system_port.file_exists.return_value = True

        result = self.service.get_files_from_config(config)

        assert self.file_system_port.file_exists.call_count == 2
        assert result == sorted(expected_files)

    def test_get_files_from_config_invalid_mode(self):
        """Тест обработки ошибки при неверном режиме."""
        config = Config(id="1", mode="invalid", path="./test", action="string")

        with pytest.raises(ValueError) as exc_info:
            self.service.get_files_from_config(config)

        assert f"Неподдерживаемый режим: {config.mode}" in str(exc_info.value)
