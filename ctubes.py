# -*- coding: utf-8 -*-
import random
import math
import matplotlib.pyplot as plt

class segment(object):
    """
    Represents line segment i.e carbon nanotubes
    """
    def __init__(self, length, domain):
        """
        Initializes all parameters for an objects
        length : Length of carbon nano tube
        domain : tuple with (x,y) where x and y are upper bounds for x and y while lower bound is (0,0)
        intersects : Dictionary containing the intersections of line with other lines { other_line: intersection point}
        origin : randomly selected origin
        a, b: represents line as ax + by = 0
        theta : slope
        end: end point of segment
        """
        self.length = length
        self.domain = domain
        self.intersects = {}
        self.origin = (random.uniform(0, self.domain[0]), random.uniform(0, self.domain[1]))
        self.a = random.uniform(-1,1)
        self.b = random.uniform(-1,1)
        self.theta = math.atan2(-self.a, self.b)
        self.end = (self.origin[0] + self.length * math.cos(self.theta), self.origin[1] + self.length * math.sin(self.theta))
    def addIntersect(self, other, point):
        """
        Adds intersect to the intersects dictionary
        """
        self.intersects[other] = point
    def getIntersects(self):
        """
        Returns intersects dictionary
        """
        return self.intersects
    def getorigin(self):
        """
        Returns origin of line
        """
        return self.origin
    def getoriginx(self):
        """
        Returns x co-ordinate of origin of line
        """
        return self.origin[0]
    def getoriginy(self):
        """
        Returns y co-ordinate of origin of line
        """
        return self.origin[1]
    def getend(self):
        return self.end
    def getendx(self):
        return self.end[0]
    def getendy(self):
        return self.end[1]
    def getlength(self):
        return self.length
    def getdomain(self):
        return self.domain
    def __str__(self):
        return str(self.origin) + '->' + str(self.end)


class Node(object):
    def __init__(self, pos):
        self.pos = pos #pos: position of node
    def getPos(self):
        return self.pos
    def __str__(self):
        return str(self.pos)  
        
def generateseg(n, length, domain):
    """
    Generates segments and adds them to the 'segments' list
    """
    segments = []
    initial = segment(domain[1], domain)
    # Initializing parameters separately for left segment
    initial.origin = (0.,0.)
    initial.end = (0., domain[1])
    initial.theta = 90
    initial.a, initial.b = 1, 0
    # Adding segment
    segments.append(initial)
    # Initializing parameters separately for right segment
    final = segment(domain[1], domain)
    final.origin = (domain[0],0.)
    final.end = (domain[0], domain[1])
    final.theta = 90
    final.a, initial.b = 1, 0
    # Adding segment
    segments.append(final)
    for i in range(n):
        segments.append(segment(length, domain))
    return segments

def plotseg(segments, domain, title):
    """
    plots each object from 'segments' list
    """
    plt.figure()
    for segment in segments:
        x = [segment.getoriginx(), segment.getendx()]
        y = [segment.getoriginy(), segment.getendy()]
        #print segment
        plt.plot(x,y)
    plt.title(title)
    plt.axis([-2.,domain[0] + 2,-2.,domain[1] + 2])

def intersect(segments):
    """
    Determines the intersection points of all the segments in the domain

    Theory:
    
    Represent lines in parametric form

        x0(t) = u0 + t v0

        x1(t) = u1 + s v1

    Here, the x's, u's, and v's are vectors in ℜ2 and t ∈ [0, 1].

    And moreover, both s, t ∈ [0, 1], then the two lines intersect. Otherwise, they do not.

    If we combine the two equalities, we get

        u0 + t v0 = u1 + s v1

    Or, equivalently,

        u0 - u1 = s v1 - t v0

        u0 = (x00, y00)

        u1 = (x10, y10)

        v0 = (x01, y01)

        v1 = (x11, y11)

    If we rewrite the above expression in matrix form, we now have that

    | x00 - x10 |   | x11 |      | x01 |
    | y00 - y10 | = | y11 | s -  | y01 | t

    This is in turn equivalent to the matrix expression

    | x00 - x10 |   | x11  x01 | | s|
    | y00 - y10 | = | y11  y01 | |-t|

    Now, we have two cases to consider. First, if this left-hand side is the zero vector, then there's trivially a solution - just set s = t = 0 and the points intersect. Otherwise, there's a unique solution only if the right-hand matrix is invertible. If we let

            | x11  x01 |
    d = det(| y11  y01 |) = x11 y01 - x01 y11

    Then the inverse of the matrix

    | x11  x01 |
    | y11  y01 |

    is given by

          |  y01   -x01 |
    (1/d) | -y11    x11 |

    Note that this matrix isn't defined if the determinant is zero, but if that's true it means that the lines are parallel and thus don't intersect.

    If the matrix is invertible, then we can solve the above linear system by left-multiplying by this matrix:

     | s|         |  y01   -x01 | | x00 - x10 |
     |-t| = (1/d) | -y11    x11 | | y00 - y10 |

                  |  (x00 - x10) y01 - (y00 - y10) x01 |
          = (1/d) | -(x00 - x10) y11 + (y00 - y10) x11 |

    So this means that

    s = (1/d)  ((x00 - x10) y01 - (y00 - y10) x01)
    t = (1/d) -(-(x00 - x10) y11 + (y00 - y10) x11)

    """    
    count = 0
    #'count' counts the number of intersection points 
    for i in range(len(segments)):
        xi_o = segments[i].getoriginx()
        yi_o = segments[i].getoriginy()
        xi_e = segments[i].getendx()
        yi_e = segments[i].getendy()
        l = segments[i].getlength()
        domain = segments[i].getdomain()
        for j in range((i+1), len(segments)):
            xj_o = segments[j].getoriginx()
            yj_o = segments[j].getoriginy()
            xj_e = segments[j].getendx()
            yj_e = segments[j].getendy()
            
            if (xj_o < xi_o + (2*l) and xj_o > xi_o - (2*l)) and \
            (yj_o < yi_o + (2*l) and yj_o > yi_o - (2*l)):
                det = ((xj_e - xj_o) * (yi_e - yi_o)) - ((xi_e - xi_o) * (yj_e - yj_o))
                if (det != 0):
                    s = (1./det) * ((xi_o - xj_o) * (yi_e - yi_o) - (yi_o - yj_o) * (xi_e - xi_o))
                    t = (-1./det) * (-(xi_o - xj_o) * (yj_e - yj_o) + (yi_o - yj_o) *  (xj_e - xj_o))
                    if (0 <= s <= 1 and 0 <= t <= 1):
                        xint = xj_o + s * (xj_e - xj_o)
                        yint = yj_o + s * (yj_e - yj_o)
                        if 0 <= xint <= domain[0] and 0 <= yint <= domain[1]:
                            node = Node((xint, yint))
                            segments[i].addIntersect(segments[j], node)
                            segments[j].addIntersect(segments[i], node)
                            count += 1
    return count


def getIntersects(segments):
    """"
    Returns the line segments which intersects with each other. The list does not contain lines which do not intersect
    """
    intersecting = []
    for segment in segments:
        for intersect in segment.getIntersects().keys():
            if intersect not in intersecting:
                intersecting.append(intersect)
    return intersecting
                

if __name__ == '__main__':
    seglist = generateseg(10, 10, (10,10))
    c = intersect(seglist)
    print c
    plotseg(seglist, (12,12), "All segments")
    intersecting = getIntersects(seglist)
    plotseg(intersecting, (10, 10), "Only Intersecting")
    plt.show()

