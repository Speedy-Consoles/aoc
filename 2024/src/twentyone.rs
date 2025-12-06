use std::{
    sync::LazyLock,
    collections::HashMap,
    io::BufRead,
    iter,
    ptr,
};

use itertools::Itertools;

use aoc_tools;

type Vector = aoc_tools::Vector<i32, 2>;

struct Keypad {
    index_button_positions: Vec<Vector>,
    apply_button_position: Vector,
    empty_position: Vector,
}

static NUMERIC_KEYPAD: LazyLock<Keypad> = LazyLock::new(|| Keypad {
    index_button_positions: vec![
        Vector::new(1, 0),
        Vector::new(0, 1),
        Vector::new(1, 1),
        Vector::new(2, 1),
        Vector::new(0, 2),
        Vector::new(1, 2),
        Vector::new(2, 2),
        Vector::new(0, 3),
        Vector::new(1, 3),
        Vector::new(2, 3),
    ],
    apply_button_position: Vector::new(2, 0),
    empty_position: Vector::new(0, 0),
});

static DIRECTIONAL_KEYPAD: LazyLock<Keypad> = LazyLock::new(|| {
    const INDEX_BUTTON_MAP: [(Vector, Vector); 4] = [
        (Vector::new( 1,  0), Vector::new(2, 0)),
        (Vector::new( 0,  1), Vector::new(1, 1)),
        (Vector::new(-1,  0), Vector::new(0, 0)),
        (Vector::new( 0, -1), Vector::new(1, 0)),
    ];
    Keypad {
        index_button_positions: Vector::DIRECTIONS_4.into_iter().map(|direction|
            INDEX_BUTTON_MAP.into_iter().find_map(|(button_direction, button_position)|
                (button_direction == direction).then_some(button_position)
            ).unwrap()
        ).collect(),
        apply_button_position: Vector::new(2, 1),
        empty_position: Vector::new(0, 1),
    }
});

fn get_paths<'a>(keypad: &'a Keypad, start: Vector, target: Vector) -> impl Iterator<Item=Vec<usize>> + 'a {
    let diff = target - start;
    [0, 1].into_iter()
        .filter_map(move |d| {
            let valid = (
                start[1 - d] != keypad.empty_position[1 - d]
                    || start[d].min(target[d]) > keypad.empty_position[d]
                    || start[d].max(target[d]) < keypad.empty_position[d]
                ) && (
                    target[d] != keypad.empty_position[d]
                    || start[1 - d].min(target[1 - d]) > keypad.empty_position[1 - d]
                    || start[1 - d].max(target[1 - d]) < keypad.empty_position[1 - d]
                );
            (diff[d] != 0 && valid || d == 0 && diff[1] == 0).then(|| {
                [d, 1 - d].into_iter()
                    .flat_map(move |d| 
                        iter::repeat(
                            Vector::DIRECTIONS_4.iter()
                                .enumerate()
                                .find(|(_, v)| v[d] == diff[d].signum())
                                .unwrap()
                                .0
                        ).take(diff[d].abs() as usize)
                    )
                    .collect()
            })
        })
}

fn get_min_num_key_presses(
    keypad: &Keypad,
    indices: &Vec<usize>,
    level: usize,
    caches: &mut Vec<HashMap<Vec<usize>, usize>>,
) -> usize {
    if level == 0 {
        return indices.len() + 1;
    }

    if ptr::eq(keypad, &*DIRECTIONAL_KEYPAD) {
        if let Some(&num_key_presses) = caches[level].get(indices) {
            return num_key_presses;
        }
    }

    let num_key_presses = iter::once(keypad.apply_button_position)
        .chain(indices.iter().map(|&index| keypad.index_button_positions[index]))
        .chain(iter::once(keypad.apply_button_position))
        .tuple_windows()
        .map(|(start, target)|
            get_paths(keypad, start, target)
                .map(|path| get_min_num_key_presses(&DIRECTIONAL_KEYPAD, &path, level - 1, caches))
                .min()
                .unwrap()
        )
        .sum();

    if ptr::eq(keypad, &*DIRECTIONAL_KEYPAD) {
        caches[level].insert(indices.clone(), num_key_presses);
    }

    num_key_presses
}

pub fn solve(input: Box<dyn BufRead>, num_robots: usize) -> usize {
    let mut caches = iter::repeat_with(|| HashMap::new()).take(num_robots).collect::<Vec<_>>();
    input.lines().map(Result::unwrap).map(|line| {
        let mut iter = line.chars();
        iter.next_back();
        let code: Vec<_> = iter.map(|c| c.to_digit(10).unwrap() as usize).collect();
        let factor = code.iter()
            .rev()
            .enumerate()
            .map(|(i, c)| c * 10usize.pow(i as u32))
            .sum::<usize>();
        let num_key_presses = get_min_num_key_presses(&NUMERIC_KEYPAD, &code, num_robots, &mut caches);
        num_key_presses * factor
    })
    .sum::<usize>()
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    format!("{}", solve(input, 3))
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    format!("{}", solve(input, 26))
}
