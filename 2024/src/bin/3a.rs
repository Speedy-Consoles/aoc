use std::io::{
    self,
    Read,
};

use regex::Regex;

fn main() {
    let re = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();

    let mut program = String::new();
    io::stdin().read_to_string(&mut program).unwrap();
    
    let result = re.captures_iter(&program)
        .map(|c|
             c.iter()
                .skip(1)
                .map(|s| s.unwrap().as_str().parse::<i32>().unwrap())
                .product::<i32>())
        .sum::<i32>();
    println!("{result}");
}