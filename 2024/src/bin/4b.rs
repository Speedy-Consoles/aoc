type Vector = lib::vector::Vector<i32, 2>;
type Grid = lib::grid::Grid<char>;

const OFFSETS: [[Vector; 2]; 2] = [
    [
        Vector::new(1, 1),
        Vector::new(-1, -1),
    ],[
        Vector::new(-1, 1),
        Vector::new(1, -1),
    ],
];

fn main() {
    let grid = Grid::from_stdin().unwrap();

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

    println!("{result}");
}