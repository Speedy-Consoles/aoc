type Vector = lib::vector::Vector<i32, 2>;
type Grid = lib::grid::Grid<char>;

const WORD: [char; 4] = ['X', 'M', 'A', 'S'];

fn main() {
    let grid = Grid::from_stdin().unwrap();

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

    println!("{result}");
}