from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray
    from typing import TextIO


class MatrixSeriesWriter:
    
    file_name: str
    file: TextIO

    def __init__(self, file_name: str):
        super().__init__()
        self.file_name = file_name

    def __enter__(self) -> MatrixSeriesWriter:
        """Returns self"""
        self.file = open(self.file_name, 'w', encoding='UTF-8')
        return self
 
    def __exit__(self, *args):
        self.file.close()

    def write_matrix(self, mat: NDArray):

        size: tuple[int, ...] = mat.shape

        self.file.write(f"{size[0]}\n")	# Height
        self.file.write(f"{size[1]}\n")	# Width
        
        # Values in reading order
        for row in mat:
            for val in row:
                self.file.write(f"{val}\n")


class MatrixSeriesReader:

    file_name: str
    file: TextIO

    def __init__(self, file_name: str):
        super().__init__()
        self.file_name = file_name

    def __enter__(self) -> MatrixSeriesReader:
        """Returns self"""
        self.file = open(self.file_name, 'r', encoding='UTF-8')
        return self
 
    def __exit__(self, *args):
        self.file.close()

    def read_matrix(self) -> NDArray | None:

        # Check if there is another matrix
        firstLine = self.file.readline().strip()
        if firstLine == "":
            return None

        # Read size
        height = int(firstLine)
        width = int(self.file.readline().strip())

        # Make array
        mat: NDArray = np.empty((height, width))

        # Read values in reading order
        for i in range(height):
            for j in range(width):
                mat[i, j] = int(self.file.readline().strip())

        return mat
