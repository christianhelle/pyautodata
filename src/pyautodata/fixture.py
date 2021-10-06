import datetime
import random
import uuid
from abc import abstractmethod


class Fixture:
    def __init__(self):
        pass

    @staticmethod
    def create(t):
        generator = TypeFactory.create(t)
        return generator.create()


class TypeDataGenerator:
    @abstractmethod
    def create(self):
        pass


class TypeFactory:
    @staticmethod
    def create(t) -> TypeDataGenerator:
        type_name = t.__name__
        if type_name == 'int':
            return IntegerGenerator()
        elif type_name == 'str':
            return StringGenerator()
        elif type_name == 'float':
            return FloatGenerator()
        elif type_name == 'datetime':
            return DatetimeGenerator()
        elif type_name == 'date':
            return DateGenerator()
        else:
            return ClassGenerator(t)


class ClassGenerator(TypeDataGenerator):
    def __init__(self, cls):
        self.instance = cls()

    def create(self):
        members = [
            attr for attr in dir(self.instance)
            if not callable(getattr(self.instance, attr)) and not attr.startswith("__")
        ]
        for member in members:
            t = type(getattr(self.instance, member))
            generator = TypeFactory.create(t)
            value = generator.create()
            setattr(self.instance, member, value)
        return self.instance


class IntegerGenerator(TypeDataGenerator):

    def create(self):
        return random.randint(0, 2147483647)


class StringGenerator(TypeDataGenerator):
    def create(self):
        return str(uuid.uuid4())


class FloatGenerator(TypeDataGenerator):
    def create(self):
        return random.uniform(0, 2147483647)


class DatetimeGenerator(TypeDataGenerator):
    def create(self):
        year = datetime.date.today().year
        return datetime.datetime(random.randint(year - 10, year + 10),
                                 random.randint(1, 12),
                                 random.randint(1, 28),
                                 random.randint(0, 23),
                                 random.randint(0, 59),
                                 random.randint(0, 59),
                                 random.randint(0, 999))


class DateGenerator(TypeDataGenerator):
    def create(self):
        year = datetime.date.today().year
        return datetime.datetime(random.randint(year - 10, year + 10),
                                 random.randint(1, 12),
                                 random.randint(1, 28))
