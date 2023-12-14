import java.util.HashSet;

public class Section2_M_STR_EC_LCS {



    public static int M_STR_EC_LCS(String X , String Y , String[] P){
        AhoCorasick<String> ac = new AhoCorasick<>(P);
        int t = ac.getStatesCount();

        // Tạo ma trận f để lưu trữ các giá trị trung gian của LCS
        int[][][] f = new int[X.length()][Y.length()][t];
        // Tập hợp các trạng thái S
        HashSet<Integer> S = new HashSet<>();
        S.add(0);

        // Tính toán giá trị f(i, j, k) cho tất cả các i, j, k
        for (int i = 0; i < X.length(); i++) {
            for (int j = 0; j < Y.length(); j++) {
                for (int k : S) {
                    // Nếu các ký tự tại vị trí i và j không giống nhau
                    if (X.charAt(i) != Y.charAt(j)) {
                        // Cập nhật giá trị f[i][j][k]
                        f[i][j][k] = Math.max(i > 0 ? f[i - 1][j][k] : 0, j > 0 ? f[i][j - 1][k] : 0);
                    } else {
                        // Nếu các ký tự giống nhau
                        int ch = X.toLowerCase().charAt(i) - 'a';
                        int next_k = ac.getTransition(k, ch);
                        // Lấy giá trị output của next_k
                        int out_k = (next_k >= 0) ? ac.getOut(next_k) : 0;

                        // Nếu không có output, cập nhật giá trị f[i][j][next_k] và thêm next_k vào tập hợp S
                        if (out_k == 0) {
                            int prev_k = (i > 0 && j > 0) ? f[i - 1][j - 1][k] : 0;
                            if (next_k >= 0) {
                                f[i][j][next_k] = Math.max(prev_k, 1 + prev_k);
                                S.add(next_k);
                            }
                        }
                    }
                }
            }
        }
        // Tìm giá trị LCS lớn nhất
        int max_length = 0;
        for (int k : S) {
            max_length = Math.max(max_length, f[X.length() - 1][Y.length() - 1][k]);
        }

        return max_length;



    }

    public static void main(String[] args) {
        // Khởi tạo từ điển và các biến cần thiết
        String[] P = {"GT", "ABCTX"};
        String X = "ABCQWETX";
        String Y = "ABCTXYOM";

        int lcs_length = M_STR_EC_LCS(X, Y, P); 

        System.out.println("Length of LCS excluding P: " + lcs_length);
    }
}
