class MetaDocument:

    def with_meta(self, **kwargs):
        return self.replace_meta(self.meta._replace(**kwargs))

    def replace_meta(self, meta):
        return self._replace(meta=meta)

    def get_edited_document(self):
        return self.meta.string

class Coordinate:

    def move(self, dx=0, dy=0):
        return self._replace(x=self.x+dx, y=self.y+dy)

class ImmutableList(tuple):

    def add(self, item):
        return self.merge((item,))

    def merge(self, items):
        return self.__class__(self+items)

    def map(self, fn):
        return self.__class__(fn(x) for x in self)

    def filter(self, fn):
        return self.__class__(x for x in self if fn(x))

    def print(self):
        for item in self:
            print(item)

class Selections(ImmutableList):

    def __repr__(self):
        return f"Selections({', '.join(repr(x) for x in self)})"
