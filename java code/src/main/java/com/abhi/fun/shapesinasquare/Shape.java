package com.abhi.fun.shapesinasquare;

public class Shape {
    private String[][] squares = null;

    public Shape(String[][] squares) {

        this.squares = squares;
    }

    private String[][] convertToRectangle(String[][] arr) {

//        String[][] newArr = new String[][][][]
        return null;

    }

    public void print() {
        for (String[] row : this.squares) {
            for (String square : row) {
                System.out.println(square);
            }
        }
    }
}
