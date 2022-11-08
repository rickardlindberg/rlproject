class Coordinate:

    def move(self, dy):
        return self._replace(y=self.y+dy)

class Selections(tuple):

    def __repr__(self):
        return f"Selections({', '.join(repr(x) for x in self)})"
