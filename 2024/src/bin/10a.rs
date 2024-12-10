use std::collections::HashSet;

use lib::ten::*;

type Vector = lib::vector::Vector<i32, 2>;

fn main() {
    let result = solve::<HashSet<Vector>>();
    println!("{result}");
}
