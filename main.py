from quadtree import Body
from quadtree import Quad
from quadtree import Node

root_quad = Quad(0, 0, 10) 

root = Node(root_quad)

bodies = [
    Body(-2, 3, 0, 0, 5),  
    Body(2, 4, 0, 0, 3),  
    Body(-1, -4, 0, 0, 2) 
]

for i, b in enumerate(bodies):
    root.insert(b)
    print(f"Body {i} yerleştirildi: ({b.x}, {b.y})")

print("\nRoot node kütle merkezi:", root.mass_x, root.mass_y, "Toplam kütle:", root.total_mass)

for name, child in [("NW", root.NW), ("NE", root.NE), ("SW", root.SW), ("SE", root.SE)]:
    if child:
        print(f"{name}: subdivided = {child.divided}, body = {child.body}")
    else:
        print(f"{name}: HİÇ OLUŞMAMIŞ")