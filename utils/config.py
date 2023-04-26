from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    """Функция для получения данных из указанного файла"""
    # создаем объект-парасер
    parser = ConfigParser()
    # считываем информацию из объекта-парсера
    parser.read(filename)
    # создаем пустой словарь для дальнешего его наполнения
    db = dict()
    # если в объекте-парсере имеется секция с указанным названием, то вытащить из нее информацию, в противном случае – поднять ошибку
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} is not found in the {1} file.'.format(section, filename))
    return db