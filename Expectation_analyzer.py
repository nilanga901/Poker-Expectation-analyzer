from poker import *
from itertools import combinations
from poker import Card
from enum import Enum
import matplotlib.pyplot as plt
import numpy as np


class HandRank(Enum):
    HIGH_CARD = 'High card'
    ONE_PAIR = 'One pair'
    TWO_PAIR = 'Two pair'
    THREE_OF_A_KIND = 'Three of a kind'
    STRAIGHT = 'Straight'
    FLUSH = 'Flush'
    FULL_HOUSE = 'Full house'
    FOUR_OF_A_KIND = 'Four of a kind'
    STRAIGHT_FLUSH = 'Straight flush'


def evaluate_hand(cards):
    # Count occurrences of each rank
    rank_count = {}
    for card in cards:
        rank_count[card.rank] = rank_count.get(card.rank, 0) + 1
        
    suit_count = {}
    for card in cards:
        suit_count[card.suit] = suit_count.get(card.suit, 0) + 1

    # Check for four of a kind
    if 4 in rank_count.values():
        return HandRank.FOUR_OF_A_KIND

    # Check for full house
    if 3 in rank_count.values() and 2 in rank_count.values():
        return HandRank.FULL_HOUSE

    # Check for three of a kind
    if 3 in rank_count.values():
        return HandRank.THREE_OF_A_KIND

    # Check for two pairs
    if list(rank_count.values()).count(2) == 2:
        return HandRank.TWO_PAIR

    # Check for one pair
    if 2 in rank_count.values():
        return HandRank.ONE_PAIR

    # Check for straight or straight flush
    for combo in combinations(cards, 5):
        sorted_ranks = sorted([card.rank for card in list(combo)])
        if ((len(set(sorted_ranks)) == 5 and Rank.difference(sorted_ranks[-1],sorted_ranks[0])==4) or set(sorted_ranks)==set([Rank('2'), Rank('3'), Rank('4'), Rank('5'), Rank('A')]) ):
            if len(set(card.suit for card in combo)) == 1:
                return HandRank.STRAIGHT_FLUSH
            else:
                return HandRank.STRAIGHT
        
    # Check for flush
    if 5 in suit_count.values():
        return HandRank.FLUSH

    # If none of the above, it's a high card
    return HandRank.HIGH_CARD



def calculate_hand_category_probabilities(hand,deck):
    # Remove player's hand and flop cards from the deck
    for card in hand:
        deck.remove(card)

    # Generate all possible combinations of unknown cards
    possible_unknwn_combinations = list(combinations(deck, 7-len(hand)))
    total_combinations = len(possible_unknwn_combinations)

    probabilities = {category: 0 for category in HandRank}

    for turn_river_combination in possible_unknwn_combinations:
        # Add player's hand, flop, turn, and river cards
        all_cards = hand + list(turn_river_combination)

        # Evaluate the hand
        hand_rank = evaluate_hand(all_cards)

        # Update probabilities dictionary
        probabilities[hand_rank] += 1

    # Normalize probabilities
    normalized_probabilities = {category: count / total_combinations for category, count in probabilities.items()}

    return normalized_probabilities
turn=[]
river=[]


# Example usage
player_hand = [Card('8s'), Card('ah')]
flop = [Card('Ah'), Card('Qd'), Card('2c')]
turn=[Card('tc')]
river=[Card('9d')]
pot=100

deck = list(Card)
probabilities = calculate_hand_category_probabilities(player_hand+flop+turn+river,deck)

#Sort probabilities for plotting
sorted_probabilities = {category: probabilities[category] for category in sorted(probabilities, key=probabilities.get, reverse=True)}

# # Convert enum values to strings
# x_labels = [category.name for category in sorted_probabilities.keys()]

# # Plot PDF (bar chart)
# plt.bar(x_labels, sorted_probabilities.values(), color='blue')
# plt.title(' (PDF) for Player')
# plt.xlabel('Hand Category')
# plt.ylabel('Probability')
# plt.xticks(rotation=45, ha='right')
# plt.show()


deck = list(Card)
for card in player_hand:
    deck.remove(card)

op_probabilities = calculate_hand_category_probabilities(flop+turn+river,deck)

x_labels = [category.name for category in probabilities.keys()]

# Plot PDF for Player and Others in a double bar graph
bar_width = 0.35
index = np.arange(len(x_labels))

# Plot for Player
plt.bar(index, probabilities.values(), bar_width, color='blue', label='Player')

# Plot for Others
plt.bar(index + bar_width, op_probabilities.values(), bar_width, color='orange', label='Others')

# Configure the plot
plt.title('PDF for Player and Others')
plt.xlabel('Hand Category')
plt.ylabel('Probability')
plt.xticks(index + bar_width / 2, x_labels, rotation=45, ha='right')
plt.legend()

# Show the plot
plt.show()



player_prob=list(probabilities.values())
opp_prob=list(op_probabilities.values())
win_prob=0
lose_prob=0
for i,label in enumerate(x_labels):
    win_prob+=player_prob[i]*(sum(opp_prob[:i])+opp_prob[i]/2)
    lose_prob+=player_prob[i]*(sum(opp_prob[i+1:])+opp_prob[i]/2)


print(f" Win Probability - {win_prob:.4f} , Loose Probability - {lose_prob:.4f}")

expect=[]
for call in np.arange(0,3*pot,pot/10):
    expect.append((call+pot)*win_prob-lose_prob*call)

calls = list(np.arange(0, 3 * pot, pot / 10))

plt.plot(calls, expect)
plt.xlabel('Call Amount')
plt.ylabel('Expected Value')
plt.title('Expected Value vs Call/Raise Amount')
plt.axhline(y=0, color='r', linestyle='--', label='Zero Expectation')
plt.axvline(x=pot, color='g', linestyle='--', label='Pot Value')

plt.show()

zero_crossing_call = calls[np.argmax(np.diff(np.sign(expect)) != 0)]

print(f"The call value where expectation crosses zero: {zero_crossing_call:.2f}")


