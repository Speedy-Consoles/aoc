use lib::six::*;

fn main() {
    let (grid, start_position, start_direction_index) = parse_input();
    let mut path_positions = path_positions(&grid, start_position, start_direction_index);
    path_positions.insert(start_position);
    let result = path_positions.len();
    println!("{result}");
}