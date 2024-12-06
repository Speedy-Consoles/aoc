use std::cmp::Ordering;

use lib::five::*;

fn main() {
    let (rules, updates) = parse_input();

    let rule_map = compute_rule_map(rules);

    let result = updates.iter()
        .map(|update| {
            let mut corrected_update = update.clone();
            corrected_update.sort_by(|a, b|
                if rule_map.get(b).is_some_and(|earliers| earliers.contains(a)) {
                    Ordering::Less
                } else if rule_map.get(a).is_some_and(|earliers| earliers.contains(b)) {
                    Ordering::Greater
                } else {
                    Ordering::Equal
                }
            );
            if *update != corrected_update {
                corrected_update[corrected_update.len() / 2]
            } else {
                0
            }
        })
        .sum::<u32>();
    println!("{result}");
}