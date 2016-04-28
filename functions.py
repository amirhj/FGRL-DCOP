class Functions1:

    def __init__(self, fg):
        self.fg = fg

    def v(self, var):
        return self.fg.getValue(var)

    def f1(self):
        return 3 * self.v("x1")**3

    def f2(self):
        return 4 * self.v("x1")**4 - self.v("x2")**2

    def f3(self):
        x3 = self.v("x3")
        return -1 * (x3**3 + x3)

    def f4(self):
        return self.v("x2")**4 + 1/self.v("x3")**2

    def f5(self):
        x3 = self.v("x3")
        return 3 * x3 + 1/x3
