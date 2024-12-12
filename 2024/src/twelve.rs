use std::collections::HashSet;

type Grid = crate::grid::Grid<char>;
type Vector = crate::vector::Vector<i32, 2>;

pub fn solve<const COMBINE_STRAIGHTS: bool>() -> usize {
    let mut visited = HashSet::new();
    let plots = Grid::from_stdin().unwrap();
    plots.indexed_iter().filter_map(|(start_pos, plant)| {
        if visited.contains(&start_pos) {
            return None
        }

        let mut perimeter = 0;
        let mut area = 0;
        visited.insert(start_pos);
        let mut fringe = vec![start_pos];

        while let Some(pos) = fringe.pop() {
            area += 1;
            for direction in Vector::DIRECTIONS_4 {
                let other_pos = pos + direction;
                if plots.get(&other_pos) == Some(plant) {
                    if !visited.contains(&other_pos) {
                        fringe.push(other_pos);
                        visited.insert(other_pos);
                    }
                } else if COMBINE_STRAIGHTS {
                    let direction_rotated = direction.rotated_ccw();
                    let neighbor = pos + direction_rotated;
                    let diagonal = neighbor + direction;
                    let neighbor_matches = plots.get(&neighbor) == Some(plant);
                    if !neighbor_matches || neighbor_matches && plots.get(&diagonal) == Some(plant) {
                        perimeter += 1;
                    }
                } else {
                    perimeter += 1;
                }
            }
        }

        Some(area * perimeter)
    }).sum::<usize>()
}
