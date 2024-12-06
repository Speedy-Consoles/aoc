use std::collections::HashSet;

use lib::six::*;

fn main() {
    let (grid, start_position, start_direction_index) = parse_input();

    let result = path_positions(&grid, start_position, start_direction_index).into_iter()
        .filter(|&obstacle| {
            let mut position = start_position;
            let mut direction_index = start_direction_index;
            let mut touched = HashSet::from([(position, direction_index)]);
            loop {
                let next_position = position + DIRECTIONS[direction_index];
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

    println!("{result}");
}