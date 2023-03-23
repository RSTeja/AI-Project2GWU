import codecs

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.adj_list = {v: set() for v in vertices}
        self.coloring = {}

    def add_edge(self, u, v):
        self.adj_list[u].add(v)
        self.adj_list[v].add(u)

    def get_unassigned_variable(self):
        unassigned = [v for v in self.vertices if v not in self.coloring]
        if not unassigned:
            return None
        return min(unassigned, key=lambda v: len(self.adj_list[v]))

    def is_valid_assignment(self, variable, value):
        for neighbor in self.adj_list[variable]:
            if neighbor in self.coloring and self.coloring[neighbor] == value:
                return False
        return True

    def csp_backtracking(self):
        variable = self.get_unassigned_variable()
        if variable is None:
            return True
        domain = list(range(1, num_colors + 1))
        domain.sort(key=lambda v: sum(self.is_valid_assignment(variable, v) for variable in self.adj_list))
        for value in domain:
            if self.is_valid_assignment(variable, value):
                self.coloring[variable] = value
                if self.csp_backtracking():
                    return True
                del self.coloring[variable]
        return False


# Read input file
filename = '/input2.txt'

with codecs.open(filename, 'r', encoding='utf-8-sig') as f:
    num_colors = int(f.readline().strip())
    vertices = [tuple(map(int, line.strip().split(','))) for line in f]

# Create graph and add edges
g = Graph(set(v for e in vertices for v in e))
for u, v in vertices:
    g.add_edge(u, v)

# Solve using CSP and MRV heuristic
if g.csp_backtracking():
    for v, color in g.coloring.items():
        print(f"Vertex {v} is assigned color {color}")
else:
    print("No solution found.")
