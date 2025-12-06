use std::{
    collections::HashMap,
    io::BufRead,
};
use itertools::Itertools;

const MASK: u64 = (1 << 24) - 1;

pub struct SecretSequence {
    secret: u64,
}

impl SecretSequence {
    pub fn new(secret: u64) -> Self {
        Self { secret }
    }
}

impl Iterator for SecretSequence {
    type Item = u64;

    fn next(&mut self) -> Option<Self::Item> {
        let old_secret = self.secret;
        self.secret = ((self.secret <<  6) ^ self.secret) & MASK;
        self.secret = ((self.secret >>  5) ^ self.secret) & MASK;
        self.secret = ((self.secret << 11) ^ self.secret) & MASK;
        Some(old_secret)
    }
}

pub fn get_secret_sequences(input: Box<dyn BufRead>) -> impl Iterator<Item=impl Iterator<Item=u64>> {
    input.lines().map(|line| SecretSequence { secret: line.unwrap().parse().unwrap() })
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let result = get_secret_sequences(input)
        .map(|mut iter| iter.nth(2000).unwrap())
        .sum::<u64>();

    format!("{result}")
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    let buyers = get_secret_sequences(input)
        .map(|iter| {
            let price_diffs = iter
                .map(|secret| secret % 10)
                .take(2001)
                .tuple_windows()
                .map(|(a, b)| (b as i32 - a as i32, b))
                .tuple_windows()
                .map(|((a, _), (b, _), (c, _), (d, price))| ((a, b, c, d), price));
            let mut price_diff_sequences = HashMap::new();
            for (price_diff_sequence, price) in price_diffs {
                price_diff_sequences.entry(price_diff_sequence).or_insert(price);
            }
            price_diff_sequences
        })
        .collect::<Vec<_>>();

    let result = itertools::iproduct!((-9..10), (-9..10), (-9..10), (-9..10))
        .map(|price_diff_sequence|
            buyers.iter()
                .map(|price_diff_sequences| price_diff_sequences.get(&price_diff_sequence).unwrap_or(&0))
                .sum::<u64>()
        )
        .max()
        .unwrap();

    format!("{result}")
}
