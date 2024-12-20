use std::collections::{
    hash_map::Entry,
    HashMap,
};

type Grid = crate::grid::Grid<char>;
type Vector = crate::vector::Vector<i32, 2>;

pub fn solve(max_cheat_length: usize) -> usize {
    let grid = Grid::from_stdin().unwrap();
    let start = grid.find(&'S').unwrap();
    let finish = grid.find(&'E').unwrap();

    let mut position = start;
    let mut distance = 0;
    let mut distances = HashMap::from([(position, distance)]);
    let mut path = vec![start];
    while position != finish {
        for direction in Vector::DIRECTIONS_4 {
            let new_position = position + direction;
            if let Entry::Vacant(entry) = distances.entry(new_position) {
                if let Some('.' | 'E') = grid.get(&new_position) {
                    position = new_position;
                    distance += 1;
                    path.push(position);
                    entry.insert(distance);
                    break;
                }
            }
        }
    }

    path
        .iter()
        .flat_map(|&position| {
            let distance = *distances.get(&position).unwrap();
            let distances = &distances;
            (2..max_cheat_length as i32 + 1).flat_map(move |cheat_length|
                Vector::DIRECTIONS_4.into_iter().flat_map(move |direction|
                    (0..cheat_length).filter(move |num_off| {
                        let end_pos = position + direction * (cheat_length - num_off)
                            + direction.rotated_ccw() * num_off;
                        distances.get(&end_pos).is_some_and(|other_distance|
                            distance - other_distance - cheat_length >= 100
                        )
                    })
                )
            )
        })
        .count()
}
