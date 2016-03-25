.. bluescript documentation master file, created by
   sphinx-quickstart on Tue Mar 22 21:23:56 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Bluescript of LidarSim Display-widget
=============================================
This documentation discribe the details of display-widget in hapipy3.

LidarSim supports multi-platform, such as
**Windows, Linux, MacOS**.


Contents:

.. toctree::
   :maxdepth: 2

   LidarsimSim显示控件.xlsx 


--------------------------------------

Function bluescript
------------------------
Import Data
++++++++++++++++++
supported data format:

**TXT, par, netCDF4, HDF5, CSV, JSON**

Lidarsim can open different data files in different format at same time.

Content Presentation
++++++++++++++++++++++
Features about how the display-widget presents the data have been list in 
``LidarsimSim显示控件.xlsx``
.


Data Presentation
+++++++++++++++++++++++++
1. use dockwidget.
2. operate as Matlab Workspace.
3. display HDF5 as tree structure.
4. data will be presented in another window.

Export Data 
++++++++++++++++++++
1. selected data can be export as
**TXT, par, netCDF4, HDF5, CSV, JSON, SQL**
file.

2. some necessary elements, such as comments, time, root, name of variable, need to be added.

Save Graph 
+++++++++++++++
1. support
**eps, bmp, tiff, png, pdf**
as format of graph.

2. some necessary parameter, such as ppi, color space, etc... need to be considered.

Interface Layout
+++++++++++++++++++
The preliminary design of interface can be found in
``LidarsimSim显示控件.vsdx``
.

And, plotwidget needs to be embedded in interface.

---------------------------------------------------------

Version control
----------------
Our work needs to control two version, libraries and widget.

Library version
+++++++++++++++++++
Display-widget lies on many entension libraries, so we need to control their dependency relationships, use
``requirement.txt``
to ensure the environment.

Widget version
+++++++++++++++++++
widget version and software version need to be considered for compatibility of the widget and software.

----------------------------------------------------------

Py3Qt5 widget
-----------------

.. line-block::

    QTreeWidget.
    QCheckBox---the state can be checked.
    QPushButton.
    QHBoxLayout.
    QVBoxLayout.
    QGridBoxLayout.
    QMenuBar.
    QToolBar.
    QDockWidget.
    QStatusBar.
    QLabelBar.
    QProgressBar.
    QSpmBox.
    QComboBox.
    QListWidget.
    QDialog.

----------------------------------------------------------

Project Structure
----------------------
The project package should include these files:

- App.py

  - module a

    - submodule aa 

    - submodule ab 

    - ...

  - module b 

    - submodule ba 

    - submodule bb

    - ...

- requirement.txt

- release.md 

- authors.md 

- licence.md 

- changelog.md 

- readme.md 

- script to build .exe

-----------------------------------------------------------

Programming Conventions 
--------------------------------
quick reference:
`Google Style Guide <https://github.com/google/styleguide>`_

The rules list below are important for us.

1. Import 
2. Globel variable
3. Operators
4. Default parameter
5. Function and Method Decorators
6. Threading
7. Style rules
    - Semicolons
    - Line length
    - Blank Lines & Whitespace
    - Shebang Line
    - Comments
    - Classes
    - Files and Sockets
8. Naming

-----------------------------------------------------------




