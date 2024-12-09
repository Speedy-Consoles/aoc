use std::io::{
    self,
    Read,
};

pub fn parse_input() -> Vec<usize> {
    let mut line = String::new();
    io::stdin().read_to_string(&mut line).unwrap();
    line.trim()
        .chars()
        .map(|c| c as usize - '0' as usize)
        .collect::<Vec<_>>()
}