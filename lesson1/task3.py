"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
Важно: решение должно быть универсальным, т.е. не зависеть от того, какие конкретно слова мы исследуем.
"""

def convert_to_bytes(words):
    if len(words) > 0:
        for word in words:
            word_length = len(word)
            b = bytes(word, 'utf-8')
            if word_length == len(b):
                print(type(b))
                print(b)
                print('-' * 80)
            else:
                b = str(b, encoding='utf-8')
                print(f"Слово '{b}' не входит в ASCII формат")
                print('-' * 80)

WORDS_LIST = ["attribute", "класс", "функция", "type"]

convert_to_bytes(WORDS_LIST)
