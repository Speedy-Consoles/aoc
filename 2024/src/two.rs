use std::io::BufRead;

use itertools::Itertools;

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let diff_funcs = [
        |a, b| b - a,
        |a, b| a - b,
    ];
    format!(
        "{}",
        input.lines()
            .filter(|r|
                diff_funcs.iter()
                    .any(|f|
                        r.as_ref().unwrap()
                            .split_whitespace()
                            .map(|s| s.parse::<i32>().unwrap())
                            .tuple_windows::<(i32, i32)>()
                            .all(|(a, b)| (1..4).contains(&f(a, b)))
                    )
            ).count()
    )
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    let diff_funcs = [
        |a, b| b - a,
        |a, b| a - b,
    ];
    format!(
        "{}",
        input.lines()
            .filter(|r| {
                let numbers = r.as_ref().unwrap()
                    .split_whitespace()
                    .map(|s| s.parse::<i32>().unwrap())
                    .collect::<Vec<_>>();
                diff_funcs.iter()
                    .any(|f|
                        (0..numbers.len()).any(|i|
                            numbers
                                .iter()
                                .enumerate()
                                .filter_map(|(j, n)| (j != i).then_some(*n))
                                .tuple_windows::<(i32, i32)>()
                                .all(|(a, b)| (1..4).contains(&f(a, b)))
                        )
                    )
            }).count()
    )
}
