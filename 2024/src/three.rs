use std::io::BufRead;
use regex::Regex;

pub fn part_1(mut input: Box<dyn BufRead>) -> String {
    let re = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();

    let mut program = String::new();
    input.read_to_string(&mut program).unwrap();

    let result = re.captures_iter(&program)
        .map(|c|
             c.iter()
                .skip(1)
                .map(|s| s.unwrap().as_str().parse::<i32>().unwrap())
                .product::<i32>())
        .sum::<i32>();
    format!("{result}")
}

pub fn part_2(mut input: Box<dyn BufRead>) -> String {
    let re = Regex::new(r"(do\(\))|(don't\(\))|(mul\((\d{1,3}),(\d{1,3})\))").unwrap();

    let mut program = String::new();
    input.read_to_string(&mut program).unwrap();

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
    format!("{result}")
}
