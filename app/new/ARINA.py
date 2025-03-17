from string import ascii_letters


class Person:
    rys_letters = "абвгдеёжзийклмнопрстуфхчцшщьъэыюя-"
    RYS_letters = rys_letters.upper()

    def __init__(self, fio, old, weight, password):
        self.varify_fio(fio)
        self.__fio = fio.split()
        self.old = old
        self.weight = weight
        self.password = password

    @classmethod
    def varify_fio(cls, fio):
        if type(fio) != str:
            raise TypeError("Данные должны быть в виде строки")

        s = fio.split()
        if len(s) != 3:
            raise TypeError("Некорректный ввод данных")
        letters = ascii_letters + cls.rys_letters + cls.RYS_letters
        for x in s:
            if len(x) < 1:
                raise TypeError("Слова должны содержать минимум одну букву")
            if len(x.strip(letters)) != 0:
                raise TypeError("Данные должны содержать только буквенные символы и дефис")

    @classmethod
    def varify_old(cls, old):
        if type(old) is not int or 120 <= old <= 14:
            raise TypeError("Возраст должен быть числом в промежутке [14; 120]")

    @classmethod
    def varify_weight(cls, weight):
        if type(weight) != float or weight < 20:
            raise TypeError("Вес должен быть вещественным числом, больше 20")

    @classmethod
    def varify_psw(cls, psw):
        if type(psw) != str:
            raise TypeError("Пароль должен быть строкой")
        f = psw.split()
        if len(f) != 2 or len(f[0]) != 4 or len(f[1]) != 6:
            raise TypeError("Некорректный ввод данных")
        for x in f:
            if not x.isdigit():
                raise TypeError("Серия и пароль должны содержать только числа")

    @property
    def fio(self):
        return self.__fio

    @property
    def old(self):
        return self.__old

    @old.setter
    def old(self, old):
        self.varify_old(old)
        self.__old = old

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, weight):
        self.varify_weight(weight)
        self.__weight = weight

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.varify_psw(password)
        self.__password = password


p = Person("Прим Август Метрофан", 18, 60.8, "2345 678901")
print(p.password)
p.old = 19
p.password = "2374 567890"
print(p.__dict__)