import java.util.Comparator;

public class Comparateur implements Comparator<Point> {

    @Override
    public int compare(Point p1, Point p2) {
        if (p1.getX() > p2.getX()) {
            return 1;
        } else if (p1.getX() == p2.getX()) {
            if (p1.getY() > p2.getY()) {
                return 1;
            } else if (p1.getY() == p2.getY()) {
                return 0;
            }
        }
        return -1;
        
    }

    
   
    
}
