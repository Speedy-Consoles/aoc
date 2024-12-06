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
    );
}
