from sip import setapi
setapi('QVariant', 2)
setapi('QString', 2)

from PyQt4.QtCore import Qt

from .util import pretty_number


class WidgetProperty(object):
    """ Base class for widget properties

    Subclasses implement, at a minimum, the "get" and "set" methods,
    which translate between widget states and python variables
    """
    def __init__(self, att):
        """
        :param att: The location, within a class instance, of the widget
        to wrap around. If the widget is nested inside another variable,
        normal '.' syntax can be used (e.g. 'sub_window.button')

        :type att: str"""
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
    def __init__(self, item):
        self.item = item

    @property
    def label(self):
        return self.item.text()

    @label.setter
    def label(self, value):
        self.item.setText(value)

    @property
    def data(self):
        return self.item.data(Qt.UserRole)

    @data.setter
    def data(self, value):
        self.item.setData(Qt.UserRole, value)

    def __iter__(self):
        return iter([self.label, self.data])


class ListProxy(object):
    def __init__(self, widget):
        self.widget = widget

    def __getitem__(self, index):
        item = self.widget.item(index)
        if item is None:
            raise IndexError("List index out of range")

        return ItemProxy(item)

    def __len__(self):
        return self.widget.count()

    @property
    def labels(self):
        return [self.widget.item(i).text() for i in range(self.widget.count())]

    @labels.setter
    def labels(self, values):
        ct = len(self)
        for i, v in enumerate(values):
            print 'seting text %i to %s' % (i, v)
            if i >= ct:
                self.widget.addItem(v)
            else:
                self[i].text = v
            assert self.widget.item(i).text() == v

        for i in range(len(values), len(self)):
            self.widget[i].text = ''

    @property
    def data(self):
        return [self[i].data for i in range(len(self))]

    @data.setter
    def data(self, values):
        ct = len(self)
        for i, v in enumerate(values):
            if i >= ct:
                self.widget.addItem('')
            self[i].data = v

        for i in range(len(values), len(self)):
            self[i].data = None

    def pop(self, row):
        item = self.widget.takeItem(row)
        if item is None:
            raise IndexError("List index out of range")
        return ListProxy(item)


class ListProperty(WidgetProperty):
    def getter(self, widget):
        return ListProxy(widget)

    def setter(self, widget, value):
        raise AttributeError()
