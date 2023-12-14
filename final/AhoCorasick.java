import java.util.LinkedList;
import java.util.Queue;

public class AhoCorasick<T> {
    private int max_states; // Tổng số trạng thái tối đa trong máy Aho-Corasick
    private int max_characters; // Số lượng ký tự tối đa (ở đây là 26 chữ cái tiếng Anh)
    private int[] out;// Mảng lưu trữ các trạng thái đầu ra
    private int[] fail;// Mảng lưu trữ hàm thất bại (failure function)
    private int[][] transitions;// Bảng chuyển trạng thái (goto)
    private T[] words; // Mảng chứa các từ cần tìm kiếm
    private int states_count; // Số lượng trạng thái thực tế trong máy Aho-Corasick

    // Constructor cho lớp AhoCorasick
    public AhoCorasick(T[] words) {
        this.max_states = 0;

        // Tính tổng số trạng thái tối đa dựa trên độ dài của các từ đầu vào
        for (T word : words) {
            this.max_states += word.toString().length();
        }

        // Maximum number of characters.
        // Currently supports only alphabets [a,z]
        this.max_characters = 26;

        // OUTPUT FUNCTION IS IMPLEMENTED USING out []
        // Bit i in this mask is 1 if the word with
        // index i appears when the machine enters this state.
        // Lets say, a state outputs two words "he" and "she" and
        // in our provided words list, he has index 0 and she has index 3
        // so value of out[state] for this state will be 1001
        // It has been initialized to all 0.
        // We have taken one extra state for the root.
        this.out = new int[this.max_states + 1];

        // FAILURE FUNCTION IS IMPLEMENTED USING fail []
        // There is one value for each state + 1 for the root
        // It has been initialized to all -1
        // This will contain the fail state value for each state
        this.fail = new int[this.max_states + 1];


        this.transitions = new int[this.max_states + 1][this.max_characters];

        // Khởi tạo mảng transitions với -1 để chỉ không có chuyển trạng thái
        for (int i = 0; i <= this.max_states; i++) {
            for (int j = 0; j < this.max_characters; j++) {
                this.transitions[i][j] = -1;
            }
        }

        // Chuyển đổi các từ đầu vào thành chữ thường và lưu trữ chúng
        this.words = words;
        this.states_count = buildMatchingMachine();
    }

    // Phương thức xây dựng máy tìm kiếm Aho-Corasick
    private int buildMatchingMachine() {
        int k = words.length;
        int states = 1;
    
        // Lặp qua từng từ đầu vào
        for (int i = 0; i < k; i++) {
            String word = words[i].toString();
            int currentState = 0;
            // Xử lý từng ký tự trong từ
            for (char character : word.toCharArray()) {
                // Chuyển đổi ký tự thành chữ thường và tính chỉ số của ký tự
                int ch = Character.toLowerCase(character) - 'a';
    
                // Kiểm tra xem chỉ số ký tự có nằm trong phạm vi hợp lệ không
                if (ch < 0 || ch >= max_characters) {
                    throw new IllegalArgumentException("Invalid character: " + character);
                }
                
                // Nếu không có chuyển trạng thái cho ký tự hiện tại, tạo một trạng thái mới
                if (transitions[currentState][ch] == -1) {
                    transitions[currentState][ch] = states;
                    states++;
                }
    
                currentState = transitions[currentState][ch];
            }
    
            // Đánh dấu trạng thái cuối cùng của từ với bit tương ứng trong mảng out
            out[currentState] |= (1 << i);
        }
    
        // Đảm bảo các chuyển trạng thái từ trạng thái ban đầu đều được đặt về trạng thái ban đầu
        for (int ch = 0; ch < max_characters; ch++) {
            if (transitions[0][ch] == -1) {
                transitions[0][ch] = 0;
            }
        }
    
        // Khởi tạo hàm thất bại bằng BFS
        Queue<Integer> queue = new LinkedList<>();
    
        for (int ch = 0; ch < max_characters; ch++) {
            if (transitions[0][ch] != 0) {
                fail[transitions[0][ch]] = 0;
                queue.add(transitions[0][ch]);
            }
        }
    
        while (!queue.isEmpty()) {
            int state = queue.poll();
    
            // Lặp qua các ký tự để xây dựng hàm thất bại
            for (int ch = 0; ch < max_characters; ch++) {
                if (transitions[state][ch] != -1) {
                    int failure = fail[state];
                    
                    // Xác định trạng thái thất bại bằng cách di chuyển ngược lên cây chuyển trạng thái
                    while (transitions[failure][ch] == -1) {
                        failure = fail[failure];
                    }
    
                    failure = transitions[failure][ch];
                    fail[transitions[state][ch]] = failure;
                    out[transitions[state][ch]] |= out[failure];
                    queue.add(transitions[state][ch]);
                }
            }
        }
    
        return states;
    }
    

    // Phương thức lấy số lượng trạng thái trong máy Aho-Corasick
    public int getStatesCount() {
        return states_count;
    }

    // Phương thức lấy trạng thái tiếp theo dựa trên trạng thái hiện tại và chỉ số ký tự
    public int getTransition(int state, int character) {
        return transitions[state][character];
    }

    // Phương thức lấy các bit đầu ra cho một trạng thái cụ thể
    public int getOut(int state) {
        return out[state];
    }
}
