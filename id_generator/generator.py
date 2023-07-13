import random


class Generator:
    __CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789*-'

    def __init__(self):
        self.__ids = set()

    def get_id(self):
        return self.__ids.pop()

    @classmethod
    def __generate_id(cls):
        result = ''.join(random.choices(cls.__CHARS, k=8))
        return result

    def start_generate(self):
        for _ in range(10000):
            elem = self.__generate_id()
            self.__ids.add(elem)

