import java.util.Scanner;
public
class Main {
public
static void main(String[] args) {
Scanner sc = new Scanner(System.in);
int x = sc.nextInt();
String s = "" + x;
String result = "";
if (s.length() == 4) {
result = "" + x;
} else if (s.length() == 3) {
result = "0" + x;
} else if (s.length() == 2) {
result = "00" + x;
} else {
result = "00x" + x; // Buggy line
}
System.out.println(result);
}
}