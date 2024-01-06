from guu256 import *
from AhoCorasickTree import *
import math
import threading
from queue import Queue
from collections import deque


from concurrent.futures import ThreadPoolExecutor

# Tạo Lock để đồng bộ hóa in kết quả
lock = threading.Lock()

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

def process_data(key, value ,  matrix):
    # Thực thi công việc tương ứng với value
    with lock:
        print(f"Thread {key}: Matrix : {value}")
        sub_lcs(matrix)


# def mapping_block(dict , all_blocks , p):
        
                
def sub_lcs(matrix):
    print(matrix)

def CGM_M_STR_EC_LCS_A(X , Y , P ):

    m  =len(X)
    n = len(Y)
    
    p = 3
    
    T = AhoCorasick(P)
    t = T.states_count
    # print(len(P))
    graph = DAG(m + 1, n + 1, t  + 1)
    # graph.print_graph()
    
    # blocks = graph.partition_block(m , n , p)
    # # print(len(graph.blocks))
    # snake_path = graph.build_snake_path(blocks , p)

    # dict_diagonal = graph.build_digonal(snake_path , p)
    
    # # Tạo ThreadPoolExecutor với số lượng luồng
    # executor = ThreadPoolExecutor(max_workers=p)
    
    # # Duyệt qua từng key và value trong dictionary
    # thread_index = 1

    # for d in range(1 , 2*p ):
    #     # print(d)
    #     values = dict_diagonal[d]
    #     for value in values:
    #         # Lấy giá trị của key và ánh xạ vào luồng tương ứng
    #         executor.submit(process_data, thread_index, value , blocks[value])
    #         thread_index+=1;
            
    #         if(thread_index > p):
    #             thread_index = 1
    #     # Đảm bảo rằng tất cả các luồng đã hoàn thành trước khi kết thúc chương trình
    # executor.shutdown()
        
    # print(graph.get_value(1 , 5 , 10))
    
    # Gán giá trị f(i, 0, 0) và f(0, j, 0) bằng 0
    # for i in range(n):
    #     graph.set_value(i , 0 , 0, 0)
    # for j in range(m):
    #     graph.set_value(0 , j , 0, 0)
        
    # graph.print_graph()
    S = {0}  # Tập hợp các trạng thái


    # print(f)
    # Tính toán giá trị f(i, j, k) cho tất cả các i, j, k
    for i in range(len(X)):
        for j in range(len(Y)):
            # print('\nindex row: ' + str(i) + ' column : ' + str(j) );
            for k in S:
                if X[i] != Y[j]:
                #INDEX TUyến tính 
                # TODO: bị thiếu 1 index so với ban đầu
                    # value = graph.get_value(i, j + 1, k + 1 )
                    value = max(graph.get_value(i, j + 1, k + 1 ), graph.get_value(i + 1 , j , k  + 1))
                    graph.set_value(i + 1, j + 1 , k + 1 , value)
                else:
                    ch = ord(X[i].lower()) - 97
                    next_k = T.goto[k][ch] #same for X[i] , Y[i] 

                    out_k = T.out[next_k]
                    print("ouput : " + str(out_k))
                    print(next_k)
                    if int(out_k) == 0:
                        value = max(graph.get_value(i , j , next_k + 1), 1 + graph.get_value(i , j ,k + 1))
                        graph.set_value(i + 1 , j + 1 , next_k + 1, value)
                        S = S | {next_k}

    # Tìm giá trị lớn nhất của f(n, m, k)

    print(S)
    # graph.print_graph()

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
    