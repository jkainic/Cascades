
sympy_ok = True


try:
    from sympy.matrices import *
    from sympy import floor
except ImportError as e:
    sympy_ok = False

from sympy import *

from copy import *

from subprocess import call

class Point:
    pass

class Vertex:
    #number of vertices defined so far.
    #this will break if we define more than one graph!
    #count = 0

    #vertex display information
    radius = 10
    click_radius = 20

    def __init__(self, x=0, y=0):
        self.i = 0
        #Vertex.count += 1
        self.x, self.y = x,y

        #keep a running tab on the degree
        self.deg = 0

        #more display information
        self.selected = False
        self.hover = False

    def move(self, x, y):
        self.x, self.y = x, y

    #True iff the given x/y coordinates are over the vertex
    def over(self, x, y):
        return ((x - self.x)**2 + (y - self.y)**2) < Vertex.click_radius**2

class Edge:
    def __init__(self, v1, v2):
        self.v1, self.v2 = v1, v2
        self.v1.deg += 1
        self.v2.deg += 1
    def has(self, v):
        return (v.i == self.v1.i or v.i == self.v2.i)

class Graph:
    def __init__(self):
        self.vcount = 0
        self.ecount = 0
        self.vertices = []
        self.edges = []

        self.viscosity = 0
        self.La = 0
        self.Ln = 0
        self.sigma = 0
        self.tau = 0
        
        self.A = []

    def add_vertex(self, x=0, y=0):
        new = Vertex(x,y)
        new.i = self.vcount
        self.vcount += 1
        self.vertices.append(new)
        self.A = self.adjacency()

    def add_edge(self, v1, v2):
        if self.A[v1.i][v2.i] == 0:
            new = Edge(v1, v2)
            self.edges.append(new)
            self.ecount += 1

            self.A = self.adjacency()

            self.edges[-1].index = 0
            for edge in self.edges:
                if edge.has(v1) and edge.has(v2):
                    self.edges[-1].index += 1

    def deselect_all(self):
        for vertex in self.vertices:
            vertex.selected = False

    def adjacency(self):
        n = len(self.vertices)

        self.A = [x[:] for x in [[0]*n]*n]
        for edge in self.edges:
            i,j = edge.v1.i, edge.v2.i
            self.A[i][j] += 1
            self.A[j][i] += 1
        return self.A

    def clear(self):
        self.vertices = []
        self.edges = []
        self.vcount = 0

    def get_last(self):
        return self.vertices[-1]

#used to associate percentage of adoption at each island (vertex)
class Divisor:
    def __init__(self, graph):
        self.graph = graph
        self.values = ([0]*len(graph.vertices))[:]
        self.generation = 0
    def extend(self, value=0):
        self.values.append(value)
    def set(self, vertex, value):
        self.values[vertex.i] = value
    def get(self, vertex):
        return self.values[vertex.i]
    def max_degree(self):
        if self.graph.vcount == 0:
            return 0
        else:
            degrees = [0]*self.graph.vcount
            for edge in self.graph.edges:
                i,j = edge.v1.i, edge.v2.i
                degrees[i]+=1
                degrees[j]+=1
            return max(degrees)

    #alters percentages based on one round of migration
    def migration(self):
        v = self.graph.viscosity
        adj_mat = self.graph.A

        for i in range(self.graph.vcount):
            bi = self.values[i]
            i_sum = 0
            j_sum = 0

            for j in range(self.graph.vcount):
                m = v*adj_mat[i][j]
                bj = self.values[j]

                i_sum += m*bi
                j_sum += m*bj

            self.values[i] = bi - i_sum + j_sum
            
    #alters percentages based on one round of conversion
    def conversion(self):
        s = self.graph.sigma
        t = self.graph.tau
        La = self.graph.La
        Ln = self.graph.Ln

        for i in range(self.graph.vcount):
            bi = self.values[i]
            self.values[i] = bi - s*bi*pow((1-bi), La) + t*(1-bi)*pow(bi, Ln)

    #attempts to calculate the equilibria percentages at each island: 
    #is not currently functional, since the sympy modules used for solving 
    #a system of equations is faulty (doesn't work well with floating point zero)
    def beta_crit(self):
        if (self.graph.sigma == 0 ) or (self.graph.tau == 0) or (self.graph.La == 0) or (self.graph.Ln == 0) or (self.graph.viscosity == 0):
            return 'Please set non-zero values for s, t, La, Ln, and v'
        s = self.graph.sigma
        t = self.graph.tau
        La = self.graph.La
        Ln = self.graph.Ln
        n = self.graph.vcount
        adj_mat = deepcopy(self.graph.A)
        v = self.graph.viscosity

        if n == 0:
            return 'There are no islands yet!'

        variables = [0]*n
        functions = [0]*n

        for i in range(n):
            variables[i] = Symbol('B' + str(i))

        for i in range(n):
            bi = variables[i]

            sumi = 0
            sumij = 0

            for j in range(n):
                m = v*adj_mat[i][j]

                sumi += m
                sumij += m * variables[j]

            bii = bi*(1-sumi) + sumij

            functions[i] = bii - s*bii*pow((1-bii), (La - 1)) + t*(1 - bii)*pow(bii, (Ln - 1)) - bi

        all_solns =  solve_poly_system(functions, variables)
        real_pos_solns = []

        for el in all_solns:
            r = 0
            for x in el:
                if (not x.is_real) or (not x>= 0):
                    r = 1
            if r == 0:
                real_pos_solns.append(el)

        return real_pos_solns



