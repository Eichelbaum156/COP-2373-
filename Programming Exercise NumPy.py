"""Analyze student exam grades with NumPy.

Author: Ean Eichelbaum
Course: COP 2373
"""

import csv
from pathlib import Path

import numpy as np


def load_grades(filename):
    """Load names and three integer exam scores into NumPy arrays."""
    # csv.reader also handles quoted names containing commas.
    with open(filename, newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        header = next(reader, [])
        rows = [row for row in reader if row]

    if header != ["First Name", "Last Name", "Exam 1", "Exam 2", "Exam3"]:
        raise ValueError("The CSV header must match the Programming Exercise CSV file.")
    if len(rows) < 10 or any(len(row) != 5 for row in rows):
        raise ValueError("The CSV needs at least 10 students and five fields per row.")

    data = np.array(rows, dtype=str)
    grades = data[:, 2:].astype(int)
    if np.any((grades < 0) | (grades > 100)):
        raise ValueError("Exam grades must be integers from 0 through 100.")
    return data, grades


def display_preview(data):
    """Print the first five student records."""
    print("Programming Exercise NumPy - Student Grade Analysis")
    print(f"Students loaded: {len(data)} | Exams per student: 3")
    print("\nFirst five records:")
    print(f"{'First Name':<14}{'Last Name':<14}{'Exam 1':>8}{'Exam 2':>8}{'Exam 3':>8}")
    for row in data[:5]:
        print(f"{row[0]:<14}{row[1]:<14}{row[2]:>8}{row[3]:>8}{row[4]:>8}")


def display_statistics(grades):
    """Print per-exam and overall descriptive statistics."""
    # axis=0 summarizes columns; no axis summarizes every exam score.
    # ddof=0 treats this entire class dataset as the population.
    statistics = [
        ("Mean", np.mean(grades, axis=0), np.mean(grades)),
        ("Median", np.median(grades, axis=0), np.median(grades)),
        ("Std. deviation", np.std(grades, axis=0, ddof=0), np.std(grades, ddof=0)),
        ("Minimum", np.min(grades, axis=0), np.min(grades)),
        ("Maximum", np.max(grades, axis=0), np.max(grades)),
    ]
    print("\nStatistics (population standard deviation):")
    print(f"{'Statistic':<18}{'Exam 1':>10}{'Exam 2':>10}{'Exam 3':>10}{'Overall':>10}")
    for label, exams, overall in statistics:
        print(f"{label:<18}{exams[0]:>10.2f}{exams[1]:>10.2f}"
              f"{exams[2]:>10.2f}{overall:>10.2f}")


def display_pass_results(grades):
    """Count passing/failing scores and calculate the overall pass percentage."""
    # A score of exactly 60 passes. Each score represents one exam attempt.
    passed = grades >= 60
    pass_counts = np.sum(passed, axis=0)
    fail_counts = grades.shape[0] - pass_counts
    print("\nPass/fail counts (passing grade: 60 or above):")
    print(f"{'Result':<18}{'Exam 1':>10}{'Exam 2':>10}{'Exam 3':>10}")
    print(f"{'Passed':<18}{pass_counts[0]:>10}{pass_counts[1]:>10}{pass_counts[2]:>10}")
    print(f"{'Failed':<18}{fail_counts[0]:>10}{fail_counts[1]:>10}{fail_counts[2]:>10}")
    total_passed = int(np.sum(passed))
    percentage = total_passed / grades.size * 100
    print(f"\nOverall pass percentage: {percentage:.2f}% "
          f"({total_passed} of {grades.size} exam scores)")


def main():
    """Locate the CSV beside this script and run the complete analysis."""
    filename = Path(__file__).resolve().with_name("grades.csv")
    try:
        data, grades = load_grades(filename)
        display_preview(data)
        display_statistics(grades)
        display_pass_results(grades)
    except (OSError, ValueError, csv.Error) as error:
        print(f"Unable to analyze grades: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
