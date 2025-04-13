from domain import Config, FileContent, ProcessingResult


class TestConfig:
    """Тесты для модели Config."""

    def test_config_creation(self):
        """Тест создания объекта Config."""
        config = Config(id="1", mode="dir", path="./test", action="string")

        assert config.id == "1"
        assert config.mode == "dir"
        assert config.path == "./test"
        assert config.action == "string"

    def test_config_default_action(self):
        """Тест значения по умолчанию для action."""
        config = Config(id="1", mode="dir", path="./test")

        assert config.action == "string"


class TestFileContent:
    """Тесты для модели FileContent."""

    def test_file_content_creation(self):
        """Тест создания объекта FileContent."""
        file_content = FileContent(file_path="test.txt", lines=["line1", "line2"])

        assert file_content.file_path == "test.txt"
        assert file_content.lines == ["line1", "line2"]


class TestProcessingResult:
    """Тесты для модели ProcessingResult."""

    def test_processing_result_creation(self):
        """Тест создания объекта ProcessingResult."""
        config_data = {"mode": "dir", "path": "./test"}
        out_data = {"1": {"1": "line1", "2": "line2"}}

        result = ProcessingResult(
            config_file="config.txt",
            config_id="1",
            config_data=config_data,
            out=out_data,
        )

        assert result.config_file == "config.txt"
        assert result.config_id == "1"
        assert result.config_data == config_data
        assert result.out == out_data
