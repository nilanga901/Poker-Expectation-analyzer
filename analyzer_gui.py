import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import StringVar



from poker import *
from itertools import combinations
from enum import Enum
import matplotlib.pyplot as plt
import numpy as np
from poker import Card

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
    print(hand)
    if (hand!=[]):
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


class Card:
    def __init__(self, card_str):
        self.card_str = card_str

# def calculate_hand_category_probabilities(cards, deck):
#     # Your implementation for calculating probabilities goes here
#     # This is a placeholder function, replace it with your actual implementation
#     probabilities = {f"Category_{i}": np.random.rand() for i in range(10)}
#     return probabilities

class PokerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Hand Probability Calculator")

        # Initialize variables
        self.player_hand = []
        self.flop = []
        self.turn = []
        self.river = []
        self.pot = 0

        # Create GUI elements
        self.create_input_widgets()
        self.create_plots()

    def create_input_widgets(self):
       # Radio buttons for suits - Player Hand
        ttk.Label(self.root, text="Player Hand 1:").grid(row=0, column=0, padx=5, pady=5)
        self.player_hand_suit_var1 = StringVar()
        self.player_hand_suit_var1.set("h")  # Set default value
        suits = ["❤️", "♦️", "♣️", "♠️"]
        suit_val=["h", "d", "c", "s"]
        for i, suit in enumerate(suits):
            ttk.Radiobutton(self.root, text=suit, variable=self.player_hand_suit_var1, value=suit_val[i]).grid(row=0, column=i + 1, padx=5, pady=5)

        # Dropdown list for cards - Player Hand
        self.player_hand_card_var1 = StringVar()
        self.player_hand_card_var1.set("2")  # Set default value
        cards = [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]
        card_dropdown = ttk.Combobox(self.root, textvariable=self.player_hand_card_var1, values=cards)
        card_dropdown.grid(row=0, column=5, padx=5, pady=5)
        
        # Radio buttons for suits - Player Hand
        ttk.Label(self.root, text="Player Hand 2:").grid(row=2, column=0, padx=5, pady=5)
        self.player_hand_suit_var2 = StringVar()
        self.player_hand_suit_var2.set("h")  # Set default value
        suits = ["❤️", "♦️", "♣️", "♠️"]
        for i, suit in enumerate(suits):
            ttk.Radiobutton(self.root, text=suit, variable=self.player_hand_suit_var2, value=suit_val[i]).grid(row=2, column=i + 1, padx=5, pady=5)

         # Dropdown list for cards - Player Hand
        self.player_hand_card_var2 = StringVar()
        self.player_hand_card_var2.set("3")  # Set default value
        cards = [str(i) for i in range(2, 10)] + ["t","J", "Q", "K", "A"]
        card_dropdown = ttk.Combobox(self.root, textvariable=self.player_hand_card_var2, values=cards)
        card_dropdown.grid(row=2, column=5, padx=5, pady=5)

 # Radio buttons for suits - Flop
        ttk.Label(self.root, text="Flop cards:").grid(row=3, column=0, padx=5, pady=5)
        self.flop_suit_vars = [StringVar() for _ in range(3)]
        default_suit = ""  # Set default value
        for i in range(3):
            self.flop_suit_vars[i].set(default_suit)
            for j, suit in enumerate(suits):
                ttk.Radiobutton(self.root, text=suit, variable=self.flop_suit_vars[i], value=suit_val[j]).grid(row=3 + i, column=j + 1, padx=5, pady=5)

        # Dropdown lists for cards - Flop
        # ttk.Label(self.root, text="Flop Cards:").grid(row=5, column=0, padx=5, pady=5)
        self.flop_card_vars = [StringVar() for _ in range(3)]
        default_card = ""  # Set default value
        for i in range(3):
            flop_card_dropdown = ttk.Combobox(self.root, textvariable=self.flop_card_vars[i], values=cards)
            flop_card_dropdown.grid(row=3 + i, column=5, padx=5, pady=5)
            self.flop_card_vars[i].set(default_card)


        # Radio buttons for suits - Turn
        ttk.Label(self.root, text="Turn:").grid(row=6, column=0, padx=5, pady=5)
        self.turn_suit_var = StringVar()
        self.turn_suit_var.set(" ")  # Set default value
        for i, suit in enumerate(suits):
            ttk.Radiobutton(self.root, text=suit, variable=self.turn_suit_var, value=suit_val[i]).grid(row=6, column=i + 1, padx=5, pady=5)

        # Dropdown list for cards - Turn
        self.turn_card_var = StringVar()
        self.turn_card_var.set("")  # Set default value
        turn_card_dropdown = ttk.Combobox(self.root, textvariable=self.turn_card_var, values=cards)
        turn_card_dropdown.grid(row=6, column=5, padx=5, pady=5)

        # Radio buttons for suits - River
        ttk.Label(self.root, text="River :").grid(row=7, column=0, padx=5, pady=5)
        self.river_suit_var = StringVar()
        self.river_suit_var.set("")  # Set default value
        for i, suit in enumerate(suits):
            ttk.Radiobutton(self.root, text=suit, variable=self.river_suit_var, value=suit_val[i]).grid(row=7, column=i + 1, padx=5, pady=5)

        # Dropdown list for cards - River
        # ttk.Label(self.root, text="River Card:").grid(row=7, column=5, padx=5, pady=5)
        self.river_card_var = StringVar()
        self.river_card_var.set("")  # Set default value
        river_card_dropdown = ttk.Combobox(self.root, textvariable=self.river_card_var, values=cards)
        river_card_dropdown.grid(row=7, column=5, padx=5, pady=5)

        ttk.Label(self.root, text="Pot:").grid(row=8, column=0, padx=5, pady=5)
        self.pot_entry = ttk.Entry(self.root)
        self.pot_entry.insert(100, "100")  # Set default value to zero
        self.pot_entry.grid(row=8, column=1, padx=5, pady=5)
        
        # Create a button to trigger calculations and update plots
        ttk.Button(self.root, text="Update Plots", command=self.update_plots).grid(row=8, column=5, columnspan=3, pady=10)

    def create_plots(self):
        # Create a figure and axis for the plots
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=10, column=4, columnspan=2)


    def update_plots(self):
        # Get user input values
        from poker import Card
        player_hand_str1 = self.player_hand_card_var1.get()+self.player_hand_suit_var1.get()
        player_hand_str2 = self.player_hand_card_var2.get()+self.player_hand_suit_var2.get()
        print(Card(player_hand_str1))
        print(Card(player_hand_str2))
        self.player_hand = [Card(player_hand_str1),Card(player_hand_str2)]
        
        self.flop=[]
        for i in range(3):
             if((self.flop_card_vars[i].get()+self.flop_suit_vars[i].get()).strip()):
                 self.flop.append(Card(self.flop_card_vars[i].get()+self.flop_suit_vars[i].get()))

        turn_str = self.turn_card_var.get()+self.turn_suit_var.get()
        self.turn = []
        if turn_str.strip():
            self.turn = [Card(turn_str)]

        river_str = self.river_card_var.get()+self.river_suit_var.get()
        self.river = []
        if river_str.strip():
            self.river = [Card(river_str)]

        self.pot = int(self.pot_entry.get())

        # Update the plots
        self.update_probability_plots()

    def update_probability_plots(self):
        # Update your probability calculation code here based on user input
        from poker import Card
        deck = list(Card)
        probabilities = calculate_hand_category_probabilities(self.player_hand+self.flop+self.turn+self.river,deck)
        
        #Sort probabilities for plotting
        sorted_probabilities = {category: probabilities[category] for category in sorted(probabilities, key=probabilities.get, reverse=True)}
        from poker import Card    
        deck = list(Card)
        if (self.player_hand!=[]):
            for card in self.player_hand:
                deck.remove(card)
        
        op_probabilities = calculate_hand_category_probabilities(self.flop+self.turn+self.river,deck)
        
        x_labels = [category.name for category in probabilities.keys()]


        # Plot PDF for Player
        bar_width = 0.35
        index = np.arange(len(x_labels))

        # Plot for Player
        self.ax1.clear()
        self.ax1.bar(index, probabilities.values(), bar_width, color='blue', label='Player')
        self.ax1.bar(index + bar_width, op_probabilities.values(), bar_width, color='orange', label='Others')
        self.ax1.set_title('PDF for Player')
        self.ax1.set_xlabel('Hand Category')
        self.ax1.set_ylabel('Probability')
        self.ax1.set_xticks(index + bar_width / 2)
        self.ax1.set_xticklabels(x_labels, rotation=45, ha='right')
        self.ax1.legend()

        # Redraw canvas
        self.canvas.draw()
        
        player_prob=list(probabilities.values())
        opp_prob=list(op_probabilities.values())
        win_prob=0
        lose_prob=0
        
        for i,label in enumerate(x_labels):
            win_prob+=player_prob[i]*(sum(opp_prob[:i])+opp_prob[i]/2)
            lose_prob+=player_prob[i]*(sum(opp_prob[i+1:])+opp_prob[i]/2)


        print(f" Win Probability - {win_prob:.4f} , Loose Probability - {lose_prob:.4f}")

        expect=[]
        for call in np.arange(0,3*self.pot,self.pot/10):
            expect.append((call+self.pot)*win_prob-lose_prob*call)

        calls = list(np.arange(0, 3 * self.pot, self.pot / 10))


        # Placeholder for the second plot - replace with actual implementation
        # You can use the second axis (self.ax2) for the second plot
        # Example: self.ax2.plot(x_data, y_data, label='Second Plot')
        self.ax2.clear()
        self.ax2.plot(calls, expect, label='Second Plot')
        self.ax2.set_title('Second Plot')
        self.ax2.set_xlabel('Call Amount')
        self.ax2.set_ylabel('Expected Value')
        self.ax2.axhline(y=0, color='r', linestyle='--', label='Zero Expectation')
        self.ax2.axvline(x=self.pot, color='g', linestyle='--', label='Pot Value')
        self.ax2.legend()

        # Redraw canvas
        self.canvas.draw()
        
        zero_crossing_call = calls[np.argmax(np.diff(np.sign(expect)) != 0)]
        info_label_text = f"The call value where expectation crosses zero: {zero_crossing_call:.2f}"

        info_label = ttk.Label(self.root, text=info_label_text)
        info_label.grid(row=10, column=0, columnspan=2)

        print(f"The call value where expectation crosses zero: {zero_crossing_call:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    poker_gui = PokerGUI(root)
    root.mainloop()
