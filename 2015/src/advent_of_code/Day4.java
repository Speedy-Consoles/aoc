package advent_of_code;

import java.util.HashSet;
import java.util.Scanner;

public class Day4 {

	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		char[] chars = sc.next().toCharArray();
		sc.close();
		int cx = 0;
		int cy = 0;
		int crx = 0;
		int cry = 0;
		HashSet<Pos> set = new HashSet<Pos>();
		set.add(new Pos(cx, cy));
		for (int i = 0; i < chars.length; i++) {
			switch (chars[i]) {
			case '>':
				cx++;
				break;
			case 'v':
				cy--;
				break;
			case '<':
				cx--;
				break;
			case '^':
				cy++;
				break;
			}
			set.add(new Pos(cx, cy));
			i++;
			switch (chars[i]) {
			case '>':
				crx++;
				break;
			case 'v':
				cry--;
				break;
			case '<':
				crx--;
				break;
			case '^':
				cry++;
				break;
			}
			set.add(new Pos(crx, cry));
		}
		System.out.println(set.size());
	}
}

class Pos {
	public int x;
	public int y;
	
	Pos(int x, int y) {
		this.x = x;
		this.y = y;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + x;
		result = prime * result + y;
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Pos other = (Pos) obj;
		if (x != other.x)
			return false;
		if (y != other.y)
			return false;
		return true;
	}
}