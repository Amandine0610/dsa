#!/usr/bin/python3
"""
Module for processing files to extract unique integers and save them sorted.
"""

import os

class UniqueIntProcessor:
    def __init__(self):
        self.seen = set()

    def process_file(self, input_file_path, output_file_path):
        """
        Process the input file to extract unique integers and save them sorted to the output file.

        Args:
            input_file_path (str): The path to the input file.
            output_file_path (str): The path to the output file.
        """
        self.read_file(input_file_path)
        self.write_file(output_file_path)

    def read_file(self, input_file_path):
        """
        Read integers from the input file and add them to the set of seen integers.

        Args:
            input_file_path (str): The path to the input file.
        """
        with open(input_file_path, 'r') as input_file:
            for line in input_file:
                cleaned_line = self.clean_line(line)
                if cleaned_line is not None:
                    self.seen.add(cleaned_line)

    def clean_line(self, line):
        """
        Clean and validate the input line.

        Args:
            line (str): The input line to clean and validate.

        Returns:
            int: The validated integer, or None if invalid.
        """
        line = line.strip()
        if line:
            parts = line.split()
            if len(parts) == 1:
                try:
                    num = int(parts[0])
                    if -1023 <= num <= 1023:
                        return num
                except ValueError:
                    pass
        return None

    def write_file(self, output_file_path):
        """
        Write the sorted unique integers to the output file.

        Args:
            output_file_path (str): The path to the output file.
        """
        with open(output_file_path, 'w') as output_file:
            for num in sorted(self.seen):
                output_file.write(f"{num}\n")

if __name__ == "__main__":
    processor = UniqueIntProcessor()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_file_path = os.path.join(current_dir, "..", "..", "sample_inputs", "sample_01.txt")
    output_file_path = os.path.join(current_dir, "..", "..", "sample_results", "sample_01.txt_result.txt")
    
    processor.process_file(input_file_path, output_file_path)

