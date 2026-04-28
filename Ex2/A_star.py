import collections
import heapq

class Graph:
    def __init__(self):
        self.graph = {}
        self.cost = {}
        self.heuristic = {}

    def initialize_graph(self):
        self.graph = {}
        self.cost = {}
        self.heuristic = {}
        print("Graph initialized")

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []
            print(f"Node '{node}' added")

    def add_edge(self, u, v, cost):
        if u in self.graph and v in self.graph:
            self.graph[u].append(v)
            self.graph[v].append(u)
            self.cost[(u, v)] = cost
            self.cost[(v, u)] = cost
            print("Edge added")

    def input_heuristic(self):
        print("\nEnter heuristic values for each node:")
        for node in self.graph:
            h = int(input(f"h({node}) = "))
            self.heuristic[node] = h

    def get_heuristic(self, node):
        return self.heuristic.get(node, 0)

    # ================= A* SEARCH =================

    def a_star_search(self, start, goal):
        if start not in self.graph or goal not in self.graph:
            print("Start or goal not in graph")
            return False

        fringe = []
        heapq.heappush(fringe, (0, 0, start, [start]))
        best_g = {start: 0}
        iteration = 1

        print(f"\n--- A* Search ({start} to {goal}) ---")

        while fringe:
            print(f"Iter {iteration}, Fringe: {fringe}")
            iteration += 1

            f, g, node, path = heapq.heappop(fringe)

            if g > best_g.get(node, float('inf')):
                continue

            if node == goal:
                print("\nGoal Found!")
                print("Path:", path)
                print("Total Cost:", g)
                return True

            for n in self.graph[node]:
                edge_cost = self.cost.get((node, n), 1)
                new_g = g + edge_cost

                if new_g < best_g.get(n, float('inf')):
                    best_g[n] = new_g
                    h = self.get_heuristic(n)
                    new_f = new_g + h
                    heapq.heappush(fringe, (new_f, new_g, n, path + [n]))

        print("Goal not found")
        return False

# ================= MENU =================

def menu_program():
    g = Graph()

    while True:
        print("\n--- Menu ---")
        print("1. Initialize Graph")
        print("2. Add Node")
        print("3. Add Edge")
        print("4. Input Heuristic")
        print("5. A* Search")
        print("6. Exit")

        ch = input("Enter choice: ")

        if ch == '1':
            g.initialize_graph()

        elif ch == '2':
            g.add_node(input("Enter node: "))

        elif ch == '3':
            u = input("Enter node u: ")
            v = input("Enter node v: ")
            c = int(input("Enter cost: "))
            g.add_edge(u, v, c)

        elif ch == '4':
            g.input_heuristic()

        elif ch == '5':
            s = input("Start node: ")
            g_node = input("Goal node: ")
            g.a_star_search(s, g_node)

        elif ch == '6':
            print("Exit")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu_program()