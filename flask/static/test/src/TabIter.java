import java.util.Iterator;

public class TabIter<E> implements Iterator<E> {
    private E[] tableau;
    private int index;
    public TabIter(E[] tableau,int index){
        this.tableau = tableau;
        this.index = index;
        
    }
    @Override
    public boolean hasNext() {        
        return index < tableau.length && tableau[index] != null;
    }

    @Override
    public E next() {
        return tableau[index++];
    }

    
    
}


