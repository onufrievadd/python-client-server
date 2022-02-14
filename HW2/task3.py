"""3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле
YAML-формата. Для этого: Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список,
второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом,
отсутствующим в кодировке ASCII (например, €); Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а также установить
возможность работы с юникодом: allow_unicode = True; Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными. """

import yaml


def data_to_yaml(first, second, third):
    data_yaml = {
        '1key': first,
        '2key': second,
        '3key': third,
    }

    with open('file.yaml', 'w', encoding='utf-8') as f_n:
        yaml.dump(data_yaml, f_n, default_flow_style=False, allow_unicode=True)

    with open('file.yaml', encoding='utf-8') as f_n:
        print(f_n.read())

    with open('file.yaml', encoding='utf-8') as f_n:
        f_n_content = yaml.load(f_n, Loader=yaml.SafeLoader)
        print(f'Данные совпадают? {data_yaml == f_n_content}')


if __name__ == '__main__':
    data_to_yaml([1, 'два', 'three'], 20, {'price1': '100€', 'price2': '200€', 'price3': '300€'})
