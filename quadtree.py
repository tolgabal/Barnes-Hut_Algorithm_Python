#QUADTREE Structure

class Body:
    
    def __init__(self, x, y, vx, vy, mass):
        #x and y notations
        self.x = x
        self.y = y
        #speed at x and y
        self.vx = vx
        self.vy = vy
        #mass
        self.mass = mass
        #mass at x and y
        self.fx = 0
        self.fy = 0
        
    def reset_force(self):
        #this function using for the reset forces at beggining
        self.fx = 0
        self.fy = 0
        
    def add_force(self, other):
        #this function is using for calculate the force of another object to this object
        G = 6.67430e-11
        dx = other.x - self.x
        dy = other.y - self.y
        dist = (dx**2 - dy**2)*0.5 + 1e-8
        F = G * self.mass * other.mass / dist**2
        self.fx += F * dx / dist
        self.fy += F * dy / dist
        
class Quad:
    
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
    
    def contains(self, body):
        half = self.size/2
        return (self.x - half <= body.x <= self.x + half and
                self.y - half <= body.y <= self.y + half)
    
    def northwest(self):
        half = self.size / 2
        return Quad(self.x - half/2, self.y + half/2, half)

    def northeast(self):
        half = self.size / 2
        return Quad(self.x + half/2, self.y + half/2, half)
    
    def southwest(self):
        half = self.size / 2
        return Quad(self.x - half/2, self.y - half/2, half)
    
    def southeast(self):
        half = self.size / 2
        return Quad(self.x + half/2, self.y - half/2, half)
    
class Node:
    
    def __init__(self, quad):
        self.quad = quad
        self.body = None
        self.total_mass = 0
        self.mass_x = 0
        self.mass_y = 0
        self.divided = False
        
        self.NW = None
        self.NE = None
        self.SW = None
        self.SE = None
        
    def is_external(self):
        return not self.divided
    
    def insert(self, body):
        if not self.quad.contains(body):
            return False
        if self.body is None and not self.divided:
            self.body = body
            self.total_mass = body.mass
            self.mass_x = body.x
            self.mass_y = body.y
            return True
        if not self.divided:
            self.subdivide()
            self._insert_into_children(self.body)
            self.body = None
            self._insert_into_children(body)
            self._update_mass(body)
        
        self._insert_into_children(body)
        
        self._update_mass(body)
        
        return True
    
    def subdivide(self):
        self.NW = Node(self.quad.northwest())
        self.NE = Node(self.quad.northeast())
        self.SW = Node(self.quad.southwest())
        self.SE = Node(self.quad.southeast())
        self.divided = True

    def _insert_into_children(self, body):
        for child in [self.NW, self.NE, self.SW, self.SE]:
            if child.insert(body):
                return
    
    def _update_mass(self, body):
        m1 = self.total_mass
        m2 = body.mass
        self.mass_x = (self.mass_x * m1 + body.x * m2) / (m1 + m2)
        self.mass_y = (self.mass_y * m1 + body.y * m2) / (m1 + m2)
        self.total_mass += m2