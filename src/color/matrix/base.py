from typing import Any


class Matrix:
    def __repr__(self):
        return f"{self.__class__.__name__} = {self.data}"

    def __rich_repr__(self):
        yield self.__class__.__name__
        yield "data", self.data

    def __eq__(self, other: Any):
        if isinstance(other, self.__class__):
            return self.data == other.data
        else:
            raise TypeError(
                f"Unable to compare {self.__class__.__name__} to {type(other)}"
            )
