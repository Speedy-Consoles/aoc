use std::{
    cmp::{
        PartialOrd,
        Ordering,
    },
    io::BufRead,
};
use itertools::Itertools;
use aoc_tools;

type Vector = aoc_tools::Vector<i64, 2>;

fn parse_input(input: Box<dyn BufRead>) -> Vec<Vector> {
    input.lines().map(|line|
        line.unwrap().split(',').map(|s| s.parse().unwrap()).collect_array().unwrap().into()
    ).collect()
}

fn solve(red_tile_positions: &Vec<Vector>, filter: impl Fn((&Vector, &Vector)) -> bool) -> String {
    let solution = red_tile_positions.iter().tuple_combinations().filter_map(|(&u, &v)| {
        filter((&u, &v)).then(|| {
            let side_lengths = u.abs_diff(&v) + aoc_tools::Vector::<u64, 2>::new(1, 1);
            side_lengths[0] * side_lengths[1]
        })
    }).max().unwrap();
    format!("{solution}")
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let red_tile_positions = parse_input(input);
    solve(&red_tile_positions, |_| true)
}

fn compare_value_to_range<T: PartialOrd>(value: T, start: T, stop: T) -> Ordering {
    if value < start {
        Ordering::Less
    } else if value < stop {
        Ordering::Equal
    } else {
        Ordering::Greater
    }
}

struct Square {
    start: Vector,
    stop: Vector,
}

impl Square {
    fn get_sector(&self, position: &Vector) -> u8 {
        let cmp_0 = compare_value_to_range(position[0], self.start[0], self.stop[0]);
        let cmp_1 = compare_value_to_range(position[1], self.start[1], self.stop[1]);
        match (cmp_0, cmp_1) {
            (Ordering::Less, Ordering::Less) => 0,
            (Ordering::Less, Ordering::Equal) => 7,
            (Ordering::Less, Ordering::Greater) => 6,
            (Ordering::Equal, Ordering::Less) => 1,
            (Ordering::Equal, Ordering::Equal) => 8,
            (Ordering::Equal, Ordering::Greater) => 5,
            (Ordering::Greater, Ordering::Less) => 2,
            (Ordering::Greater, Ordering::Equal) => 3,
            (Ordering::Greater, Ordering::Greater) => 4,
        }
    }
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    let red_tile_positions = parse_input(input);

    // Assuming that the boundary does not touch itself
    solve(&red_tile_positions, |(&u, &v)| {
        let start = Vector::new(u[0].min(v[0]), u[1].min(v[1])) + Vector::new(1, 1);
        let stop = Vector::new(u[0].max(v[0]), u[1].max(v[1]));
        let square = Square { start, stop };
        let mut sector_diff = 0;
        let mut prev_sector = square.get_sector(&red_tile_positions[red_tile_positions.len() - 1]);
        for position in red_tile_positions.iter() {
            let sector = square.get_sector(position);
            if sector == 8 {
                return false;
            }
            let diff = sector as i8 - prev_sector as i8;
            let short_diff = if diff > 4 {
                diff - 8
            } else if diff < -4 {
                diff + 8
            } else {
                diff
            };
            if short_diff.abs() > 2 {
                return false;
            }
            sector_diff += short_diff;
            prev_sector = sector;
        }
        if sector_diff == 0 {
            return false;
        }
        true
    })
}
