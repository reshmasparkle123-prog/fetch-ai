
def validate_stock(opening, received, issued, closing):
    # Check whether the quantities are valid
    if opening < 0 or received < 0 or issued < 0 or closing < 0:
        return {
            "valid": False,
            "message": "Invalid report: stock quantities cannot be negative."
        }

    # Calculate the expected closing stock
    expected_closing = opening + received - issued

    # Check whether enough stock was available to issue
    if issued > opening + received:
        return {
            "valid": False,
            "message": "Invalid report: issued stock exceeds available stock."
        }

    # Compare calculated and reported closing stock
    if expected_closing == closing:
        return {
            "valid": True,
            "message": "Stock report passed the calculation check."
        }

    return {
        "valid": False,
        "message": (
            f"Stock mismatch! Expected closing stock: "
            f"{expected_closing}, but reported closing stock: {closing}."
        )
    }


# Test the function
if __name__ == "__main__":
    result = validate_stock(
        opening=100,
        received=50,
        issued=30,
        closing=120
    )

    print(result)
