from sip import setapi
setapi('QString', 2)
setapi('QVariant', 2)

import pytest

from PyQt4.QtGui import QApplication, QCheckBox, QListWidget
from PyQt4.QtCore import Qt

from ..properties import ButtonProperty, ListProperty

def setup_module(module):
    module.app = QApplication([''])


class TestWidget(object):
    btn = ButtonProperty('_btn')
    lst = ListProperty('_lst')

    def __init__(self):
        self._btn = QCheckBox()
        self._lst = QListWidget()


def assert_button_synced(prop, widget):
    assert prop == widget.isChecked()


def assert_list_widget_synced(prop, widget, labels=None, data=None):
    assert len(prop) == widget.count()
    if labels is not None:
        assert len(prop) == len(labels)
        assert prop.labels == labels

    for i in range(len(prop)):
        label, datum = prop[i]
        assert widget.item(i).text() == label
        assert widget.item(i).data(Qt.UserRole) is datum

        if labels is not None:
            assert prop[i].label == labels[i]

        if data is not None:
            assert prop[i].data is data[i]


def test_button():
    tw = TestWidget()
    assert_button_synced(tw.btn, tw._btn)

    tw.btn = True
    assert_button_synced(tw.btn, tw._btn)

    tw.btn = False
    assert_button_synced(tw.btn, tw._btn)

    tw._btn.setChecked(True)
    assert_button_synced(tw.btn, tw._btn)

    tw._btn.setChecked(False)
    assert_button_synced(tw.btn, tw._btn)


def test_list():
    tw = TestWidget()

    tw.lst.labels = ['a', 'b', 'c']
    assert_list_widget_synced(tw.lst, tw._lst,
                              labels=['a', 'b', 'c'],
                              data=[None, None, None])

    tw.lst.data = [1, 2, 3]
    assert_list_widget_synced(tw.lst, tw._lst,
                              labels=['a', 'b', 'c'],
                              data=[1, 2, 3])

    tw.lst.data = [1, 2, 3, 4]
    assert_list_widget_synced(tw.lst, tw._lst,
                              labels=['a', 'b', 'c', ''],
                              data=[1, 2, 3, 4])

    tw.lst[3].label = 'd'
    assert_list_widget_synced(tw.lst, tw._lst,
                              labels=['a', 'b', 'c', 'd'],
                              data=[1, 2, 3, 4])

    with pytest.raises(IndexError) as exc:
        tw.lst[4].label = 'Out of Bounds'
    assert exc.value.args[0] == 'List index out of range'

    tw.lst.pop(1)
    assert_list_widget_synced(tw.lst, tw._lst,
                              labels=['a', 'c', 'd'],
                              data=[1, 3, 4])

    with pytest.raises(IndexError) as exc:
        tw.lst.pop(3)

    tw.lst[0].data = 100
    assert_list_widget_synced(tw.lst, tw._lst,
                              labels=['a', 'c', 'd'],
                              data=[100, 3, 4])
