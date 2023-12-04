package advent_of_code;

import java.util.Scanner;

public class Day1 {

	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		char[] chars = sc.next().toCharArray();
		sc.close();
		int floor = 0;
		int firstBasementPos = 0;
		for (int i = 0; i < chars.length; i++) {
			if (chars[i] == '(')
				floor++;
			else if (chars[i] == ')')
				floor--;
			if (floor == -1 && firstBasementPos == 0)
				firstBasementPos = i + 1;
		}
		System.out.println(floor);
		System.out.println(firstBasementPos);
	}
}
