import random
from deck import build_deck, shuffle_deck, draw_cards
from player import show_hand, can_play

def is_special_card(card):
    """
    Check if a card is a special card (action or wild).

    Args:
        card (str): The card to check.

    Returns:
        bool: True if card is special, False otherwise.
    """
    special_keywords = ["Skip", "Reverse", "Draw Two", "Draw Four", "Wild"]
    return any(word in card for word in special_keywords)


def setup_game():
    """
    Initialize the game:
        - Build and shuffle deck
        - Draw initial hands for players
        - Determine AI players
        - Set up UNO declarations
        - Set starting card and color/value

    Returns:
        tuple: All relevant game variables for starting play
    """
    uno_deck = shuffle_deck(build_deck())
    discard_pile = [uno_deck.pop(0)]  # Start with the top card as discard
    players = []
    ai_players = []

    # Get number of players (2–4)
    num_players = int(input("Enter total number of players (2–4): "))
    while num_players < 2 or num_players > 4:
        num_players = int(input("Invalid number. Enter between 2 and 4: "))

    # Get number of AI players
    num_ai = int(input(f"How many AI players? (0–{num_players}): "))
    while num_ai < 0 or num_ai > num_players:
        num_ai = int(input(f"Invalid. Enter between 0 and {num_players}: "))

    # Draw 5 cards for each player
    for _ in range(num_players):
        players.append(draw_cards(uno_deck, 5))

    # Identify AI players (last N players)
    ai_players = list(range(num_players - num_ai, num_players))
    uno_declared = [False] * num_players  # Track UNO declarations

    # Determine starting color and value from the first discard
    first_card = discard_pile[0].split(" ", 1)
    current_color = first_card[0]
    current_value = first_card[1] if len(first_card) > 1 else "Any"

    return uno_deck, discard_pile, players, current_color, current_value, num_players, ai_players, uno_declared


def play_game():
    """
    Main game loop for UNO:
        - Handles player and AI turns
        - Applies special card effects
        - Manages UNO declarations and penalties
        - Checks win conditions
    """
    # Initialize game variables
    uno_deck, discard_pile, players, current_color, current_value, num_players, ai_players, uno_declared = setup_game()
    colors = ['Red', 'Yellow', 'Green', 'Blue']
    play_direction = 1  # 1 = clockwise, -1 = counterclockwise
    player_turn = 0
    playing = True

    while playing:
        print(f"\nTop card: {discard_pile[-1]}")
        print("------------------------------")

        # Check for UNO penalty if player forgot to declare last turn
        if len(players[player_turn]) == 1 and not uno_declared[player_turn]:
            print(f"Player {player_turn + 1} failed to declare UNO! Drawing 2 penalty cards.")
            players[player_turn].extend(draw_cards(uno_deck, 2))
        uno_declared[player_turn] = False  # Reset declaration

        # PLAYER TURN
        if player_turn in ai_players:
            # AI TURN
            print(f"AI Player {player_turn + 1}'s Turn")
            playable_cards = [card for card in players[player_turn] if can_play(current_color, current_value, [card])]

            if playable_cards:
                # AI randomly chooses a playable card
                chosen_card = random.choice(playable_cards)
                print(f"AI played: {chosen_card}")
                players[player_turn].remove(chosen_card)
                discard_pile.append(chosen_card)
            else:
                # No playable card: draw one
                print("AI cannot play. Drawing one card.")
                players[player_turn].extend(draw_cards(uno_deck, 1))
                chosen_card = None
        else:
            # HUMAN TURN
            show_hand(player_turn, players[player_turn])
            if can_play(current_color, current_value, players[player_turn]):
                card_index = int(input("Select a card to play: ")) - 1
                chosen_card = players[player_turn][card_index]

                # Keep prompting if invalid card selected
                while not can_play(current_color, current_value, [chosen_card]):
                    card_index = int(input("You can’t play that card. Choose another: ")) - 1
                    chosen_card = players[player_turn][card_index]

                # Play selected card
                discard_pile.append(players[player_turn].pop(card_index))
                print(f"You played: {chosen_card}")
            else:
                # No playable card: draw one
                print("You cannot play. Drawing one card.")
                players[player_turn].extend(draw_cards(uno_deck, 1))
                chosen_card = None

        # Update current color/value and handle special card effects
        if chosen_card:
            split_card = discard_pile[-1].split(" ", 1)
            current_color = split_card[0]
            current_value = split_card[1] if len(split_card) > 1 else "Any"

            # Handle special cards
            if "Wild" in chosen_card:
                if player_turn in ai_players:
                    current_color = random.choice(colors)
                    print(f"AI chooses {current_color}")
                else:
                    # Prompt human player to choose color
                    for i, c in enumerate(colors, 1):
                        print(f"{i}) {c}")
                    new_color = int(input("Choose a color: "))
                    current_color = colors[new_color - 1]

            elif "Reverse" in chosen_card:
                play_direction *= -1
                print("Play direction reversed!")

            elif "Skip" in chosen_card:
                print("Next player skipped!")
                player_turn = (player_turn + play_direction) % num_players

            elif "Draw Two" in chosen_card:
                next_player = (player_turn + play_direction) % num_players
                players[next_player].extend(draw_cards(uno_deck, 2))
                print(f"Player {next_player + 1} draws 2 cards!")

            elif "Draw Four" in chosen_card:
                next_player = (player_turn + play_direction) % num_players
                players[next_player].extend(draw_cards(uno_deck, 4))
                print(f"Player {next_player + 1} draws 4 cards!")

        # Check for UNO declaration
        if len(players[player_turn]) == 1:
            if player_turn in ai_players:
                # AI randomly declares UNO 80% of the time
                if random.random() < 0.8:
                    print(f"AI Player {player_turn + 1} declares UNO!")
                    uno_declared[player_turn] = True
                else:
                    print(f"AI Player {player_turn + 1} forgets to declare UNO!")
                    uno_declared[player_turn] = False
            else:
                # Human player declares UNO
                declare = input("You have 1 card left! Type 'UNO' to declare: ").strip().lower()
                uno_declared[player_turn] = (declare == "uno")

        # WIN CONDITION
        if len(players[player_turn]) == 0:
            last_card = discard_pile[-1]
            if is_special_card(last_card):
                # Cannot finish on special card
                print("You cannot finish on a special card! Drawing one card instead.")
                players[player_turn].extend(draw_cards(uno_deck, 1))
            else:
                print(f"\n Player {player_turn + 1} wins!")
                playing = False
                break

        # Move to next player based on direction
        player_turn = (player_turn + play_direction) % num_players

    print("Game Over")
