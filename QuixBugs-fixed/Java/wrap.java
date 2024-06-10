import java.util.*;
public
class WRAP {
public
  static void main(String[] args) {
    System.out.println("abc".lastIndexOf("c", 30));
  }
public
  static ArrayList<String> wrap(String text, int cols) {
    ArrayList<String> lines = new ArrayList<String>();
    String line;
    while (text.length() > cols) {
      int end = text.lastIndexOf(" ", cols);
      if (end == -1) {
        end = cols - 1;
      }
      if(end == 0){
          end = cols;
      }
      line = text.substring(0, end);
      text = text.substring(end);
      lines.add(line);
    }
    if(text.length()!=0){
      lines.add(text);
    }
    return lines;
  }
}
/* Tracking parameters `text` and `end` reveals that when `end` equals 0, `line` would be a single space, and the next `line` would also have a single space as its first character, since `text = text.substring(end);`. This behavior can be observed in the failed test cases: the output lines can only be wrapped at spaces, resulting in no more than a single space at the start of each line. 
Thus, checking if `end` equals 0 enables handling the scenario when the text is longer than the column width and does not have a space within `cols` to wrap at. In this case, the program wraps at `end = cols`.
 */