import chess
import chess.pgn

game = chess.pgn.Game()
game.headers["Event"] = "morning"
node = game.add_variation(chess.Move.from_uci("e2e4"))
node = node.add_variation(chess.Move.from_uci("e7e5"))
node.comment = "Comment"

node = game.game()
node = node.add_variation(chess.Move.from_uci("d2d4"))
node = node.add_variation(chess.Move.from_uci("d7d5"))
node = node.add_variation(chess.Move.from_uci("c2c4"))
node = node.parent
node = node.add_variation(chess.Move.from_uci("g1f3"))


print(game)
