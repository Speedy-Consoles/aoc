use std::collections::HashSet;

use aoc_tools;

type Grid = aoc_tools::Grid<char>;
type Vector = aoc_tools::Vector<i32, 2>;

pub fn parse_input() -> (Grid, Vector, usize) {
    let mut grid = Grid::from_stdin().unwrap();

    let position = grid.indexed_iter().find(|(_, &c)| c == '^').unwrap().0;
    let direction_index = 3;
    grid[position] = '.';
    (grid, position, direction_index)
}

pub fn path_positions(
    grid: &Grid,
    start_position: Vector,
    start_direction_index: usize
) -> HashSet<Vector> {
    let mut position = start_position;
    let mut direction_index = start_direction_index;
    let mut touched = HashSet::new();
    loop {
        let next_position = position + Vector::DIRECTIONS_4[direction_index];
        if !grid.in_bounds(&next_position) {
            break;
        } else if grid[next_position] == '.' {
            position = next_position;
            touched.insert(position);
        } else {
            direction_index += 1;
            direction_index %= 4;
        }
    }
    touched
}
