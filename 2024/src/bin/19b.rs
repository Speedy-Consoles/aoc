use std::collections::HashMap;

use lib::nineteen::*;

fn count_possibilities<'a>(design: &'a str, towels: &[String], cache: &mut HashMap<String, usize>) -> usize {
    if design.is_empty() {
        return 1;
    }
    if let Some(&num_possibilities) = cache.get(design) {
        return num_possibilities;
    };
    let num_possibilities = towels.iter()
        .map(|towel| {
            if design.len() >= towel.len() && design[..towel.len()] == *towel {
                count_possibilities(&design[towel.len()..], towels, cache)
            } else {
                0
            }
        })
        .sum();
    cache.insert(design.to_string(), num_possibilities);
    num_possibilities
}

fn main() {
    let (towels, designs_iter) = parse_input();
    let mut cache = HashMap::new();
    let result = designs_iter
        .map(|design| count_possibilities(&design, &towels[..], &mut cache))
        .sum::<usize>();

    println!("{result}");
}
