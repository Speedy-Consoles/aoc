use std::{
    collections::HashSet,
    io::BufRead,
};

use aoc_tools;

type Grid = aoc_tools::Grid<u8>;
type Vector = aoc_tools::Vector<i32, 2>;

pub trait TrailAccumulator {
    fn new() -> Self;
    fn insert(&mut self, tail_position: Vector);
    fn len(&self) -> usize;
}

impl TrailAccumulator for HashSet<Vector> {
    fn new() -> Self {
        HashSet::new()
    }

    fn insert(&mut self, tail_position: Vector) {
        HashSet::insert(self, tail_position);
    }

    fn len(&self) -> usize {
        self.len()
    }
}

impl TrailAccumulator for usize {
    fn new() -> Self {
        0
    }

    fn insert(&mut self, _tail_position: Vector) {
        *self += 1;
    }

    fn len(&self) -> usize {
        *self
    }
}

pub fn solve<T: TrailAccumulator>(mut input: Box<dyn BufRead>) -> usize {
    let grid = Grid::from_buf_read(&mut input).unwrap();

    return grid.indices().filter_map(|start_pos| {
        if grid[start_pos] != 0 {
            return None;
        }
        let mut fringe = vec![start_pos];
        let mut tails = T::new();
        while let Some(pos) = fringe.pop() {
            let current_height = grid[pos];
            if current_height == 9 {
                tails.insert(pos);
            } else {
                for direction in Vector::DIRECTIONS_4 {
                    let next_pos = pos + direction;
                    if grid.in_bounds(&next_pos) && grid[next_pos] == current_height + 1 {
                        fringe.push(next_pos);
                    }
                }
            }
        }
        Some(tails.len())
    }).sum::<usize>();
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let result = solve::<HashSet<Vector>>(input);
    format!("{result}")
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    let result = solve::<usize>(input);
    format!("{result}")
}
