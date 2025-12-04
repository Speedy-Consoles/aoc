use std::io::BufRead;

fn solve(input: Box<dyn BufRead>, length: usize) -> u64 {
    input.lines().map(|line_result|
        line_result
            .unwrap()
            .chars()
            .map(|c| c.to_digit(10).unwrap())
            .fold(vec![0; length + 1], |mut accu, new| {
                accu[0] = new;
                if let Some(end) = (1..length + 1).rfind(|&i| accu[i - 1] > accu[i])
                {
                    accu[0..end + 1].rotate_right(1); // That's a rotate!
                }
                accu
            })[1..]
            .iter()
            .enumerate()
            .map(|(i, &x)| 10u64.pow(i as u32) * x as u64)
            .sum::<u64>()
    ).sum()
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let solution = solve(input, 2);
    format!("{solution}")
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    let solution = solve(input, 12);
    format!("{solution}")
}
