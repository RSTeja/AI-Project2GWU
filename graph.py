import codecs

class GraphProject:
    def __init__(self, vertices):
        self.vertices = vertices
        self.lists = {v: set() for v in vertices}
        self.color = {}

    def assignVariable(self):
        unassigned = [v for v in self.vertices if v not in self.color]
        if not unassigned:
            return None
        return min(unassigned, key=lambda v: len(self.lists[v]))

    def valid(self, variable, value):
        for neighbor in self.lists[variable]:
            if neighbor in self.color and self.color[neighbor] == value:
                return False
        return True
    
    def edges(self, u, v):
        self.lists[u].add(v)
        self.lists[v].add(u)

    def backtracking(self):
        variable = self.assignVariable()
        if variable is None:
            return True
        domain = list(range(1, num_colors + 1))
        domain.sort(key=lambda v: sum(self.valid(variable, v) for variable in self.lists))
        for value in domain:
            if self.valid(variable, value):
                self.color[variable] = value
                if self.backtracking():
                    return True
                del self.color[variable]
        return False

filename = '/input3.txt'

with codecs.open(filename, 'r', encoding='utf-8-sig') as f:
    num_colors = int(f.readline().strip())
    vertices = [tuple(map(int, line.strip().split(','))) for line in f]


g = GraphProject(set(v for e in vertices for v in e))
for u, v in vertices:
    g.edges(u, v)

if g.backtracking():
    for v, color in g.color.items():
        print(f"Vertex {v} ..... color {color}")
else:
    print("These vertices won't give any solution.")
