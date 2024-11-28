from tkinter import *
import random

class TicTacToe:
    def __init__(self, window):
        self.window = window
        self.window.title("Tic-Tac-Toe")
        self.players = ["x", "o"]
        self.player = random.choice(self.players)
        self.buttons = []
        self.board_size = 3
        self.time_limit = 10
        self.timer_id = None
        self.timer_enabled = True
        self.scores = { "x": 0, "o": 0 }

        # Default Colors
        self.player_colors = {"x": "lightblue", "o": "lightpink"}
        self.default_color = "white"

        # UI Setup
        self.label = Label(text=self.player + " turn", font=('consolas', 40), bg=self.player_colors[self.player])
        self.label.pack(side="top")

        self.timer_label = Label(text=f"Time Left: {self.time_limit}s", font=('consolas', 20))
        self.timer_label.pack(side="top")

        self.score_label = Label(text=f"Scores - X: {self.scores['x']} O: {self.scores['o']}", font=('consolas', 20))
        self.score_label.pack(side="top")

        self.reset_button = Button(text="Restart", font=('consolas', 20), command=self.new_game)
        self.reset_button.pack(side="top")

        self.reset_score_button = Button(text="Reset Scores", font=('consolas', 20), command=self.reset_scores)
        self.reset_score_button.pack(side="top")

        self.timer_toggle_button = Button(text="Toggle Timer", font=('consolas', 20), command=self.toggle_timer)
        self.timer_toggle_button.pack(side="top")

        self.tutorial_button = Button(text="Tutorial", font=('consolas', 20), command=self.show_tutorial)
        self.tutorial_button.pack(side="top")

        self.frame = Frame(window)
        self.frame.pack()

        # Board Size Selection
        self.size_frame = Frame(window)
        self.size_frame.pack(side="bottom")

        for size in range(3, 6):
            Button(self.size_frame, text=f"{size}x{size}", font=('consolas', 15),
                   command=lambda size=size: self.set_board_size(size)).pack(side="left", padx=10)

        # Theme Selection
        self.theme_frame = Frame(window)
        self.theme_frame.pack(side="bottom", pady=10)

        Label(self.theme_frame, text="Themes:", font=('consolas', 15)).pack(side="left", padx=10)

        Button(self.theme_frame, text="Blue & Pink", font=('consolas', 15),
               command=lambda: self.set_theme("lightblue", "lightpink")).pack(side="left", padx=10)

        Button(self.theme_frame, text="Green & Orange", font=('consolas', 15),
               command=lambda: self.set_theme("lightgreen", "orange")).pack(side="left", padx=10)

        Button(self.theme_frame, text="Purple & Yellow", font=('consolas', 15),
               command=lambda: self.set_theme("purple", "yellow")).pack(side="left", padx=10)

        Button(self.theme_frame, text="Dark Mode", font=('consolas', 15),
               command=lambda: self.set_theme("black", "white", True)).pack(side="left", padx=10)

        # Symbol Selection
        self.symbol_frame = Frame(window)
        self.symbol_frame.pack(side="bottom", pady=10)

        Label(self.symbol_frame, text="Symbols:", font=('consolas', 15)).pack(side="left", padx=10)

        Button(self.symbol_frame, text="X & O", font=('consolas', 15),
               command=lambda: self.set_symbols("X", "O")).pack(side="left", padx=10)

        Button(self.symbol_frame, text="/ \\", font=('consolas', 15),
               command=lambda: self.set_symbols("/", "\\")).pack(side="left", padx=10)

        Button(self.symbol_frame, text="A & B", font=('consolas', 15),
               command=lambda: self.set_symbols("A", "B")).pack(side="left", padx=10)

        self.set_board_size(self.board_size)
        self.new_game()

    def set_board_size(self, size):
        self.board_size = size
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.buttons[row][col] = Button(self.frame, text="", font=('consolas', 40), width=5, height=2,
                                               command=lambda row=row, col=col: self.next_turn(row, col))
                self.buttons[row][col].grid(row=row, column=col)

        self.new_game()

    def set_theme(self, color1, color2, dark_mode=False):
        self.player_colors = {"x": color1, "o": color2}
        self.default_color = color1 if dark_mode else "white"
        self.new_game()

    def set_symbols(self, symbol1, symbol2):
        self.players = [symbol1, symbol2]
        self.new_game()

    def new_game(self):
        self.player = random.choice(self.players)
        self.label.config(text=self.player + " turn", bg=self.player_colors[self.player])

        for row in range(self.board_size):
            for col in range(self.board_size):
                self.buttons[row][col].config(text="", bg=self.default_color)

        self.reset_timer()

    def reset_scores(self):
        self.scores = { "x": 0, "o": 0 }
        self.update_score_label()

    def update_score_label(self):
        self.score_label.config(text=f"Scores - X: {self.scores['x']} O: {self.scores['o']}")

    def reset_timer(self):
        if self.timer_enabled:
            self.time_limit = 10
            self.timer_label.config(text=f"Time Left: {self.time_limit}s")
            if self.timer_id:
                self.window.after_cancel(self.timer_id)
            self.timer_id = self.window.after(1000, self.countdown)

    def countdown(self):
        if self.time_limit > 0 and self.timer_enabled:
            self.time_limit -= 1
            self.timer_label.config(text=f"Time Left: {self.time_limit}s")
            self.timer_id = self.window.after(1000, self.countdown)
        elif self.timer_enabled:
            self.label.config(text=f"{self.player} lost by timeout!", bg="red")
            self.stop_timer()

    def stop_timer(self):
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None

    def toggle_timer(self):
        self.timer_enabled = not self.timer_enabled
        if not self.timer_enabled:
            self.stop_timer()
            self.timer_label.config(text="Timer Disabled")
        else:
            self.reset_timer()

    def next_turn(self, row, column):
        if self.buttons[row][column]['text'] == "" and self.check_winner() is False:
            self.buttons[row][column]['text'] = self.player
            if self.check_winner() is False:
                self.player = self.players[1] if self.player == self.players[0] else self.players[0]
                self.label.config(text=self.player + " turn", bg=self.player_colors[self.player])
                self.reset_timer()
            elif self.check_winner() is True:
                self.label.config(text=self.player + " wins", bg="lightgreen")
                self.scores[self.player] += 1
                self.update_score_label()
                self.stop_timer()
            elif self.check_winner() == "Tie":
                self.label.config(text="Tie!", bg="yellow")
                self.stop_timer()

    def check_winner(self):
        for row in range(self.board_size):
            if all(self.buttons[row][col]['text'] == self.player for col in range(self.board_size)) and self.buttons[row][0]['text'] != "":
                for col in range(self.board_size):
                    self.buttons[row][col].config(bg="gold")
                return True

        for col in range(self.board_size):
            if all(self.buttons[row][col]['text'] == self.player for row in range(self.board_size)) and self.buttons[0][col]['text'] != "":
                for row in range(self.board_size):
                    self.buttons[row][col].config(bg="gold")
                return True

        if all(self.buttons[i][i]['text'] == self.player for i in range(self.board_size)) and self.buttons[0][0]['text'] != "":
            for i in range(self.board_size):
                self.buttons[i][i].config(bg="gold")
            return True

        if all(self.buttons[i][self.board_size-i-1]['text'] == self.player for i in range(self.board_size)) and self.buttons[0][self.board_size-1]['text'] != "":
            for i in range(self.board_size):
                self.buttons[i][self.board_size-i-1].config(bg="gold")
            return True

        if not self.empty_spaces():
            for row in range(self.board_size):
                for col in range(self.board_size):
                    self.buttons[row][col].config(bg="yellow")
            return "Tie"

        return False

    def empty_spaces(self):
        return any(self.buttons[row][col]['text'] == "" for row in range(self.board_size) for col in range(self.board_size))

    def show_tutorial(self):
        tutorial_window = Toplevel(self.window)
        tutorial_window.title("How to Play Tic-Tac-Toe")
        tutorial_label = Label(tutorial_window, text=(
            "Tic-Tac-Toe Rules:\n"
            "1. The game is played on a grid of 3x3 (or larger, depending on board size).\n"
            "2. Players take turns placing their symbols (X or O) in empty squares.\n"
            "3. The first player to get 3 of their symbols in a row (horizontally, vertically, or diagonally) wins.\n"
            "4. If all squares are filled and no player has 3 in a row, the game ends in a tie.\n"
            "5. You have a time limit to make your move; running out of time results in a loss."
        ), font=('consolas', 15), padx=20, pady=20, wraplength=400)
        tutorial_label.pack()

if __name__ == "__main__":
    window = Tk()
    game = TicTacToe(window)
    window.mainloop()
