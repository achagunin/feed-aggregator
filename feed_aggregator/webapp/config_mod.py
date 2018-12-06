from configparser import ConfigParser


def read_config(filename='./config.ini', section='') -> dict:
    """ Считывает конфигурацию базы данных из файла config.ini и записывет её в словарь
    :param filename: имя файла конфигурации и путь к нему
    :param section: секция в файле конфигурации
    :return: словарь с параметрами
    """

    try:
        with open(filename, 'r') as config:
            parser = ConfigParser()
            parser.read_file(config)

            try:
                configuration = {}
                if parser.has_section(section):
                    items = parser.items(section)
                    for item in items:
                        configuration[item[0]] = item[1]
                else:
                    raise Exception('{} not found in the {} file'.format(section, filename))

                return configuration

            except Exception as err:
                print('Not found section in file:', str(err))

    except FileNotFoundError as err:
        print('The data file is missing.', str(err))
    except PermissionError as err:
        print('This is not allowed.', str(err))
    except Exception as err:
        print('Some other error occurred:', str(err))

