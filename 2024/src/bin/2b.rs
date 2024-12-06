use std::io;

use itertools::Itertools;

fn main() {
    let diff_funcs = [
        |a, b| b - a,
        |a, b| a - b,
    ];
    println!(
        "{}",
        io::stdin().lines()
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
            }
            ).count()
    );
}
