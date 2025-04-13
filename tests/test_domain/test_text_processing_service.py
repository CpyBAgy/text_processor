from domain import TextProcessingService


class TestTextProcessingService:
    """Тесты для сервиса обработки текста."""

    def test_replace_letters(self):
        """Тест замены английских букв на числа."""
        service = TextProcessingService()

        assert service.replace_letters("ABC", 1) == "234"

        assert service.replace_letters("abc", 1) == "234"

        assert service.replace_letters("Abc", 2) == "345"

        assert service.replace_letters("A-1 Б", 1) == "2-1 Б"

        assert service.replace_letters("Hello, World!", 1) == "96131316, 241619135!"

    def test_count_words(self):
        """Тест подсчета слов в строке."""
        service = TextProcessingService()

        assert service.count_words("one two three") == 3

        assert service.count_words("") == 0

        assert service.count_words("   ") == 0

        assert service.count_words("hello, world! How are you?") == 5
