import abc


class A(metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    @abc.abstractmethod
    def call(self):
        pass


class B(A):

    def __init__(self):
        pass

    def call(self):
        print('call')


# a = A()
b = B()
# print(a.__class__.__name__)
print(B.__class__)

