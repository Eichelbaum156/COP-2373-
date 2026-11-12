"""Five-card draw poker: deal five cards and replace selected cards once."""

import random


class Card:
    """One playing card with a rank and suit."""

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        names = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}
        return f"{names.get(self.rank, self.rank)} of {self.suit}"


class Deck:
    """A standard 52-card deck with no jokers."""

    def __init__(self):
        self.cards = []
        for suit in ("Clubs", "Diamonds", "Hearts", "Spades"):
            for rank in range(1, 14):
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if not self.cards:
            raise ValueError("The deck is empty.")
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)


def display_hand(hand, heading):
    """Print the five cards with positions numbered 1 through 5."""
    print(f"\n{heading}")
    for position, card in enumerate(hand, start=1):
        print(f"{position}. {card}")


def get_replacements():
    """Read unique positions, accepting commas or spaces as separators."""
    while True:
        entry = input("\nCards to replace (example: 1, 3, 5; Enter to keep all): ")
        if not entry.strip():
            return []
        try:
            positions = [int(value) for value in entry.replace(",", " ").split()]
        except ValueError:
            print("Please enter whole numbers from 1 to 5.")
            continue
        if not positions or any(number < 1 or number > 5 for number in positions):
            print("Each card number must be from 1 to 5.")
        elif len(positions) != len(set(positions)):
            print("Enter each card number only once.")
        else:
            return positions


def draw_cards(deck, hand, positions):
    """Replace selected cards using the remaining deck."""
    for position in positions:
        hand[position - 1] = deck.deal()


def main():
    """Play one round of five-card draw."""
    print("FIVE-CARD DRAW POKER")
    deck = Deck()
    deck.shuffle()
    hand = [deck.deal() for _ in range(5)]
    display_hand(hand, "Your original hand:")
    positions = get_replacements()
    draw_cards(deck, hand, positions)
    print(f"\nReplaced {len(positions)} card(s).")
    display_hand(hand, "Your final hand:")
    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
