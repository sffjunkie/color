from collections.abc import Iterable
from numbers import Number
from typing import Any

from typing_extensions import Self

from .base import Matrix


class Matrix2x1(Matrix):
    size = (2, 1)

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
            return Matrix2x1.from_iterable(data)
        else:
            raise TypeError(f"Unable to multiply matrix by type {type(other)}")

    @classmethod
    def from_iterable(cls, data: Iterable[Number]):
        return cls(data)


class Matrix2x2(Matrix):
    size = (2, 2)

    def __init__(
        self,
        data: Iterable[Number] | Iterable[Iterable[Number]] | None = None,
    ):
        if data is None:
            self.data = ((1.0, 0.0), (0.0, 1.0))
        elif isinstance(data[0], Iterable):
            self.data = (tuple(data[0]), tuple(data[1]))
        else:
            self.data = (tuple(data[:2]), tuple(data[2:4]))

    def __getitem__(self, idx):
        return self.data[idx]

    def __mul__(self, other: Any) -> Self:
        if isinstance(other, Matrix2x2):
            return matrix_multiply_2x2(self, other)
        elif isinstance(other, Matrix2x1):
            return matrix_multiply_2x1(self, other)
        elif isinstance(other, Number):
            d = self.data
            data = (
                d[0][0] * other,
                d[0][1] * other,
                d[1][0] * other,
                d[1][1] * other,
            )
            return Matrix2x2.from_iterable(data)

    @classmethod
    def from_iterable(
        cls,
        data: Iterable[Number] | Iterable[Iterable[Number]],
    ):
        return cls(data)

    @classmethod
    def identity(cls):
        data = ((1.0, 0.0), (0.0, 1.0))
        return cls.from_iterable(data)

    def transpose(self) -> Self:
        d = self.data
        data = (
            (d[0][0], d[1][0]),
            (d[0][1], d[1][1]),
        )
        return Matrix2x2.from_iterable(data)

    def determinant(self) -> Number:
        return (self.data[0][0] * self.data[1][1]) - (self.data[0][1] * self.data[1][0])

    def inverse(self) -> Self:
        det = self.determinant()
        if det == 0:
            raise ValueError("Determinant is 0: Unable to calculate inverse")

        d = self.data
        data = (
            (d[1][1] / det, -d[0][1] / det),
            (-d[1][0] / det, d[0][0] / det),
        )
        m = Matrix2x2.from_iterable(data)
        return m


def matrix_multiply_2x1(a: Matrix2x2, b: Matrix2x1) -> Matrix2x1:
    return Matrix2x1.from_iterable(
        (a[0][0] * b[0] + a[0][1] * b[1], a[1][0] * b[0] + a[1][1] * b[1])
    )


def matrix_multiply_2x2(a: Matrix2x2, b: Matrix2x2) -> Matrix2x2:
    elems = (
        (a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]),
        (a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]),
    )
    return Matrix2x2.from_iterable(elems)
