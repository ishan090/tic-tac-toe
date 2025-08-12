# tic-tac-toe
The objective of this project is to find not just any, but the most efficient (space and time) form of a tic-tac-toe AI. I hope to implement my findings from here onto the [Connect4AI](https://github.com/ishan090/Connect4AI)

## Minimax

The idea behind this move is to make your current best move considering the opponent makes their best move.

### Progress

#### Depth
Initially the bare minimax, I tried adding a depth to the search - 4 moves ahead.
However, this resulted in suboptimal results as the above assumption is rendered false.
Therefore the program mistook the other player's mistakes, circumstancial outcomes, to be carefully thought moves, something inevitable.

#### Dynamic Programming
This idea removed the depth element and instead mapped the states already visited to their determined value and then used these values whenever the same state came along again.

#### Tokenization and comparison
Now, take the previous idea further.

1) simplify the representation of the state (lists are expensive to store) and
2) find a way of finding isomers of these tokens so that there're less tokens to store anyways.

