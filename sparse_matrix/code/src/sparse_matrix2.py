import os

class SparseMatrix:
    def __init__(self, numRows, numCols):
        self.numRows = numRows
        self.numCols = numCols
        self.elements = {}

    @staticmethod
    def from_file(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        numRows = int(lines[0].strip().split('=')[1])
        numCols = int(lines[1].strip().split('=')[1])

        matrix = SparseMatrix(numRows, numCols)
        
        for line in lines[2:]:
            if line.strip():
                row, col, value = map(int, line.strip()[1:-1].split(','))
                matrix.set_element(row, col, value)
        
        return matrix

    def to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write("rows={}\n".format(self.numRows))
            file.write("cols={}\n".format(self.numCols))
            for (row, col), value in self.elements.items():
                file.write("({}, {}, {})\n".format(row, col, value))

    def set_element(self, row, col, value):
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)]

    def get_element(self, row, col):
        return self.elements.get((row, col), 0)

    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions must match for addition.")
        
        result = SparseMatrix(self.numRows, self.numCols)
        
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value + other.get_element(row, col))
        
        for (row, col), value in other.elements.items():
            if (row, col) not in result.elements:
                result.set_element(row, col, value)
        
        return result

    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions must match for subtraction.")
        
        result = SparseMatrix(self.numRows, self.numCols)
        
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value - other.get_element(row, col))
        
        for (row, col), value in other.elements.items():
            if (row, col) not in result.elements:
                result.set_element(row, col, -value)
        
        return result

    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Number of columns in first matrix must equal number of rows in second matrix for multiplication.")
        
        result = SparseMatrix(self.numRows, other.numCols)
        
        # Create a transpose of the other matrix to optimize column access
        other_transpose = SparseMatrix(other.numCols, other.numRows)
        for (row, col), value in other.elements.items():
            other_transpose.set_element(col, row, value)
        
        for (row, col), value in self.elements.items():
            for k in range(other.numCols):
                if (col, k) in other_transpose.elements:
                    result.set_element(row, k, result.get_element(row, k) + value * other_transpose.get_element(k, col))
        
        return result

def main():
    input_dir = os.path.expanduser("~/dsa/sparse_matrix/sample_inputs")
    output_dir = os.path.expanduser("~/dsa/sparse_matrix/code/src")

    matrix_files = [os.path.join(input_dir, fname) for fname in os.listdir(input_dir) if fname.endswith('.txt')]
    if len(matrix_files) < 2:
        raise ValueError("There must be at least two matrix files in the input directory.")

    print("Select operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    operation = int(input("Enter operation number: "))

    print("Available matrix files:")
    for i, fname in enumerate(matrix_files):
        print("{}: {}".format(i, fname))

    index1 = int(input("Enter first matrix file index:\n"))
    index2 = int(input("Enter second matrix file index:\n"))
    output_file = input("Enter output file name:\n")

    matrix1 = SparseMatrix.from_file(matrix_files[index1])
    matrix2 = SparseMatrix.from_file(matrix_files[index2])

    if operation == 1:
        result_matrix = matrix1.add(matrix2)
    elif operation == 2:
        result_matrix = matrix1.subtract(matrix2)
    elif operation == 3:
        result_matrix = matrix1.multiply(matrix2)
    else:
        raise ValueError("Invalid operation number.")

    result_matrix.to_file(os.path.join(output_dir, output_file))
    print("Operation completed. Result saved to {}.".format(output_file))

if __name__ == "__main__":
    main()

