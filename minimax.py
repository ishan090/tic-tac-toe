
# Uses the idea of minimax.
import random
from copy import deepcopy


xo_vals = "OX"


class Grid:
    def __init__(self, state=None, player=None, winner=None):
        if state is None:
            state = [[None, None, None] for i in range(3)]
        if player is None:
            player = random.randint(0, 1)
        self.winner = winner
        self.state = state
        self.player = player
    
    def show(self):
        out = f"Current Player: {xo_vals[self.player]}\n|"+"+".join(["-"*3 for i in range(3)])+"|\n" + ("\n|"+"+".join(["-"*3 for i in range(3)])+"|\n").join(
            ["| "+" | ".join([" " if i is None else xo_vals[i] for i in row])+" |" for row in self.state]
        ) + "\n|"+"+".join(["-"*3 for i in range(3)])+"|\n"
        print(out)

    
    def getIndex(self, index):
        return self.state[index[0]][index[1]]
    
    def getState(self):
        return deepcopy(self.state)
    
    def stateTuple(self):
        return tuple([tuple(i) for i in self.state])
    
    def actions(self):
        """
        returns the available actions one can take from any given state
        """
        actions = [(i, j) for i in range(3) for j in range(3) if self.getIndex((i, j)) is None]
        print('selected actions:', actions)
        return actions
    
    def getVectors(self, action):
        vectors = []
        current_index = action
        candidates = [(-1, 0), (-1, 1), (0, 1), (1, 1)]
        for candidate in candidates:
            group = []
            new_index = [current_index[i]+candidate[i] for i in range(2)]
            rev_candidate = [-1*i for i in candidate]
            rev = [current_index[i]+rev_candidate[i] for i in range(2)]
            if all([0 <= i <= 2 for i in new_index]):
                group.append(tuple(candidate))
            if all([0 <= i <= 2 for i in rev]):
                group.append(tuple(rev_candidate))
            if group:
                vectors.append(group)
        return vectors
    
    def winning_move(self, action, target):
        for pair in self.getVectors(action):
            chain = 1
            for vector in pair:
                new_index = tuple([action[i] + vector[i] for i in range(2)])
                while all([0 <= i <= 2 for i in new_index]) and self.getIndex(new_index) == target:
                    chain += 1
                    new_index = tuple([new_index[i] + vector[i] for i in range(2)])
            if chain >= 3:
                return True
        return False
    
    def full(self):
        return all([not None in i for i in self.state])
    
    def makeMove(self, action, fr=None):
        print("this is the grid before making the move", action, "from:", fr)
        self.show()
        assert self.getIndex(action) is None, f"Index {action} not empty: {self.getIndex(action)}"
        player = self.player
        self.state[action[0]][action[1]] = player
        print("\tgrid after: full?", self.full(), self.state, [all(i) for i in self.state])
        self.show()
        print("seeing if someone won..")
        if self.winning_move(action, player):
            print("true")
            self.winner = 1 if player == 1 else -1
        elif self.full():
            print("grids full")
            self.winner = 0
        self.player = 1-player
        print("val of winner after making the move:", self.winner)



def minimax(state, best_val, check_func, other_func, depth=4, memo={}):
    best = None
    move = None

    if state.winner is not None:
        return state.winner, None

    for action in state.actions():
        print("possible move:", action)
        new_state = Grid(state=state.getState(), player=state.player)
        new_state.makeMove(action, "max")
        if memo.get(new_state.stateTuple(), None) is not None:
            val = memo[new_state.stateTuple()]
        elif depth == 1:
            val = 0
        else:
            val = minimax(new_state, -best_val, other_func, check_func, depth)[0]
            memo[new_state.stateTuple()] = val
        print("val is:", val, "best is:", best)
        if val == best_val:
            return val, action
        elif best is None or check_func(val, best):
            best = val
            move = action
    return best, move


def play(grid=None, human_player=None):

    if human_player is None:
        human_player = random.randint(0, 1)

    print("Human plays:", xo_vals[human_player])
    check_funcs = [lambda x, y: x > y, lambda x, y: x < y]
    # print("AI Plays:", xo_vals[1-human_player], f"and with use the {min_max_map[1-human_player]} func\n")

    game = Grid(grid)
    
    while game.winner is None:
        game.show()
        if game.player == human_player:
            available_moves = [str(a[0])+str(a[1]) for a in game.actions()]
            print("Your turn~")
            while True:
                move = input("What's your move? Enter the coords (00 - top left, 22 bottom right):\n--> ").strip()
                if move not in available_moves:
                    print("Invalid move. Try again")
                else:
                    break
            move = tuple([int(i) for i in move])
        else:
            target = 1 if game.player == 1 else -1
            move = minimax(game, target, *check_funcs[::target])[1]
        print("move to make:", move)
        game.makeMove(move)
        print("Played the move:", move)
    
    print("Game over...")
    print("Winner is", game.winner)
    game.show()


if __name__ == "__main__":
    play()