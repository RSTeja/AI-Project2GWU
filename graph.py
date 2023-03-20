from typing import Dict, List, Set


class Graph:
    def __init__(self, vertices: List[int], num_colors: int, edges: Dict[int, Set[int]]):
        self.vertices = vertices
        self.num_colors = num_colors
        self.edges = edges


class CSP:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.domains = {v: set(range(graph.num_colors)) for v in graph.vertices}
        self.constraints = {v: set() for v in graph.vertices}
        for v1, v2 in graph.edges.items():
            self.constraints[v1].add(v2)
            self.constraints[v2].add(v1)

    def solve(self):
        assignment = {}
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        if len(assignment) == len(self.graph.vertices):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
        return None

    def select_unassigned_variable(self, assignment):
        unassigned_vars = [v for v in self.graph.vertices if v not in assignment]
        return self.most_constrained_variable(unassigned_vars)

    def order_domain_values(self, var, assignment):
        return list(self.domains[var])

    def is_consistent(self, var, value, assignment):
        for neighbor in self.constraints[var]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True

    def most_constrained_variable(self, variables):
        return min(variables, key=lambda v: len(self.domains[v]))


def read_input_file(file_path: str) -> Graph:
    with open(file_path, 'r', encoding='utf-8-sig') as file:  # use 'utf-8-sig' encoding to remove BOM
        num_colors = int(file.readline().strip())
        edges = {}
        for line in file:
            v1, v2 = map(int, line.strip().split(','))
            if v1 not in edges:
                edges[v1] = set()
            if v2 not in edges:
                edges[v2] = set()
            edges[v1].add(v2)
            edges[v2].add(v1)
        vertices = sorted(edges.keys())
    return Graph(vertices, num_colors, edges)


if __name__ == '__main__':
    graph = read_input_file('input.txt')
    csp = CSP(graph)
    solution = csp.solve()
    if solution is not None:
        print('Solution:', solution)
    else:
        print('No solution found')
