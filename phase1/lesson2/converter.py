# --- IMPORTING LIBRARIES ---
import math
from datetime import datetime

# --- FUNCTION WITH RETURN VALUE ---
def convert_currency(amount: float, rate: float) -> float:
    return round(amount * rate, 2)

def convert_kg_to_lbs(kg: float) -> float:
    return round(kg * 2.205, 2)

print(convert_kg_to_lbs(70))
# --- ERROR HANDLING ---
def safe_convert(amount_str: str, rate: float) -> None:
    try:
        amount = float(amount_str)
        result = convert_currency(amount, rate)
        print(f"Converted: ₹{result}")
    except ValueError:
        print(f"Error: '{amount_str}' is not a valid number.")
    except Exception as e:
        print(f"Unexpected error: {e}")

# --- USING IMPORTED LIBRARIES ---
def show_info(amount: float) -> None:
    now = datetime.now()
    rounded = math.ceil(amount)
    print(f"Time     : {now.strftime('%H:%M:%S')}")
    print(f"Rounded  : ₹{rounded}")

# --- RUN ---
print("=== Currency Converter ===")
safe_convert("100", 83.5)
safe_convert("fifty", 83.5)
safe_convert("250.50", 83.5)
show_info(20916.75)