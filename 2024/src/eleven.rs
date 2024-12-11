use std::{
    collections::HashMap,
    io::{
        self,
        Read,
    },
};

fn count_children(number: u64, num_blinks: usize, cache: &mut HashMap<(u64, usize), usize>) -> usize {
    if num_blinks == 0 {
        return 1;
    }
    if let Some(&num_children) = cache.get(&(number, num_blinks)) {
        return num_children;
    }

    let mut count_children = |number| count_children(number, num_blinks - 1, cache);

    let num_children = if number == 0 {
        count_children(1)
    } else {
        let mut power = 10;
        let mut half_power = 10;
        loop {
            if number < power {
                break count_children(number * 2024);
            }
            power *= 10;
            if number < power {
                break count_children(number % half_power)
                    + count_children(number / half_power);
            }
            power *= 10;
            half_power *= 10;
        }
    };

    cache.insert((number, num_blinks), num_children);
    return num_children;
}

pub fn solve(num_blinks: usize) -> usize {
    let mut s = String::new();
    let mut cache = HashMap::new();
    io::stdin().read_to_string(&mut s).unwrap();
    s.split_whitespace()
        .map(str::parse)
        .map(Result::unwrap)
        .map(|number| count_children(number, num_blinks, &mut cache))
        .sum()
}
