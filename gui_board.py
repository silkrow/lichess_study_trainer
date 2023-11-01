import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsPixmapItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class Chessboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chessboard")
        self.setGeometry(100, 100, 400, 400)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.initUI()

    def initUI(self):
        self.board_size = 8
        self.square_size = 50
        self.chessboard = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]

        self.createChessboard()
        self.initializeChessPieces()

    def createChessboard(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
                square = QGraphicsRectItem(col * self.square_size, row * self.square_size, self.square_size, self.square_size)
                square.setBrush(Qt.gray if color == (0, 0, 0) else Qt.white)
                square.setAcceptDrops(True)
                square.setZValue(-1)
                self.scene.addItem(square)

    def initializeChessPieces(self):
        piece_positions = [
            "rnbqkbnr",
            "pppppppp",
            "        ",
            "        ",
            "        ",
            "        ",
            "PPPPPPPP",
            "RNBQKBNR",
        ]

        for row, row_data in enumerate(piece_positions):
            for col, piece in enumerate(row_data):
                if piece != ' ':
                    piece_color = 'black' if piece.islower() else 'white'
                    piece_name = piece.lower()
                    piece_img = QPixmap(f"images/{piece_name}_{piece_color}.png")
                    piece_item = QGraphicsPixmapItem(piece_img)
                    piece_item.setPos(col * self.square_size, row * self.square_size)
                    piece_item.setFlag(QGraphicsPixmapItem.ItemIsMovable)
                    self.scene.addItem(piece_item)
                    self.chessboard[row][col] = piece_item

    def mousePressEvent(self, event):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.chessboard[row][col] is not None and self.chessboard[row][col].isUnderMouse():
                    self.selected_piece = self.chessboard[row][col]
                    self.selected_row, self.selected_col = row, col

    def mouseReleaseEvent(self, event):
        if hasattr(self, 'selected_piece'):
            target_row, target_col = self.selected_row, self.selected_col
            target_x = target_col * self.square_size + self.square_size / 2
            target_y = target_row * self.square_size + self.square_size / 2

            if (target_row, target_col) != (self.selected_row, self.selected_col):
                self.selected_piece.setPos(target_x, target_y)

            delattr(self, 'selected_piece')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chessboard = Chessboard()
    chessboard.show()
    sys.exit(app.exec_())

