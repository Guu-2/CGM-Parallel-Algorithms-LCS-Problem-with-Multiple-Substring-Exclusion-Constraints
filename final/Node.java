import java.util.ArrayList;
import java.util.List;

public class Node {
    private int i;
    private int j;
    private int k;
    private List<Node> children;

    public Node(int i, int j, int k) {
        this.i = i;
        this.j = j;
        this.k = k;
        this.children = new ArrayList<>();
    }

    public int getI() {
        return i;
    }

    public int getJ() {
        return j;
    }

    public int getK() {
        return k;
    }

    public List<Node> getChildren() {
        return children;
    }

    public void addChild(Node child) {
        children.add(child);
    }
}