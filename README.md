qtpy
====

A pythonic interface to PyQt4

Most widgets manage some piece of state (for example, a check box represents some boolean property, a combo box represents a list of items, etc.). Qt provides methods to get and set this state, but they are somewhat verbose:

    furnace_on = furnace.thermostat_power_checkbox.isChecked()
    furnace.thermostat_power_checkbox.setChecked(True)
    
qtpy provides wrappers for the most common pieces of widget state. It lets you define state properties, leading to simpler code that looks like this:

    furnace_on = furnace.power
    furnace.power = True

Basic Usage
===========

Here's the basic usage pattern:

```
class Furnace(QWidget):
	power = qtpy.ButtonProperty('thermostat_power_checkbox')
	
	def __init__(self, parent=None):
	    super(Furnace, self).__init__(parent)
	    self.thermostat_power_checkbox = QCheckBox()
	   	...etc...
```	   		   

Here, `power` is a qtpy wrapper around the `Furnace.thermostat_power_checkbox`
widget. The `ButtonProperty` behaves like a boolean property that reflects the check state of the widget::

      f = Furnace()
      f.power         # equivalent to f.thermostat_power_checkbox.isChecked()
      f.power = True  # equivalent to f.thermostat_power_checkbox.setChecked(True)

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