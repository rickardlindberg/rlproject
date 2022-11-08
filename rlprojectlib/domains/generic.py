class Coordinate:

    def move(self, dy):
        return self._replace(y=self.y+dy)
