import argparse


class RbGame:
    def __init__(self, num_red, num_blue, version, first_player, depth):
        self.num_red = num_red
        self.num_blue = num_blue
        self.version = version
        self.first_player = first_player
        self.depth = depth
        self.board = {"red": num_red, "blue": num_blue}
        self.score = 0

    def print_board(self):
        print("Current board: Red - {}, Blue - {}".format(self.board["red"], self.board["blue"]))

    def get_valid_input(self, prompt):
        while True:
            try:
                num_marbles = int(input(prompt))
                if num_marbles in [1, 2]:
                    return num_marbles
                else:
                    raise ValueError("Invalid input. Please enter 1 or 2.")
            except ValueError as e:
                print("Error:", e)

    def remove_marbles(self, color, num_marbles):
        self.board[color] -= num_marbles

    def is_game_over(self):
        return self.board["red"] == 0 or self.board["blue"] == 0

    def calculate_score(self):
        self.score = self.board["red"] * 2 + self.board["blue"] * 3

    def minmax(self, depth, alpha, beta, is_maximizing):
        if self.is_game_over():
            if self.version == "standard":
                return -1 if self.board["red"] == 0 else 1
            else:
                return 1 if self.board["red"] == 0 else -1
        if depth == 0:
            return self.evaluation()
        if is_maximizing:
            best_score = -float('inf')
            for color in ["red", "blue"]:
                for num_marbles in [1, 2]:
                    if self.board[color] >= num_marbles:
                        self.remove_marbles(color, num_marbles)
                        score = self.minmax(depth - 1, alpha, beta, False)
                        self.board[color] += num_marbles
                        best_score = max(best_score, score)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float('inf')
            for color in ["red", "blue"]:
                for num_marbles in [1, 2]:
                    if self.board[color] >= num_marbles:
                        self.remove_marbles(color, num_marbles)
                        score = self.minmax(depth - 1, alpha, beta, True)
                        self.board[color] += num_marbles
                        best_score = min(best_score, score)
                        beta = min(beta, score)
                        if beta <= alpha:
                            break
            return best_score

    def evaluation(self):
        if self.version == "standard":
            return self.board["red"] - self.board["blue"]
        else:
            return self.board["blue"] - self.board["red"]

    def computer_move(self):
        best_score = -float('inf')
        best_move = None
        for color in ["red", "blue"]:
            for num_marbles in [1, 2]:
                if self.board[color] >= num_marbles:
                    self.remove_marbles(color, num_marbles)
                    score = self.minmax(self.depth, -float('inf'), float('inf'), False)
                    self.board[color] += num_marbles
                    if score > best_score:
                        best_score = score
                        best_move = (color, num_marbles)
        self.remove_marbles(best_move[0], best_move[1])
        print("Computer removes {} {} marbles.".format(best_move[1], best_move[0]))

    def play_game(self):
        current_player = self.first_player
        while not self.is_game_over():
            self.print_board()
            if current_player == "human":
                color = input("Enter 'red' or 'blue' to remove marbles: ")
                num_marbles = self.get_valid_input("Enter 1 or 2 to remove marbles: ")
                if num_marbles > self.board[color]:
                    print("You can't remove that many marbles. There are only {} {} marbles left.".format(
                        self.board[color], color))
                    continue
                self.remove_marbles(color, num_marbles)
            else:
                self.computer_move()
            current_player = "computer" if current_player == "human" else "human"

        self.print_board()
        self.calculate_score()
        print("Your final score is:", self.score)

        # Announce the winner based on the game version
        if self.version == "standard":
            if self.board["red"] == 0 or self.board["blue"] == 0:
                winner = "human" if current_player == "computer" else "computer"
                print(f"Game over! The winner is {winner}.")
        else:  # Misere version
            if self.board["red"] == 0 or self.board["blue"] == 0:
                winner = "computer" if current_player == "computer" else "human"
                print(f"Game over! The winner is {winner}.")


def main():
    parser = argparse.ArgumentParser(description="Red-Blue Nim Game")
    parser.add_argument("--num-red", type=int, default=10, help="Number of red marbles")
    parser.add_argument("--num-blue", type=int, default=10, help="Number of blue marbles")
    parser.add_argument("--first-player", choices=["human", "computer"], default="human", help="First player")
    parser.add_argument("--depth", type=int, default=5, help="Search depth for AI")

    args = parser.parse_args()

    # Prompt user to choose the game version
    while True:
        version_choice = input("Choose game version: Press 1 for Standard, 2 for Misere: ")
        if version_choice == '1':
            version = "standard"
            break
        elif version_choice == '2':
            version = "misere"
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    game = RbGame(args.num_red, args.num_blue, version, args.first_player, args.depth)
    game.play_game()


if __name__ == "__main__":
    main()
