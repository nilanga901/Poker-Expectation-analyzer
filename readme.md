
# Poker Expectation Analyzer

This project is a Python-based application that analyzes the probabilities of different hand categories in poker and calculates the expected value (EV) for a given situation. It provides a graphical user interface (GUI) for inputting the player's hand, community cards (flop, turn, and river), and pot size, and visualizes the probability density functions (PDFs) for the player and opponents, as well as the EV curve for different call/raise amounts.

## Features

- Input player's hand, flop, turn, and river cards using a user-friendly GUI
- Calculate the probabilities of different hand categories for the player and opponents
- Visualize the PDFs for the player and opponents in a double bar chart
- Plot the expected value curve based on the call/raise amount
- Determine the call value where the expectation crosses zero

## Prerequisites

- Python 3.x
- Required Python packages:
  - `tkinter`
  - `matplotlib`
  - `numpy`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/poker-expectation-analyzer.git
```

2. Navigate to the project directory:

```bash
cd poker-expectation-analyzer
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
python poker_gui.py
```

2. The Poker Hand Probability Calculator GUI will open.

3. Input the player's hand, flop, turn, and river cards using the radio buttons and dropdown menus.

4. Enter the pot size in the provided entry field.

5. Click the "Update Plots" button to calculate the probabilities and update the plots.

6. The GUI will display the following plots:
   - A double bar chart showing the PDFs for the player and opponents
   - A line plot showing the expected value curve based on the call/raise amount

7. The call value where the expectation crosses zero will be displayed below the plots.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- The project utilizes the `poker` library for handling card representations and evaluations.
- The GUI is built using the `tkinter` library and integrates `matplotlib` for plotting.
