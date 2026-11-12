"""Five-card draw poker: deal five cards and replace selected cards once."""

import random


class Deck:
    """Deck implementation from Section 11.5 (page 366)."""

    def __init__(self, size):
        self.card_list = [i for i in range(size)]
        random.shuffle(self.card_list)
        self.current_card = 0
        self.size = size

    def deal(self):
        if self.size - self.current_card < 1:
            random.shuffle(self.card_list)
            self.current_card = 0
            print("Reshuffling...!!!")
        self.current_card += 1
        return self.card_list[self.current_card - 1]


def card_name(card):
    """Convert a number from 0 to 51 into its rank and suit."""
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9',
             '10', 'J', 'Q', 'K', 'A']
    suits = ['clubs', 'diamonds', 'hearts', 'spades']
    return f"{ranks[card % 13]} of {suits[card // 13]}"


def display_hand(hand, heading):
    """Print the five cards with positions numbered 1 through 5."""
    print(f"\n{heading}")
    for position, card in enumerate(hand, start=1):
        print(f"{position}. {card_name(card)}")


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
    deck = Deck(52)
    hand = [deck.deal() for _ in range(5)]
    display_hand(hand, "Your original hand:")
    positions = get_replacements()
    draw_cards(deck, hand, positions)
    print(f"\nReplaced {len(positions)} card(s).")
    display_hand(hand, "Your final hand:")
    print("\nThanks for playing!")


if __name__ == "__main__":
    main()

