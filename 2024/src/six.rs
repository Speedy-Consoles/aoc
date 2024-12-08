use std::collections::HashSet;

type Grid = crate::grid::Grid<char>;
type Vector = crate::vector::Vector<i32, 2>;

pub const DIRECTIONS: [Vector; 4] = [
    Vector::new(1, 0),
    Vector::new(0, 1),
    Vector::new(-1, 0),
    Vector::new(0, -1),
];

pub fn parse_input() -> (Grid, Vector, usize) {
    let mut grid = Grid::from_stdin();

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
        let next_position = position + DIRECTIONS[direction_index];
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