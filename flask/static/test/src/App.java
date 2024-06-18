
public class App {
    public static void main(String[] args){
          Integer[] intArray = {1,5,3,6,7} ;
          int index = 0;
          TabIter<Integer> intIter = new TabIter<>(intArray,index);
          while(intIter.hasNext()){
            System.out.println(intIter.next());
          }
          String[] strArray = {"ahmed","sabar","mouna","nessiba"};
          TabIter<String> strIter = new TabIter<>(strArray,index);
          while(strIter.hasNext()){
            System.out.println(strIter.next());
          }
            
    }
}