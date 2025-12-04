use std::collections::HashSet;

use lib::ten::*;

use aoc_tools;

type Vector = aoc_tools::Vector<i32, 2>;

fn main() {
    let result = solve::<HashSet<Vector>>();
    println!("{result}");
}
