import chess
import chess.pgn

game = chess.pgn.Game()
game.headers["Event"] = "morning"
node = game.add_variation(chess.Move.from_uci("e2e4"))
node = node.add_variation(chess.Move.from_uci("e7e5"))
node.comment = "Comment"

node = game.game()
node = node.add_variation(chess.Move.from_uci("d2d4"))
node1 = node.add_variation(chess.Move.from_uci("d7d5"))
node2 = node1.add_variation(chess.Move.from_uci("c2c4"))
node3 = node2.parent
node4 = node3.add_variation(chess.Move.from_uci("g1f3"))


print(game)
print(node)
print(node.variations)
print(node.starts_variation())
print(node.is_main_variation())
print(node1)
print(node1.variations)
print(node1.starts_variation())
print(node1.is_main_variation())
print(node2)
print(node2.variations)
print(node2.starts_variation())
print(node2.is_main_variation())
print(node3)
print(node4)
print(node4.variations)
print(node4.starts_variation())
print(node4.is_main_variation())
