from guu256 import *
from AhoCorasickTree import *
import math
import threading
from queue import Queue
from collections import deque


from concurrent.futures import ThreadPoolExecutor

# Tạo Lock để đồng bộ hóa in kết quả
lock = threading.Lock()

communicate = set()



# TODO: chia luồng và làm như bình thường

# # Tạo dictionary với key và value tương ứng
# data = {
#     1: [0],
#     2: [4, 1],
#     3: [8, 5, 2],
#     4: [12, 9, 6, 3],
#     5: [13, 10, 7],
#     6: [14, 11],
#     7: [15]
# }


def process_data(X , Y , T , graph , key, value ,  matrix , diagonal):
    # Thực thi công việc tương ứng với value
    # graph.print_graph()
    global communicate
    with lock:

        print(f"Thread {key}: Matrix : {value} ( in diagonal : {diagonal})")
        # S.add(diagonal)
        sub_lcs(X , Y , T , graph ,matrix)
        # graph.print_graph()
        # print(T.states_count)






def sub_lcs(X , Y , T , graph ,matrix):
    
    global S
    
    # print(matrix)
    sub_row = len(matrix)
    sub_col = len(matrix[0])

    # print(T)
    # print(len(matrix[0]))
    
    # Tập hợp các trạng thái k
    
    #Tính toán giá trị f(i, j, k) cho tất cả các i, j, k
    for i in range(sub_row):
        for j in range(sub_col):
            # print(i , j)
            #TODO: index không tuyến tính
            curr_node = matrix[i][j]
            curr_row =curr_node.get_vertical()
            curr_col =curr_node.get_horizontal()
            # print(curr_row , curr_col)

            # value = graph.get_value(curr_row - 1, curr_col - 1 , 8)
            # print(value)
            for k in S:
                if X[curr_row - 1] != Y[curr_col - 1]:
                # TODO: bị thiếu 1 index so với ban đầu
                    value = max(graph.get_value(curr_row - 1, curr_col, k + 1), graph.get_value(curr_row , curr_col - 1, k + 1))
                    graph.set_value(curr_row, curr_col , k + 1 , value)
                    # print(X , X[curr_row -1] ,Y, Y[curr_col -1])
                else:
                    # print(X , X[curr_row -1] ,Y, Y[curr_col -1])
                    #     # TODO: cụm này tách ra làm tiền xử lý
                    ch = ord(X[curr_row - 1].lower()) - 97
                    next_k = T.goto[k][ch] #same for X[i] , Y[i] 
                    out_k = T.out[next_k]
                    print("ouput : " + str(out_k))
                    print(next_k)
                    if int(out_k) == 0:
                        # print("??")
                        value = max(graph.get_value(curr_row - 1 , curr_col  -1, next_k + 1), 1 + graph.get_value(curr_row  -1 , curr_col -1 ,k + 1))
                        graph.set_value(curr_row , curr_col , next_k + 1, value)
                        S  = S | {next_k}


    # # TODO: chạy tay từng khối con => xác định S' , U' , V' để gửi
    # # PROBLEM: đâu là index toàn phần , đúng cho tất cả các trường hợp 
    Sp = [matrix[len(matrix) - 1][len(matrix[0]) - 1 ]]
    print(Sp)
    # print(Sp[0].get_vertical())
    # print(Sp[0].get_horizontal())
    # list_col = [i for i in range(Sp[0].get_horizontal()- sub_col + 1, Sp[0].get_horizontal())]
    # # print(list_col)
    # # print(sub_col)
    # Up = [graph.get_node(Sp[0].get_vertical(),i) for i in range(Sp[0].get_horizontal()- sub_col + 1, Sp[0].get_horizontal())]
    # # print(Up)
    # Vp = [graph.get_node(j,Sp[0].get_horizontal()) for j in range(Sp[0].get_vertical()- sub_row + 1, Sp[0].get_vertical())]
    # # print(Vp)
    tmp = [graph.get_value(Sp[0].get_vertical() ,Sp[0].get_horizontal() , k + 1) for k in range( T.states_count)]
    
    print(tmp)
    
    # return  
    
def CGM_M_STR_EC_LCS_A(X , Y , P ):
    
    global S
    
    m  =len(X)
    n = len(Y)
    
    p = 3
    
    T = AhoCorasick(P)
    t = T.states_count
    # print(t)
    # print(len(P))
    graph = DAG(m + 1, n + 1, t  + 1)
    # graph.print_graph()
    
    blocks = graph.partition_block(m , n , p) #LIST MATRIX
    # print(blocks)
    snake_path = graph.build_snake_path(blocks , p)

    dict_diagonal = graph.build_digonal(snake_path , p)
    
    # Tạo ThreadPoolExecutor với số lượng luồng
    executor = ThreadPoolExecutor(max_workers=p)
    
    # TODO: build next matrix
    

    # Duyệt qua từng key và value trong dictionary
    thread_index = 1
    
    S = {0}
    
    for d in range(1 , 2*p ):
        # print(d)
        values = dict_diagonal[d]
        for value in values:
            #TODO: vẫn còn bất đồng bộ (ĐỒNG BỘ TÙY DUYÊN =)) )
            # Lấy giá trị của key và ánh xạ vào luồng tương ứng
            executor.submit(process_data,X, Y, T , graph, thread_index, value , blocks[value] , d)
            thread_index+=1;
            
            if(thread_index > p):
                thread_index = 1
    # Đảm bảo rằng tất cả các luồng đã hoàn thành trước khi kết thúc chương trình
    executor.shutdown()
        
    print(S)

    list_result = [graph.get_value(len(X) , len(Y) ,  k + 1) for k in range(t)]
    print(list_result)
    max_length = max(list_result)
    
    

    return max_length



# Driver code
if __name__ == "__main__":
    
    
    X = "ABCQWETX"
    Y = "ABCTXYOM"
    P = ["GT" , "ABCTX"]
    # processors = 4
    
    lcs_length = CGM_M_STR_EC_LCS_A(X , Y , P)
    # sub_lcs(submatrices[0])

    print("Length of LCS excluding P:", lcs_length)



    
    # print(rounded_up) # Output:
    