# DashDoor — "Fix My Code" Challenge

> **DashDoor** is a scrappy food delivery startup. Their only
> backend dev is an intern named **John Intern** wrote the whole ordering system
> with claude Haiku, pushed straight to `main`, and left for a
> semester abroad in Barcelona. He's not answering our calls and will be promptly fired upon return.
>
> Since launch, things have gone wrong. You've been hired as DashDoor's
> emergency **QA team**. John Intern left no tests. Your job is to write them, prove
> what's broken, and save my job before the CEO finds this out on linkedin
> The investor demo is Tuesday at 3:30pm.


## Your mission

1. Figure out what each function should do (read the docstrings in `logic.py`)
2. Write tests for normal inputs
3. Think of edge cases
4. Run your tests
5. Find the bugs

## Setup

```bash
#in your terminal:
python -m venv .venv # if python doesnt work, try python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python db.py        # builds dashdoor.db (run once)
python app.py       # go to your browser: http://127.0.0.1:5000
```

Logins:
- `john / intern ` - John Intern himself (normal account)
- `admin / DashD00r!2024` - staff (can reach `/admin`)

## Where to look

- **`logic.py`** — the core business functions. Every docstring is the spec.
  A function is only "buggy" if it disagrees with its own docstring. This is
  where most of your tests go. Run them with `pytest`.

- **`app.py`** — (extra credit) the Flask routes (login, home, checkout, admin). Two of the bug reports live here. One is about the search box. One is about carts. These are somewhat harder to spot than logic.py's bugs, so i reccomend doing this last.

- **`register.html`** (extra extra credit) Something's fishy about this register page... You will get a bonus prize if you're able to solve why!

## Writing tests

make your own file and start writing your test cases (for example, test_cases.py is a good name) and start with the normal case:

```python
from logic import calculate_subtotal

def test_subtotal_counts_quantity():
    cart = [{"price": 4.50, "quantity": 2}, {"price": 3.00, "quantity": 1}]
    assert calculate_subtotal(cart) == 12.00
```

Run it:

```bash
pytest -q 
```

Then ask yourself, for each function, what's the weird input?

plz fix guys I need this my job is kinda homeless
