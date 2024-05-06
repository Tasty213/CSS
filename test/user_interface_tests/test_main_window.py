from main_ui import Window
from pytestqt.qtbot import QtBot


def test_title(qtbot: QtBot):
    window = Window()
    window.show()
    qtbot.addWidget(window)

    assert window.windowTitle() == "CSS Tech Test"
