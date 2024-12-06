use std::io::{
    self,
    Read,
};

use regex::Regex;

fn main() {
    let re = Regex::new(r"(do\(\))|(don't\(\))|(mul\((\d{1,3}),(\d{1,3})\))").unwrap();

    let mut program = String::new();
    io::stdin().read_to_string(&mut program).unwrap();
    
    let mut result = 0;
    let mut enabled = true;
    for captures in re.captures_iter(&program) {
        if captures.get(1).is_some() {
            enabled = true;
        } else if captures.get(2).is_some() {
            enabled = false;
        } else if enabled && captures.get(3).is_some() {
            result += (4..6)
                .map(|i| captures.get(i).unwrap().as_str().parse::<i32>().unwrap())
                .product::<i32>()
        }
    }
    println!("{result}");
}