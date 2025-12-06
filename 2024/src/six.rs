use std::{
    collections::HashSet,
    io::BufRead,
};

use aoc_tools;

type Grid = aoc_tools::Grid<char>;
type Vector = aoc_tools::Vector<i32, 2>;

pub fn parse_input(mut input: Box<dyn BufRead>) -> (Grid, Vector, usize) {
    let mut grid = Grid::from_buf_read(&mut input).unwrap();

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

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let (grid, start_position, start_direction_index) = parse_input(input);
    let mut path_positions = path_positions(&grid, start_position, start_direction_index);
    path_positions.insert(start_position);
    let result = path_positions.len();
    format!("{result}")
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    let (grid, start_position, start_direction_index) = parse_input(input);

    let result = path_positions(&grid, start_position, start_direction_index).into_iter()
        .filter(|&obstacle| {
            let mut position = start_position;
            let mut direction_index = start_direction_index;
            let mut touched = HashSet::from([(position, direction_index)]);
            loop {
                let next_position = position + Vector::DIRECTIONS_4[direction_index];
                if !grid.in_bounds(&next_position) {
                    break false;
                } else if grid[next_position] == '.' && next_position != obstacle {
                    if touched.contains(&(next_position, direction_index)){
                        break true;
                    } else {
                        position = next_position;
                        touched.insert((position, direction_index));
                    }
                } else {
                    direction_index += 1;
                    direction_index %= 4;
                }
            }
        })
        .count();

    format!("{result}")
}
