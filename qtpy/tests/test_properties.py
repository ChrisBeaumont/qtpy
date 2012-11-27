from sip import setapi
setapi('QString', 2)
setapi('QVariant', 2)

import pytest

from PyQt4.QtGui import (QApplication, QCheckBox, QListWidget, QComboBox,
                         QSlider, QDoubleSpinBox, QSpinBox)

from PyQt4.QtCore import Qt

from ..properties import ButtonProperty, ListProperty, ValueProperty

def setup_module(module):
    module.app = QApplication([''])


class TestWidget(object):
    btn = ButtonProperty('_btn')
    lst = ListProperty('_lst')
    combo = ListProperty('_cmbo')
    spn_int = ValueProperty('_spn_int')
    spn_double = ValueProperty('_spn_double')
    slider = ValueProperty('_slider')

    def __init__(self):
        self._btn = QCheckBox()
        self._lst = QListWidget()
        self._cmbo = QComboBox()
        self._spn_int = QSpinBox()
        self._spn_double = QDoubleSpinBox()
        self._slider = QSlider()

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

def assert_combo_box_synced(prop, widget, labels=None, data=None):
    assert len(prop) == widget.count()
    if labels is not None:
        assert len(prop) == len(labels)
        assert prop.labels == labels

    for i in range(len(prop)):
        label, datum = prop[i]
        assert widget.itemText(i) == label
        assert widget.itemData(i) == datum

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


def test_list_list_widget():
    tw = TestWidget()
    _test_list(tw.lst, tw._lst, assert_list_widget_synced)

def test_list_combo_box():
    tw = TestWidget()
    _test_list(tw.combo, tw._cmbo, assert_combo_box_synced)

def _test_list(proxy, widget, assert_valid):

    proxy.labels = ['a', 'b', 'c']
    assert_valid(proxy, widget,
                 labels=['a', 'b', 'c'],
                 data=[None, None, None])

    proxy.data = [1, 2, 3]
    assert_valid(proxy, widget,
                 labels=['a', 'b', 'c'],
                 data=[1, 2, 3])

    proxy.data = [1, 2, 3, 4]
    assert_valid(proxy, widget,
                 labels=['a', 'b', 'c', ''],
                 data=[1, 2, 3, 4])

    proxy[3].label = 'd'
    assert_valid(proxy, widget,
                 labels=['a', 'b', 'c', 'd'],
                 data=[1, 2, 3, 4])

    with pytest.raises(IndexError) as exc:
        proxy[4].label = 'Out of Bounds'
    assert exc.value.args[0] == 'List index out of range'

    proxy.pop(1)
    assert_valid(proxy, widget,
                 labels=['a', 'c', 'd'],
                 data=[1, 3, 4])

    with pytest.raises(IndexError) as exc:
        proxy.pop(3)

    proxy[0].data = 100
    assert_valid(proxy, widget,
                 labels=['a', 'c', 'd'],
                 data=[100, 3, 4])

def test_range_spin():
    tw = TestWidget()
    _test_range(tw, 'spn_int', tw._spn_int)

def test_range_double_spin():
    tw = TestWidget()
    _test_range(tw, 'spn_double', tw._spn_double)

def test_slider():
    tw = TestWidget()
    _test_range(tw, 'slider', tw._slider)

def _test_range(widget, prop, target):
    def _assert_synced(value):
        assert getattr(widget, prop) == value
        assert target.value() == value

    setattr(widget, prop, 1)
    _assert_synced(1)

    setattr(widget, prop, 2)
    _assert_synced(2)

    target.setValue(1)
    _assert_synced(1)
