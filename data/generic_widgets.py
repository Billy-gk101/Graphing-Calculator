# =============================================================================
# CODE IMPORTS
# =============================================================================
import os, sys, io, math, pickle
from functools import partial
from numbers import Number
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# ---- PyQt UI Objects
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget

# ---- Local addins
from _global_ import *
import geometric_objects

# ---- PyQt UI Structs
import wdg_matplot
import wdg_calc
import wdg_triangle

# lets use mathplot to show the graphing instead of PIL taht is not intended for stuff like this
# https://www.pythonguis.com/tutorials/plotting-matplotlib/
# https://stackoverflow.com/questions/56283481/how-to-track-the-mouse-over-the-matplots-canvas-in-qwidget
class QMatplot(QWidget, wdg_matplot.Ui_Form):
    def __init__(self, parent:QWidget=None, width:Number=10, height:Number=8, dpi:Number=300):
        # setup widget and load to parent layout
        super().__init__(parent)
        self.setupUi(self)
        lay = parent.layout()
        if lay is not None: lay.addWidget(self)

        # build the Matplot widget thing
        self.label.setText('coords: ')
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.mpl_connect("motion_notify_event", self.on_move)
        self.widget.layout().addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)

        # display this widget
        self.show()
        return

    def on_move(self, event):
        if event.inaxes == None:
            self.label.setText('place mouse over plot')
            return
        self.label.setText(f'coords: x={round(event.xdata,2)}, y={round(event.ydata,2)}')
        return
    
    def fill(self, *args, data=None, **kwargs):
        return self.canvas.axes.fill(*args, data=data, **kwargs)
    
    def plot(self,*args, scalex=True, scaley=True, data=None, **kwargs):
        return self.canvas.axes.plot(*args, scalex=scalex, scaley=scaley, data=data, **kwargs)
    
    def add_line(self, line:geometric_objects.Line_Segment, **kwargs):
        x1,y1 = line.start_point
        x2,y2 = line.end_point
        l = matplotlib.lines.Line2D([x1, x2], [y1, y2], **kwargs)
        return self.canvas.axes.add_line(l)
    
    def annotate(self, text:str, point:tuple[Number, Number], xytext=None, xycoords='data', textcoords=None, arrowprops=None, annotation_clip=None, **kwargs):
        return self.canvas.axes.annotate(text, point, xytext=xytext, xycoords=xycoords, textcoords=textcoords, arrowprops=arrowprops, annotation_clip=annotation_clip, **kwargs)
    
    def clear_plot(self):
        self.canvas.axes.clear()
        self.figure.canvas.draw_idle()        
        return

class QPushbuttonRTF(QPushButton):
    def __init__(self, parent:QWidget, text_rtf:str):
        super().__init__(parent)

        # the label to support RTF
        self.label:QLabel = QLabel("", self)
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setText(text_rtf)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setMouseTracking(True)

        objects = [self.label]
        for obj in objects:
            obj.enterEvent = self.enterEvent
            obj.leaveEvent = self.leaveEvent
            obj.mousePressEvent = self.mousePressEvent
            obj.mouseReleaseEvent = self.mouseReleaseEvent
        return
    
    def mousePressEvent(self, event):
        return super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        return super().mouseReleaseEvent(event)
    
    def enterEvent(self, event):
        return super().enterEvent(event)

    def leaveEvent(self, event):
        return super().leaveEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.label.resize(self.size())
        return

class QColorSwatchLabel(QLabel):
    clicked       = pyqtSignal(bool)
    color_changed = pyqtSignal()
    def __init__(self, *args, **kwargs):
        # pop our kwargs out as QLabel breaks if we leave them in
        color = QColor()
        k = 'color'
        if k in kwargs:
            color = QColor(kwargs[k])
            kwargs.pop(k)

        self.__manageColorPick = True
        k = 'manage_color_picker'
        if k in kwargs:
            self.__manageColorPick = bool(kwargs[k])
            kwargs.pop(k)
        
        # now init QLabel
        super().__init__(*args, **kwargs)
        self.setMinimumSize(32,32)
        self.setMaximumSize(32,32)

        # apply our plucked color now; because QLabel.__init__ must be called before this
        self.color = color
        pass

    def __updateColorPick(self):
        if not self.has_color():return None
        self.setStyleSheet(f"background-color: {self.get_html_rgba()};border: 1px solid black;")
        self.color_changed.emit()
        return
        
    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, color:QColor):
        self.__color = color
        self.__updateColorPick()
        return
    
    def pick_new_color(self):
        color_dialog  = QColorDialog()
        color_dialog.setCurrentColor(self.color)
        color_dialog.setWindowTitle(self.toolTip())
        color_dialog.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel, on=True)
        if color_dialog.exec_() == QDialog.DialogCode.Accepted:
            self.color = color_dialog.selectedColor()
        color_dialog.deleteLater()
        return
    
    def mousePressEvent(self, event):
        if self.__manageColorPick:
            self.pick_new_color()
        self.clicked.emit(False)
        return super().mousePressEvent(event)

    def has_color(self) -> bool:
        if hasattr(self, 'color'):
            if isinstance(self.color, QColor):
                return True
        return False
    
    def get_rgba_int(self) -> tuple[Number,Number,Number,Number]:
        if not self.has_color():return None
        return (self.color.red(),self.color.green(),self.color.blue(),self.color.alpha())
    
    def set_rgba_int(self, values):
        clr = QColor()
        clr.setRed(values[0])
        clr.setGreen(values[1])
        clr.setBlue(values[2])
        clr.setAlpha(values[3])
        self.color = QColor(clr)
    
    def get_matplotlib_rgba(self) -> tuple[Number,Number,Number,Number]:
        if not self.has_color():return None
        r = self.color.red()/256
        g = self.color.green()/256
        b = self.color.blue()/256
        a = self.color.alpha()/256
        return (r,g,b,a)
    
    def get_html_rgba(self) -> str:
        if not self.has_color():return None
        return f'rgba({self.color.red()}, {self.color.green()}, {self.color.blue()}, {self.color.alpha()})'

class QCalcWidget(QWidget, wdg_calc.Ui_Form):
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self.setupUi(self)
        self.show()

        self.__frmla  = ''
        self._sqrting = False
        self._dpSqrt  = 0

        hstLy = parent.layout()
        hstLy.addWidget(self)

        self.pushButton_28.clicked.connect(self.calculate)
        self.pushButton_29.clicked.connect(self.clear_history)
        self.pushButton_31.clicked.connect(self.clear_history)
        self.pushButton_30.clicked.connect(self.clear_current)
        

        # use the designer/standard buttons and add out overlay to them
        btn:QPushButton = self.pushButton_21
        btn_layout = btn.parent().layout()

        #region top row items
        self._pb_oox = QPushbuttonRTF(btn.parent(),"X<sup>-1</sup>")
        self._pb_oox.clicked.connect(partial(self.eval_prefix_append, '1/(', '<sup>-1</sup>('))
        btn_layout.replaceWidget(btn, self._pb_oox)
        btn.setParent(None)
        btn.deleteLater()

        btn:QPushButton = self.pushButton_25
        self._pb_asin = QPushbuttonRTF(btn.parent(),"Sin<sup>-1</sup>")
        self._pb_asin.clicked.connect(partial(self.prefix_formula, 'math.asin(', 'Sin<sup>-1</sup>('))
        btn_layout.replaceWidget(btn, self._pb_asin)
        btn.setParent(None)
        btn.deleteLater()

        btn:QPushButton = self.pushButton_26
        self._pb_acos = QPushbuttonRTF(btn.parent(),"Cos<sup>-1</sup>")
        self._pb_acos.clicked.connect(partial(self.prefix_formula, 'math.acos(', 'Cos<sup>-1</sup>('))
        btn_layout.replaceWidget(btn, self._pb_acos)
        btn.setParent(None)
        btn.deleteLater()

        btn:QPushButton = self.pushButton_27
        self._pb_atan = QPushbuttonRTF(btn.parent(),"Tan<sup>-1</sup>")
        self._pb_atan.clicked.connect(partial(self.prefix_formula, 'math.atan(', 'Tan<sup>-1</sup>('))
        btn_layout.replaceWidget(btn, self._pb_atan)
        btn.setParent(None)
        btn.deleteLater()
        #endregion

        #region 2nd row items
        
        btn:QPushButton = self.pushButton_20
        self._pb_sqr = QPushbuttonRTF(btn.parent(),"X<sup>2</sup>")
        self._pb_sqr.clicked.connect(partial(self.append_formula, '**2', '**2'))
        btn_layout.replaceWidget(btn, self._pb_sqr)
        btn.setParent(None)
        btn.deleteLater()

        btn:QPushButton = self.pushButton_22
        self._pb_sin = QPushbuttonRTF(btn.parent(),"Sin")
        self._pb_sin.clicked.connect(partial(self.prefix_formula, 'math.sin(', 'Sin('))
        btn_layout.replaceWidget(btn, self._pb_sin)
        btn.setParent(None)
        btn.deleteLater()

        btn:QPushButton = self.pushButton_23
        self._pb_cos = QPushbuttonRTF(btn.parent(),"Cos")
        self._pb_cos.clicked.connect(partial(self.prefix_formula, 'math.cos(', 'Cos('))
        btn_layout.replaceWidget(btn, self._pb_cos)
        btn.setParent(None)
        btn.deleteLater()

        btn:QPushButton = self.pushButton_24
        self._pb_tan = QPushbuttonRTF(btn.parent(),"Tan")
        self._pb_tan.clicked.connect(partial(self.prefix_formula, 'math.tan(', 'Tan('))
        btn_layout.replaceWidget(btn, self._pb_tan)
        btn.setParent(None)
        btn.deleteLater()
        #endregion

        #region 3rd row items
        btn:QPushButton = self.pushButton_19
        self._pb_sqrt = QPushbuttonRTF(btn.parent(),'<span style="white-space: nowrap">&radic;<span style="text-decoration:overline;">&nbsp;X&nbsp;</span></span>')
        self._pb_sqrt.clicked.connect(self.sqrt_start)
        btn_layout.replaceWidget(btn, self._pb_sqrt)
        btn.setParent(None)
        btn.deleteLater()
        #endregion

        #region generic calc buttons
        self.pushButton_18.clicked.connect(partial(self.append_formula, '(', '('))
        self.pushButton_17.clicked.connect(partial(self.append_formula, ')', ')'))
        self.pushButton_13.clicked.connect(partial(self.append_formula, '/', '/'))
        self.pushButton_12.clicked.connect(partial(self.append_formula, '*', '*'))
        self.pushButton_11.clicked.connect(partial(self.append_formula, '-', '-'))        
        self.pushButton_10.clicked.connect(partial(self.append_formula, '+', '+'))

        self.pushButton_14.clicked.connect(partial(self.append_formula, '7', '7'))
        self.pushButton_15.clicked.connect(partial(self.append_formula, '8', '8'))
        self.pushButton_16.clicked.connect(partial(self.append_formula, '9', '9'))
        self.pushButton_7.clicked.connect(partial(self.append_formula, '4', '4'))
        self.pushButton_8.clicked.connect(partial(self.append_formula, '5', '5'))
        self.pushButton_9.clicked.connect(partial(self.append_formula, '6', '6'))
        self.pushButton_4.clicked.connect(partial(self.append_formula, '1', '1'))
        self.pushButton_5.clicked.connect(partial(self.append_formula, '2', '2'))
        self.pushButton_6.clicked.connect(partial(self.append_formula, '3', '3'))

        self.pushButton_2.clicked.connect(partial(self.append_formula, '.', '.'))
        self.pushButton_3.clicked.connect(partial(self.append_formula, '(-', '(-'))
        self.pushButton.clicked.connect(partial(self.append_formula, '0', '0'))
        #endregion

        return
    
    def sqrt_start(self):
        self._sqrting = True
        self.append_text(self.textEdit, '<span style="white-space: nowrap">&radic;<span style="text-decoration:overline;">&nbsp;')
        self.__frmla = f'{self.__frmla}math.sqrt('
        return
    
    def eval_prefix_append(self, formula, html):
        self.__frmla = f'{formula}{self.__frmla})'
        self.textEdit.append({html})
        return
    
    def append_text(self, text_edit:QTextEdit, text:str):
        text_edit.selectAll()
        md:QMimeData = text_edit.createMimeDataFromSelection()        
        text_edit.setText(f'{md.text()}{text}')
        return
    
    def prefix_text(self, text_edit:QTextEdit, text:str):
        text_edit.selectAll()
        md:QMimeData = text_edit.createMimeDataFromSelection()
        text_edit.setText(f'{text}{md.text()}')
        return
    
    def prefix_formula(self, formula, html):
        self.__frmla = f'{formula}{self.__frmla})'
        self.prefix_text(self.textEdit,html)
        self.append_text(self.textEdit,')')
        return
    
    def append_formula(self, formula, html):
        self.__frmla = f'{self.__frmla}{formula}'
        if self._sqrting and html=='(':
            self._dpSqrt += 1
            self.append_text(self.textEdit,html)
        elif self._sqrting and html==')':
            self._sqrting = bool(self._dpSqrt > 0)
            if self._dpSqrt > 0:
                self._dpSqrt -= 1
                self.append_text(self.textEdit,html)
            else:
                self._dpSqrt = 0
                self.textEdit.selectAll()
                md:QMimeData = self.textEdit.createMimeDataFromSelection()
                vals = md.text().split('√')
                self.textEdit.setText(f'{vals[0]}<span style="white-space: nowrap">&radic;<span style="text-decoration:overline;">&nbsp;{vals[1]}</span></span>')
                self._sqrting = False
        else:
            self.append_text(self.textEdit,html)
        return
    
    def calculate(self):
        if self.__frmla is not None:
            try:
                self.textEdit.selectAll()
                self.textEdit_2.selectAll()
                md:QMimeData = self.textEdit.createMimeDataFromSelection()
                mh:QMimeData = self.textEdit_2.createMimeDataFromSelection()

                val = eval(self.__frmla)
                if val < 0:
                    val = f'({val})'
                self.textEdit.setText(f'<b>{val}</b>')
                self.textEdit_2.setText(f'{md.text()}=<b>{val}</b><br><br>{mh.text()}')
            except Exception as e:
                print(f"failed to eval: '{self.__frmla}'\n{e}")
                return self.clear_current()
            self.__frmla = ''
        return
    
    def clear_history(self):
        self.textEdit_2.setText('')        
        return
    
    def clear_current(self):
        self.textEdit.setText('')
        self.__frmla = ''
        return

class QTriangle_Solver(QWidget, wdg_triangle.Ui_Form):
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self.setupUi(self)
        self.show()
        parent.layout().addWidget(self)
        self.pushButton.clicked.connect(self._solveTriangle)

        # load in the matplot canvas
        self._cnvs = QMatplot(self.tab, width=5, height=4, dpi=100)

        # link to an empty triangle to get used later
        self.__t = geometric_objects.Triangle()

        # load in the Wiki
        self.textEdit.setText(self.__t.wiki_html)

        # link the radio buttons checked change
        self.radioButton_2.clicked.connect(partial(self._solveTypeChange,['Side A', 'Side B', 'Side C']))
        self.radioButton_3.clicked.connect(partial(self._solveTypeChange,['Angle A', 'Angle B', 'Side A']))
        self.radioButton_6.clicked.connect(partial(self._solveTypeChange,['Angle A', 'Side C', 'Angle B']))
        self.radioButton_5.clicked.connect(partial(self._solveTypeChange,['Side A', 'Side B', 'Angle A']))
        self.radioButton.clicked.connect(partial(self._solveTypeChange,['Side A', 'Angle C', 'Side B']))
        self.radioButton_13.clicked.connect(partial(self._solveTypeChange,['Coord A', 'Coord B', 'Coord C']))

        self.spinBox:QSpinBox
        self.spinBox.valueChanged.connect(self._reloadValues)

        # link up annotation parts
        self.__annotationsParts()
        
        # default info for triange
        self.__defaultTriangle()
        return
    
    def __annotationsParts(self):
        self.__exportSetting = QAction(QIcon(os.path.join(PTH_IMG,'export.png')), "Export Settings", self)
        self.__importSetting = QAction(QIcon(os.path.join(PTH_IMG,'import.png')), "Import Settings", self)
        self.__exportSetting.triggered.connect(partial(self.__pickleSettings, False))
        self.__importSetting.triggered.connect(partial(self.__pickleSettings, True))
        self.toolButton_6.setDefaultAction(self.__importSetting) # import settings
        self.toolButton_7.setDefaultAction(self.__exportSetting) # export settings

        # --- settings
        self.settings:dict[str, dict[str,QWidget]] = {}
        self.settings['fill']    = {'checkBox':None, 'label':self.label_51}
        self.settings['outline'] = {'checkBox':None, 'label':self.label_53}

        self.settings['lengths'] = {'label':self.label_55, 'checkBox':self.checkBox}
        self.settings['points']  = {'label':self.label_58, 'checkBox':[self.radioButton_9, self.radioButton_10, self.radioButton_11, self.radioButton_12]}
        self.settings['medians'] = {'label':self.label_54, 'checkBox':[self.radioButton_7, self.radioButton_4, self.radioButton_8]}

        # --- --- update label object to custom object
        for k in self.settings.keys():
            # build custom label object <QColorSwatchLabel>
            label  = QColorSwatchLabel(self, **{'color':QColor('#aa007d')})            
            label.setToolTip(f"Pick '{k.title()}' color")
            label.color_changed.connect(self._renderGraph) # partial(self.__selectColor, k)
            
            # replace built-in QLabel with our QColorSwatchLabel
            layout = self.settings[k]['label'].parent().layout()
            layout.replaceWidget(self.settings[k]['label'], label)

            # store the label object
            self.settings[k]['label'] = label

            # link the checkbox action to refresh matplotlib object
            cb = self.settings[k]['checkBox']
            if isinstance(cb, QCheckBox):
                cb.stateChanged.connect(self._renderGraph)
            elif isinstance(cb, list):
                item:QRadioButton
                for item in cb:
                    item.toggled.connect(self._renderGraph)
        return
    
    def __defaultTriangle(self):
        self.lineEdit.setText('4')
        self.lineEdit_2.setText('3')
        self.lineEdit_3.setText('5')
        self._solveTriangle()
        # --- --- import user conifig
        if os.path.isfile(PTH_PKL):
            self.__pickleSettings(True)
        return
    
    def __get_setting_pickle(self) -> dict:
        '''coverts the Qt widget info into picklable dict'''
        rtn = {}
        for k,v in self.settings.items():
            rtn[k] = v['label'].get_rgba_int()
        return rtn
    
    def __set_setting_pickle(self, data:dict) -> None:
        '''coverts the pickled dict back into settings dict'''
        pks = data.keys()
        for k,v in self.settings.items():
            if k in pks:
                v['label'].set_rgba_int(data[k])
        return
    
    def __pickleSettings(self, import_file:bool):   
        if import_file:
            file = open(PTH_PKL, 'rb')
            self.__set_setting_pickle(pickle.load(file))
            file.close()
            QMessageBox.information(None,"System Information Notification",'Import complete')
        else:
            file = open(PTH_PKL, 'wb')
            pickle.dump(self.__get_setting_pickle(), file)
            file.close()
            QMessageBox.information(None,"System Information Notification",'Export complete')
        return
    
    def _reloadValues(self):
        self.__prc = self.spinBox.value()
        self.__dta = self.__t.get_data()
        v = self.__dta
        self.label_7.setText('{:,g}'.format(round(v['side_a'].length,self.__prc)))
        self.label_8.setText('{:,g}'.format(round(v['side_b'].length,self.__prc)))
        self.label_9.setText('{:,g}'.format(round(v['side_c'].length,self.__prc)))
        self.label_16.setText('{:,g}'.format(round(v['angle_a'],self.__prc)))
        self.label_17.setText('{:,g}'.format(round(v['angle_b'],self.__prc)))
        self.label_18.setText('{:,g}'.format(round(v['angle_c'],self.__prc)))
        self.label_19.setText('{:,g}'.format(round(v['area'],self.__prc)))
        self.label_22.setText('{:,g}'.format(round(v['perimeter'],self.__prc)))

        # --- load medians lengths        
        self.label_47.setText('{:,g}'.format(round(v['lmA'].length,self.__prc)))
        self.label_48.setText('{:,g}'.format(round(v['lmB'].length,self.__prc)))
        self.label_49.setText('{:,g}'.format(round(v['lmC'].length,self.__prc)))

        # --- load coords
        lbl:QLabel
        key:str
        for lbl, key in {self.label_29:'side_a', self.label_30:'side_b', self.label_31:'side_c',self.label_34:'lmA', self.label_37:'lmB', self.label_38:'lmC'}.items():
            x1,y1 = v[key].start_point
            x2,y2 = v[key].end_point
            a = f"{'{:,g}'.format(round(x1,self.__prc))}, {'{:,g}'.format(round(y1,self.__prc))}"
            b = f"{'{:,g}'.format(round(x2,self.__prc))}, {'{:,g}'.format(round(y2,self.__prc))}"
            lbl.setText(f"({a}) ({b})")
        
        
        # finally render the triangle; so we have all the data we might need to label said graph
        return self._renderGraph()

    def _solveTriangle(self):
        # check the provided information
        # -- if values missing we cannot solve
        p1 = self.lineEdit.text()
        p2 = self.lineEdit_2.text()
        p3 = self.lineEdit_3.text()
        if self.radioButton_13.isChecked():
            # try to cast as CSV x,y coords
            try:
                temp = []
                temp += p1.split(',')
                temp += p2.split(',')
                temp += p3.split(',')
                v = [float(i) for i in temp]
                x1 = v[0]
                y1 = v[1]
                x2 = v[2]
                y2 = v[3]
                x3 = v[4]
                y3 = v[5]
                self.__t.solve_coords((x1,y1), (x2,y2), (x3,y3))
                return self._reloadValues()
            except Exception as ex:
                return warningMessageWindow(self, inspect.stack()[0], f"Could not cast provided values as CSV x,y coords; please try again\n{ex}")
        else:
            try:
                p1 = float(p1)
                p2 = float(p2)
                p3 = float(p3)
            except Exception as ex:
                return warningMessageWindow(self, inspect.stack()[0], "This does not do symbol solves at this time ... speak with dev")

        # determin what way to solve the triangle
        # then have the class solve it
        t = self.__t
        try:
            if self.radioButton_2.isChecked():    # SSS
                t.solve_SSS(p1, p2, p3)
            elif self.radioButton_3.isChecked():  # AAS
                t.solve_AAS(p1, p2, p3)
            elif self.radioButton_6.isChecked():  # ASA
                t.solve_ASA(p1, p2, p3)
            elif self.radioButton_5.isChecked():  # SSA
                t.solve_SSA(p1, p2, p3)
            elif self.radioButton.isChecked():    # SAS
                t.solve_SAS(p1, p2, p3)
        except Exception as e:
            return warningMessageWindow(self, inspect.stack()[0], f"Could not solve triangle; please ensure you've selected the right option to solve.\nError: '{e}'")
        
        # now that its solved load that info on the form        
        return self._reloadValues()
    
    def _renderGraph(self, *args, **kwargs):
        # allowing args and kwargs so our shit dont break if passed some shit

        # get the specified colors of the polygon
        fc = self.settings['fill']['label'].get_matplotlib_rgba()
        ol = self.settings['outline']['label'].get_matplotlib_rgba()

        # clear previous data from graph
        self._cnvs.clear_plot()

        # get polygon coord list and plot polygon
        x,y = self.__t.triangle_matplotlib_coords
        self._cnvs.fill(x,y,facecolor=fc, edgecolor=ol, linewidth=1)

        # expand the graph with hidden dots
        m = max([max(x),max(y)])
        m = m+(m/3)
        self._cnvs.plot(m,m)
        self._cnvs.plot(-m/3,-m/3) 

        # get the triangle data for use
        if not self.radioButton_9.isChecked() or not self.radioButton_7.isChecked() or self.checkBox.isChecked():
            dta = self.__dta
            mid = self.__t.triangle_matplotlib_midpoint_coords

            abc = {'A':{'index':0,'offset':(-1,-1)},
                   'B':{'index':1,'offset':(.5,.5)},
                   'C':{'index':2,'offset':(0,-1)}}
            
            m_abc = {'mA':{'index':0,'offset':(-1.5,-.5),'shift':(.25,-.5)},
                     'mB':{'index':1,'offset':(0,.25),'shift':(0,-1)},
                     'mC':{'index':2,'offset':(0,-.25),'shift':(-1.75,0)}}

            # lengths notation
            if self.checkBox.isChecked():
                sec_color = self.settings['lengths']['label'].get_matplotlib_rgba()
                for k,v in m_abc.items():
                    x1,y1 = mid[0][v['index']], mid[1][v['index']]
                    k1 = f'side_{k[1:].lower()}'
                    self._cnvs.annotate('{:,g}'.format(round(dta[k1].length,self.__prc)),(x1,y1),xytext=v['shift'],textcoords='offset fontsize',color=sec_color)

            # point notation        
            if not self.radioButton_9.isChecked():                
                sec_color = self.settings['points']['label'].get_matplotlib_rgba()
                if self.radioButton_10.isChecked(): # Names
                    for k,v in abc.items():
                        x1,y1 = x[v['index']], y[v['index']]
                        self._cnvs.annotate(k,(x1,y1),xytext=v['offset'],textcoords='offset fontsize',color=sec_color)
                elif self.radioButton_12.isChecked(): # coords
                    for k,v in abc.items():
                        x1,y1 = x[v['index']], y[v['index']]
                        self._cnvs.annotate(f'({round(x1,self.__prc)}, {round(y1,self.__prc)})',(x1,y1),xytext=v['offset'],textcoords='offset fontsize',color=sec_color)
                elif self.radioButton_11.isChecked(): # Angles
                    for k,v in abc.items():
                        x1,y1 = x[v['index']], y[v['index']]
                        a = dta[f"angle_{k.lower()}"]
                        self._cnvs.annotate(f'{round(a,self.__prc)}°',(x1,y1),xytext=v['offset'],textcoords='offset fontsize',color=sec_color)

            # median notation
            if not self.radioButton_7.isChecked():
                sec_color = self.settings['medians']['label'].get_matplotlib_rgba()                
                if self.radioButton_4.isChecked(): # Names
                    for k,v in m_abc.items():
                        x1,y1 = mid[0][v['index']], mid[1][v['index']]
                        self._cnvs.annotate(f'{k}',(x1,y1),xytext=v['offset'],textcoords='offset fontsize',color=sec_color)
                elif self.radioButton_8.isChecked(): # Lines
                    d = self.__t.medians
                    for k,v in m_abc.items():
                        self._cnvs.add_line(d[f"l{k}"], marker='o', color=sec_color, linewidth=1)
        return
        
    def _solveTypeChange(self, quick_label:list[str], checked:bool):
        if not checked: return
        lbl = [self.label, self.label_2, self.label_3]
        for i in range(3):
            lbl[i].setText(quick_label[i])
        return
    
    def test_triangle(self):
        self.__t.solve_SSA(12,9,87)
        self._renderGraph()
        # x,y = self.__t.coords_list

        # self._cnvs.fill(x,y,facecolor='lightblue', edgecolor='black', linewidth=1)
        # for i in range(1,len(x)-1):
        #     self._cnvs.annotate(f'({x[i]}, {y[i]})',(x[i],y[i]),xytext=(.5,.5),textcoords='offset fontsize')
        
        # m = max([max(x),max(y)])
        # m = m+(m/3)
        # self._cnvs.plot(m,m)
        # self._cnvs.plot(-m/3,-m/3)
        return

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    plt.show()