import collections
import heapq

class Graph:
    def __init__(self):
        self.graph = {}
        self.cost = {}   # ONLY for UCS (does not affect BFS/DFS)
    
    def initialize_graph(self):
        self.graph = {}
        self.cost = {}
        print("Graph initialized ")
    
    def create_graph(self):
        n = int(input("Enter no. of nodes: "))
        nodes_to_add = n
        while nodes_to_add > 0:
            node = input(f"Enter node ({n - nodes_to_add + 1}/{n}): ")
            if node in self.graph:
                print(f"Error: Node '{node}' already exists.")
                continue
            self.add_node(node)
            nodes_to_add -= 1

        e = int(input("Enter the no. of edges: "))
        for _ in range(e):
            u = input("Enter the 1st node: ")
            v = input("Enter the 2nd node: ")
            cost = int(input("Enter edge cost: "))
            self.add_edge(u, v, cost)
    
    def add_node(self, n_name):
        if n_name not in self.graph:
            self.graph[n_name] = []
            print(f"Node '{n_name}' added")
        else:
            print(f"Node '{n_name}' already exists")

    def delete_node(self, n_del):
        if n_del in self.graph:
            for n in self.graph[n_del]:
                self.graph[n].remove(n_del)
            del self.graph[n_del]
            print(f"Node '{n_del}' deleted")
        else:
            print("Node not found")

    def add_edge(self, u, v, cost=1):
        if u in self.graph and v in self.graph:
            if v not in self.graph[u]:
                self.graph[u].append(v)
                self.graph[v].append(u)
                self.cost[(u, v)] = cost
                self.cost[(v, u)] = cost
                print("Edge added")
            else:
                print("Edge already exists")
        else:
            print("Node not exist")

    def delete_edge(self, u, v):
        if u in self.graph and v in self.graph:
            if v in self.graph[u]:
                self.graph[u].remove(v)
                self.graph[v].remove(u)
                self.cost.pop((u, v), None)
                self.cost.pop((v, u), None)
                print("Edge deleted")
            else:
                print("Edge not found")
        else:
            print("Node not found")

    def display(self):
        print("\n--- Graph Adjacency List ---")
        for node in self.graph:
            print(node, "->", self.graph[node])
        print("----------------------------")
    
    def display_adjacency(self):
        self.display()

    # ================= BFS & DFS (UNCHANGED LOGIC) =================

    def bfs_lefttoright(self, start, goal):
        if start not in self.graph or goal not in self.graph:
            print("Start or goal node not in graph.")
            return False
        fringe = collections.deque([start])
        explored = list()
        iteration_count = 1
        print(f"\n--- BFS Left-to-Right Search ({start} to {goal}) ---")
        while fringe:
            print(f"Iter {iteration_count}, fringe: {list(fringe)}, explored: {explored}")
            iteration_count += 1
            node = fringe.popleft()
            if node == goal:
                print("Goal found!")
                return True
            explored.append(node)
            for n in self.graph[node]:
                if n not in explored and n not in fringe:
                    fringe.append(n)
        print("Goal not found.")
        return False

    def bfs_righttoleft(self, start, goal):
        if start not in self.graph or goal not in self.graph:
            print("Start or goal node not in graph.")
            return False
        fringe = collections.deque([start])
        explored = list()
        iteration_count = 1
        print(f"\n--- BFS Right-to-Left Search ({start} to {goal}) ---")
        while fringe:
            print(f"Iter {iteration_count}, fringe: {list(fringe)}, explored: {explored}")
            iteration_count += 1
            node = fringe.popleft()
            if node == goal:
                print("Goal found!")
                return True
            if node not in explored:
                explored.add(node)
                for n in reversed(self.graph[node]):
                    if n not in explored and n not in fringe:
                        fringe.append(n)
        print("Goal not found.")
        return False

    def dfs_lefttoright(self, start, goal):
        if start not in self.graph or goal not in self.graph:
            print("Start or goal node not in graph.")
            return False
        explored = list()
        fringe = [start]
        iteration_count = 1
        print(f"\n--- DFS Left-to-Right Search ({start} to {goal}) ---")
        while fringe:
            print(f"Iter {iteration_count}, fringe: {fringe}, explored: {explored}")
            iteration_count += 1
            node = fringe.pop()
            if node == goal:
                print("Goal found!")
                return True
            if node not in explored:
                explored.add(node)
                for n in reversed(self.graph[node]):
                    if n not in explored and n not in fringe:
                        fringe.append(n)
        print("Goal not found.")
        return False
    
    def dfs_righttoleft(self, start, goal):
        if start not in self.graph or goal not in self.graph:
            print("Start or goal node not in graph.")
            return False
        explored = list()
        fringe = [start]
        iteration_count = 1
        print(f"\n--- DFS Right-to-Left Search ({start} to {goal}) ---")
        while fringe:
            print(f"Iter {iteration_count}, fringe: {fringe}, explored: {explored}")
            iteration_count += 1
            node = fringe.pop()
            if node == goal:
                print("Goal found!")
                return True
            if node not in explored:
                explored.add(node)
                for n in self.graph[node]:
                    if n not in explored and n not in fringe:
                        fringe.append(n)
        print("Goal not found.")
        return False

    # ================= UNIFORM COST SEARCH (APPENDED) =================



    def uniform_cost_search(self, start, goal):
        if start not in self.graph or goal not in self.graph:
            print("Start or goal node not in graph.")
            return False

        fringe = []
        heapq.heappush(fringe, (0, start, [start]))
        explored = set()
        best_cost = {start: 0}
        iteration = 1

        print(f"\n--- Uniform Cost Search ({start} to {goal}) ---")

        while fringe:
            fringe = self.clean_fringe(fringe, best_cost)
            heapq.heapify(fringe)

            print(f"Iter {iteration}, Fringe: {fringe}, Explored: {explored}")
            iteration += 1

            cost, node, path = heapq.heappop(fringe)

            if node == goal:
                print("Goal found!")
                print("Path:", path)
                print("Total Cost:", cost)
                return True

            explored.add(node)

            for n in self.graph[node]:
                edge_cost = self.cost.get((node, n), 1)
                new_cost = cost + edge_cost

                if n not in best_cost or new_cost < best_cost[n]:
                    best_cost[n] = new_cost
                    fringe.append((new_cost, n, path + [n]))

        print("Goal not found.")
        return False
    def clean_fringe(self,fringe, best_cost):
            cleaned = {}
            for cost, node, path in fringe:
                if node not in cleaned or cost < cleaned[node][0]:
                    cleaned[node] = (cost, path)
            return [(c, n, p) for n, (c, p) in cleaned.items()]
# ================= MENU PROGRAM =================

def menu_program():
    g = Graph()
    while True:
        print("\n--- Menu ---")
        print("1. Initialize graph")
        print("2. Create graph")
        print("3. Add node")
        print("4. Add edge")
        print("5. Delete node")
        print("6. Delete edge")
        print("7. Display graph")
        print("8. Display adjacency")
        print("9. BFS Right-to-Left")
        print("10. BFS Left-to-Right")
        print("11. DFS Right-to-Left")
        print("12. DFS Left-to-Right")
        print("13. Uniform Cost Search")
        print("14. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            g.initialize_graph()
        elif choice == '2':
            g.create_graph()
        elif choice == '3':
            g.add_node(input("Enter node: "))
        elif choice == '4':
            u = input("Enter 1st node: ")
            v = input("Enter 2nd node: ")
            cost = int(input("Enter cost: "))
            g.add_edge(u, v, cost)
        elif choice == '5':
            g.delete_node(input("Enter node: "))
        elif choice == '6':
            g.delete_edge(input("Enter 1st node: "), input("Enter 2nd node: "))
        elif choice == '7':
            g.display()
        elif choice == '8':
            g.display_adjacency()
        elif choice == '9':
            g.bfs_righttoleft(input("Start: "), input("Goal: "))
        elif choice == '10':
            g.bfs_lefttoright(input("Start: "), input("Goal: "))
        elif choice == '11':
            g.dfs_righttoleft(input("Start: "), input("Goal: "))
        elif choice == '12':
            g.dfs_lefttoright(input("Start: "), input("Goal: "))
        elif choice == '13':
            start = input("Enter start node: ")
            goal = input("Enter goal node: ")
            g.uniform_cost_search(start, goal)
        elif choice == '14':
            print("Exiting program.")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu_program()
    