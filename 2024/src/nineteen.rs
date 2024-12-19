use std::io;

pub fn parse_input() -> (Vec<String>, impl Iterator<Item=String>) {
    let mut line_iter = io::stdin().lines();
    let towels = line_iter
        .next()
        .unwrap()
        .unwrap()
        .split(", ")
        .map(str::to_string)
        .collect();
    assert!(line_iter.next().unwrap().unwrap().is_empty());
    (towels, line_iter.map(Result::unwrap))
}