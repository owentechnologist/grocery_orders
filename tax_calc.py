def calculate_income_tax(income: float) -> float:
    # Defined as (limit, rate)
    # Note: Using 23200 as the top of the first bracket
    brackets = [
        (23200, 0.00),
        (94300, 0.12),
        (201050, 0.22),
        (383900, 0.24),
        (487450, 0.32)
    ]
    
    tax_due = 0.0
    previous_limit = 0
    
    for limit, rate in brackets:
        if income > previous_limit:
            # Determine how much of the income falls into this specific bracket
            taxable_in_this_bracket = min(income, limit) - previous_limit
            tax_due += taxable_in_this_bracket * rate
            previous_limit = limit
        else:
            break
            
    # Handle income above the highest defined bracket (over 487,450)
    # If the 32% applies to everything above 383,901 indefinitely, 
    # the logic above handles it up to 487,450.
    if income > 487450:
        # Assuming the top rate of 32% continues for income above 487,450
        tax_due += (income - 487450) * 0.32
        
    return round(tax_due, 2)


if __name__ == "__main__":
    # --- Testing the script ---
    income_input = float(input("Enter total income: "))
    total_tax = calculate_income_tax(income_input)

    print(f"Total tax due for {income_input:,.2f} is: ${total_tax:,.2f}")
