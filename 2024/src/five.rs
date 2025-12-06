use std::{
    cmp::Ordering,
    collections::{
        HashMap,
        HashSet,
    },
    io::BufRead,
};

pub fn parse_input(mut input: Box<dyn BufRead>) -> (Vec<(u32, u32)>, Vec<Vec<u32>>) {
    let mut s = String::new();
    input.read_to_string(&mut s).unwrap();
    let [order_strings, rule_strings] = s.trim().split("\n\n")
        .map(|s| s.split('\n'))
        .collect::<Vec<_>>()
        .try_into()
        .unwrap();
    let rules = order_strings.map(|s|
        <[u32; 2]>::try_from(
        s.split('|')
            .map(|s| s.parse().unwrap())
            .collect::<Vec<_>>())
            .unwrap()
            .into()
        ).collect();
    let updates = rule_strings.map(|s|
        s.split(',').map(|s| s.parse().unwrap()).collect()
    ).collect();

    (rules, updates)
}

pub fn compute_rule_map(orders: Vec<(u32, u32)>) -> HashMap<u32, Vec<u32>> {
    let mut rule_map: HashMap<u32, Vec<u32>> = HashMap::new();
    for (first, second) in orders {
        rule_map.entry(second).or_default().push(first);
    }
    rule_map
}

pub fn part_1(input: Box<dyn BufRead>) -> String {
    let (rules, updates) = parse_input(input);

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
    format!("{result}")
}

pub fn part_2(input: Box<dyn BufRead>) -> String {
    let (rules, updates) = parse_input(input);

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
    format!("{result}")
}
