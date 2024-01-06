import threading
from queue import Queue

# Biến đồng bộ để đảm bảo chỉ một luồng được in ra tại một thời điểm
print_lock = threading.Lock()

S  ={0}
def worker(key, values, queue):
    # global S
    # Lặp qua từng giá trị trong tập giá trị
    for value in values:
        # Xử lý giá trị trong luồng
        squared_value = value ** 2

        # Đảm bảo chỉ một luồng được in ra tại một thời điểm
        with print_lock:
            print(f"Key: {key}, Value: {value}, Squared Value: {squared_value}")
            S = S | {value}
        # Thêm giá trị đã xử lý vào hàng đợi
        queue.put(squared_value)

def process_values(key, values):
    # Tạo hàng đợi để lưu trữ giá trị đã xử lý
    queue = Queue()

    # Tạo danh sách các luồng
    threads = []

    # Lặp qua từng giá trị trong tập giá trị
    for value in values:
        # Tạo luồng và thực hiện công việc
        t = threading.Thread(target=worker, args=(key, [value], queue))
        t.start()
        threads.append(t)

    # Chờ tất cả các luồng hoàn thành
    for thread in threads:
        thread.join()

    # Lấy các giá trị đã xử lý từ hàng đợi
    processed_values = []
    while not queue.empty():
        processed_values.append(queue.get())

    print(S)
    return processed_values

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

# Lặp qua từng key trong từ điển và xử lý giá trị bằng đa luồng
for key, values in dict_values.items():
    processed_values = process_values(key, values)
    print(f"Processed values for key {key}: {processed_values}")