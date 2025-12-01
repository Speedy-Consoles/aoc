use std::io;

fn main() {
    let mut position = 50;
    let mut count = 0;
    for line in io::stdin().lines().map(Result::unwrap) {
        let mut char_iter = line.chars();
        let dir = char_iter.next().unwrap();
        let sign = (dir == 'R') as i32 - (dir == 'L') as i32;
        let amount = char_iter.as_str().parse::<u32>().unwrap();
        if sign < 0 && amount >= position {
            count += (amount - position) / 100 + 1 - (position == 0) as u32;
        } else if sign > 0 && amount + position >= 100 {
            count += (amount + position) / 100;
        }
        position = (position as i32 + (sign * amount as i32)).rem_euclid(100) as u32;
    }
    println!("{count}");
}
