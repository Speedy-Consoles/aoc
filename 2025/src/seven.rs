use std::{
    collections::HashMap,
    io::BufRead,
};

fn solve(input: Box<dyn BufRead>) -> (u64, u64) {
    let mut rays = HashMap::new();
    let mut num_splits = 0;
    for line in input.lines().map(Result::unwrap) {
        for (i, c) in (0..).zip(line.chars()) {
            match c {
                '.' => (),
                'S' => {
                    rays.insert(i, 1);
                },
                '^' => {
                    if let Some(num_timelines) = rays.remove(&i) {
                        num_splits += 1;
                        assert!(i > 0);
                        for offset in [-1, 1] {
                            *rays.entry((i as i64 + offset) as u64).or_insert(0) += num_timelines;
                        }
                    }
                },
                x => panic!("unexpected character {x}"),
            }
        }
    }
    (num_splits, rays.values().sum::<u64>())
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    solve(input).0.to_string()
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    solve(input).1.to_string()
}
