use lib::eighteen::*;

use aoc_tools;

type Grid = aoc_tools::BoundedSparseGrid<char>;

fn main() {
    let mut grid = Grid::new(71, 71);
    for position in parse_input().take(1024) {
        grid.insert(position, '#');
    }

    println!("{}", find_path(&grid).unwrap());
}
