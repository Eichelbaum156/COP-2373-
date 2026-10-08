"""Validate common phone, SSN, and ZIP code formats with regular expressions."""

import re
import sys


def _matches(pattern, value):
    """Return whether the complete value matches a regular expression."""
    # fullmatch prevents valid-looking text from having extra characters around it.
    return re.fullmatch(pattern, value) is not None


def is_valid_phone(phone):
    """Check a 10-digit US phone number, optionally prefixed by country code 1.

    Accepted separators are spaces, periods, and hyphens. The area code may
    optionally be enclosed in parentheses.
    """
    # Keep the expression local so each validator states its own accepted format.
    pattern = r"(?:\+?1[-. ]?)?(?:\(\d{3}\)|\d{3})[-. ]?\d{3}[-. ]?\d{4}"
    return _matches(pattern, phone)


def is_valid_ssn(ssn):
    """Check the standard nine-digit SSN display format NNN-NN-NNNN."""
    # This checks formatting only; it does not determine whether an SSN was issued.
    pattern = r"\d{3}-\d{2}-\d{4}"
    return _matches(pattern, ssn)


def is_valid_zip(zip_code):
    """Check a five-digit ZIP code or ZIP+4 value written with a hyphen."""
    # ZIP+4 uses exactly four digits after the hyphen.
    pattern = r"\d{5}(?:-\d{4})?"
    return _matches(pattern, zip_code)


def run_tests():
    """Run representative valid and invalid examples and print a test report."""
    # Each case records a validator, the sample value, and its expected result.
    cases = [
        ("phone", is_valid_phone, "555-123-4567", True),
        ("phone", is_valid_phone, "(555) 123-4567", True),
        ("phone", is_valid_phone, "+1 555 123 4567", True),
        ("phone", is_valid_phone, "555-12-4567", False),
        ("phone", is_valid_phone, "555-123-4567 ext 2", False),
        ("SSN", is_valid_ssn, "123-45-6789", True),
        ("SSN", is_valid_ssn, "12-345-6789", False),
        ("SSN", is_valid_ssn, "123-45-67890", False),
        ("ZIP", is_valid_zip, "34231", True),
        ("ZIP", is_valid_zip, "34231-1234", True),
        ("ZIP", is_valid_zip, "3423", False),
        ("ZIP", is_valid_zip, "34231-123", False),
    ]

    # Count mismatches so the command returns a useful success or failure status.
    failures = 0
    print("Programming Exercise 6 - validation tests")
    for label, validator, sample, expected in cases:
        actual = validator(sample)
        status = "PASS" if actual == expected else "FAIL"
        failures += actual != expected
        print(f"{status} {label:5} {sample!r}: expected {expected}, got {actual}")
    print(f"\n{len(cases) - failures}/{len(cases)} tests passed")
    return failures == 0


def main():
    """Run tests when requested, otherwise prompt for three values to validate."""
    # A test flag makes the checks repeatable without interactive input.
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        return 0 if run_tests() else 1

    # Collect one value for each required data type.
    phone = input("Enter a phone number: ").strip()
    ssn = input("Enter an SSN (NNN-NN-NNNN): ").strip()
    zip_code = input("Enter a ZIP code: ").strip()

    # Print a clear result for each independent validation.
    print(f"Phone number valid: {is_valid_phone(phone)}")
    print(f"Social Security number format valid: {is_valid_ssn(ssn)}")
    print(f"ZIP code valid: {is_valid_zip(zip_code)}")
    return 0


if __name__ == "__main__":
    # Keep executable behavior inside main while supporting imports for reuse.
    raise SystemExit(main())
