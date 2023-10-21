public class Shape {
    private String[][] squares = null;

    public Shape(String[][] squares) {
        this.squares = squares;
    }

    public void print() {
        for (String[] row : this.squares) {
            for (String square : row) {
                System.out.println(square);
            }
        }
    }
}
