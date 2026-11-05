"""Programming Exercise BankAcct.

Author: Ean Eichelbaum
Date: November 5, 2026
Course: COP 2373
"""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


class BankAcct:
    """Manage an account and calculate simple interest using a 365-day year."""

    def __init__(self, name, account_number, amount=0, interest_rate=0):
        """Create an account; interest_rate is a percentage, such as 5 for 5%."""
        if not str(name).strip() or not str(account_number).strip():
            raise ValueError("Name and account number cannot be blank.")
        self.name = str(name).strip()
        # Keep account numbers as strings to preserve leading zeros.
        self.account_number = str(account_number).strip()
        self.amount = self._number(amount, "Opening amount").quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.interest_rate = self._number(interest_rate, "Interest rate")
        self.interest_days = 0
        self.interest_amount = Decimal("0.00")

    def _number(self, value, label):
        """Convert an input to a finite, nonnegative Decimal."""
        try:
            number = Decimal(str(value))
        except (InvalidOperation, ValueError):
            raise ValueError(f"{label} must be a number.") from None
        if not number.is_finite() or number < 0:
            raise ValueError(f"{label} must be finite and nonnegative.")
        return number

    def _reset_interest(self):
        """Clear an old interest estimate after a balance or rate change."""
        self.interest_days = 0
        self.interest_amount = Decimal("0.00")

    def adjust_interest_rate(self, new_rate):
        """Set the annual percentage rate without changing the balance."""
        self.interest_rate = self._number(new_rate, "Interest rate")
        self._reset_interest()

    def deposit(self, amount):
        """Deposit a positive amount and return the updated balance."""
        deposit_amount = self._number(amount, "Deposit").quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP)
        if deposit_amount <= 0:
            raise ValueError("Deposit must be at least $0.01.")
        self.amount += deposit_amount
        self._reset_interest()
        return self.amount

    def withdraw(self, amount):
        """Withdraw a positive amount if funds are available; return balance."""
        withdrawal = self._number(amount, "Withdrawal").quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP)
        if withdrawal <= 0:
            raise ValueError("Withdrawal must be at least $0.01.")
        if withdrawal > self.amount:
            raise ValueError("Insufficient funds.")
        self.amount -= withdrawal
        self._reset_interest()
        return self.amount

    def get_balance(self):
        """Return the current account balance."""
        return self.amount

    def calculate_interest(self, days):
        """Return simple interest for whole days; do not deposit the interest."""
        day_count = self._number(days, "Days")
        if day_count != day_count.to_integral_value():
            raise ValueError("Days must be a whole number.")
        self.interest_days = int(day_count)
        # Simple interest = principal x annual rate x days / 365.
        self.interest_amount = (
            self.amount * self.interest_rate / Decimal("100")
            * day_count / Decimal("365")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return self.interest_amount

    def __str__(self):
        """Display the balance and the most recently calculated interest."""
        return (f"Owner: {self.name} | Account: {self.account_number}\n"
                f"Balance: ${self.amount:,.2f} | Annual rate: {self.interest_rate:.2f}%\n"
                f"Interest for {self.interest_days} day(s): "
                f"${self.interest_amount:,.2f}")


def test_bank_acct():
    """Test each method with known results and rejected transactions."""
    print("BANKACCT CLASS TESTS")
    print("Simple interest: balance x (annual rate / 100) x (days / 365)\n")

    # Constructor and __str__ display a new account.
    account = BankAcct("Alex Rivera", "00123456", "1000.00", "5.00")
    assert account.get_balance() == Decimal("1000.00")
    assert account.account_number == "00123456"
    print("1. New account")
    print(account)

    # Deposit and withdrawal must update the balance correctly.
    assert account.deposit("250.00") == Decimal("1250.00")
    print("\n2. Deposit $250.00: balance = $1,250.00 [PASS]")
    assert account.withdraw("100.00") == Decimal("1150.00")
    print("3. Withdraw $100.00: balance = $1,150.00 [PASS]")

    # Verify the new rate and interest for different day counts.
    account.adjust_interest_rate("4.00")
    assert account.interest_rate == Decimal("4.00")
    assert account.calculate_interest(30) == Decimal("3.78")
    assert account.get_balance() == Decimal("1150.00")
    print("4. Change annual rate to 4.00%; 30-day interest = $3.78 [PASS]")
    print(account)
    assert account.calculate_interest(365) == Decimal("46.00")
    print("5. Interest for 365 days = $46.00 [PASS]")
    assert account.calculate_interest(0) == Decimal("0.00")
    print("6. Interest for 0 days = $0.00 [PASS]")

    # Each invalid operation must raise ValueError and leave funds unchanged.
    for label, operation in [
        ("Overdraft", lambda: account.withdraw("2000")),
        ("Negative deposit", lambda: account.deposit("-10")),
        ("Zero withdrawal", lambda: account.withdraw("0")),
        ("Negative rate", lambda: account.adjust_interest_rate("-1")),
        ("Negative days", lambda: account.calculate_interest(-1)),
        ("Fractional days", lambda: account.calculate_interest("1.5")),
        ("Nonfinite deposit", lambda: account.deposit("NaN")),
    ]:
        try:
            operation()
        except ValueError as error:
            print(f"   {label} rejected: {error} [PASS]")
        else:
            raise AssertionError(f"{label} was incorrectly accepted.")
        assert account.get_balance() == Decimal("1150.00")

    # An exact-balance withdrawal must succeed without an overdraft.
    assert account.withdraw("1150.00") == Decimal("0.00")
    assert account.calculate_interest(30) == Decimal("0.00")
    print("7. Withdraw remaining funds: balance and interest = $0.00 [PASS]")
    print("\nALL TESTS PASSED")


if __name__ == "__main__":
    test_bank_acct()

