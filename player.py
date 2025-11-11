def show_hand(player_id, hand):
    """
    Display the player's current hand in a readable format.
    
    Args:
        player_id (int): The index of the player (0-based).
        hand (list): The list of cards the player currently holds.
    """
    print(f"\nPlayer {player_id + 1}'s Turn")  # Display which player's turn it is (1-based for readability)
    print("------------------------------")
    
    # List each card in the hand with a number for easy selection
    for i, card in enumerate(hand, start=1):
        print(f"{i}) {card}")
    print("------------------------------")


def can_play(color, value, hand):
    """
    Check if the player has any playable cards based on the current color or value.
    
    Args:
        color (str): The current color on top of the discard pile.
        value (str): The current value on top of the discard pile.
        hand (list): The player's hand to check.
    
    Returns:
        bool: True if the player can play at least one card, False otherwise.
    """
    for card in hand:
        # A card is playable if:
        # 1. It is a Wild card
        # 2. Its color matches the current color
        # 3. Its value matches the current value
        if "Wild" in card or color in card or value in card:
            return True
    return False
