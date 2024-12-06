use std::collections::HashSet;

use lib::five::*;

fn main() {
    let (rules, updates) = parse_input();

    let rule_map = compute_rule_map(rules);

    let result = updates.iter().map(|update| {
        let mut forbidden = HashSet::new();
        for page in update.iter() {
            if forbidden.contains(page) {
                return 0;
            }
            forbidden.extend(rule_map.get(page).iter().flat_map(|v| v.iter().copied()));
        }
        update[update.len() / 2]
    }).sum::<u32>();
    println!("{result}");
}