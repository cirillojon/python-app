import random
import tkinter as tk

class HomeScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Launcher")
        self.currency = 100 # initialize currency

        self.games = {
            "Coin Toss Betting": CoinTossGame,
            "Number Guessing Game": NumberGuessingGame,
            "Rock Paper Scissors": RockPaperScissorsGame
        }

        for i, (name, game_class) in enumerate(self.games.items()):
            button = tk.Button(self, text=name, command=lambda c=game_class: self.launch_game(c))
            button.pack(pady=10)

        self.current_game = None

    def launch_game(self, game_class):
        if self.current_game:
            self.current_game.destroy()  # remove the previous game instance

        game = game_class(self)
        game.pack()
        self.current_game = game

    def update_currency(self, amount):
        self.currency += amount

class CoinTossGame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

        # Add a balance attribute to keep track of the user's currency
        self.balance = 100

        self.balance_label = tk.Label(self, text=f"Balance: {self.balance} currency")
        self.balance_label.pack()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Coin Toss")
        self.title_label.pack()

        self.instructions_label = tk.Label(self, text="Guess heads or tails:")
        self.instructions_label.pack()

        self.guess_entry = tk.Entry(self)
        self.guess_entry.pack()

        # Modify the toss_coin function to include betting logic
        self.toss_button = tk.Button(self, text="Toss Coin", command=self.toss_coin)
        self.toss_button.pack()

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

    def toss_coin(self):
        guess = self.guess_entry.get().lower()
        if guess not in ['heads', 'tails']:
            self.result_label.config(text="Please enter 'heads' or 'tails'")
        else:
            coin = random.choice(['heads', 'tails'])

            # Add betting logic
            if self.bet_amount > self.currency:
                self.result_label.config(text="Not enough currency to place bet.")
                return

            if guess == coin:
                self.result_label.config(text="Congratulations, you guessed correctly!")
                self.currency += self.bet_amount
            else:
                self.result_label.config(f"Sorry, the coin landed on {coin}. Better luck next time!")
                self.currency -= self.bet_amount

            # Update currency label and reset bet amount
            self.currency_label.config(text=f"Currency: {self.currency}")
            self.bet_amount = 0
            self.bet_label.config(text="Bet amount: 0")

    # Add a function to handle setting the bet amount
    def set_bet_amount(self, amount):
        self.bet_amount = amount
        self.bet_label.config(text=f"Bet amount: {self.bet_amount}")

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Coin Toss")
        self.title_label.pack()

        self.instructions_label = tk.Label(self, text="Guess heads or tails:")
        self.instructions_label.pack()

        self.guess_entry = tk.Entry(self)
        self.guess_entry.pack()

        self.toss_button = tk.Button(self, text="Toss Coin", command=self.toss_coin)
        self.toss_button.pack()


        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

        # Add a frame for the betting controls
        self.bet_frame = tk.Frame(self)
        self.bet_frame.pack(pady=10)

       # Add buttons for different bet amounts
        for amount in [10, 20, 50]:
            bet_button = tk.Button(self.bet_frame, text=f"Bet {amount}", command=lambda a=amount: self.set_bet_amount(a))
            bet_button.pack(side="left", padx=5)

        # Add a label to display the current bet amount
        self.bet_amount_label = tk.Label(self.bet_frame, text="Current bet: 0")
        self.bet_amount_label.pack(side='left', padx=5)

    def set_bet_amount(self, amount):
        self.bet_amount = amount
        self.bet_amount_label.config(text=f"Current bet: {self.bet_amount}")

    def toss_coin(self):
        guess = self.guess_entry.get().lower()
        if guess not in ['heads', 'tails']:
            self.result_label.config(text="Please enter 'heads' or 'tails'")
        elif not self.bet_amount:
            self.result_label.config(text="Please place a bet first")
        else:
            coin = random.choice(['heads', 'tails'])
            if guess == coin:
                self.result_label.config(text="Congratulations, you guessed correctly!")
                self.win_bet()
            else:
                self.result_label.config(text=f"Sorry, the coin landed on {coin}. Better luck next time!")
                self.lose_bet()

    def win_bet(self):
        self.balance += self.bet_amount
        self.balance_label.config(text=f"Balance: {self.balance}")
        self.result_label.config(text=f"You won {self.bet_amount}!")

    def lose_bet(self):
        self.balance -= self.bet_amount
        self.balance_label.config(text=f"Balance: {self.balance}")
        self.result_label.config(text=f"You lost {self.bet_amount} :( ")

            
class NumberGuessingGame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Number Guessing Game")
        self.title_label.pack()

        self.instructions_label = tk.Label(self, text="Guess a number between 1 and 10:")
        self.instructions_label.pack()

        self.guess_entry = tk.Entry(self)
        self.guess_entry.pack()

        self.guess_button = tk.Button(self, text="Guess", command=self.check_guess)
        self.guess_button.pack()

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

        self.play_again_button = tk.Button(self, text="Play again", command=self.reset_game, state=tk.DISABLED)
        self.play_again_button.pack()

        self.answer = random.randint(1, 10)

    def check_guess(self):
        guess = self.guess_entry.get()
        if not guess.isdigit():
            self.result_label.config(text="Please enter a valid number.")
        elif int(guess) < 1 or int(guess) > 10:
            self.result_label.config(text="Number must be between 1 and 10.")
        elif int(guess) == self.answer:
            self.result_label.config(text="Congratulations, you guessed the number!")
            self.play_again_button.config(state=tk.NORMAL)
            self.guess_button.config(state=tk.DISABLED)
            self.guess_entry.config(state=tk.DISABLED)
        else:
            self.result_label.config(text="Wrong, try again.")

    def reset_game(self):
        self.answer = random.randint(1, 10)
        self.result_label.config(text="")
        self.guess_entry.delete(0, tk.END)
        self.guess_button.config(state=tk.NORMAL)
        self.guess_entry.config(state=tk.NORMAL)
        self.play_again_button.config(state=tk.DISABLED)

class RockPaperScissorsGame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Rock Paper Scissors")
        self.title_label.pack()

        self.player_choice_label = tk.Label(self, text="Choose rock, paper, or scissors:")
        self.player_choice_label.pack()

        self.rock_button = tk.Button(self, text="Rock", command=lambda: self.play_game("rock"))
        self.rock_button.pack()

        self.paper_button = tk.Button(self, text="Paper", command=lambda: self.play_game("paper"))
        self.paper_button.pack()

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

        self.scissors_button = tk.Button(self, text="Scissors", command=lambda: self.play_game("scissors"))
        self.scissors_button.pack()


    def play_game(self, player_choice):
        computer_choice = random.choice(["rock", "paper", "scissors"])

        if player_choice == computer_choice:
            result = "It's a tie!"
        elif player_choice == "rock" and computer_choice == "scissors":
            result = "You win!"
        elif player_choice == "paper" and computer_choice == "rock":
            result = "You win!"
        elif player_choice == "scissors" and computer_choice == "paper":
            result = "You win!"
        else:
            result = "You lose!"

        self.result_label.config(text=f"Computer chose {computer_choice}. {result}")

root = HomeScreen()
root.geometry("400x400") 
root.mainloop()






