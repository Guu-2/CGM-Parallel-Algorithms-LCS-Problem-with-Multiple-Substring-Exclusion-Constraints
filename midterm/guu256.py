import math
from collections import deque

class Node:
    def __init__(self, i, j):
        # self.value = i*10 + j
        self.vertical = i
        self.horizontal = j
        self.struct_nodes = []
        self.pre_dp_nodes = []
        self.post_dp_nodes = []

    def get_vertical(self):
        return self.vertical;
    
    def get_horizontal(self):
        return self.horizontal;
        
    def struct(self, k):
        struct_node = StructNode(self.vertical, self.horizontal, k)
        self.struct_nodes.append(struct_node)
        
    def get_struct_value(self, k):
        for struct_node in self.struct_nodes:
            if struct_node.state == k:
                return struct_node.value
        return None

    def set_struct_value(self, k, value):
        for struct_node in self.struct_nodes:
            if struct_node.state == k:
                struct_node.set_value(value)
                break

    def pre_dependencies(self, node):
        self.pre_dp_nodes.append(node)

    def post_dependencies(self, node):
        self.post_dp_nodes.append(node)

    def __repr__(self):
        return f"{(self.vertical, self.horizontal)}"


class StructNode:
    def __init__(self, i, j, k):
        # self.value = i*100 + j*10 + k
        self.value = 0
        self.vertical = i
        self.horizontal = j
        self.state = k

    def set_state(self, state):
        self.state = state

    def set_value(self, val):
        self.value = val

    def __repr__(self):
        return f"({self.vertical}, {self.horizontal}, {self.state}) : {self.value}"


class DAG:
    def __init__(self, m, n ,k):
        self.graph = {}
        self.blocks  = {}

        # Build the DAG graph from the matrix
        for i in range(m):
            for j in range(n):
                curr_node = Node(i, j)

                if i > 0 and j > 0:
                    diag_node = Node(i-1, j-1)
                    curr_node.pre_dependencies(diag_node)

                if i > 0 and j != 0:
                    left_node = Node(i-1, j)
                    curr_node.pre_dependencies(left_node)

                if j > 0 and i != 0:
                    bottom_node = Node(i, j-1)
                    curr_node.pre_dependencies(bottom_node)

                if i < m - 1 and j != 0:
                    post_bottom_node = Node(i+1, j)
                    curr_node.post_dependencies(post_bottom_node)

                if j < n - 1 and i != 0:
                    post_right_node = Node(i, j+1)
                    curr_node.post_dependencies(post_right_node)

                if i < m - 1 and j < n - 1:
                    post_diag_node = Node(i+1, j+1)
                    curr_node.post_dependencies(post_diag_node)

                
                if len(curr_node.pre_dp_nodes) != 0 or len(curr_node.post_dp_nodes) != 0 and curr_node.get_vertical() != 0 and curr_node.get_horizontal() != 0:
                    for l in range(1 ,k):
                        curr_node.struct(l)
                self.graph[(i, j)] = curr_node


    def struct_nodes(self, i, j, k):
        node = self.graph[(i, j)]
        node.struct(k)


    def get_block(self, start_row, end_row, start_col, end_col , index):
        # Tạo khối con bằng cách trích xuất phần của ma trận ban đầu
        submatrix = []
        # submatrices = []
        for row in range(start_row + 1, end_row + 1):
            if  row > 0 : 
                submatrix_row = []
                for col in reversed(range(start_col + 1, end_col +1)):
                    if col > 0 :
                        value = self.get_node(row, col)
                        submatrix_row.insert(0 ,value)
                submatrix.append(submatrix_row)
                
        # Lưu trữ ma trận con trong từ điển submatrices
        self.blocks[index] = submatrix
        # print(submatrix)
        return submatrix
    
    # PARTITION BLOCK THEO DAG
    def partition_block(self, m , n , processors):
        # XEM LẠI PHẦN 4.1 -> CÓ LIÊN QUAN ĐẾN DAG KHÔNG (KHÔNG VÌ NÓ ĐA LUỒNG TRONG XỬ LÝ KÝ TỰ THUỘC TẬP CON CỦA BẢNG CHỮ CÁI PHÂN CHO NÓ
        # //TODO: testing

        p = processors   # Số lượng khối theo chiều dọc và chiều ngang
        alpha = math.ceil(m / p)  # Kích thước của mỗi khối theo chiều ngang
        # print(alpha)
        beta = math.ceil( n / p)  # Kích thước của mỗi khối theo chiều dọc
        # print(beta)
        flag = 0
        index = 0
        submatrices = []
        for i in range(p):
            for j in range(p):
                # Xác định chỉ số hàng và cột kết thúc của khối con
                start_row = i * alpha - flag
                start_col = j * beta - flag
                end_row = min(start_row + beta, m)
                end_col = min(start_col + alpha, n) 
                if alpha * p > m and i == 0:
                    flag = 1
                    # start_row = i*alpha -1
                    end_row = n- alpha*(p - 1)
                # //Xác định lần đầu tiên
                if beta * p > n and j == 0:
                    flag = 1
                    # start_col = j*beta - 1
                    end_col = m - beta*(p - 1)
                
                # print(" row: " + str(start_row) + " : " + str(end_row) +", col " +  str(start_col) + " : " + str(end_col))

                # end_row = min(start_row + beta, m)
                # end_col = min(start_col + alpha, n)
                
                submatrix = self.get_block(start_row, end_row , start_col, end_col , index)
                submatrices.append(submatrix)
                index+=1
                
        return submatrices

    def build_snake_path(self , submatrices , p):
        startIndex = 0
        queue = deque()
        queue.append(startIndex)

        snake_path = []

        visited = set()
        visited.add(startIndex)

        while queue:
            currentIndex = queue.popleft()
            snake_path.append(currentIndex)

            if currentIndex + 1 < len(submatrices):
                indexP = currentIndex + p
                if indexP < len(submatrices) and indexP not in visited:
                    queue.append(indexP)
                    visited.add(indexP)

                nextIndex = currentIndex + 1
                if nextIndex not in visited:
                    queue.append(nextIndex)
                    visited.add(nextIndex)

        print("Snake line path:", snake_path)
        return snake_path

    def build_digonal(self , snake_path , p):
        dict = {}

        d = 1
        key = 1

        currentIndex = 0

        while currentIndex < len(snake_path):
            row = []
            for i in range(d):
                if currentIndex < len(snake_path):
                    row.append(snake_path[currentIndex])
                    currentIndex += 1
            dict[key] = row
            key += 1

            if key > p:
                d -= 1
            else:
                d += 1

        # In ra giá trị của Dictionary
        print("Dictionary contents:")
        for k, v in dict.items():
            print("Key:", k, ", Value:", v)
        return dict





    def print_graph(self):
        for vertex, node in self.graph.items():
            print(f"Node: {vertex}")
            print(f"  Pre-Dependencies: {node.pre_dp_nodes}")
            print(f"  Post-Dependencies: {node.post_dp_nodes}")
            print("  Structs:")
            for struct_node in node.struct_nodes:
                print(f"    {struct_node}")


    def get_node(self , i , j ):
        return self.graph[(i, j)]
        
        
    def set_value(self, i, j, k, value):
        node = self.graph[(i, j)]
        node.set_struct_value(k, value)

    def get_value(self, i, j, k):
        node = self.graph[(i, j)]
        if node.get_struct_value(k) is not None:
            return node.get_struct_value(k)
        else:
            return 0

m = 5 #ĐỘ DÀi Y
n = 5 #ĐỘ DÀi X
r = 5 #SỐ NODE CỦA CÂY TÌM KIẾM

processor = 3

graph = DAG(m + 1, n + 1 , r + 1)

# graph.partition_block(m , n , processor)

graph.print_graph()

# print(test)

# xx = graph.get_value(5 , 5 , 4)
# print("bef: "  + str(xx))
# graph.set_value(5 , 5 , 4 , 9999)
# xx = graph.get_value(5 , 5 , 4)
# print("af: "  + str(xx))


