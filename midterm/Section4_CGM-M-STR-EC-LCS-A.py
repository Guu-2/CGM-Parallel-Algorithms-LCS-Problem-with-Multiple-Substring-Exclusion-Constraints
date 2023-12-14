import multiprocessing
import math



# Python program for implementation of
# Aho-Corasick algorithm for string matching

# defaultdict is used only for storing the final output
# We will return a dictionary where key is the matched word
# and value is the list of indexes of matched word
from collections import defaultdict

# For simplicity, Arrays and Queues have been implemented using lists. 
# If you want to improve performance try using them instead
class AhoCorasick:
    def __init__(self, words):

        # Max number of states in the matching machine.
        # Should be equal to the sum of the length of all keywords.
        self.max_states = sum([len(word) for word in words])

        # Maximum number of characters.
        # Currently supports only alphabets [a,z]
        self.max_characters = 26

        # OUTPUT FUNCTION IS IMPLEMENTED USING out []
        # Bit i in this mask is 1 if the word with
        # index i appears when the machine enters this state.
        # Lets say, a state outputs two words "he" and "she" and
        # in our provided words list, he has index 0 and she has index 3
        # so value of out[state] for this state will be 1001
        # It has been initialized to all 0.
        # We have taken one extra state for the root.
        self.out = [0]*(self.max_states+1)

        # FAILURE FUNCTION IS IMPLEMENTED USING fail []
        # There is one value for each state + 1 for the root
        # It has been initialized to all -1
        # This will contain the fail state value for each state
        self.fail = [-1]*(self.max_states+1)

        # GOTO FUNCTION (OR TRIE) IS IMPLEMENTED USING goto [[]]
        # Number of rows = max_states + 1
        # Number of columns = max_characters i.e 26 in our case
        # It has been initialized to all -1.
        self.goto = [[-1]*self.max_characters for _ in range(self.max_states+1)]

        # Convert all words to lowercase
        # so that our search is case insensitive
        for i in range(len(words)):
            words[i] = words[i].lower()

        # All the words in dictionary which will be used to create Trie
        # The index of each keyword is important:
        # "out[state] & (1 << i)" is > 0 if we just found word[i]
        # in the text.
        self.words = words

        # Once the Trie has been built, it will contain the number
        # of nodes in Trie which is total number of states required <= max_states
        self.states_count = self.__build_matching_machine()


	# Builds the String matching machine.
	# Returns the number of states that the built machine has.
    # States are numbered 0 up to the return value - 1, inclusive.
    def __build_matching_machine(self):
        k = len(self.words)

        # Initially, we just have the 0 state
        states = 1

        # Convalues for goto function, i.e., fill goto
        # This is same as building a Trie for words[]
        for i in range(k):
            word = self.words[i]
            current_state = 0

            # Process all the characters of the current word
            for character in word:
                ch = ord(character) - 97 # Ascii value of 'a' = 97

                # Allocate a new node (create a new state)
                # if a node for ch doesn't exist.
                if self.goto[current_state][ch] == -1:
                    self.goto[current_state][ch] = states
                    states += 1

                current_state = self.goto[current_state][ch]

            # Add current word in output function
            self.out[current_state] |= (1<<i)

        # For all characters which don't have
        # an edge from root (or state 0) in Trie,
        # add a goto edge to state 0 itself
        for ch in range(self.max_characters):
            if self.goto[0][ch] == -1:
                self.goto[0][ch] = 0
        
        # Failure function is computed in 
        # breadth first order using a queue
        queue = []

        # Iterate over every possible input
        for ch in range(self.max_characters):

            # All nodes of depth 1 have failure
            # function value as 0. For example,
            # in above diagram we move to 0
            # from states 1 and 3.
            if self.goto[0][ch] != 0:
                self.fail[self.goto[0][ch]] = 0
                queue.append(self.goto[0][ch])

        # Now queue has states 1 and 3
        while queue:

            # Remove the front state from queue
            state = queue.pop(0)

            # For the removed state, find failure
            # function for all those characters
            # for which goto function is not defined.
            for ch in range(self.max_characters):

                # If goto function is defined for
                # character 'ch' and 'state'
                if self.goto[state][ch] != -1:

                    # Find failure state of removed state
                    failure = self.fail[state]

                    # Find the deepest node labeled by proper
                    # suffix of String from root to current state.
                    while self.goto[failure][ch] == -1:
                        failure = self.fail[failure]
                    
                    failure = self.goto[failure][ch]
                    self.fail[self.goto[state][ch]] = failure

                    # Merge output values
                    self.out[self.goto[state][ch]] |= self.out[failure]

                    # Insert the next level node (of Trie) in Queue
                    queue.append(self.goto[state][ch])
        
        return states



 
class Node:
    def __init__(self, value):
        # positon value
        self.value = value
        # struct list for k node
        self.struct_list = []
        # dependencies edge
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
            

    def print_struct(self):
        for _, node in self.graph.items():
            print(f"{node.value} -> {node.struct_list}")


def get_delta(i, p , str):
    alphabet = len(str)
    rounded_up = math.ceil(alphabet / p)
    start_index = i * rounded_up
    end_index = min((i + 1) * rounded_up, alphabet)
    char_list = [str[x] for x in range(start_index, end_index)]
    return char_list

def partition_block(start_row, end_row, start_col, end_col):
    # Tạo khối con bằng cách trích xuất phần của ma trận ban đầu
    submatrix = []
    # submatrices = []
    for row in reversed(range(start_row + 1, end_row + 1)):
        if  row > 0 : 
            submatrix_row = []
            for col in reversed(range(start_col + 1, end_col +1)):
                if col > 0 :
                    value = (row, col)
                    submatrix_row.insert(0 ,value)
            submatrix.append(submatrix_row)
    # submatrices.append(submatrix)
    return submatrix


# dynamic programming algorithm to solve LCS With expluding constraint (solve sub_lcs )
def sub_lcs(X , Y , block , P):
    print(X)
    print(Y)
    n = len(block)
    m = len(block[0])
    # print(m)
    # print(n)
    # # t = len(P) 
    T = AhoCorasick(P)
    t = T.states_count
    # print(t)
    # # Khởi tạo ma trận f(i, j, k)
    f = [[[-1] * (t) for _ in range(m)] for _ in range(n)]
    # Gán giá trị f(i, 0, 0) và f(0, j, 0) bằng 0
    for i in range(n):
        f[i][0][0] = 0
    for j in range(m):
        f[0][j][0] = 0
        
    S = {0}  # Tập hợp các trạng thái
    # print(f)
    # Tính toán giá trị f(i, j, k) cho tất cả các i, j, k
    for i in range(n):
        for j in range(m):
            (x , y) = block[i][j]
            # print(x, y)
            # print('\nindex row: ' + str(i) + ' column : ' + str(j) );
            for k in S:
                if X[x] != Y[y]:
                    
                    f[i][j][k] = max(f[i - 1][j][k], f[i][j - 1][k])
                    # print(f[i][j][k])
                else:
                    ch = ord(X[x].lower()) - 97
                    next_k = T.goto[k][ch] #same for X[i] , Y[i] 

                    out_k = T.out[next_k]
                    print("ouput : " + str(out_k))
                    # k = T[k].get(X[i - 1], 0)
                    if int(out_k) == 0:
                        f[i][j][next_k] = max(f[i - 1][j - 1][next_k], 1 + f[i - 1][j - 1][k])
                        # print(f[i][j][next_k])
                        # print(f[n-1][m-1][next_k])
                        S = S | {next_k}
    max_length = (f[n - 1 ][m -1][k] for k in range(t))
    return max_length



def linear_mapping(blocks, processors):
    mapping = []
    for i, block in enumerate(blocks):
        processor = i % processors
        mapping.append((block, processor))
    return mapping


def CGM_M_STR_EC_LCS_A(X , Y , P , processors):

    # //TODO: testing
    m = len(X)  # Số hàng
    n = len(Y)  # Số cột
    T = AhoCorasick(P)
    p = processors   # Số lượng khối theo chiều dọc và chiều ngang
    alpha = math.ceil(m / p)  # Kích thước của mỗi khối theo chiều ngang
    print(alpha)
    beta = math.ceil( n / p)  # Kích thước của mỗi khối theo chiều dọc
    print(beta)
    flag = 0
    submatrices = []
    for i in range(p):
        for j in range(p):
            # Xác định chỉ số hàng và cột kết thúc của khối con
            start_row = i * alpha - flag
            start_col = j * beta - flag
            res= [1 , 1 ,2 ]
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
            
            submatrix = partition_block(start_row, end_row , start_col, end_col)
            submatrices.append(submatrix)
            
    pool = multiprocessing.Pool(processes=processors)
    results = []
    # print(submatrices[8])
    unique_chars = set(X.lower() + Y.lower())
    unique_str = ''.join(unique_chars)
    print(unique_str)
    
    next_matrix = []

    # build next matrix
    for i in range(processors):
        list_delta = get_delta(i, processors ,unique_str)
        for k in range(T.states_count):
            for j in list_delta:
                # print(j)
                next_matrix.append(T.goto[k][ord(j.lower()) - 97])
    mapping = linear_mapping(submatrices , processors)
    
    # mapping block to processor
    for block, p in mapping:
        # print(block)
        # print(f"{block} is mapped to Processor {processor}")
        result = pool.apply_async(sub_lcs, (X , Y , block , P))
        results.append(result)
        
    pool.close()
    pool.join()
    
    lcs_length = 0

    for x in res:
        lcs_length+=x
    
    print(results)
    print(lcs_length)

    return lcs_length
# Driver code
if __name__ == "__main__":
    
    
    X = "ABCTXIYZ"
    Y = "ABCDTXYO"
    P = ["GT" , "ABCTX"]
    processors = 3
    
    lcs_length = CGM_M_STR_EC_LCS_A(X , Y , P , processors)
    
    print("Length of LCS excluding P:", lcs_length)



    
    # print(rounded_up) # Output:
    
    # m = 5
    # n = 5
    # r = 5
    # # Khởi tạo đồ thị DAG từ ma trận bằng cách gọi phương thức __init__
    # graph = Graph(m + 1, n  +1, r +1)

    # # In đồ thị
    # graph.print_graph()
    # graph.print_struct()
