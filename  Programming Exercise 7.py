"""Display and count sentences, including sentences beginning with numbers.

Author: Ean Eichelbaum
Date: October 22, 2026
Course: COP 2373
"""

import re


def get_paragraph():
    """Read one paragraph from the keyboard and return it as a string."""
    # Enter the entire paragraph on one line, then press Enter.
    paragraph = input("Enter a paragraph: ").strip()
    return paragraph


def split_sentences(paragraph):
    """Return complete sentences that start with a capital letter or number."""
    # Adapted from Section 7.4 of Supercharged Python (Overland and Bennett).
    # Add digits to BOTH the starting class and the look-ahead class.
    # Allow multiple spaces between sentences; preserve decimal points and
    # abbreviations followed by lowercase words, as in the textbook example.
    pattern = r"[A-Z0-9].*?[.!?](?=\s+[A-Z0-9]|$)"
    sentences = re.findall(pattern, paragraph, flags=re.DOTALL | re.MULTILINE)
    return sentences


def display_sentences(sentences):
    """Print each sentence on its own line and print the sentence count."""
    print("\nIndividual sentences:")

    # Number each sentence beginning with 1 for readable output.
    for number, sentence in enumerate(sentences, start=1):
        print(f"{number}. {sentence}")

    # An empty paragraph produces an empty list and a count of zero.
    print(f"\nSentence count: {len(sentences)}")


def main():
    """Collect the paragraph, separate its sentences, and show the results."""
    paragraph = get_paragraph()
    sentences = split_sentences(paragraph)
    display_sentences(sentences)


if __name__ == "__main__":
    # Only the entry point is outside functions; program logic is in functions.
    main()
