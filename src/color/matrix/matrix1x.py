from collections.abc import Iterable
from numbers import Number
from typing import Any

from typing_extensions import Self

from .base import Matrix
from .matrix2x import Matrix2x1
from .matrix3x import Matrix3x1


class Matrix1x2(Matrix):
    size = (1, 2)

    def __init__(
        self,
        data: Iterable[Number] | None = None,
    ):
        if data is None:
            self.data = (0.0, 0.0)
        else:
            self.data = tuple(data[:2])

    def __getitem__(self, idx):
        return self.data[idx]

    def __mul__(self, other: Any) -> Self | Number:
        if isinstance(other, Number):
            data = (self.data[0] * other, self.data[1] * other)
            return Matrix1x2.from_iterable(data)
        elif isinstance(other, Matrix2x1):
            d = self.data
            return d[0] * other[0] + d[1] * other[1]
        else:
            raise TypeError(f"Unable to multiply matrix by type {type(other)}")

    # def __eq__(self, other: Any):
    #     if isinstance(other, Matrix1x2):
    #         return self.data == other.data
    #     else:
    #         raise TypeError(
    #             f"Unable to compare {self.__class__.__name__} to {type(other)}"
    #         )

    @classmethod
    def from_iterable(cls, data: Iterable[Number]):
        return cls(data)


class Matrix1x3(Matrix):
    size = (1, 3)

    def __init__(
        self,
        data: Iterable[Number] | None = None,
    ):
        if data is None:
            self.data = (0.0, 0.0, 0.0)
        else:
            self.data = tuple(data[:3])

    def __getitem__(self, idx):
        return self.data[idx]

    def __mul__(self, other: Any) -> Self | Number:
        if isinstance(other, Number):
            data = (self.data[0] * other, self.data[1] * other, self.data[2] * other)
            return Matrix1x3.from_iterable(data)
        elif isinstance(other, Matrix3x1):
            value = (
                self.data[0] * other.data[0]
                + self.data[1] * other.data[1]
                + self.data[2] * other.data[2]
            )
            return value
        else:
            raise TypeError(f"Unable to multiply matrix by type {type(other)}")

    @classmethod
    def from_iterable(cls, data: Iterable[Number]):
        return cls(data)
