class Coordinate:

    def move(self, dx=0, dy=0):
        return self._replace(x=self.x+dx, y=self.y+dy)

class ImmutableList(tuple):

    def add(self, item):
        return ImmutableList(self+(item,))

    def map(self, fn):
        return ImmutableList(fn(x) for x in self)

    def filter(self, fn):
        return ImmutableList(x for x in self if fn(x))

    def print(self):
        for item in self:
            print(item)

class Selections(ImmutableList):

    def __repr__(self):
        return f"Selections({', '.join(repr(x) for x in self)})"
