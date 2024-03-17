from const import START_TIME_PER_TURN
from helpers.timer import Timer
from logic.bacteria_creator import get_random_bacterias
from logic.bacteria_strategies.random_strategy import random_strategy
from logic.event_emitter import EventEmitter
from logic.history_runner import HistoryRunner
from logic.turn_runner import TurnRunner
from models.board import Board
from models.food import Food
from models.settings import Settings

BOARD_WIDTH = 100
BOARD_HEIGHT = 100

ON_TURN_FINISHED = "on_turn_finished"
ON_PAUSE_PLAY_TOGGLE = "on_pause_play_toggle"


class GameRunner(EventEmitter):
    def __init__(self, history_runner: HistoryRunner, time_per_turn: int = 1):
        super().__init__()
        self.settings = Settings()
        self.live_turn_number = 0
        self.turn_runner = TurnRunner(self.settings.food_per_turn)
        self.history_runner = history_runner
        self.time_per_turn = time_per_turn
        self.board = None
        self.timer: Timer = Timer(START_TIME_PER_TURN)
        self.is_running = False
        self.running_from_history = False
        self.timer.timeout.connect(self.run_turn)

    def create_board(self):
        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT)
        bacterias = get_random_bacterias(BOARD_WIDTH, BOARD_HEIGHT, 30)

        for bacteria, location in bacterias:
            self.board.add_bacteria(
                bacteria,
                location)

    def toggle_play_pause(self, to_start: bool = True):
        if to_start:
            self.__start()
        else:
            self.__pause()

        if (to_start != self.is_running):
            self.fire_event(ON_PAUSE_PLAY_TOGGLE, to_start)
            self.is_running = to_start

    def change_speed(self, speed: int):
        self.time_per_turn = round(START_TIME_PER_TURN / speed)
        self.timer.interval = round(START_TIME_PER_TURN / speed)

        if (self.is_running):
            self.timer.stop()
            self.timer.start()

    def run_turn(self):
        updated_board = None

        if self.running_from_history:
            updated_board = self.history_runner.get_turn(self.board)

            if not updated_board:
                self.running_from_history = False

        if not self.running_from_history:
            updated_board = self.turn_runner.run_turn(
                self.board, self.live_turn_number)
            self.live_turn_number += 1

        self.board = updated_board

        self.fire_event(ON_TURN_FINISHED, updated_board)

    def on_settings_change(self, settings: Settings):
        self.settings = settings
        self.turn_runner.food_per_turn = settings.food_per_turn

    def start_run_from_history(self, from_turn: int):
        self.running_from_history = True
        self.history_runner.turn = from_turn
        self.board = self.history_runner.get_turn(self.board, False)

    def __start(self):
        if not (self.is_running):
            self.fire_event(ON_TURN_FINISHED, self.board)
            self.timer.start()

    def __pause(self):
        if (self.is_running):
            self.timer.stop()
