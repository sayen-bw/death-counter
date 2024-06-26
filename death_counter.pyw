import json
import sys
from pathlib import Path

from pynput.keyboard import Key, Listener
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

FILE = "config.json"
NEW_CONF = {
    "window_x": 0, 
    "window_y": 0,
    "deaths": 0
}
LABEL_STYLE = (
    "QLabel {"
    "font-family: Consolas;"
    "font-size: 34px;"
    "background-color: white;"
    "}"
    )

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.config = get_config()
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setGeometry(0, 0, 100, 40)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # transparent background
        self.move(self.config["window_x"], self.config["window_y"])

        self.KEY_PRESSED_ONCE: bool = False
        self.deaths: int = self.config["deaths"]
        self.deaths_this_session: int = 0

        self.label = QLabel(self)
        self.label.setText(str(self.deaths))
        self.label.setStyleSheet(LABEL_STYLE)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.adjustSize()

        self.show()

    def close_app(self) -> None:
        """Closes the application"""
        QtWidgets.qApp.quit()
    
    def save_current_pos(self) -> None:
        """Saves current window position for the next start with F7"""
        file_path = Path(FILE)
        data = None
        with open(file_path, "r") as file:
            data = json.load(file)

        data["window_x"] = self.x()
        data["window_y"] = self.y()

        with open(file_path, "w") as file:
            data = json.dumps(data, indent=4)
            file.write(data)
        return (self.x(), self.y())

    def mousePressEvent(self, event) -> None:
        """Save old Position from the click"""
        self.current_pos = event.globalPos()

    def mouseMoveEvent(self, event): 
        """Allows to drag the window around"""
        delta = QtCore.QPoint(event.globalPos() - self.current_pos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.current_pos = event.globalPos()

    def increment_death(self) -> None:
        """Increments death by 1"""
        self.deaths_this_session += 1
        self.deaths += 1
        self.update_death()

    def update_death(self) -> None:
        """Updates label with death"""
        self.label.setText(str(self.deaths))
        self.label.setStyleSheet(LABEL_STYLE)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.adjustSize()


def get_config() -> json:
    """Opens the config file for the application.
        If no config exists it creates a new one with the same data set 0.
    """
    try:
        file_path = Path(FILE)
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("> Creating new config file")
        with open(file_path, "w") as file:
            data = json.dumps(NEW_CONF, indent=4)
            file.write(data)

        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as err:
        print("> Something went wrong:")
        print(err)

def save_deaths(new_deaths: int) -> None:
    """Save current counted deaths to file"""
    file_path = Path(FILE)
    data = None
    with open(file_path, "r") as file:
        data = json.load(file)

    data["deaths"] = new_deaths

    with open(file_path, "w") as file:
        data = json.dumps(data, indent=4)
        file.write(data)

def on_press(key: Key) -> None:
    """Manage key press events"""
    global window

    if key == Key.f8 and not window.KEY_PRESSED_ONCE:
        window.KEY_PRESSED_ONCE = True # Set to True so you cant loop key presses
        window.increment_death()

def on_release(key: Key) -> None:
    """Manage key release events"""
    global window

    window.KEY_PRESSED_ONCE = False # Unlock pressed Key

    match key:
        case Key.f7: # Get position and save in config file
            pos = window.save_current_pos()
            print(f"Saved current position to coordinates: {pos}")
        case Key.f8: # Print current deaths
            print("You died. Current deaths: ", window.deaths)
        case Key.f9: # Closes the application
            print(f"Quit. You have died -{window.deaths_this_session}- times this Session!")
            save_deaths(window.deaths)
            window.close_app()
            return False
        case _:
            pass


if __name__ == '__main__':
    # Initialize and start keyboard listener
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()
    
    app = QApplication(sys.argv)
    window = MainWindow()
    
    app.exec()