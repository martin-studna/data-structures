class Matrix:
    """Interface of a matrix.

    This class provides only the matrix size N and a method for swapping
    two items. The actual storage of the matrix in memory is provided by
    subclasses in testing code.
    """

    def __init__(self, N):
        self.N = N

    def swap(self, i1, j1, i2, j2):
        """Swap elements (i1,j1) and (i2,j2)."""

        # Overridden in subclasses
        raise NotImplementedError

    def transpose(self):
        """Transpose the matrix."""
        N = self.N
        # Transpose submatrix method gets coordinates of the uppermost, leftmost element
        # and the bottom-most, rightmost element of the matrix. 
        self.transpose_and_swap_submatrix(0, 0, N - 1, N - 1)

    def transpose_and_swap_submatrix(self, i1, j1, i2, j2):
      # If we have a submatrix on the diagonal, we make only three recursive calls.
      # Otherwise we make four recursive calls

        if (i1 == i2) or (j1 == j2):
          self.swap_submatrix(i1, j1, i2, j2)
        else:
          # middle row index
          i_mid = int((i1 + i2) / 2)
          # middle column index
          j_mid = int((j1 + j2) / 2)
          # Transpose upper left submatrix.
          self.transpose_and_swap_submatrix(i1, j1, i_mid, j_mid)
          # Transpose bottom left submatrix.
          self.transpose_and_swap_submatrix(i_mid + 1, j1, i2, j_mid)
          # Transpose bottom right submatrix.
          self.transpose_and_swap_submatrix(i_mid + 1, j_mid + 1, i2, j2)
          if i1 >= j_mid + 1:
            # Transpose upper right submatrix.
            self.transpose_and_swap_submatrix(i1, j_mid + 1, i_mid, j2)

    def swap_submatrix(self, i1, j1, i2, j2):
        # Swap everything except the elements on the diagonal.
        for i in range(i1, i2 + 1):
          for j in range(j1, j2 + 1):
            if i != j:
              self.swap(i, j, j, i)