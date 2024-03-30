import java.util.*;
import java.io.*;
import java.math.*;
import java.text.*;
public
class Main {
public
static void main(String args[]) throws IOException {
Read sc = new Read();
String s = sc.next();
String t = sc.next();
sc.println(ok(s, t) ? "Yes" : "No");
sc.bw.flush();
sc.bw.close();
}
public
static boolean ok(String s, String t) {
List<Integer> list = new ArrayList<>();
for (int i = 0; i < s.length(); i++) {
if (s.charAt(i) != t.charAt(i)) {
list.add(i);
}
}
if (list.size() == 0) {
return true;
}
if (list.size() != 2) {
return false;
}
int a = list.get(0), b = list.get(1);
return s.charAt(a) == t.charAt(b) && s.charAt(b) == t.charAt(a); // Buggy line
<INFILL> // Missing this line causes a bug
}
}
class Read {
BufferedReader bf;
StringTokenizer st;
BufferedWriter bw;
public
Read() {
bf = new BufferedReader(new InputStreamReader(System.in));
st = new StringTokenizer("");
bw = new BufferedWriter(new OutputStreamWriter(System.out));
}
public
String nextLine() throws IOException { return bf.readLine(); }
public
String next() throws IOException {
while (!st.hasMoreTokens()) {
st = new StringTokenizer(bf.readLine());
}
return st.nextToken();
}
public
char nextChar() throws IOException { return next().charAt(0); }
public
int nextInt() throws IOException { return Integer.parseInt(next()); }
public
long nextLong() throws IOException { return Long.parseLong(next()); }
public
double nextDouble() throws IOException { return Double.parseDouble(next()); }
public
float nextFloat() throws IOException { return Float.parseFloat(next()); }
public
byte nextByte() throws IOException { return Byte.parseByte(next()); }
public
short nextShort() throws IOException { return Short.parseShort(next()); }
public
BigInteger nextBigInteger() throws IOException {
return new BigInteger(next());
}
public
void println(int a) throws IOException {
bw.write(String.valueOf(a));
bw.newLine();
return;
}
public
void print(int a) throws IOException {
bw.write(String.valueOf(a));
return;
}
public
void println(String a) throws IOException {
bw.write(a);
bw.newLine();
return;
}
public
void print(String a) throws IOException {
bw.write(a);
return;
}
public
void println(long a) throws IOException {
bw.write(String.valueOf(a));
bw.newLine();
return;
}
public
void print(long a) throws IOException {
bw.write(String.valueOf(a));
return;
}
public
void println(double a) throws IOException {
bw.write(String.valueOf(a));
bw.newLine();
return;
}
public
void print(double a) throws IOException {
bw.write(String.valueOf(a));
return;
}
public
void print(BigInteger a) throws IOException {
bw.write(a.toString());
return;
}
public
void print(char a) throws IOException {
bw.write(String.valueOf(a));
return;
}
public
void println(char a) throws IOException {
bw.write(String.valueOf(a));
bw.newLine();
return;
}
}