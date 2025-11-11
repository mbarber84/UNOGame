import random  # Import the random module for shuffling the deck

def build_deck():
    """
    Build a standard UNO deck.
    
    Returns:
        deck (list): A list containing all UNO cards as strings.
    """
    colors = ['Red', 'Yellow', 'Green', 'Blue']  # The four colors in UNO
    values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "Draw Two"]
    wilds = ["Wild", "Wild Draw Four"]  # Wild cards that can be played anytime
    deck = []

    # Create numbered and action cards for each color
    for color in colors:
        for value in values:
            card = f"{color} {value}"  # Combine color and value
            deck.append(card)  # Add the card to the deck
            if value != "0":  # All cards except 0 appear twice in UNO
                deck.append(card)

    # Add 4 Wild and 4 Wild Draw Four cards
    for _ in range(4):
        deck.extend(wilds)

    return deck  # Return the completed deck


def shuffle_deck(deck):
    """
    Shuffle the UNO deck in place.
    
    Args:
        deck (list): The deck to shuffle.
    
    Returns:
        deck (list): The shuffled deck.
    """
    random.shuffle(deck)  # Shuffle the deck randomly
    return deck


def draw_cards(deck, num_cards):
    """
    Draw a number of cards from the top of the deck.
    
    Args:
        deck (list): The deck to draw from.
        num_cards (int): Number of cards to draw.
    
    Returns:
        drawn (list): List of drawn cards.
    """
    drawn = [deck.pop(0) for _ in range(num_cards)]  # Remove cards from the top of the deck
    return drawn
