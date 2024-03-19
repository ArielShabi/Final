from PyQt5.QtWidgets import QMainWindow, QStackedWidget


from helpers.color import get_bacteria_color
from logic.bacteria_creator import get_random_bacteria
from logic.history_saver import HistorySaver
from ui.pages.graph_page import GraphPage
from ui.pages.simulation_page import SimulationPage
from ui.utils import createColoredIcon

CSS_FILE = "main_window.css"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        history_saver = HistorySaver()
        self.simulation_page = SimulationPage(self.go_to_graph_page, history_saver)
        self.graph_page = GraphPage(history_saver)
        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)
        self.stackedWidget.addWidget(self.simulation_page)
        self.stackedWidget.addWidget(self.graph_page)
        self.graph_page.go_back_button.clicked.connect(self.go_to_simulation_page)

    def go_to_simulation_page(self):
        self.stackedWidget.setCurrentIndex(0)        

    def go_to_graph_page(self):
        self.stackedWidget.setCurrentIndex(1)
        self.graph_page.on_page_set()

    def initUI(self):
        super().__init__()
        self.setWindowTitle("Bacteria Game")
        self.__set_icon()

    def __set_icon(self):
        random_bacteria = get_random_bacteria()
        color = get_bacteria_color(random_bacteria.properties)
        self.setWindowIcon(createColoredIcon("assets/bacteria.svg", color))
