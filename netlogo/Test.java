import static java.lang.System.out;

import java.util.*;

public class Test {

  List<Integer> l = new ArrayList<>();
  
  public static void main(String[] argv) {
    for (int i=10;i<100;i++) {
      l.add(3*i);
    }
    out.println(l);

  }
}
