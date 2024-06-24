#!/usr/bin/python3
""""""
import os
import ast
import sys


def has_docstring(node):
    """Check if a node has a docstring."""
    return ast.get_docstring(node) is not None


def check_file(file_path):
    """Check a single file for docstrings."""
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)

    missing_docstrings = []

    # Check module docstring
    if not has_docstring(tree):
        missing_docstrings.append(f"""Module {file_path} is missing a \
                                  docstring.""")

    # Check classes and their methods
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if not has_docstring(node):
                missing_docstrings.append(f"""Class {node.name} in {file_path}\
                                           is missing a docstring.""")
            for body_item in node.body:
                if isinstance(body_item, ast.FunctionDef):
                    if not has_docstring(body_item):
                        missing_docstrings.append(
                            f"""Method {node.name}.{body_item.name} in
                              {file_path} is missing a docstring."""
                            )
        elif isinstance(node, ast.FunctionDef):
            if not has_docstring(node):
                missing_docstrings.append(
                    f"""Function {node.name} in {file_path} is missing a
                      docstring.""")

    return missing_docstrings


def check_directory(directory, skip_tests=False):
    """Check all Python files in a directory for docstrings."""
    missing_docstrings = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                if skip_tests and file.startswith('test_'):
                    continue
                file_path = os.path.join(root, file)
                missing_docstrings.extend(check_file(file_path))
    return missing_docstrings


def main():
    """"""
    directories = ['.']  # Change these to your directories
    skip_tests = len(sys.argv) > 1 and sys.argv[1] == 'skiptest'

    missing_docstrings = []
    for directory in directories:
        missing_docstrings.extend(check_directory(directory, skip_tests))

    if missing_docstrings:
        print("Missing docstrings found:")
        for message in missing_docstrings:
            print(message)
    else:
        print("All modules, classes, and functions are properly documented.")


if __name__ == "__main__":
    main()
