use std::{
    collections::HashMap,
    io::BufRead,
};

use aoc_tools::Grid;

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let mut numbers: HashMap<(usize, usize), u64> = HashMap::new();
    for (i, line) in input.lines().map(Result::unwrap).enumerate() {
        if line.chars().next().unwrap().is_digit(10) {
            numbers.extend(
                line
                    .split_whitespace()
                    .enumerate()
                    .map(|(j, s)| ((i, j), s.parse::<u64>().unwrap()))
            );
        } else {
            let solution = line
                .split_whitespace()
                .enumerate()
                .map(|(i, op)| {
                    let numbers = numbers
                        .iter()
                        .filter(|&(&(_, k), _)| i == k)
                        .map(|((_, _), number)| number);
                    match op {
                        "+" => numbers.sum::<u64>(),
                        "*" => numbers.product(),
                        x => panic!("invalid operator {x}"),
                    }
                })
                .sum::<u64>();
            return format!("{solution}");
        }
    }
    panic!("no operator line found")
}

pub fn part_2(mut input: Box<dyn BufRead>) -> String {
    let mut grid: Grid<char> = Grid::from_buf_read(&mut input).unwrap();
    grid.transpose();
    grid.flip_vertically();
    let mut solution = 0;
    let mut numbers = Vec::new();
    for row in grid.rows() {
        let mut number = None;
        let mut operator = None;
        for c in row {
            match c {
                '0'..='9' => {
                    let number = number.get_or_insert(0);
                    *number = *number * 10 + c.to_digit(10).unwrap();
                },
                op @ '+' | op @ '*' => {
                    operator = Some(op);
                },
                ' ' => (),
                _ => panic!("unexpected character"),
            }
        }

        if let Some(number) = number {
            numbers.push(number as u64);
        }

        if let Some(operator) = operator {
            solution += match operator {
                '+' => numbers.iter().sum::<u64>(),
                '*' => numbers.iter().product::<u64>(),
                _ => unreachable!(),
            };
            numbers.clear();
        }
    }
    format!("{solution}")
}
