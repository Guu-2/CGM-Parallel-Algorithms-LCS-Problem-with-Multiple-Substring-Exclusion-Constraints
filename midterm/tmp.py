

def process_data():
    global S

    for i in range(100):
    # Sử dụng biến toàn cục S
        S = S | {i} 



def ins():
    print(S)
    
if __name__ == "__main__":
    # Khởi tạo biến toàn cục S

    S = {0}
    # Gọi hàm con
    
    process_data()
    ins()
    print(S)