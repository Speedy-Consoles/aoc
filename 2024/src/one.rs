use std::io::BufRead;

use itertools::Itertools;

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let (mut a, mut b): (Vec<_>, Vec<_>) = input.lines()
        .map(|r| r.unwrap().split_whitespace().map(|s| s.parse::<i32>().unwrap()).collect_tuple::<(_, _)>().unwrap())
        .unzip();

    a.sort();
    b.sort();

    let result: i32 = a.into_iter().zip(b)
        .map(|(a, b)| (a - b).abs())
        .sum();
    format!("{result}")
}
