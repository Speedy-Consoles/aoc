use std::collections::HashMap;

use itertools::Itertools;

use lib::twentytwo::*;

fn main() {
    let buyers = get_secret_sequences()
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

    println!("{result}");
}
