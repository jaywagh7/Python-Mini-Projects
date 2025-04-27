import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import pygame

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe 🎮")
        self.root.geometry("400x500")

        # Initialize Pygame mixer for sound
        pygame.mixer.init()
        self.click_sound = "click.wav"  # <-- You need to have this file or use a built-in sound

        self.players = {}
        self.scores = {"X": 0, "O": 0}
        self.player = "X"
        self.mode = "Friend"  # Default mode
        self.theme = "Light"

        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.get_player_names()
        self.create_menu()
        self.create_scoreboard()
        self.create_board()

    def get_player_names(self):
        self.players["X"] = simpledialog.askstring("Player X", "Enter name for Player X:")
        self.players["O"] = simpledialog.askstring("Player O", "Enter name for Player O:")

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        mode_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Mode", menu=mode_menu)
        mode_menu.add_command(label="Play vs Friend", command=lambda: self.change_mode("Friend"))
        mode_menu.add_command(label="Play vs Easy AI", command=lambda: self.change_mode("Easy"))
        mode_menu.add_command(label="Play vs Hard AI", command=lambda: self.change_mode("Hard"))

        theme_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_command(label="Light", command=lambda: self.change_theme("Light"))
        theme_menu.add_command(label="Dark", command=lambda: self.change_theme("Dark"))

    def create_scoreboard(self):
        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=("Helvetica", 14))
        self.score_label.pack(pady=10)

    def get_score_text(self):
        return f"{self.players['X']} (X): {self.scores['X']}  |  {self.players['O']} (O): {self.scores['O']}"

    def create_board(self):
        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text="", font=('Helvetica', 24), width=5, height=2,
                                command=lambda row=i, col=j: self.on_click(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        self.update_theme()

    def change_mode(self, mode):
        self.mode = mode
        self.reset_board()

    def change_theme(self, theme):
        self.theme = theme
        self.update_theme()

    def update_theme(self):
        bg_color = "white" if self.theme == "Light" else "#2C2C2C"
        fg_color = "black" if self.theme == "Light" else "white"
        btn_bg = "SystemButtonFace" if self.theme == "Light" else "#4D4D4D"

        self.root.configure(bg=bg_color)
        self.score_label.configure(bg=bg_color, fg=fg_color)

        for row in self.buttons:
            for btn in row:
                btn.configure(bg=btn_bg, fg=fg_color)

    def on_click(self, row, col):
        if self.buttons[row][col]["text"] == "":
            self.play_sound()

            self.buttons[row][col]["text"] = self.player

            if self.check_winner():
                self.scores[self.player] += 1
                self.highlight_winner(self.winning_cells)
                messagebox.showinfo("Game Over", f"{self.players[self.player]} wins!")
                self.update_scoreboard()
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.reset_board()
            else:
                self.player = "O" if self.player == "X" else "X"

                if self.mode in ["Easy", "Hard"] and self.player == "O":
                    self.root.after(500, self.ai_move)

    def play_sound(self):
        try:
            pygame.mixer.Sound(self.click_sound).play()
        except:
            pass  # Sound file missing or error, ignore

    def ai_move(self):
        if self.mode == "Easy":
            self.easy_ai()
        elif self.mode == "Hard":
            self.hard_ai()

    def easy_ai(self):
        empty = [(i, j) for i in range(3) for j in range(3) if self.buttons[i][j]["text"] == ""]
        if empty:
            move = random.choice(empty)
            self.on_click(*move)

    def hard_ai(self):
        best_score = -float('inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["text"] == "":
                    self.buttons[i][j]["text"] = "O"
                    score = self.minimax(False)
                    self.buttons[i][j]["text"] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            self.on_click(*best_move)

    def minimax(self, is_maximizing):
        if self.check_winner(return_bool=True):
            return 1 if self.player == "O" else -1
        if self.check_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = "O"
                        score = self.minimax(False)
                        self.buttons[i][j]["text"] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = "X"
                        score = self.minimax(True)
                        self.buttons[i][j]["text"] = ""
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, return_bool=False):
        board = [[self.buttons[i][j]["text"] for j in range(3)] for i in range(3)]

        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != "":
                self.winning_cells = [(i, 0), (i, 1), (i, 2)]
                return True
            if board[0][i] == board[1][i] == board[2][i] != "":
                self.winning_cells = [(0, i), (1, i), (2, i)]
                return True

        if board[0][0] == board[1][1] == board[2][2] != "":
            self.winning_cells = [(0, 0), (1, 1), (2, 2)]
            return True
        if board[0][2] == board[1][1] == board[2][0] != "":
            self.winning_cells = [(0, 2), (1, 1), (2, 0)]
            return True

        return False if return_bool else None

    def check_draw(self):
        for row in self.buttons:
            for btn in row:
                if btn["text"] == "":
                    return False
        return True

    def highlight_winner(self, cells):
        for (i, j) in cells:
            self.buttons[i][j].config(bg='lightgreen')

    def update_scoreboard(self):
        self.score_label.config(text=self.get_score_text())

    def reset_board(self):
        for row in self.buttons:
            for btn in row:
                btn.config(text="", bg="SystemButtonFace" if self.theme == "Light" else "#4D4D4D")
        self.player = "X"

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
