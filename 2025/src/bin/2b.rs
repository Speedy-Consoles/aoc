use std::io::{
    self,
    Read,
};

fn main() {
    let mut line = String::new();
    io::stdin().read_to_string(&mut line).unwrap();
    let mut sum = 0;
    for range_string in line.trim().split(",") {
        let [start, end] = range_string
            .split('-')
            .map(|id_string| id_string.parse::<i64>().unwrap())
            .collect::<Vec<_>>()
            .try_into()
            .unwrap();
        for id in start..end + 1 {
            let id_string = id.to_string();
            for n in 1..id_string.len() / 2 + 1 {
                if id_string.len() % n == 0 && id_string == id_string[..n].repeat(id_string.len() / n) {
                    sum += id;
                    break;
                }
            }
        }
    }
    println!("{sum}");
}
