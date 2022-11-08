from collections import namedtuple

from rlprojectlib.domains.string import String

class StringToLines(
    namedtuple("StringToLines", "string lines")
):

    @staticmethod
    def project(string):
        """
        >>> string = String.from_string(string="one\\ntwo")
        >>> print_namedtuples(StringToLines.project(string).lines)
        String(string='one', selections=Selections(Selection(start=0, length=0)))
        String(string='two', selections=Selections(Selection(start=0, length=0)))
        """
        return StringToLines(
            string=string,
            lines=tuple(
                String(x, string.selections)
                for x in string.string.splitlines()
            )
        )

    def keyboard_event(self, event):
        return StringToLines.project(self.string.keyboard_event(event))

def print_namedtuples(namedtuples):
    print("\n".join(repr(x) for x in namedtuples))
