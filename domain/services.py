class TextProcessingService:
    """Сервис для обработки текста."""

    @staticmethod
    def replace_letters(text: str, file_number: int) -> str:
        """Замена английских букв на числа."""
        result = ""
        for char in text:
            order = ord(char)
            if 65 <= order <= 90:  # Заглавные английские буквы
                result += str(order - 64 + file_number)
            elif 97 <= order <= 122:  # Строчные английские буквы
                result += str(order - 96 + file_number)
            else:
                result += char
        return result

    @staticmethod
    def count_words(text: str) -> int:
        """Подсчет количества слов в строке."""
        return len(text.split())
