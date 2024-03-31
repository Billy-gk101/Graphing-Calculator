# =============================================================================
# CODE IMPORTS
# =============================================================================
from __future__ import annotations
import math, copy
from numbers import Number
from shapely import Point, LineString, Polygon, GeometryCollection
from shapely.geometry.base import BaseGeometry
    
class Line_Segment():
    def __init__(self, *args, **kwargs):
        self.__lineString:LineString = None
        return
    
    def __str__(self):
        return f"{self.length}"
    
    def get_data(self) -> dict:
        rtn = {}
        rtn['length']      = self.length
        rtn['start_point'] = self.start_point
        rtn['end_point']   = self.end_point
        rtn['mid_point']   = self.mid_point
        return rtn
    
    #region checks
    def intersection(self, geometry:BaseGeometry):
        '''Returns the points that is shared between this and provided geometry.'''
        return self.__lineString.intersection(geometry)

    def crosses(self, geometry:BaseGeometry) -> bool:
        '''does this line and geometry intersect'''
        return self.__lineString.crosses(geometry)       
    #endregion

    #region properties
    @property
    def geometry(self):
        return LineString(self.coords)
    
    @property
    def start_point(self) -> tuple[Number,Number]:
        '''line start-point coordinate'''
        return self.coords[0]
    
    @property
    def end_point(self) -> tuple[Number,Number]:
        '''line end-point coordinate'''
        return self.coords[1]
    
    @property
    def mid_point(self) -> tuple[Number,Number]:
        c = self.coords
        x1, y1 = c[0]
        x2, y2 = c[1]
        return ((x1+x2)/2, (y1+y2)/2)
    
    @property
    def coords(self) -> list[tuple[Number,Number],tuple[Number,Number]]:
        '''
        line geometry coordinates

        Returns
        -------
        list[tuple[Number,Number],tuple[Number,Number]]
            [(start_x, start_y), (end_x, end_y)]
        '''
        return list(self.__lineString.coords)
    
    @property
    def y_intercept(self) -> Number:
        '''
        Where the line intercepts (crosses) the Y-axis

        this is defined algebraically as y=mx+b where b is the intercept value
        so to reverse this from information known we'd use b=y-(m*x)
        '''
        m   = self.slope
        x,y = self.start_point
        if isinstance(m, Number):
            return y-(m*x)
        return f"{y}-({m}*{x})"

    @ property
    def slope(self) -> Number:
        '''
        slope of line

        this has a few terms; slope, gradient, rise/run, etc
        this is defined algebraically as m=(y₂-y₁)/(x₂-x₁)
        '''
        c = self.coords
        if not None in c:
            x,y = c
            try:
                return (y[1]-y[0])/(x[1]-x[0])
            except Exception as e:
                return f"{y[1]-y[0]}/{x[1]-x[0]}"
        return None
    
    @property
    def length(self):
        '''
        length of line

        this is defined algebraically as d=√( (x2-x1)² + (y2-y1)² )
        '''
        return self.__lineString.length
    #endregion

    #region solvers
    def get_PSL_points(self, point:tuple[Number,Number], slope:Number, length:Number) -> list[tuple[Number,Number],tuple[Number,Number]]:
        '''
        solves line from provided information

        create/solve a line with only knowing its start_point, slope and length; this will give us 2 values when we substitute
        a point to either side of the provided point
        The equation of a line in point slope form is y-y1 = m(x-x1); with this lets substitute with information we know
        x1,y1=start_point; m=slope; c=1/√(1+(m**2)); rc=length*c; s=m/√(1+(m**2)); rs=length*s
        now we can define the other point (x1-rc, ry1-rs) or (x1+rc, y1+rs,rv)

        Parameters
        ----------
        point : tuple[Number,Number]
            a point of the line to define
        slope : Number
            slope of the line to define
        length: Number
            length of the line to define
        
        Returns
        -------
        points to either side of the given point along the line and distance provided as length 
        list[tuple[Number,Number],tuple[Number,Number]]
            [(x1, y1), (x2, y2)]
        '''
        rv    = 6
        m2    = slope**2
        c     = 1/math.sqrt(1+m2)
        s     = slope/math.sqrt(1+m2)
        x1,y1 = point
        rc    = length*c
        rs    = length*s        
        return [(round(x1-rc,rv), round(y1-rs,rv)),(round(x1+rc,rv), round(y1+rs,rv))]
    
    def solve_start_SL(self, point:tuple[Number,Number], slope:Number, length:Number):
        '''
        assumes the provided is the start point and the 2nd calculated value from get_PSL_points function is the end of the line

        this then populates properties to completely define the line

        Parameters
        ----------
        point : tuple[Number,Number]
            start point of the line to define
        slope : Number
            slope of the line to define
        length: Number
            length of the line to define
        '''
        points = self.get_PSL_points(point, slope, length)
        self.__lineString = LineString([point, points[1]])
        return
    
    def solve_end_SL(self, point:tuple[Number,Number], slope:Number, length:Number):
        '''
        assumes 1st calculated value from get_PSL_points function is the start of the line and the provided is the end point

        this then populates properties to completely define the line
        
        Parameters
        ----------
        point : tuple[Number,Number]
            end point of the line to define
        slope : Number
            slope of the line to define
        length: Number
            length of the line to define
        '''
        points = self.get_PSL_points(point, slope, length)
        self.__lineString = LineString([points[0], point])
        return
    
    def solve_points(self, start_point:tuple[Number,Number], end_point:tuple[Number,Number]):
        '''
        assumes 1st calculated value from get_PSL_points function is the start of the line and the provided is the end point

        this then populates properties to completely define the line
        
        Parameters
        ----------
        start_point : tuple[Number,Number]
            start point of the line to define
        end_point   : tuple[Number,Number]
            end point of the line to define
        '''
        self.__lineString = LineString([start_point, end_point])
        return
    #endregion
        
    #region wiki stuff
    @property
    def equation_points(self):
        sq  = '<sup>2</sup>'
        s1  = '<sub>1</sub>'
        s2  = '<sub>2</sub>'
        slf = self.equation_slope['equation']
        return {'title':'Solving Line from points', 'desc':"Finding length of line and slope given just its points", 
                'equation':f'start with getting the slope "{slf}" now let d be the length with "d=<span style="white-space: nowrap">&radic;<span style="text-decoration:overline;">(x{s2}-x{s1}){sq} + (y{s2}-y{s1}){sq})</span></span>"'}
    
    @property
    def equation_pointLine(self):
        return {'title':'Solving Line using point and slope', 'desc':"Finding other end of line given start_point and slope; this results in 2 plausible points", 
                'equation':f'x1,y1=start_point; m=slope; c=1/√(1+(m**2)); rc=length*c; s=m/√(1+(m**2)); rs=length*s || now th points are (x1-rc, y1-rs),(x1+rc, y1+rs)'}
    
    @property
    def equation_slope(self):
        s1 = '<sub>1</sub>'
        s2 = '<sub>2</sub>'
        return {'title':'Solving slope', 'desc':"taking coords of line and determining the slope", 
                'equation':f'let m be slope: m = (y{s2}-y{s1})/(x{s2}-x{s1})'}
    
    def wiki_html(self) -> str:
        # remove space/padd from headings
        h1 = f'<h1 style="padding:0;margin:0;">'
        h2 = f'<h2 style="padding:0;margin:0;">'
        h3 = f'<h3 style="padding:0;margin:0;">'

        # compile the info (Laws and Equations) from the class
        compiled = ''

        compiled += f'{h1}Line Segments</h1>'
        for d in [self.equation_slope, self.equation_pointLine, self.equation_points]:
            compiled += f"{h3}{d['title']}</h3><i>{d['desc']}</i><br>{d['equation']}<br>"

        return compiled
    #endregion

class Triangle():
    '''
    Container (not collection) of shapely objects used to define a triangle

    Leveraging Shaply to assist in the managment of items and checking overlap, intersects, boundary, etc.
    not doing inheritance as this class has solvers that will generate all the dependent geometry;
    it will build collections such as the line_segments (Line_Segment) that build the triangle iteself
    '''
    ## https://www.mathsisfun.com/algebra/trig-solving-triangles.html
    #             Bϴ
    #           .    .
    #         .        .
    #        C           A
    #     .                .
    #   .                    .
    # Aϴ . . . .  B  . . . .  Cϴ
    def __init__(self) -> None:

        # angles of triangle ... these dont appear to be anywhere in the shapely structure
        self.__Aϴ:Number = None # the angle at point A between lAC & lAB
        self.__Bϴ:Number = None # the angle at point B between lAB & lBC
        self.__Cϴ:Number = None # the angle at point C between lAC & lBC

        # union these to create a triangle then we can get more info from it
        self.__lAC:Line_Segment = None # the line between point A and C (side b) 
        self.__lBC:Line_Segment = None # the line between point B and C (side a)
        self.__lAB:Line_Segment = None # the line between point A and B (side c)

        # here are the medians
        self.__lmA:Line_Segment = None # the line between point A and midpoint lBC
        self.__lmB:Line_Segment = None # the line between point B and midpoint lAC
        self.__lmC:Line_Segment = None # the line between point C and midpoint lAB

        # to get set to the colection of lAC, lAB, lBC everytime they're redefined
        self.__tri:GeometryCollection = None
        return
    
    def get_data(self):
            '''quick way to get form information about the triangle geometry'''
        #     v['lmA']}")
        # self.label_48.setText(f"{v['lmB']}")
        # self.label_49.setText(f"{v['lmC']}")
            return {"side_a":self.side_a, "side_b":self.side_b, "side_c":self.side_c, 
                    "angle_a":self.Aϴ, "angle_b":self.Bϴ, "angle_c":self.Cϴ, 
                    "area":self.area, "perimeter":self.perimeter, "inradius":self.inradius,
                    "circumradius":self.circumradius, "centroid":self.centroid, 'medians':self.medians,
                    'lmA':self.lmA, 'lmB':self.lmB, 'lmC':self.lmC}
    
    # region matplotlib_helpers
    @property
    def triangle_matplotlib_coords(self) -> list[list[Number], list[Number]]:
        '''Separate arrays of X and Y coordinate values of triangle geometry'''        
        # the built in XY feature throws and error 'NotImplementedError'
        # self.__tri.xy -- doing this myself
        x,y = [],[]
        for coord in self.triangle_coords:
            x.append(coord[0])
            y.append(coord[1])
        return [x,y]
    @property
    def triangle_matplotlib_midpoint_coords(self) -> list[list[Number], list[Number]]:
        '''Separate arrays of X and Y coordinate values of triangle geometry midpoints'''
        x,y = [],[]
        for coord in self.triangle_midpoint_coords:
            x.append(coord[0])
            y.append(coord[1])
        return [x,y]
    # endregion

    # region property defs
    @property
    def perimeter(self):        
        return self.__tri.length
    @property
    def area(self) -> float:
        '''Unitless area of the triangle geometry'''
        a = self.side_a.length
        b = self.side_b.length
        c = self.side_c.length
        s = self.perimeter/2
        # Area = Square root of √( s(s-a)(s-b)(s-c) ) where s is half the perimeter
        return math.sqrt(s*(s-a)*(s-b)*(s-c))
    @property
    def bounds(self) -> tuple:
        '''minimum bounding region of the triangle geometry'''
        return self.__tri.bounds
    @property
    def inradius(self):
        '''triangle geometry area/perimeter'''
        return self.area/self.perimeter
    @property
    def centroid(self) -> Point:
        '''geometric center of the triangle geometry'''
        return self.__tri.centroid
    @property
    def circumradius(self):
        '''the distance from centroid to A,B, or C points of triangle'''
        cr = Line_Segment()
        cr.solve_points(self.centroid, self.__lAC.end_point)
        return cr.length
    @property
    def Aϴ(self) -> Number:
        '''the angle (in degrees) at point A between lAC & lAB'''
        return self.__Aϴ    
    @property
    def Bϴ(self) -> Number:
        '''the angle (in degrees) at point B between lAB & lBC'''
        return self.__Bϴ    
    @property
    def Cϴ(self) -> Number:
        '''the angle (in degrees) at point C between lAC & lBC'''
        return self.__Cϴ    
    @property
    def lAC(self) -> Line_Segment:
        '''the line between point A and C (side b)'''
        return copy.deepcopy(self.__lAC)
    @property
    def lBC(self) -> Line_Segment:
        '''the line between point B and C (side a)'''
        return copy.deepcopy(self.__lBC)
    @property
    def lAB(self) -> Line_Segment:
        '''the line between point A and B (side c)'''
        return copy.deepcopy(self.__lAB)
    @property
    def side_a(self):
        '''side a: the line between point B and C'''
        return self.lBC
    @property
    def side_b(self):
        '''side b: the line between point A and C'''
        return self.lAC
    @property
    def side_c(self):
        '''side c: the line between point A and B'''
        return self.lAB
    @property
    def lmA(self) -> Line_Segment:
        '''the line between point A and midpoint lBC'''
        return copy.deepcopy(self.__lmA)
    @property
    def lmB(self) -> Line_Segment:
        '''the line between point B and midpoint lAC'''
        return copy.deepcopy(self.__lmB)
    @property
    def lmC(self) -> Line_Segment:
        '''the line between point C and midpoint lAB'''
        return copy.deepcopy(self.__lmC)
    @property
    def triangle_coords(self) -> list[Point]:
        '''triangle geometry coordinates'''
        A,C = self.__lAC.coords
        B   = self.__lBC.coords[0]
        # WTF; self.__tri.coords returns NotImplementedError
        return [A,B,C]
    @property
    def triangle_midpoint_coords(self) -> list[Point]:
        '''triangle geometry midpoint coordinates'''
        return [self.side_a.mid_point,self.side_b.mid_point,self.side_c.mid_point]
    @property
    def medians(self) -> dict[str, Line_Segment]:
        '''medians of triangle geometry'''
        return {'lmA':self.lmA, 'lmB':self.lmB, 'lmC':self.lmC}
    # endregion

    #region wiki stuff
    @property
    def wiki_html(self) -> str:
        # remove space/padd from headings
        h1 = f'<h1 style="padding:0;margin:0;">'
        h2 = f'<h2 style="padding:0;margin:0;">'
        h3 = f'<h3 style="padding:0;margin:0;">'
        
        # compile the info (Laws and Equations) from the class
        compiled = ''

        # {'title', 'desc', 'equation'}
        compiled += f'{h1}Laws</h1>'
        for d in [self.law_sines, self.law_cosines]:
            compiled += f"{h3}{d['title']}</h3><i>{d['desc']}</i><br>{d['equation']}<br>"
        
        compiled += f'{h1}Equations</h1>'
        for d in [self.equation_AAS, self.equation_ASA, self.equation_SAS, self.equation_SSA, self.equation_SSS]:
            compiled += f"{h3}{d['title']}</h3><i>{d['desc']}</i><br>{d['equation']}<br>"

        compiled += f'{h1}Miscellaneous</h1>'
        for d in [self.equation_median, self.equation_area]:
            compiled += f"{h3}{d['title']}</h3><i>{d['desc']}</i><br>{d['equation']}<br>"
        
        compiled += Line_Segment().wiki_html()
        return compiled
    
    def __medianFormula(self, p:list[str]) -> str:        
        return f'm<sup>{p[0]}</sup><span style="white-space: nowrap">&radic;<span style="text-decoration:overline;">(2{p[1]}<sup>2</sup>+2{p[2]}<sup>2</sup>-{p[0]}<sup>2</sup>)/4</span></span>'
    
    @property
    def equation_area(self):
        return {'title':"area [Heron's Formula]", 'desc':"Heron of Alexandria formula for triangle area", 
                'equation':'Area = Square root of <span style="white-space: nowrap">&radic;<span style="text-decoration:overline;">s(s-a)(s-b)(s-c)</span></span> where s is half the perimeter'}

    @property
    def equation_AAS(self):
        return {'title':'Angle-Angle-Side', 'desc':'Two Angles and a Side not between',
                'equation':'use The Law of Sines first to calculate one of the other two angles<br>then use the three angles add to 180° to find the other angle<br>finally use The Law of Sines again to find the unknown side'}
    
    @property
    def equation_ASA(self):
        return {'title':'Angle-Side-Angle', 'desc':'Two Angles and a Side between', 
                'equation':'find the third angle using the three angles add to 180°<br>then use The Law of Sines to find each of the other two sides.'}
    
    @property
    def equation_SAS(self):
        return {'title':'Side-Angle-Side', 'desc':'Two Sides and an Angle between', 
                'equation':'use The Law of Cosines to calculate the unknown side<br>then use The Law of Sines to find the smaller of the other two angles<br>then use the three angles add to 180° to find the last angle'}
    
    @property
    def equation_SSA(self):
        return {'title':'Side-Side-Angle', 'desc':'Two Sides and a Angle not between', 
                'equation':'use the three angles add to 180° to find the other angle<br>then The Law of Sines to find each of the other two sides.'}
   
    @property
    def equation_SSS(self):
        return {'title':'Side-Side-Side', 'desc':'three sides of the triangle, and want to find the missing angles',
                'equation':'use The Law of Cosines first to calculate one of the angles<br>then use The Law of Cosines again to find another angle<br>and finally use angles of a triangle add to 180° to find the last angle'}
    
    @property
    def equation_median(self):
        e = self.__medianFormula(['a', 'b', 'c'])
        e += f" | {self.__medianFormula(['b', 'a', 'c'])}"
        e += f" | {self.__medianFormula(['c', 'a', 'b'])}"
        return {'title':'Median of a Triangle', 'desc':"a line segment that goes from one of a triangle's three vertexes to the midpoint of the opposite side", 
                'equation':e}
    
    @property
    def law_sines(self):
        return {'title':'Law of Sines', 'desc':"The Law of Sines (or Sine Rule) is very useful for solving triangles", 
                'equation':'a/sin(A) == b/sin(B) == c/sin(C)'}
    
    @property
    def law_cosines(self):
        return {'title':'Law of Cosines', 'desc':"The Law of Cosines (or Cosine Rule) is very useful for solving triangles", 
                'equation':'c<sup>2</sup> = a<sup>2</sup> + b<sup>2</sup> - 2ab cos(C)'}
    #endregion
        
    #region solvers
    def __finishSolve(self, A:Number):

        # finish up with AAS now we have all the degrees and are given side_ via A
        # a/sin(A) = b/sin(B) = c/sin(C)
        sa = round(A/math.sin(math.radians(self.__Aϴ)),2) # a/sin(A)        
        
        C = math.sin(math.radians(self.__Cϴ))*sa
        B = math.sin(math.radians(self.__Bϴ))*sa

        self.__lAB = Line_Segment()
        self.__lAB.solve_start_SL((0,0), math.tan(math.radians(self.__Aϴ)), C)
        self.__lAC = Line_Segment()
        self.__lAC.solve_start_SL((0,0), 0, B)
        self.__lBC = Line_Segment()
        self.__lBC.solve_points(self.__lAB.end_point, self.__lAC.end_point)

        # place lines into a collection for properties
        self.__tri = GeometryCollection([self.__lAC.geometry, self.__lBC.geometry, self.__lAB.geometry])

        # medians
        self.__linesMedians()
        return
    
    def __linesPerimeter(self, coord_A:tuple[Number, Number], coord_B:tuple[Number, Number], coord_C:tuple[Number, Number]):
        self.__lAC = Line_Segment()
        self.__lAC.solve_points(coord_A, coord_C)
        self.__lBC = Line_Segment()
        self.__lBC.solve_points(coord_B, coord_C)
        self.__lAB = Line_Segment()
        self.__lAB.solve_points(coord_A, coord_B)

        self.__tri = GeometryCollection([self.__lAC.geometry, self.__lBC.geometry, self.__lAB.geometry])
        return
    
    def __linesMedians(self):
        A,B,C = self.triangle_coords
        # A,C = self.__lAC.coords
        # B   = self.__lBC.coords[0]
        self.__lmA = Line_Segment()
        self.__lmA.solve_points(A, self.__lBC.mid_point)
        self.__lmB = Line_Segment()
        self.__lmB.solve_points(B, self.__lAC.mid_point)
        self.__lmC = Line_Segment()
        self.__lmC.solve_points(C, self.__lAB.mid_point)
        return
    
    def __solveAnglesFromSides(self,A,B,C):
        a2=A**2
        b2=B**2
        c2=C**2
        self.__Aϴ = math.degrees(math.acos((b2+c2-a2)/(2*B*C)))
        self.__Bϴ = math.degrees(math.acos((c2+a2-b2)/(2*C*A)))
        self.__Cϴ = 180-(self.__Aϴ+self.__Bϴ)
        return
    
    def solve_AAS(self, Aϴ:Number, Bϴ:Number, A:Number):
        '''
        solve a triangle via Angle-Angle-Side (AAS)

        Two Angles and a Side not between
        
        Parameters
        ----------
        Aϴ : Number
            angle (in degrees) at point A
        Bϴ : Number
            angle (in degrees) at point B
        A  : Number
            length of line BC (side a)
            
        Algebraic steps
        ---------------
            find Cϴ: 180-(Aϴ+Bϴ)
            then The Law of Sines "a/sin(A) = b/sin(B) = c/sin(C)" to find each of the other two sides.
        '''
        self.__Aϴ = Aϴ
        self.__Bϴ = Bϴ
        self.__Cϴ = 180-(Aϴ+Bϴ)
        self.__finishSolve(A)
        return
    
    def solve_SSA(self, A:Number, B:Number, Aϴ:Number):
        '''
        solve a triangle via Side-Side-Angle (SSA)

        Two Sides and an Angle not between
        
        Parameters
        ----------
        A  : Number
            length of line BC (side a)
        B  : Number
            length of line AC (side b)
        Aϴ : Number
            angle (in degrees) at point A
            
        Algebraic steps
        ---------------
            use The Law of Sines first to calculate one of the other two angles
            then use the three angles add to 180° to find the other angle
            finally use The Law of Sines again to find the unknown side
        '''
        sa        = round((B*math.sin(math.radians(Aϴ)))/A,4)
        self.__Aϴ = Aϴ
        self.__Bϴ = math.degrees(math.asin(sa))
        self.__Cϴ = 180-(Aϴ+self.__Bϴ)

        self.__finishSolve(A)
        return
    
    def solve_ASA(self, Aϴ, C, Bϴ):
        '''
        solve a triangle via Angle-Side-Angle (ASA)

        Two Angles and a Side between
        
        Parameters
        ----------
        Aϴ : Number
            angle (in degrees) at point A
        C  : Number
            length of line AB (side c)
        Bϴ : Number
            angle (in degrees) at point B
            
        Algebraic steps
        ---------------
            find the third angle using the three angles add to 180°
            then use The Law of Sines to find each of the other two sides.
        '''
        self.__Aϴ = Aϴ
        self.__Bϴ = Bϴ
        self.__Cϴ = 180-(Aϴ+Bϴ)

        # math to find side a so we can complete via AAS
        sa = C/math.sin(math.radians(self.__Cϴ))
        A = math.sin(math.radians(Aϴ))*sa
        self.__finishSolve(A)
        return
    
    def solve_SAS(self, B, Aϴ, C):
        '''
        solve a triangle via Side-Angle-Side (SAS)

        Two Angles and a Side between
        
        Parameters
        ----------
        B  : Number
            length of line AC (side b)
        Aϴ : Number
            angle (in degrees) at point A
        C  : Number
            length of line AB (side c)
            
        Algebraic steps
        ---------------
            use The Law of Cosines to calculate the unknown side
            then use The Law of Sines to find the smaller of the other two angles
            and then use the three angles add to 180° to find the last angle.
        '''
        A = math.sqrt((B**2)+(C**2)-((2*B*C)*math.cos(math.radians(Aϴ))))
        return self.solve_SSS(A,B,C)
    
    def solve_SSS(self, A, B, C):
        '''
        solve a triangle via Side-Side-Side (SSS)

        know the 3 sides but no angles
        
        Parameters
        ----------
        A  : Number
            length of line BC (side a)
        B  : Number
            length of line AC (side b)
        Aϴ : Number
            angle (in degrees) at point A
        C  : Number
            length of line AB (side c)
            
        Algebraic steps
        ---------------
            use The Law of Cosines first to calculate one of the angles
            then use The Law of Cosines again to find another angle
            and finally use angles of a triangle add to 180° to find the last angle.
        '''
        self.__solveAnglesFromSides(A, B, C)
        self.__finishSolve(A)
        return
    
    def solve_coords(self, coord_A:tuple[Number, Number], coord_B:tuple[Number, Number], coord_C:tuple[Number, Number]):
        '''
        solve a triangle via Side-Side-Side (SSS) from the lines coordinates

        know the 3 sides but no angles
        
        Parameters
        ----------
        coord_A : tuple[Number, Number]
            coordinates for point A
        coord_B : tuple[Number, Number]
            coordinates for point B
        coord_C : tuple[Number, Number]
            coordinates for point C
            
        Algebraic steps
        ---------------
            find the line length of each line using the coords d=√( (x2-x1)² + (y2-y1)² )
            complete with SSS solving:
                use The Law of Cosines first to calculate one of the angles
                then use The Law of Cosines again to find another angle
                and finally use angles of a triangle add to 180° to find the last angle.
        '''
        # build the line segments on the coords ...
        self.__linesPerimeter(coord_A, coord_B, coord_C)

        # solve angles
        self.__solveAnglesFromSides(self.__lBC.length, self.__lAC.length, self.__lAB.length)

        # load in the medians
        self.__linesMedians()
        return
    #endregion

if __name__ == '__main__':
    # CoordinateSequence
    l1 = LineString([(0,0), (9,9)])
    l2 = LineString([(0,9), (9,0)])
    print(l1.intersection(l2))

    ml = Line_Segment()
    ml.solve_points((0,0), (9,9))
    print(ml.mid_point)

    t = Triangle()
    t.solve_SSS(4,3,5)
    print(t.triangle_coords)