#!/bin/bash

mkdir -p test_files

cat > test_files/file1.txt << EOF
Это первая строка файла 1.
Вторая строка содержит слова abc для проверки замены.
В третьей строке пять слов всего.
А здесь aaa bbb ccc проверка.
EOF

cat > test_files/file2.txt << EOF
Первая строка второго файла.
Эта строка имеет семь слов в ней.
Третья строка вторая abc проверка замены.
EOF

cat > test_files/file3.txt << EOF
Строка 1 файла 3.
В этой строке abc много разных букв.
Три слова тут.
Четвертая строка с abcdef проверкой.
Пятая строка.
EOF

cat > config.txt << EOF
#1
#mode: dir
#path: ./test_files
#action: string

#2
#mode: files
#path: ./test_files/file1.txt, ./test_files/file2.txt
#action: count

#3
#mode: files
#path: ./test_files/file1.txt, ./test_files/file3.txt
#action: replace

#4
#mode: dir
#path: ./test_files
#action: count

#5
#mode: files
#path: ./test_files/file2.txt, ./test_files/file3.txt
EOF

echo "Тестовое окружение создано!"
echo "Для запуска программы используйте команду:"
echo "python script.py config.txt <номер_конфигурации>"
