use std::io::BufRead;
use aoc_tools;

type Vector = aoc_tools::Vector<i32, 2>;
type Grid = aoc_tools::Grid<char>;

const WORD: [char; 4] = ['X', 'M', 'A', 'S'];

pub fn part_1(mut input: Box<dyn BufRead>) -> String {
    let grid = Grid::from_buf_read(&mut input).unwrap();

    let grid = &grid;
    let result = (0..grid.width()).flat_map(|x|
        (0..grid.height()).flat_map(move |y|
            Vector::DIRECTIONS_8.into_iter().filter(move |&direction|
                WORD.iter().enumerate().all(|(i, &c)| {
                    let pos = Vector::new(x as i32, y as i32) + direction * i as i32;
                    grid.in_bounds(&pos) && grid[pos] == c
                })
            )
        )
    ).count();

    format!("{result}")
}

const OFFSETS: [[Vector; 2]; 2] = [
    [
        Vector::new(1, 1),
        Vector::new(-1, -1),
    ],[
        Vector::new(-1, 1),
        Vector::new(1, -1),
    ],
];

pub fn part_2(mut input: Box<dyn BufRead>) -> String {
    let grid = Grid::from_buf_read(&mut input).unwrap();

    let grid = &grid;
    let result = (1..grid.width() - 1).flat_map(|x|
        (1..grid.height() - 1).filter(move |&y| {
            let base = Vector::new(x as i32, y as i32);
            grid[Vector::new(x as i32, y as i32)] == 'A'
                && OFFSETS.iter().all(|&directions|
                    directions.iter().map(|&direction| {
                        match grid[base + direction] {
                            'M' => 1,
                            'S' => 2,
                            _ => 0,
                        }
                    }).sum::<u8>() == 3
                )
        })
    ).count();

    format!("{result}")
}
