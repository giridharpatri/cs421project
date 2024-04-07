import sys
import pandas 
import spacy
import numpy
import os

def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
            print(f"Contents of '{file_path}':")
            print(contents)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

def main():
    directory = 'essays_dataset/essays/'
    file_name = input("Enter the name of the text file to read from: ").strip("'\"")
    file_path = os.path.join(directory, file_name)
    read_text_file(file_path)

if __name__ == "__main__":
    main()