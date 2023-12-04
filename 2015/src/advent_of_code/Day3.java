package advent_of_code;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Scanner;

public class Day3 {

	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		String s = sc.next();
		sc.close();
		MessageDigest md = null;
		try {
			md = MessageDigest.getInstance("MD5");
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		}
		//		byte[] bytes = Arrays.copyOf(s.getBytes(), 16);
		int number = 0;
		while (true) {
			byte[] md5 = md.digest((s + Integer.toString(number)).getBytes());
			if (md5[0] == 0 && md5[1] == 0 && md5[2] == 0) {// (md5[2] & 0xF0) == 0) {
				System.out.println("Number: " + number);
				System.out.println("Hash: " + bytesToHex(md5));
				System.exit(0);
			}
			number++;
		}
	}

	final protected static char[] hexArray = "0123456789ABCDEF".toCharArray();

	public static String bytesToHex(byte[] bytes) {
		char[] hexChars = new char[bytes.length * 2];
		for (int j = 0; j < bytes.length; j++) {
			int v = bytes[j] & 0xFF;
			hexChars[j * 2] = hexArray[v >>> 4];
			hexChars[j * 2 + 1] = hexArray[v & 0x0F];
		}
		return new String(hexChars);
	}
}