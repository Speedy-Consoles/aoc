use std::io;

fn main() {
    let mut position = 50;
    let mut count = 0;
    for line in io::stdin().lines().map(Result::unwrap) {
        let mut char_iter = line.chars();
        let dir = char_iter.next().unwrap();
        let sign = (dir == 'R') as i32 - (dir == 'L') as i32;
        let amount = char_iter.as_str().parse::<i32>().unwrap();
        position = (position + sign * amount) % 100;
        if position == 0 {
            count += 1;
        }
    }
    println!("{count}");
}
