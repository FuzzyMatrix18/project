
import java.util.Scanner;

class RectangleDemo {
    double width, height;

    RectangleDemo() {
        width = height = 1;
    }

    RectangleDemo(double width, double height) {
        this.width = width;
        this.height = height;
    }

    double getArea() {
        return height * width;
    }

    double getPerimeter() {
        return 2 * (width + height);
    }

    void display() {
        System.out.println("Width: " + this.width + "\n" + "Height: " + this.height + "\n" + "Area is: " + getArea() + "\n");
    }
}

public class rectangle {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        double width1 = sc.nextDouble();
        double height1 = sc.nextDouble();
        double width2 = sc.nextDouble();
        double height2 = sc.nextDouble();

        RectangleDemo r1 = new RectangleDemo(width1, height1);
        RectangleDemo r2 = new RectangleDemo(width2, height2);

        r1.display();
        r2.display();
    }
}