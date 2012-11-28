from sip import setapi
setapi('QVariant', 2)
setapi('QString', 2)

from PyQt4.QtCore import Qt

from .util import pretty_number


class WidgetProperty(object):
    """ Base class for widget properties

    Subclasses implement, at a minimum, the "getter" and "setter" methods,
    which translate between widget states and python variables
    """
    def __init__(self, att):
        """
        :param att: The location, within a class instance, of the widget
        to wrap around. If the widget is nested inside another variable,
        normal '.' syntax can be used (e.g. 'sub_window.button')

        :type att: str
        """
        self._att = att.split('.')

    def __get__(self, instance, type=None):
        widget = reduce(getattr, [instance] + self._att)
        return self.getter(widget)

    def __set__(self, instance, value):
        widget = reduce(getattr, [instance] + self._att)
        self.setter(widget, value)

    def getter(self, widget):
        """ Return the state of a widget. Depends on type of widget,
        and must be overridden"""
        raise NotImplementedError()

    def setter(self, widget, value):
        """ Set the state of a widget to a certain value"""
        raise NotImplementedError()


class ButtonProperty(WidgetProperty):
    """Wrapper around the check state for QAbstractButton widgets"""
    def getter(self, widget):
        return widget.isChecked()

    def setter(self, widget, value):
        widget.setChecked(value)


class FloatLineProperty(WidgetProperty):
    """Wrapper around the text state for QLineEdit widgets.

    Assumes that the text is a floating point number
    """
    def getter(self, widget):
        try:
            return float(widget.text())
        except ValueError:
            return 0

    def setter(self, widget, value):
        widget.setText(pretty_number(value))
        widget.editingFinished.emit()


class ItemProxy(object):
    """Interface to a particular row in a list-like Qt model

    Defines 2 attibutes: label and data. These wrap the
    DisplayRole and UserRole items for a model index

    User's shouldn't have to create ItemProxies directly --
    they are automatically created from other properties
    """
    def __init__(self, model, idx):
        self.model = model
        self.idx = idx

    @property
    def label(self):
        return str(self.model.data(self.idx, Qt.DisplayRole))

    @label.setter
    def label(self, value):
        self.model.setData(self.idx, value, Qt.DisplayRole)

    @property
    def data(self):
        return self.model.data(self.idx, Qt.UserRole)

    @data.setter
    def data(self, value):
        self.model.setData(self.idx, value, Qt.UserRole)

    def __iter__(self):
        yield self.label
        yield self.data

    def __str__(self):
        return "%s (data %r)" % (self.label, self.data)


class ListProxy(object):
    """Wrapper around list-like Qt model classes.

    Users normally don't create ListProxies directly. Rather, they
    are automatically created from other properties.

    The basic interface for ListProxy:

    len(p) -> number of rows in the list

    p[i] -> fetches ith row, returns as a
            :class:`qtpy.properties.itemProxy` instance

    p.laels -> list of strings, giving label for each row
    p.data -> list of objects, giving user data for each row

    Both labels and data can be reassigned.

    for row in p:   # iterates over each row, using an ItemProxy
        print row.label, row.data

    p.pop(3) -> remove 3rd row, return removed row as an ItemProxy
    """
    def __init__(self, model):
        self.model = model

    def __getitem__(self, index):
        item = self.model.index(index, 0)
        if not item.isValid():
            raise IndexError("List index out of range")

        return ItemProxy(self.model, item)

    def __len__(self):
        return self.model.rowCount()

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    @property
    def labels(self):
        return [i.label for i in self]

    @labels.setter
    def labels(self, values):
        ct = len(self)
        for i, v in enumerate(values):
            if i >= ct:
                self._add_row()
            self[i].label = v

        for i in range(len(values), len(self)):
            self[i].label = ''

    @property
    def data(self):
        return [i.data for i in self]

    @data.setter
    def data(self, values):
        ct = len(self)
        for i, v in enumerate(values):
            if i >= ct:
                self._add_row()
            self[i].data = v

        for i in range(len(values), len(self)):
            self[i].data = None

    def _add_row(self):
        result = self.model.insertRow(len(self))
        if not result:
            raise IndexError("Could not add row to model")
        self[len(self) - 1].label = ''

    def pop(self, row):
        result = self[row]
        r = self.model.removeRows(row, 1)
        if not r:
            raise IndexError("Cannot remove frow from model")
        return result

    def __str__(self):
        return "list with %i elements" % len(self)

class ListProperty(WidgetProperty):
    """Wrapper for widgets with list-like Qt models. This includes:
       * QComboBox
       * QListView
       * QListWidget
       * QHelpIndexWidget
       * QUndoView

       And any other class with a model() method that returns a
       list-like Qt model

       Accessing the property returns a ListProxy
    """
    def getter(self, widget):
        return ListProxy(widget.model())

    def setter(self, widget, value):
        raise AttributeError()


class ValueProperty(WidgetProperty):
    """ Wrapper for widgets with a value() method. This includes:
        * QSlider
        * QSpinBox
        * QDoubleSpinBox
        * QProgressBar
        * QScrollBar
        * QDial

    Getting / setting this property calls value() / setValue()
    """
    def getter(self, widget):
        return widget.value()

    def setter(self, widget, value):
        widget.setValue(value)
