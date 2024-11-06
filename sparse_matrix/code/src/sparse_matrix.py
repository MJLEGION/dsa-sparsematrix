class SparseMatrix:
    def __init__(self, matrix_file_path=None, num_rows=None, num_cols=None):
        """
        Initialize the SparseMatrix. It can be initialized either by loading from a file
        or by specifying the number of rows and columns.

        :param matrix_file_path: Path to the file containing the sparse matrix data (optional)
        :param num_rows: Number of rows in the matrix (optional if matrix_file_path is provided)
        :param num_cols: Number of columns in the matrix (optional if matrix_file_path is provided)
        """
        if matrix_file_path:
            self.load_matrix(matrix_file_path)
        elif num_rows is not None and num_cols is not None:
            self.num_rows = num_rows
            self.num_cols = num_cols
            self.elements = {}  # Dictionary to store non-zero elements with keys as (row, col)
        else:
            raise ValueError("Either matrix_file_path or num_rows and num_cols must be provided.")

    def load_matrix(self, matrix_file_path):
        """
        Load the sparse matrix from a file.

        :param matrix_file_path: Path to the file containing the sparse matrix data
        """
        try:
            with open(matrix_file_path, 'r') as file:
                lines = file.readlines()
                self.num_rows = int(lines[0].strip().split('=')[1])
                self.num_cols = int(lines[1].strip().split('=')[1])
                self.elements = {}
                for line in lines[2:]:
                    line = line.strip()
                    if not line:
                        continue
                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError("Input file has wrong format")
                    try:
                        row, col, value = map(int, line[1:-1].split(','))
                        self.elements[(row, col)] = value
                    except ValueError:
                        raise ValueError("Input file has wrong format")
        except Exception as e:
            raise ValueError(f"An error occurred while reading the file: {e}")

    def get_element(self, curr_row, curr_col):
        """
        Get the value of the element at the specified row and column.

        :param curr_row: Row index
        :param curr_col: Column index
        :return: The value at the specified location, or 0 if the element is not explicitly stored
        """
        return self.elements.get((curr_row, curr_col), 0)

    def set_element(self, curr_row, curr_col, value):
        """
        Set the value of the element at the specified row and column.

        :param curr_row: Row index
        :param curr_col: Column index
        :param value: The value to be set
        """
        self.elements[(curr_row, curr_col)] = value

    def add(self, other):
        """
        Add two sparse matrices.

        :param other: The other sparse matrix to be added
        :return: A new SparseMatrix representing the result
        :raises ValueError: If the dimensions of the matrices do not match
        """
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices dimensions do not match for addition.")
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        result.elements = self.elements.copy()
        for (row, col), value in other.elements.items():
            if (row, col) in result.elements:
                result.elements[(row, col)] += value
            else:
                result.elements[(row, col)] = value
        return result

    def subtract(self, other):
        """
        Subtract one sparse matrix from another.

        :param other: The other sparse matrix to be subtracted
        :return: A new SparseMatrix representing the result
        :raises ValueError: If the dimensions of the matrices do not match
        """
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices dimensions do not match for subtraction.")
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        result.elements = self.elements.copy()
        for (row, col), value in other.elements.items():
            if (row, col) in result.elements:
                result.elements[(row, col)] -= value
            else:
                result.elements[(row, col)] = -value
        return result

    def multiply(self, other):
        """
        Multiply two sparse matrices.

        :param other: The other sparse matrix to be multiplied
        :return: A new SparseMatrix representing the result
        :raises ValueError: If the number of columns of the first matrix is not equal to the number of rows of the second matrix
        """
        if self.num_cols != other.num_rows:
            raise ValueError("Matrices dimensions do not match for multiplication.")
        result = SparseMatrix(num_rows=self.num_rows, num_cols=other.num_cols)
        for (row, col), value in self.elements.items():
            for k in range(other.num_cols):
                if (col, k) in other.elements:
                    if (row, k) in result.elements:
                        result.elements[(row, k)] += value * other.elements[(col, k)]
                    else:
                        result.elements[(row, k)] = value * other.elements[(col, k)]
        return result

    def __str__(self):
        """
        String representation of the sparse matrix in the required format.

        :return: String representation of the matrix
        """
        output = f"rows={self.num_rows}\ncols={self.num_cols}\n"
        for (row, col), value in sorted(self.elements.items()):
            output += f"({row}, {col}, {value})\n"
        return output

def main():
    input_dir = r'C:\Users\user\Desktop\dsa\sparse_matrix\sample_inputs'
    output_dir = r'C:\Users\user\Desktop\dsa\sparse_matrix\sample_results'

    # Load matrices from files
    matrix1 = SparseMatrix(matrix_file_path=f"{input_dir}/easy_sample_02_1.txt")
    matrix2 = SparseMatrix(matrix_file_path=f"{input_dir}/easy_sample_02_2.txt")

    print(f"Matrix 1: {matrix1.num_rows} rows, {matrix1.num_cols} cols")
    print(f"Matrix 2: {matrix2.num_rows} rows, {matrix2.num_cols} cols")

    while True:
        print("Select operation: (will fail if there's a dimension mismatch)")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            try:
                result = matrix1.add(matrix2)
                print("Addition Result:\n", result)
                with open(f"{output_dir}/addition_result.txt", 'w') as f:
                    f.write(str(result))
            except ValueError as e:
                print(e)

        elif choice == '2':
            try:
                result = matrix1.subtract(matrix2)
                print("Subtraction Result:\n", result)
                with open(f"{output_dir}/subtraction_result.txt", 'w') as f:
                    f.write(str(result))
            except ValueError as e:
                print(e)

        elif choice == '3':
            result = matrix1.multiply(matrix2)
            print("Multiplication Result:\n", result)
            with open(f"{output_dir}/multiplication_result.txt", 'w') as f:
                f.write(str(result))

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
