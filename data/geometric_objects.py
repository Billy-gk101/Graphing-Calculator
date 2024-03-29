# =============================================================================
# CODE IMPORTS
# =============================================================================
import math, copy
from numbers import Number

class Line_Segment():
    '''
    A linear equation is any equation whose graph is a line. All linear equations can be written in the form 
    Ax + By = C
    where A, B, and C are real numbers and A and B are not both zero. The following examples are linear equations and their respective A, B, and C values.
    ie. x+y=0 == A=1,B=1,C=0 || 3x-4y=9 == A=3,B=-4,C=9 || x=-6 == A=1,B=0,C=-6 || y=7 == A=0,B=1,C=7
    '''
    def __init__(self, length:Number=None, slope:Number=None, start_point:tuple[Number,Number]=None, end_point:tuple[Number,Number]=None) -> None:
        self.__s = start_point
        self.__e = end_point
        self.__l = length
        self.__m = slope
        if None not in [length, slope, start_point, end_point]: return
        if None not in [start_point, end_point]:
            self.solve_points(start_point, end_point)
        elif None not in [length, start_point, slope]:
            self.solve_slope_start_point(start_point, slope, length)
        elif None not in [length, end_point, slope]:
            self.solve_slope_end_point(start_point, slope, length)
        return
    
    def __solve_length(self):
        '''solve the length: d = √((x2 – x1)² + (y2 – y1)²)'''
        x1, y1 = self.__s
        x2, y2 = self.__e
        self.__l = math.sqrt(((x2-x1)**2)+((y2-y1)**2))
        return
    
    def __solve_slope(self):
        '''solve the slope: m = (y₂ - y₁) / (x₂ - x₁)'''
        x1, y1 = self.__s
        x2, y2 = self.__e
        v1, v2 = (y2-y1),(x2-x1)
        if 0 in [v1, v2]: self.__m = 0
        else: self.__m = v1/v2
        self.__solve_length()
        return

    def __slope_points(self, point:tuple[Number,Number], slope:Number, length:Number) -> list[tuple]:
        self.__l = length        
        self.__m = slope
        x1,y1 = point
        m2 = slope**2
        c = 1/math.sqrt(1+m2)
        s = slope/math.sqrt(1+m2)
        rc = length*c
        rs = length*s
        rv = 6
        return [(round(x1-rc,rv), round(y1-rs,rv)),(round(x1+rc,rv), round(y1+rs,rv))]
    
    @property
    def coords(self):
        return [self.__s, self.__e]
    
    @property
    def start_point(self):
        return copy.deepcopy(self.__s)
    
    @property
    def end_point(self):
        return copy.deepcopy(self.__e)
    
    @property
    def mid_point(self):
        return self.get_midpoint()
    
    def get_midpoint(self):
        x1, y1 = self.__s
        x2, y2 = self.__e
        return ((x1+x2)/2, (y1+y2)/2)
    
    def set_endpoint(self, end_point:tuple[Number,Number]):
        self.__e = end_point
        return
    
    def solve_slope_start_point(self, start_point:tuple[Number,Number], slope:Number, length:Number) -> list[tuple]:
        '''
        this will assume the positive values of points are to be the end point; but returns both
        x1,y1=start_point; m=slope; c=1/√(1+(m**2)); rc=length*c; s=m/√(1+(m**2)); rs=length*s
        return [(x1-rc, y1-rs),(x1+rc, y1+rs)]

        use set_endpoint and return[0] if return[1] is not the desired point
        '''
        v = self.__slope_points(start_point, slope, length)
        self.__s = start_point
        self.__e = copy.deepcopy(v[1])
        return v
    
    def solve_slope_end_point(self, end_point:tuple[Number,Number], slope:Number, length:Number) -> list[tuple]:
        '''
        this will assume the positive values of points are to be the end point; but returns both
        x1,y1=start_point; m=slope; c=1/√(1+(m**2)); rc=length*c; s=m/√(1+(m**2)); rs=length*s
        return [(x1-rc, y1-rs),(x1+rc, y1+rs)]

        use set_endpoint and return[1] if return[0] is not the desired point
        '''
        v = self.__slope_points(end_point, slope, length)
        self.__e = end_point
        self.__s = copy.deepcopy(v[0])
        return v
    
    def solve_points(self, start_point:tuple[Number,Number], end_point:tuple[Number,Number]):
        '''
        If we are just given two points (x1,y1) and (x2,y2), we must first work out the gradient using the gradient formula
        m=(y2-y1)/(x2-x1)
        then substitute either point to finish definition of line
        y=mx+b
        '''
        # store known vals
        self.__s = start_point
        self.__e = end_point

        # find m
        self.__solve_slope()
        # x1,y1 = start_point
        # x2,y2 = end_point
        # self.__m = (y2-y1)/(x2-x1)

        # # solve the length d=√((x2 – x1)² + (y2 – y1)²)
        # self.__solve_length()     
        return
    
    @property
    def length(self):
        return copy.deepcopy(self.__l)
    
    def get_length(self):
        return self.length
    
    def get_points(self):
        return (copy.deepcopy(self.__s),copy.deepcopy(self.__e))
    
    def get_slope(self):
        return copy.deepcopy(self.__m)
    
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

class Poloygon():
    def __init__(self) -> None:

        return

class Triangle(Poloygon):
    ## https://www.mathsisfun.com/algebra/trig-solving-triangles.html
    #             Bϴ
    #           .    .
    #         .        .
    #        C           A
    #     .                .
    #   .                    .
    # Aϴ . . . .  B  . . . .  Cϴ
    def __init__(self) -> None:
        super().__init__()
        self.A = None
        self.B = None
        self.C = None
        self.Aϴ = None
        self.Bϴ = None
        self.Cϴ = None
        self.lAC = None
        self.lBC = None
        self.lAB = None
        self.lmA = None
        self.lmB = None
        self.lmC = None

        self.__centroid = None
        return
    
    def __buildLineSegments_coords(self, coord_A:tuple[Number, Number], coord_B:tuple[Number, Number], coord_C:tuple[Number, Number]):
        self.lAC = Line_Segment(start_point=coord_A, end_point=coord_C)
        self.lAB = Line_Segment(start_point=coord_A, end_point=coord_B)
        self.lBC = Line_Segment(start_point=coord_B, end_point=coord_C)
        return
    
    def __buildLineSegments_medians(self):
        self.lmA = Line_Segment(start_point=self.lAC.start_point, end_point=self.lBC.mid_point)
        self.lmB = Line_Segment(start_point=self.lBC.start_point, end_point=self.lAC.mid_point)
        self.lmC = Line_Segment(start_point=self.lAC.end_point,   end_point=self.lAB.mid_point)
        return
    
    def get_area(self, dec_places=None):
        '''area via Heron's Formula'''
        # SAS
        a = .5*(self.B*self.C)*math.sin(math.radians(self.Aϴ))

        # Heron's Formula
        s = self.get_perimeter(None)/2
        s = s*((s-self.A)*(s-self.B)*(s-self.C))
        s = math.sqrt(s)
        if dec_places is None: return s
        return round(s, dec_places)
    
    def get_circumradius(self, dec_places=None):
        '''side_a/(2*sin(angle_a))'''
        c = self.A/(2*math.sin(math.radians(self.AΘ)))
        if dec_places is None: return c
        return round(c, dec_places)
    
    def get_points(self, dec_places=None):
        rtn = self.points
        if dec_places is None: return rtn
        for k,v in rtn.items():
            x,y = v
            rtn[k] = (round(x, dec_places), round(y, dec_places))
        return rtn
    
    def get_data(self, dec_places=2):
            return {"side_a":round(self.A, dec_places), "side_b":round(self.B, dec_places), "side_c":round(self.C, dec_places),
                    "angle_a":round(self.Aϴ, dec_places), "angle_b":round(self.Bϴ, dec_places), "angle_c":round(self.Cϴ, dec_places),
                    "area":self.get_area(dec_places), "perimeter":self.get_perimeter(dec_places), "inradius":self.get_inradius(dec_places),
                    "circumradius":self.get_circumradius(dec_places)}
    
    def get_inradius(self, dec_places=None):
        '''area/perimeter'''
        v = self.get_area(None)/self.get_perimeter(None)
        if dec_places is None: return v
        return round(v, dec_places)
    
    def get_median_lengths(self, dec_places=None):
        rtn = self.medians
        if dec_places is None: return rtn
        v:Line_Segment
        for k,v in rtn.items():
            rtn[k] = round(v.length, dec_places)
        return rtn
    
    def get_perimeter(self, dec_places=None):
        '''perimeter: length of all sides added up'''
        v = self.A+self.B+self.C
        if dec_places is None: return v
        return round(v, dec_places)
    
    @property
    def points(self):
        return {'point_a':self.lAC.start_point, 'point_b':self.lBC.start_point, 'point_c':self.lAC.end_point, 'point_mA':self.lBC.mid_point, 'point_mB':self.lAC.mid_point, 'point_mC':self.lAB.mid_point}
    
    @property
    def medians(self):
        return{'lmA':copy.deepcopy(self.lmA), 'lmB':copy.deepcopy(self.lmB), 'lmC':copy.deepcopy(self.lmC)}
    
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
    
    #region equation
    def __medianFormula(self, p:list[str]) -> str:        
        return f'm<sup>{p[0]}</sup><span style="white-space: nowrap">&radic;<span style="text-decoration:overline;">(2{p[1]}<sup>2</sup>+2{p[2]}<sup>2</sup>-{p[0]}<sup>2</sup>)/4</span></span>'
    
    @property
    def coords_list(self):
        x,y = [], []
        c = self.lAC.coords
        x.append(c[0][0])
        y.append(c[0][1])

        c = self.lBC.coords
        x.append(c[0][0])
        y.append(c[0][1])
        x.append(c[1][0])
        y.append(c[1][1])

        # close shape
        x.append(x[0])
        y.append(y[0])

        return x,y
    
    @property
    def equation_area(self):
        return {'title':"area [Heron's Formula]", 'desc':"Heron of Alexandria formula for triangle area", 
                'equation':'Area = Square root of <span style="white-space: nowrap">&radic;<span style="text-decoration:overline;">s(s-a)(s-b)(s-c)</span></span> where s is half the perimeter or simplify to <span style="white-space: nowrap">&radic;<span style="text-decoration:overline;">(a+b+c)/2</span></span>'}

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
    def __finishSolve(self):
        s = (0,0)
        self.lAC = Line_Segment(length=self.B, start_point=s, end_point=(self.B,0))
        self.lAB = Line_Segment(length=self.C, slope=math.tan(math.radians(self.Aϴ)), start_point=s)
        self.lBC = Line_Segment(length=self.A, start_point=self.lAB.end_point, end_point=self.lAC.end_point)

        # medians
        self.__buildLineSegments_medians()
        return
    
    def solve_AAS(self, Aϴ, Bϴ, A):
        '''
        Angle-Angle-Side Solve
        Two Angles and a Side not between
            Angle A
            Angle B
            Side  A
        '''
        self.Aϴ = Aϴ
        self.Bϴ = Bϴ
        self.A  = A
        self.Cϴ = 180-(Aϴ+Bϴ)
        
        sa = self.A/math.sin(math.radians(self.Aϴ))
        self.B = math.sin(math.radians(self.Bϴ))*sa
        self.C = math.sin(math.radians(self.Cϴ))*sa
        self.__finishSolve()
        return
    
    def solve_SSA(self, A, B, Aϴ):
        '''
        Side-Side-Angle; 
        Two Sides and an Angle not between
            Side  A
            Side  B
            Angle A
        Steps
            find Cϴ: sin(Cϴ)/C = sin(Aϴ)/A
            find Bϴ: 180-Aϴ-Cϴ
            find  B: B/sin(Bϴ) = A/sin(Aϴ)
        '''
        self.A  = A     # 8
        self.B  = B     # 13
        self.Aϴ = Aϴ    # 31

        # find  C: sin(Cϴ)/C = sin(Aϴ)/A
        sa = (B*math.sin(math.radians(Aϴ)))/A
        self.Bϴ = math.degrees(math.asin(sa))   # 56.818 ...
        self.Cϴ = 180-Aϴ-self.Bϴ                # 92.181 ...
        # print(f"Aϴ={self.Aϴ}; Bϴ={self.Bϴ}; Cϴ={self.Cϴ}")

        self.C = (math.sin(math.radians(self.Cϴ))*A)/math.sin(math.radians(Aϴ))
        # print(f"A={self.A}; B={self.B}; C={self.C}")

        self.__finishSolve()
        return
    
    def solve_ASA(self, Aϴ, C, Bϴ):
        '''
        Angle-Side-Angle
        Two Angles and a Side between
            Angle A
            Side  C
            Angle B
        '''
        self.Aϴ = Aϴ
        self.Bϴ = Bϴ
        self.Cϴ = 180-(self.Aϴ+self.Bϴ)
        self.C  = C

        sa = self.C/math.sin(math.radians(self.Cϴ))
        self.A = math.sin(math.radians(self.Aϴ))*sa
        self.B = math.sin(math.radians(self.Bϴ))*sa
        self.__finishSolve()
        return
    
    def solve_SAS(self, A, Cϴ, B):
        '''
        Side-Angle-Side Solve
        Two Sides and an Angle between
            Side  A
            Angle C
            Side  B           
        '''
        self.A = A
        self.B = B
        self.Cϴ = Cϴ
        self.C = math.sqrt((self.A**2+self.B**2)-((2*self.A*self.B)*math.cos(math.radians(self.Cϴ))))
        return self.from_SSS(self.A, self.B, self.C)
    
    def solve_SSS(self, A, B, C):
        '''
        Side-Side-Side Solve
        Three Sides
            Side  A
            Side  B
            Side  C
        '''
        self.A = A
        self.B = B
        self.C = C
        a2=self.A*self.A
        b2=self.B*self.B
        c2=self.C*self.C

        self.AΘ = math.degrees(math.acos((b2+c2-a2)/(2*self.B*self.C)))
        self.BΘ = math.degrees(math.acos((c2+a2-b2)/(2*self.C*self.A)))
        self.CΘ = 180-self.AΘ-self.BΘ
        self.__finishSolve()
        return
    
    def solve_coords(self, coord_A:tuple[Number, Number], coord_B:tuple[Number, Number], coord_C:tuple[Number, Number]):
        # build the line segments on the coords ...
        self.__buildLineSegments_coords(coord_A, coord_B, coord_C)

        # solve SSS
        self.solve_SSS(self.lBC.length, self.lAC.length, self.lAB.length)

        # now override the '__finishSolve' line segments to be at the specified points
        self.__buildLineSegments_coords(coord_A, coord_B, coord_C)
        self.__buildLineSegments_medians()
        return
    #endregion
