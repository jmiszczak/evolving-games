import org.nlogo.headless.HeadlessWorkspace;

import static java.lang.System.out;

public class CalculationSave {
  public static void main(String[] argv) {
    HeadlessWorkspace ws = HeadlessWorkspace.newInstance();
    try {
      ws.open("calculations-example.netlogo");
      ws.command("set population 500");
      ws.command("setup");
      for (int i = 0; i < 10; i++) {
        ws.command("go");
        out.println("[INFO] avg-enegry: " + ws.report("avg-energy"));
      }
      ws.dispose();
    } catch (Exception ex) {
      ex.printStackTrace();
    }
  }
}
