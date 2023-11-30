

class Node:
    def __init__(self, value):
        self.value = value
        self.struct_list = []
        self.edge_list = []

    def struct(self , node):
        self.struct_list.append(node)
        
    def dependencies_edge(self, node):
        self.edge_list.append(node)
        

    def __repr__(self):
        return f"{self.value}"


class Graph:
    def __init__(self, m , n , r):
        self.graph = {}

        # Xây dựng đồ thị DAG từ ma trận
        for i in range(m):
            for j in range(n):
                # Tạo nút cho mỗi ô trong ma trận
                curr_node = Node((i , j))

                # Kiểm tra và thêm cạnh từ (i-1, j-1) nếu tồn tại
                if i > 0 and j > 0:
                    diag_node = Node((i-1, j-1))
                    curr_node.dependencies_edge(diag_node)

                # Kiểm tra và thêm cạnh từ (i-1, j) nếu tồn tại
                if i > 0 and j!= 0:
                    left_node = Node((i-1, j))
                    curr_node.dependencies_edge(left_node)

                # Kiểm tra và thêm cạnh từ (i, j-1) nếu tồn tại
                if j > 0 and i!= 0:
                    bottom_node = Node((i, j-1))
                    curr_node.dependencies_edge(bottom_node)

                # Lưu trữ nút trong đồ thị
                if len(curr_node.edge_list) != 0 :
                    for l in range(r):
                        struct_node = Node((i, j, l))
                        curr_node.struct(struct_node)
                self.graph[(i, j)] = curr_node

    def print_graph(self):
        for vertex, node in self.graph.items():
            print(f"{vertex} -> {node.edge_list}")
            print(f"{node.value} -> {node.struct_list}")



m = 5
n = 5
r = 5
# Khởi tạo đồ thị DAG từ ma trận bằng cách gọi phương thức __init__
graph = Graph(m + 1, n  +1, r +1)

# In đồ thị
graph.print_graph()