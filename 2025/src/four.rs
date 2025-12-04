use std::io::BufRead;

use aoc_tools;

type Grid = aoc_tools::Grid<char>;
type Vector = aoc_tools::Vector<i32, 2>;

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let grid = Grid::from_lines(input.lines().map(Result::unwrap)).unwrap();

    let count = grid.indexed_iter().filter(|&(pos, &c)|
        c == '@' && Vector::DIRECTIONS_8
            .into_iter()
            .filter(|&dir| grid.get(&(pos + dir)).is_some_and(|c2| *c2 == '@'))
            .count() < 4
    ).count();
    format!("{count}")
}


pub fn part_2(input: Box<dyn BufRead>) -> String {
    let mut grid = Grid::from_lines(input.lines().map(Result::unwrap)).unwrap();

    let mut count = 0;
    loop {
        let old_count = count;
        for pos in grid.indices() {
            if grid.get(&pos).is_some_and(|c|
                *c == '@' && Vector::DIRECTIONS_8
                    .into_iter()
                    .filter(|&dir| grid.get(&(pos + dir)).is_some_and(|c2| *c2 == '@'))
                    .count() < 4
            ) {
                grid[pos] = '.';
                count += 1;
            }
        }
        if old_count == count {
            break;
        }
    }
    format!("{count}")
}
