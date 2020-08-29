import abc

from errors import ParamException
from instrument import utils


class A(metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    @abc.abstractmethod
    def call(self):
        pass


class B(A):

    def __init__(self):
        pass

    def call(self, s):
        def ma():
            print('a')

        def mb():
            print('b')
        switch = {'a': ma, 'b': mb}
        return switch.get(s, lambda: utils.raiser(ParamException()))


# a = A()
b = B()
# print(a.__class__.__name__)
b.call('c')()

