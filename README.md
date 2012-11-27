qtpy
====

A pythonic interface to PyQt4


Basic Usage
===========

The objects in qtpy are descriptors that wrap around specific Qt
widgets, and provide a simple property-like interface to the most frequently used widget states. Here's the basic usage pattern:

```
class AwesomeToggle(QWidget):
      awesome = qtpy.ButtonProperty('_awesome')
      
  	  def __init__(self, parent=None):
  	      super(AwesomeToggle, self).__init__(parent)
          layout = QHBoxLayout()
	      label = QLabel("Awesome on?")
	      self._awesome = QCheckBox()

	      layout.addWidget(label)
	      layout.addWidget(self._awesome)
	      self.setLayout(layout)
```

Here, `awesome` is a qtpy wrapper around the `AwesomeToggle._awesome`
check box widget The `ButtonProperty` behaves like a boolean value that reflects the check state of the widget::

      at = AwesomeToggle()
      at.awesome = True  # equivalent to at._awesome.setChecked(True)
      assert at.awesome  # equivalent to assert qt._awesome.isChecked()

Note that qtpy wrappers are defined at the class level (i.e. outside of `__init__`), and reference the wrapped widget by name. Normal dot syntax can be used to reference nested widgets. For example:

```
class Foo(object):
	def __init__(self):
		self.box = QCheckBox()
		
class Bar(object):
	wrapper = qtpy.ButtonProperty('ui.box')
	def __init__(self):
		self.ui = Foo()		
```

Wrapper Library
===============		

ButtonProperty
---------------
Wraps the check state of any `QAbstractButton`. 

```
class Foo(object):
	button = ButtonProperty('widget')
	def __init__(self):
		self.widget = QCheckBox()
		
f = Foo()
f.button          # equivalent to f.widget.isChecked()
f.button = state  # equivalent to f.widget.setChecked(state)
```

ListProperty
------------
Wraps around `QComboBox`, `QListWidget`, `QListView`, and any other list-based view class. Provides an interface to the label and user data for each row.

```
class Rainbow(object):
	color = ListProperty('color_combo')
	def __init__(self):
		self.color_combo = QComboBox()
		
r = Rainbow()
r.color.labels = ['Red', 'Green', 'Blue']         # auto-adds 3 rows
r.color.data = ['#ff0000', '#00ff00', '#0000ff']  # sets user data for each row

r.color[i].label # r.color_combo.itemText(i)
r.color[i].data  # r.color_combo.itemData(i)
r.color[0].label = 'black'    # r.color_combo.setItemText('black')
r.color[0].label = '#000000'  # r.color_combo.setItemData('#000000')

row = r.color.pop(0)  # removes and returns first row
row.label  # 'black'
row.data   # '#000000'
```

ValueProperty
-------------

Wraps around any widget with `value()` and `setValue()` methods. This includes, for example, `QSlider`, `QSpinBox`, `QDoubleSpinBox`, `QDial`, and `QSlider`.

```
class Thermometer(object):
    temperature = ValueProperty('temperature_dial')
    
    def __init__(self):
    	self.temperature_dial = QSpinBox()
   
t = Thermometer()
t.temperature      # t.temperature_dial.value()
t.temperature = 5  # t.temperature_dial.setValue(5)
```