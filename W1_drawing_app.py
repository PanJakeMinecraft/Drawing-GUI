import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from functools import partial

# create a list of colors
COLORS = ["white", "black", "#5ec623", "#f5d00e", "#0e51f5", "#ada5f9", "#00aefe", "#498600", "#025900", "#b91800", "#9000bb", "#fb6700", "#fb00e1", "#fcb9f5"]

# create canvas class...
class Canvas(QLabel):
    def __init__(self):
        super().__init__()
        self.pen_color = QColor("black")  # Default color
        self.pen_width = 3  # Default pen width
        canvas = QPixmap(1000, 700)  
        canvas.fill(Qt.GlobalColor.white)
        self.setPixmap(canvas)
        self.last_x, self.last_y = None, None

    def set_pen_color(self, color):
        self.pen_color = QColor(color)
        self.pen_width = 3

    def set_eraser(self):
        self.pen_color = QColor("white")  
        self.pen_width = 20

    def mouseMoveEvent(self, e):
        if self.last_x is None:  # Start drawing when mouse is moved
            self.last_x = int(e.position().x())
            self.last_y = int(e.position().y())
            print(f"X-position: {self.last_x}")
            print(f"Y-position: {self.last_y}")
            print("---------------------------------")
            return
        
        canvas = self.pixmap()
        painter = QPainter(canvas)
        pen = QPen(self.pen_color, self.pen_width)  # Use current pen color and width
        painter.setPen(pen)
        painter.drawLine(self.last_x, self.last_y, int(e.position().x()), int(e.position().y()))
        painter.end()
        self.setPixmap(canvas)

        # Update the last position
        self.last_x = int(e.position().x())
        self.last_y = int(e.position().y())

    # When the mouse is being released
    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

class QPaletteButton(QPushButton):
    def __init__(self, color):
        super().__init__()
        self.setFixedSize(30, 30)
        self.setStyleSheet(f"background-color: {color};")
        self.color = color

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.canvas = Canvas()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(self.canvas)

        # Create color palette buttons
        palette = QHBoxLayout()
        self.add_palette_buttons(palette)
        
        # Add Eraser Button
        eraser_button = QPushButton("Eraser")
        eraser_button.setFixedSize(QSize(100, 50))
        eraser_button.setStyleSheet(
                                    """
                                    font-family: Tahoma;
                                    font-weight: bold;
                                    font-size: 16px;
                                    """
        )
        eraser_button.clicked.connect(self.canvas.set_eraser)
        palette.addWidget(eraser_button)
        
        layout.addLayout(palette)
        
        self.setCentralWidget(widget)
        self.setWindowTitle("Drawing Application")

    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(partial(self.canvas.set_pen_color, c))
            layout.addWidget(b)

app = QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)

window = Main()
window.show()
app.exec()
