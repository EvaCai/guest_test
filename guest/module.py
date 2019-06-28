# coding=utf-8


class Calculator():
    """实现两位数的加、减、乘、除"""

    def __init__(self, a, b):
        self.a = a
        self.b = b


    # 加法
    def add(self):
        return self.a + self.b

    # 减法
    def sub(self):
        return self.a - self.b

    # 乘法
    def mul(self):
        return self.a * self.b

    # 除法
    def div(self):
        return self.a / self.b