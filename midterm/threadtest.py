import threading
import time

# Biến đồng bộ để đảm bảo chỉ một luồng được in ra tại một thời điểm
print_lock = threading.Lock()

def worker(key, values):
    # Số lượng luồng đồng thời
    num_threads = min(len(values), 4)
    
    # Tạo danh sách các luồng
    threads = []

    # Lặp qua từng giá trị trong tập giá trị
    for i in range(num_threads):
        # Tạo luồng và thực hiện công việc
        t = threading.Thread(target=process_value, args=(key, values[i::num_threads]))
        t.start()
        threads.append(t)

    # Chờ tất cả các luồng hoàn thành
    for thread in threads:
        thread.join()

def process_value(key, values):
    # Xử lý giá trị trong luồng
    squared_values = [value ** 2 for value in values]

    # Đảm bảo chỉ một luồng được in ra tại một thời điểm
    with print_lock:
        for value, squared_value in zip(values, squared_values):
            print(f"Key: {key}, Value: {value}, Squared Value: {squared_value}")

# Tạo từ điển giá trị
dict_values = {
    1: [0],
    2: [4, 1],
    3: [8, 5, 2],
    4: [12, 9, 6, 3],
    5: [13, 10, 7],
    6: [14, 11],
    7: [15]
}

# Lặp qua từng key trong từ điển và tạo luồng
for key, values in dict_values.items():
    worker(key, values)
    # time.sleep(1)  # Chờ 1 giây trước khi tiếp tục với key tiếp theo