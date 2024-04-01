>built project on python3.10.12
>![Logo of the project](https://github.com/Billy-gk101/Graphing-Calculator/blob/main/img_geometry.png)
# Graphing-Calculator
> Attempt at creating a expanding calculator for Pre-Algebra thru Calculous
recreating wheel but for my education/practice

`App.py` is the main file; it uses `QT` to do the GUI windows, color picking, etc.
Graph shown via `Matplotlib` (with the QT hook provided by matplotlib)

color of rendered objects can be configured and exported so next load you keep your prefered colors


### Goals
- Create a function calculator.
- Create a triangle solver


### Dependancies -pypi
>qdarktheme may not work with new
```shell
PyQt5
qt5-applications
pyqtdarktheme
matplotlib
shapely
```
- QT; for the GUI
- pyqtdarktheme; helps mimic current user desktop theme
- shapely; helps manage geometry
- matplotlib; used to show/plot geometry
