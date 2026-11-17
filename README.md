# tiny-chess-01 entry

A chess engine in under 4 KB of Python 3 (stdlib only), for make.fun `tiny-chess-01`.
`main.py` is a raw-deflate payload in a latin-1 string, unpacked and exec'd.

- 10x12 mailbox board, flipped so the side to move is always upper case
- full legal moves: castling, en passant, promotion (to queen)
- negamax alpha-beta, quiescence, transposition table, check extension,
  null move, late-move reductions, futility, killer + history ordering
- tapered piece-square eval from formulas, bishop pair, repetition draws
- iterative deepening to a fixed node budget, never a clock: same position,
  same move

License: MIT.
