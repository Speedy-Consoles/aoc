use std::iter;

use lib::nine::*;

fn main() {
    let memory = parse_input();

    let num_blocks: usize = memory.iter()
        .copied()
        .step_by(2)
        .map(usize::from)
        .sum::<usize>();

    let mut src = memory.iter()
        .enumerate()
        .rev()
        .filter_map(|(i, &n)|
            (i % 2 == 0).then_some(
                iter::repeat(i / 2)
                    .take(n)
            )
        ).flatten();

    let dst = memory.iter()
        .enumerate()
        .flat_map(|(i, &n)|
            iter::repeat(
                (i % 2 == 0).then_some(i / 2)
            ).take(n)
        );

    let result = dst.take(num_blocks)
        .enumerate()
        .map(|(i, id)| id.unwrap_or_else(|| src.next().unwrap()) * i)
        .sum::<usize>();

    println!("{result}");
}
