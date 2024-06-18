
public class Point implements Comparable<Point> {
    private int x;
    private int y;
    public Point (int x, int y){
        this.x = x;
        this.y = y;

    }

    public int getX() {
        return this.x;
    }

    public void setX(int x) {
        this.x = x;
    }

    public int getY() {
        return this.y;
    }

    public void setY(int y) {
        this.y = y;
    }
    
    
    public int compareTo(Point p) {
        if (this.x > p.x) {
            return 1;
        } else if (this.x == p.x) {
            if (this.y > p.y) {
                return 1;
            } else if (this.y == p.y) {
                return 0;
            }
        }
        return -1;
    }
    
}
