use lib::eighteen::*;

use aoc_tools;

type Grid = aoc_tools::BoundedSparseGrid<char>;

fn main() {
    let mut grid = Grid::new(71, 71);
    for position in parse_input() {
        grid.insert(position, '#');
        if find_path(&grid).is_none() {
            println!("{},{}", position[0], position[1]);
            break;
        }
    }
}
