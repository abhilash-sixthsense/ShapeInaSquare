package com.abhi.fun.shapesinasquare;

public class Shape {
    private int[][] squares = null;

    public Shape(int[][] squares) {
        this.doSanityCheck(squares);
        this.squares = squares;
        this.print();
    }

    public void doSanityCheck(int[][] squares) throws RuntimeException {
        int shapeNumber = -1;
        for (int[] row : squares) {
            for (int square : row) {
                if (square <= 0) {
                    throw new RuntimeException("Array should not contain negative numbers");
                }
                if (shapeNumber == -1) {
                    shapeNumber = square;
                } else if (shapeNumber != square) {
                    throw new RuntimeException("Multiple numbers are used " + shapeNumber + "  " + square);
                }
                System.out.printf("%3d", square);
            }
            System.out.println();
        }
    }

    public void print() {
        for (int[] row : this.squares) {
            for (int square : row) {
                System.out.printf("%3d", square);
            }
            System.out.println();
        }
    }
}
