import java.util.ArrayList;
import java.util.Arrays;

class Node {
    ArrayList<Integer> name;
    ArrayList<Node> children;
    ArrayList<ArrayList<Integer>> struct;

    public Node(ArrayList<Integer> name) {
        this.name = name;
        this.children = new ArrayList<>();
        this.struct = new ArrayList<>();
    }

    public void addChild(Node child) {
        this.children.add(child);
    }

    public void addStruct(ArrayList<Integer> s) {
        this.struct.add(s);
    }
}

public class DAG {
    public static void main(String[] args) {
        String X = "abcde";
        String Y = "afdbf";
        String P = "abc";

        ArrayList<Node> nodes = new ArrayList<>();
        for (int i = 1; i <= X.length(); i++) {
            for (int j = 1; j <= Y.length(); j++) {
                nodes.add(new Node(new ArrayList<>(Arrays.asList(i, j))));
            }
        }

        for (Node i : nodes) {
            int a = i.name.get(0) - 1;
            int b = i.name.get(1) - 1;
            if (a == 0 && b == 0) {
                i.addChild(new Node(new ArrayList<>(Arrays.asList(0, 0))));
            }
            for (Node j : nodes) {
                if (a != 0 && j.name.equals(Arrays.asList(a, i.name.get(1)))) {
                    i.addChild(j);
                }
                if (b != 0 && j.name.equals(Arrays.asList(i.name.get(0), b))) {
                    i.addChild(j);
                }
                if (a != 0 && b != 0 && j.name.equals(Arrays.asList(a, b))) {
                    i.addChild(j);
                }
            }
            if (i.children.size() < 3) {
                i.addChild(new Node(new ArrayList<>(Arrays.asList(0, 0))));
                i.addChild(new Node(new ArrayList<>(Arrays.asList(0, 0))));
            }
        }

        for (Node i : nodes) {
            for (int j = 0; j < P.length(); j++) {
                i.addStruct(new ArrayList<>(Arrays.asList(i.name.get(0), i.name.get(1), j)));
            }
        }

        for (Node i : nodes) {
            System.out.println("p: " + i.name);
            for (Node j : i.children) {
                System.out.println("c: " + j.name);
            }
            System.out.println("-------------");
        }

        for (Node i : nodes) {
            for (ArrayList<Integer> s : i.struct) {
                System.out.println(s);
            }
            break;
        }
    }
}
