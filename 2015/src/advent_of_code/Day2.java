package advent_of_code;

import java.util.Scanner;

public class Day2 {

	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		int totalPaper = 0;
		int totalRibbon = 0;
		while(sc.hasNext()) {
			String[] sizeStrings = sc.next().split("x");
			int[] sizes = new int[3];
			int longestEdge = Integer.MIN_VALUE;
			int longestEdgeIndex = 0;
			for (int i = 0; i < 3; i++) {
				sizes[i] = Integer.parseInt(sizeStrings[i]);
				if (sizes[i] > longestEdge) {
					longestEdge = sizes[i];
					longestEdgeIndex = i;
				}
			}
			int smallestArea = Integer.MAX_VALUE;
			for (int i = 0; i < 3; i++) {
				int area = sizes[(i + 1) % 3] * sizes[(i + 2) % 3];
				if (area < smallestArea)
					smallestArea = area;
				totalPaper += 2 * area;
				if (i != longestEdgeIndex)
					totalRibbon += 2 * sizes[i];
			}
			totalRibbon += sizes[0] * sizes[1] * sizes[2];
			totalPaper += smallestArea;
		}
		sc.close();
		System.out.println(totalPaper);
		System.out.println(totalRibbon);
	}

}
