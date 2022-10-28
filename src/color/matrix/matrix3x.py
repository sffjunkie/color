from collections.abc import Iterable
from numbers import Number
from typing import Any

from typing_extensions import Self

from .base import Matrix
from .matrix2x import Matrix2x2


class Matrix3x1(Matrix):
    size = (3, 1)

    def __init__(self, data: Iterable[Number] | None = None):
        if data is None:
            self.data = (0.0, 0.0, 0.0)
        else:
            self.data = data[:3]

    def __getitem__(self, idx):
        return self.data[idx]

    def __mul__(self, other: Any):
        d = self.data
        if isinstance(other, Number):
            data = (d[0] * other, d[1] * other, d[2] * other)
            return Matrix3x1.from_iterable(data)
        else:
            raise TypeError(f"Unable to multiply matrix by type {type(other)}")

    @classmethod
    def from_iterable(cls, number_array: Iterable[Number]):
        return cls(tuple(number_array[:3]))


class Matrix3x3(Matrix):
    size = (3, 3)

    def __init__(self, data: Iterable[Iterable[Number]] | None = None):
        if data is None:
            self.data = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
        else:
            self.data = data

    def __getitem__(self, idx):
        return self.data[idx]

    def __mul__(self, other: Any) -> Self:
        if isinstance(other, Matrix3x3):
            return matrix_multiply_3x3(self, other)
        elif isinstance(other, Matrix3x1):
            return matrix_multiply_3x1(self, other)
        elif isinstance(other, Number):
            data = ()
            for row in range(3):
                row_data = ()
                for column in range(3):
                    value = self.data[row][column] * float(other)
                    row_data += (value,)

                data += row_data

            return Matrix3x3.from_iterable(data)
        else:
            raise TypeError(f"Unable to multiply matrix but type {type(other)}")

    @classmethod
    def from_iterable(cls, number_array: Iterable[Number]):
        if isinstance(number_array[0], Iterable):
            return cls(number_array)
        return cls(
            (
                tuple(number_array[:3]),
                tuple(number_array[3:6]),
                tuple(number_array[6:9]),
            )
        )

    @classmethod
    def identity(cls):
        data = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
        return cls.from_iterable(data)

    def transpose(self) -> Self:
        d = self.data
        data = (
            (d[0][0], d[1][0], d[2][0]),
            (d[0][1], d[1][1], d[2][1]),
            (d[0][2], d[1][2], d[2][2]),
        )

        return Matrix3x3.from_iterable(data)

    def determinant(self) -> Number:
        d = (self.data[0] * 2, self.data[1] * 2, self.data[2] * 2)
        return (
            d[0][0] * d[1][1] * d[2][2]
            + d[0][1] * d[1][2] * d[2][3]
            + d[0][2] * d[1][3] * d[2][4]
            - d[0][0] * d[1][2] * d[2][1]
            - d[0][1] * d[1][0] * d[2][2]
            - d[0][2] * d[1][1] * d[2][0]
        )

    def adjoint(self) -> Self:
        elements: Iterable[Iterable[Matrix2x2]] = [[], [], []]

        d = self.data
        all_rows = set(range(3))
        all_columns = set(range(3))
        for row in range(3):
            other_rows = tuple(all_rows - set((row,)))
            for column in range(3):
                other_columns = tuple(all_columns - set((column,)))
                tl = d[other_rows[0]][other_columns[0]]
                bl = d[other_rows[1]][other_columns[0]]
                tr = d[other_rows[0]][other_columns[1]]
                br = d[other_rows[1]][other_columns[1]]
                m = Matrix2x2.from_iterable([tl, tr, bl, br])
                elements[row].append(m)

        sign = 1
        dets = []
        for row in range(3):
            for column in range(3):
                dets.append(elements[row][column].determinant() * sign)
                sign *= -1

        m = Matrix3x3.from_iterable(dets)
        return m.transpose()

    def inverse(self) -> Self:
        det = self.determinant()
        if det == 0:
            raise ValueError("Determinant is 0: Unable to calculate inverse")

        adjoint = self.adjoint()
        return adjoint * (1 / det)


def matrix_multiply_3x1(a: Matrix3x3, b: Matrix3x1) -> Matrix3x1:
    elems = (
        b[0] * a[0][0] + b[1] * a[0][1] + b[2] * a[0][2],
        b[0] * a[1][0] + b[1] * a[1][1] + b[2] * a[1][2],
        b[0] * a[2][0] + b[1] * a[2][1] + b[2] * a[2][2],
    )
    return Matrix3x1.from_iterable(elems)


def matrix_multiply_3x3(a: Matrix3x3, b: Matrix3x3) -> Matrix3x3:
    """3x3 matrix multiplication

    http://www.ams.org/journals/bull/1976-82-01/S0002-9904-1976-13988-2/S0002-9904-1976-13988-2.pdf
    """
    terms = []

    terms.append(
        (a[0][0] + a[0][1] + a[0][2] - a[1][0] - a[1][1] - a[2][1] - a[2][2]) * b[1][1]
    )
    terms.append((a[0][0] - a[1][0]) * (-b[0][1] + b[1][1]))
    terms.append(
        a[1][1] * (-b[0][0] + b[0][1] + b[1][0] - b[1][1] - b[1][2] - b[2][0] + b[2][2])
    )
    terms.append((-a[0][0] + a[1][0] + a[1][1]) * (b[0][0] - b[0][1] + b[1][1]))
    terms.append((a[1][0] + a[1][1]) * (-b[0][0] + b[0][1]))
    terms.append(a[0][0] * b[0][0])
    terms.append((-a[0][0] + a[2][0] + a[2][1]) * (b[0][0] - b[0][2] + b[1][2]))
    terms.append((-a[0][0] + a[2][0]) * (b[0][2] - b[1][2]))
    terms.append((a[2][0] + a[2][1]) * (-b[0][0] + b[0][2]))
    terms.append(
        (a[0][0] + a[0][1] + a[0][2] - a[1][1] - a[1][2] - a[2][0] - a[2][1]) * b[1][2]
    )
    terms.append(
        a[2][1] * (-b[0][0] + b[0][2] + b[1][0] - b[1][1] - b[1][2] - b[2][0] + b[2][1])
    )
    terms.append((-a[0][2] + a[2][1] + a[2][2]) * (b[1][1] + b[2][0] - b[2][1]))
    terms.append((a[0][2] - a[2][2]) * (b[1][1] - b[2][1]))
    terms.append(a[0][2] * b[2][0])
    terms.append((a[2][1] + a[2][2]) * (-b[2][0] + b[2][1]))
    terms.append((-a[0][2] + a[1][1] + a[1][2]) * (b[1][2] + b[2][0] - b[2][2]))
    terms.append((a[0][2] - a[1][2]) * (b[1][2] - b[2][2]))
    terms.append((a[1][1] + a[1][2]) * (-b[2][0] + b[2][2]))
    terms.append(a[0][1] * b[1][0])
    terms.append(a[1][2] * b[2][1])
    terms.append(a[1][0] * b[0][2])
    terms.append(a[2][0] * b[0][1])
    terms.append(a[2][2] * b[2][2])

    return Matrix3x3.from_iterable(
        [
            terms[5] + terms[13] + terms[18],
            terms[0]
            + terms[3]
            + terms[4]
            + terms[5]
            + terms[11]
            + terms[13]
            + terms[14],
            terms[5]
            + terms[6]
            + terms[8]
            + terms[9]
            + terms[13]
            + terms[15]
            + terms[17],
            terms[1]
            + terms[2]
            + terms[3]
            + terms[5]
            + terms[13]
            + terms[15]
            + terms[16],
            terms[1] + terms[3] + terms[4] + terms[5] + terms[19],
            terms[13] + terms[15] + terms[16] + terms[17] + terms[20],
            terms[5]
            + terms[6]
            + terms[7]
            + terms[10]
            + terms[11]
            + terms[12]
            + terms[13],
            terms[11] + terms[12] + terms[13] + terms[14] + terms[21],
            terms[5] + terms[6] + terms[7] + terms[8] + terms[22],
        ]
    )
