from domain import Config, ProcessingResult
from presentation import ConsoleFormatter, JsonFormatter


class TestConsoleFormatter:
    """Тесты для форматирования вывода в консоль."""

    def test_format_configs(self):
        """Тест форматирования списка конфигураций."""
        configs = [
            Config(id="1", mode="dir", path="/path/to/directory", action="string"),
            Config(
                id="2",
                mode="files",
                path="/path/to/file1.txt,/path/to/file2.txt",
                action="count",
            ),
            Config(
                id="3",
                mode="dir",
                path="/very/long/path/that/should/be/truncated/because/it/is/longer/than/forty/characters",
                action="replace",
            ),
        ]
        config_file = "test_config.txt"

        result = ConsoleFormatter.format_configs(configs, config_file)

        assert config_file in result
        assert "ID" in result
        assert "Режим" in result
        assert "Действие" in result
        assert "Путь" in result
        assert "1" in result and "dir" in result and "string" in result
        assert "2" in result and "files" in result and "count" in result
        assert "3" in result and "dir" in result and "replace" in result
        assert "..." in result

    def test_format_error(self):
        """Тест форматирования сообщения об ошибке."""
        error_message = "Тестовое сообщение об ошибке"

        result = ConsoleFormatter.format_error(error_message)

        assert "Ошибка: " in result
        assert error_message in result


class TestJsonFormatter:
    """Тесты для форматирования данных в JSON."""

    def test_format_result(self, tmp_path):
        """Тест преобразования результата обработки в JSON строку."""
        result = ProcessingResult(
            config_file="/path/to/config.txt",
            config_id="1",
            config_data={"mode": "dir", "path": "./test"},
            out={"1": {"1": "data1", "2": "data2"}},
        )

        json_str = JsonFormatter.format_result(result)

        assert '"configFile": "/path/to/config.txt"' in json_str
        assert '"configurationID": "1"' in json_str
        assert '"mode": "dir"' in json_str
        assert '"path": "./test"' in json_str
        assert '"out"' in json_str
        assert '"1"' in json_str and '"2"' in json_str
        assert '"data1"' in json_str and '"data2"' in json_str

    def test_save_to_file(self, tmp_path):
        """Тест сохранения результата в JSON файл."""
        result = ProcessingResult(
            config_file="/path/to/config.txt",
            config_id="1",
            config_data={"mode": "dir", "path": "./test"},
            out={"1": {"1": "data1", "2": "data2"}},
        )
        test_file = tmp_path / "test_result.json"

        file_path = JsonFormatter.save_to_file(result, str(test_file))

        assert file_path == str(test_file)
        assert test_file.exists()

        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert '"configFile": "/path/to/config.txt"' in content
            assert '"configurationID": "1"' in content
            assert '"out"' in content

    def test_save_to_file_default_path(self, tmp_path, monkeypatch):
        """Тест сохранения результата в файл со стандартным именем."""
        monkeypatch.chdir(tmp_path)

        result = ProcessingResult(
            config_file="/path/to/config.txt",
            config_id="1",
            config_data={"mode": "dir", "path": "./test"},
            out={"1": {"1": "data1", "2": "data2"}},
        )

        file_path = JsonFormatter.save_to_file(result)

        expected_path = str(tmp_path / f"results/result_config_{result.config_id}.json")
        assert file_path in expected_path
        assert (tmp_path / f"results/result_config_{result.config_id}.json").exists()
