use std::{
    collections::HashSet,
    io::{
        self,
        Read,
    },
};

use aoc_tools;

type Grid = aoc_tools::Grid<char>;
type Vector = aoc_tools::Vector<i32, 2>;

pub fn solve<F, I>(field_mapper: F) -> i32
where
    F: Fn(char) -> I,
    I: Iterator<Item=char>,
{
    let mut s = String::new();
    io::stdin().read_to_string(&mut s).unwrap();
    let [warehouse_string, program_string] = s.split("\n\n")
        .collect::<Vec<_>>()
        .try_into()
        .unwrap();

    let field_mapper = &field_mapper;
    let mut grid = Grid::from_line_iterators(warehouse_string.lines().map(|line|
        line.chars().flat_map(field_mapper)
    )).unwrap();
    let mut position = grid.indexed_iter()
        .find_map(|(position, &c)| (c == '@').then_some(position))
        .unwrap();
    for direction_char in program_string.chars().filter(|&c| c != '\n') {
        let direction = match direction_char {
            '>' => Vector::new( 1,  0),
            '^' => Vector::new( 0, -1),
            '<' => Vector::new(-1,  0),
            'v' => Vector::new( 0,  1),
            _ => panic!("unexpected direction character"),
        };
        let mut to_move = vec![position];
        let mut found = HashSet::from([position]);
        let mut index = 0;
        let possible = loop {
            if index >= to_move.len() {
                break true;
            }
            let src = to_move[index];
            let dst = src + direction;
            if !grid.in_bounds(&dst) {
                break false;
            }
            let dst_object = grid[dst];
            match dst_object {
                '#' => break false,
                '.' => (),
                'O' | '[' | ']' => {
                    if !found.contains(&dst) {
                        to_move.push(dst);
                        found.insert(dst);
                        if dst_object != 'O' && ['^', 'v'].contains(&direction_char) {
                            let sign = match dst_object {
                                '[' => 1,
                                ']' => -1,
                                _ => unreachable!(),
                            };
                            let other = dst + Vector::new(sign, 0);
                            to_move.push(other);
                            found.insert(other);
                        }
                    }
                },
                o => panic!("unexpected object {}", o),
            }
            index += 1;
        };
        if possible {
            for &src in to_move.iter().rev() {
                grid[src + direction] = grid[src];
                grid[src] = '.';
            }
            position += direction;
        }
        // println!("{}", grid);
    }

    grid.indexed_iter()
        .filter_map(|(pos, &object)| ['[', 'O'].contains(&object).then(|| pos[0] + pos[1] * 100))
        .sum()
}
