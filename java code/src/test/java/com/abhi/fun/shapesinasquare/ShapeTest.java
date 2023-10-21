package com.abhi.fun.shapesinasquare;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertThrows;

public class ShapeTest {

    private static void print(String str) {
        System.out.println(str);
    }

    @Test
    void testConstructor() {
        System.out.println("Inside test constructor");
        int[][] arr = {{1, 1}};
        Shape s = new Shape(arr);
    }

    @Test
    void testSanityCheck() {
        int[][] arr = {{1, 2}};
        Exception e = assertThrows(RuntimeException.class, () -> new Shape(arr));
        print(e.getMessage());
    }
}
