class Element:
    def __init__(self, y, x):
        self.x, self.y = x, y
        self.is_opened = False
    
    def __str__(self) :
        return "(y={}, x={})".format(self.y, self.x)

    def open(self):
        self.is_opened = True

class Nothing(Element):
    def __init__(self, y, x):
        super().__init__(y, x)
        self.cnt = 0

    def __str__(self) :
        return "NUM{} : ".format(self.cnt) + super().__str__()

    def icon(self):
        return str(self.cnt)
    
    def plus(self):
        self.cnt += 1

class Wall(Element):
    def __init__(self, y, x):
        super().__init__(y, x)

    def __str__(self) :
        return "Wall : " + super().__str__()
    
    def icon(self):
        return "X"

class Mine(Element):
    def __init__(self, y, x):
        super().__init__(y, x)

    def __str__(self) :
        return "Mine : " + super().__str__()
    
    def icon(self):
        return "M"

if __name__ == '__main__':
    element = Element(10, 20)
    empty = Empty(20, 30)
    wall = Wall(30, 40)
    print(element, empty, wall)