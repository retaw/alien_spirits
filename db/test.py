class Base:
    def __init__(self):
        self.a = 1

    def printData(self):
        print self.a


class Derived(Base):
    def __init__(self):
        Base.__init__(self)
        self.b = 2

d = Derived()

print d.a
print d.b
d.printData()
