from concurrent.futures import ThreadPoolExecutor
import threading

# TODO: chia luồng và làm như bình thường

# Tạo dictionary với key và value tương ứng
data = {
    1: [0],
    2: [4, 1],
    3: [8, 5, 2],
    4: [12, 9, 6, 3],
    5: [13, 10, 7],
    6: [14, 11],
    7: [15]
}

# Số lượng luồng
num_threads = 4

# Tạo Lock để đồng bộ hóa in kết quả
lock = threading.Lock()

def process_data(key, value):
    # Thực thi công việc tương ứng với value
    with lock:
        print(f"Thread {key}: Value {value}")

# Tạo ThreadPoolExecutor với số lượng luồng
executor = ThreadPoolExecutor(max_workers=num_threads)

# Duyệt qua từng key và value trong dictionary
thread_index = 1
for key in data:
    values = data[key]
    for value in values:
        # Lấy giá trị của key và ánh xạ vào luồng tương ứng
        executor.submit(process_data, thread_index, value)
        thread_index+=1;
        
        if(thread_index > 4):
            thread_index = 1
        

# Đảm bảo rằng tất cả các luồng đã hoàn thành trước khi kết thúc chương trình
executor.shutdown()