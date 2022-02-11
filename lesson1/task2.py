"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования
в последовательность кодов (не используя методы encode и decode) и определить тип,
содержимое и длину соответствующих переменных.
"""


def convert_to_bytes_eval(words):
    if len(words) > 0:
        for word in words:
            b = eval(f"b'{word}'")
            print(b)
            print(type(b))
            print('len: ', len(b))
            print('-' * 80)


if __name__ == '__main__':
    words_list = ["class", "function", "method"]
    convert_to_bytes_eval(words_list)
