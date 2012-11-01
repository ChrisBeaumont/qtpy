from PyQt4.QtGui import QApplication, QCheckBox

from ..properties import ButtonProperty

def setup_module(module):
    module.app = QApplication([''])


class TestWidget(object):
    btn = ButtonProperty('_btn')

    def __init__(self):
        self._btn = QCheckBox()


def test_button():
    tw = TestWidget()
    assert tw.btn == tw._btn.isChecked()

    tw.btn = True
    assert tw.btn == tw._btn.isChecked()

    tw.btn = False
    assert tw.btn == tw._btn.isChecked()

    tw._btn.setChecked(True)
    assert tw.btn == tw._btn.isChecked()

    tw._btn.setChecked(False)
    assert tw.btn == tw._btn.isChecked()
