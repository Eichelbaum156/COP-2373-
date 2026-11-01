"""Write and display student exam grades using CSV files.

Author: Ean Eichelbaum
Date: November 1, 2026
Course: COP 2373
"""

import csv


def get_integer(prompt, minimum, maximum=None):
    """Read an integer within the inclusive limits."""
    while True:
        try:
            value = int(input(prompt))
            if value >= minimum and (maximum is None or value <= maximum):
                return value
        except ValueError:
            pass
        # Repeat the prompt when the entry is not a valid integer.
        if maximum is None:
            print(f"Enter a whole number of at least {minimum}.")
        else:
            print(f"Enter a whole number from {minimum} to {maximum}.")


def get_name(prompt):
    """Read and return a nonempty student name."""
    while True:
        name = input(prompt).strip()
        if name:
            return name
        print("Name cannot be blank.")


def write_grades(filename):
    """Collect student records and write the CSV header and records."""
    student_count = get_integer("How many students? ", 0)
    # newline prevents extra blank CSV rows; with closes the file automatically.
    with open(filename, "w", newline="", encoding="utf-8") as grades_file:
        writer = csv.writer(grades_file)
        writer.writerow(["First Name", "Last Name", "Exam 1", "Exam 2", "Exam3"])
        for student_number in range(1, student_count + 1):
            print(f"\nStudent {student_number}")
            first_name = get_name("First name: ")
            last_name = get_name("Last name: ")
            exam1 = get_integer("Exam 1: ", 0, 100)
            exam2 = get_integer("Exam 2: ", 0, 100)
            exam3 = get_integer("Exam 3: ", 0, 100)
            # csv.writer quotes names containing commas when necessary.
            writer.writerow([first_name, last_name, exam1, exam2, exam3])
    print(f"\nSaved {student_count} student record(s) to {filename}.")


def read_grades(filename):
    """Read the CSV file and display its records in aligned columns."""
    with open(filename, "r", newline="", encoding="utf-8") as grades_file:
        reader = csv.reader(grades_file)
        header = next(reader)
        rows = list(reader)
    # Expand name columns to fit the longest name or heading.
    first_width = max([len(header[0])] + [len(row[0]) for row in rows]) + 2
    last_width = max([len(header[1])] + [len(row[1]) for row in rows]) + 2
    print("\nStudent Exam Grades")
    print(f"{header[0]:<{first_width}}{header[1]:<{last_width}}"
          f"{header[2]:>8}{header[3]:>8}{header[4]:>8}")
    print("-" * (first_width + last_width + 24))
    for row in rows:
        print(f"{row[0]:<{first_width}}{row[1]:<{last_width}}"
              f"{int(row[2]):>8}{int(row[3]):>8}{int(row[4]):>8}")
    if not rows:
        print("No student records.")


def main():
    """Run grade entry followed by the separate file display function."""
    filename = "grades.csv"
    try:
        write_grades(filename)
        read_grades(filename)
    except (OSError, csv.Error, ValueError, StopIteration, IndexError) as error:
        print(f"Unable to process grades: {error}")


if __name__ == "__main__":
    main()
