
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
        #print('selected actions:', actions)
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
    
    def standard_rotation(self):
        """tic tac toe boards can be rotated without changing the dynamic of the game
        This function standardises rotation and represents the result in a 9 bitstring which
        can serve as an identifier to tokenize rotations"""

        def wrap(x, times=1):
            x = deepcopy(x)
            for i in range(times):
                x = x[1:] + x[0:1]
            return x
        
        def bitstring(x):
            return "".join([str(i) for i in x])

        state = self.getState()
        num_val = {None: 0, 1: 1, 0: -1}
        center = [num_val.get(state[1][1], 1)]
        edges = [num_val.get(state[i][j], 1) for i, j in [(0, 1), (1, 2), (2, 1), (1, 0)]]
        corners = [num_val.get(state[i][j], 1) for i, j in [(0, 0), (0, 2), (2, 2), (2, 0)]]

        #print(edges, corners)
        # loop through the rotations for the corners
        best = []
        best_val = 0
        screen = [*range(4, 0, -1)]
        for rot in range(4):
            val = sum([screen[i] * abs(corners[i]) for i in range(len(corners))])
            #print("val for rot:", val)
            if best_val == 0 or val > best_val:
                best = [rot]
                best_val = val
            elif best_val == val:
                best.append(rot)
            corners = wrap(corners)
        #print("bests:", best)
        
        # now the edges
        if len(best) != 1:
            new_best = best[0]
            best_val = 0
            for rot in best:
                s = wrap(edges, rot)
                val = sum([screen[i] + s[i] for i in range(len(s))])
                if val > best_val:
                    new_best = rot
                    best_val = val
            best = new_best
        else:
            best = best[0]
        
        return bitstring(wrap(corners, best)+wrap(edges, best)+center), best

    
    def full(self):
        return all([not None in i for i in self.state])
    
    def makeMove(self, action, fr=None):
        #print("this is the grid before making the move", action, "from:", fr)
        # self.show()
        assert self.getIndex(action) is None, f"Index {action} not empty: {self.getIndex(action)}"
        player = self.player
        self.state[action[0]][action[1]] = player
        #print("\tgrid after: full?", self.full(), self.state, [all(i) for i in self.state])
        # self.show()
        #print("seeing if someone won..")
        if self.winning_move(action, player):
            #print("true")
            self.winner = 1 if player == 1 else -1
        elif self.full():
            #print("grids full")
            self.winner = 0
        self.player = 1-player
        #print("val of winner after making the move:", self.winner)



def minimax(state, best_val, check_func, other_func, memo={}, thresh=0.2, calls=0):

    calls += 1

    best = None
    move = None
    best_memo = None
    if state.winner is not None:
        return state.winner, None, memo, calls

    for action in state.actions():
        #print("possible move:", action)
        new_state = Grid(state=state.getState(), player=state.player)
        new_state.makeMove(action, "max")

        if memo.get(new_state.stateTuple(), None) is not None:
            val = memo[new_state.stateTuple()]
        else:
            out = minimax(new_state, -best_val, other_func, check_func, memo)
            val, c = out[0], out[-1]
            calls += c
            memo[new_state.stateTuple()] = val
        #print("val is:", val, "best is:", best)
        if val == best_val:
            return val, action, memo, calls
        elif best is None or check_func(val, best):
            best = val
            move = action
        elif best == val and random.random() < thresh: # if they're the same, then change your move given a certain probability
            move = action
    return best, move, memo, calls

def minimax2(state, best_val, check_func, other_func, memo={}, thresh=0.2, calls=0):
    
    calls += 1

    best = None
    move = None
    best_memo = None
    if state.winner is not None:
        return state.winner, None, memo, calls

    for action in state.actions():
        #print("possible move:", action)
        new_state = Grid(state=state.getState(), player=state.player)
        new_state.makeMove(action, "max")

        token, rot = new_state.standard_rotation()

        if token in memo:
            val = memo[token]
        else:
            out = minimax2(new_state, -best_val, other_func, check_func)
            val, new_memo, c = out[0], out[2], out[-1]
            calls += c
            memo[token] = val
            memo = new_memo | memo
        #print("val is:", val, "best is:", best)
        if val == best_val:
            return val, action, memo, calls
        elif best is None or check_func(val, best):
            best = val
            move = action
        elif best == val and random.random() < thresh: # if they're the same, then change your move given a certain probability
            move = action
    return best, move, memo, calls


def play(grid=None, human_player=None, minmax_func=minimax):

    print("Welcome to this Tic-Tac-Toe game.")
    print("-->You'll be playing against the minimax algorithm optimised using memoization and further improved through tokenization of the numerous tic-tac-toe states")

    if human_player is None:
        human_player = random.randint(0, 1)

    print("Human plays:", xo_vals[human_player])
    check_funcs = [lambda x, y: x > y, lambda x, y: x < y]
    # print("AI Plays:", xo_vals[1-human_player], f"and with use the {min_max_map[1-human_player]} func\n")
    print("Bon chance~\n")
    game = Grid(grid)
    mem = {}
    
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
            v, move, m, c = minmax_func(game, target, *check_funcs[::target])
            mem = m | mem
        # print("move to make:", move)
        game.makeMove(move)
        print("Played the move:", move)
    
    print("Game over...")
    if game.winner == 0:
        print("That was a draw; good game.")
    else:
        print(("You" if game.winner == human_player else "Algo"), "Won! Good game.")
    game.show()


if __name__ == "__main__":
    # x = [
    #     [1, 0, 1],
    #     [None, None, None],
    #     [None, 1, None]
    # ]
    # y = [
    #     [None, None, 1],
    #     [1, None, 0],
    #     [None, None, 1]
    # ]
    # x = Grid(x)
    # y = Grid(y)
    # print(x.standard_rotation())
    # print(y.standard_rotation())

    play(minmax_func=minimax2)

    # z = Grid()
    # check_funcs_ = [lambda x, y: x > y, lambda x, y: x < y]
    # v, m, mem, c = minimax(z, 1, *check_funcs_)
    # total = 0
    # zeros = 0
    # ones = 0
    # draw = 0
    # for i in mem.values():
    #     if i == 1:
    #         ones += 1
    #     elif i == 0:
    #         draw += 1
    #     else:
    #         zeros += 1
    #     total += 1
    # print("Total:", total)
    # print("Total calls:", c)
    # print("1:", ones)
    # print("0:", zeros)
    # print("Draws:", draw)
