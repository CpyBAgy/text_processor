import sys
from unittest.mock import patch, mock_open, Mock
from domain import ProcessingResult
from presentation import CLI


class TestCLI:
    """Тесты для интерфейса командной строки."""

    def test_parse_args_help(self):
        """Тест разбора аргументов при вызове справки."""
        original_argv = sys.argv
        original_exit = sys.exit

        try:
            test_cases = [
                ["script.py", "help"],
                ["script.py", "-h"],
                ["script.py", "--help"],
                ["script.py", "/?"],
            ]

            for args in test_cases:
                sys.argv = args
                sys.exit = lambda code: None

                with patch("builtins.print") as mock_print:
                    CLI.parse_args()
                    mock_print.assert_called()
        finally:
            sys.argv = original_argv
            sys.exit = original_exit

    def test_parse_args_with_config_only(self):
        """Тест разбора аргументов при указании только конфигурационного файла."""
        original_argv = sys.argv

        try:
            sys.argv = ["script.py", "config.txt"]

            config_file, config_id = CLI.parse_args()

            assert config_file == "config.txt"
            assert config_id is None
        finally:
            sys.argv = original_argv

    def test_parse_args_with_config_and_id(self):
        """Тест разбора аргументов при указании файла и ID конфигурации."""
        original_argv = sys.argv

        try:
            sys.argv = ["script.py", "config.txt", "1"]

            config_file, config_id = CLI.parse_args()

            assert config_file == "config.txt"
            assert config_id == "1"
        finally:
            sys.argv = original_argv

    def test_parse_args_invalid(self):
        """Тест разбора неверных аргументов."""
        original_argv = sys.argv
        original_exit = sys.exit

        try:
            sys.argv = ["script.py", "file1.txt", "file2.txt", "extra_arg"]
            sys.exit = lambda code: None

            with patch("builtins.print") as mock_print:
                CLI.parse_args()
                mock_print.assert_called_with(
                    "Неверные аргументы\nВоспользуйтесь командой 'python script.py' для справки"
                )
        finally:
            sys.argv = original_argv
            sys.exit = original_exit

    def test_show_help(self):
        """Тест вывода справочной информации."""
        with patch("builtins.print") as mock_print:
            CLI.show_help()
            mock_print.assert_called()
            args, kwargs = mock_print.call_args
            help_text = args[0]
            assert "ИСПОЛЬЗОВАНИЕ:" in help_text
            assert "АРГУМЕНТЫ:" in help_text
            assert "ФОРМАТЫ КОНФИГУРАЦИИ:" in help_text
            assert "ПРИМЕРЫ:" in help_text

    def test_display_configs(self):
        """Тест вывода списка конфигураций."""
        original_argv = sys.argv

        try:
            sys.argv = ["script.py", "config.txt"]

            configs = [
                Mock(id="1", mode="dir", path="/path/to/directory", action="string"),
                Mock(
                    id="2",
                    mode="files",
                    path="/long/path/that/should/be/truncated/because/it/is/longer/than/forty/characters",
                    action="count",
                ),
            ]

            with patch("builtins.print") as mock_print:
                CLI.display_configs(configs)
                mock_print.assert_called()
                assert mock_print.call_count >= 5
        finally:
            sys.argv = original_argv

    def test_save_result(self):
        """Тест сохранения результата."""
        result = ProcessingResult(
            config_file="/path/to/config.txt",
            config_id="1",
            config_data={"mode": "dir", "path": "./test"},
            out={"1": {"1": "data1", "2": "data2"}},
        )

        m = mock_open()
        with patch("builtins.open", m):
            with patch("builtins.print") as mock_print:
                with patch("json.dump") as mock_json_dump:
                    CLI.save_result(result)

                    m.assert_called_once_with(
                        f"results/result_config_{result.config_id}.json",
                        "w",
                        encoding="utf-8",
                    )
                    mock_json_dump.assert_called_once()
                    mock_print.assert_called_once()
