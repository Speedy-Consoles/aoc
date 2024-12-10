use std::{
    fmt::{
        self,
        Debug,
        Display,
    },
    io,
    ops::{
        Index,
        IndexMut,
    },
};

type Vector =  crate::vector::Vector<i32, 2>;

pub struct Grid<T> {
    cells: Vec<T>,
    width: usize,
    height: usize,
}

impl<T> Grid<T> {
    pub fn width(&self) -> usize {
        self.width
    }

    pub fn height(&self) -> usize {
        self.height
    }

    pub fn iter(&self) -> impl Iterator<Item=&T> {
        self.cells.iter()
    }

    pub fn indexed_iter(&self) -> impl Iterator<Item=(Vector, &T)> {
        (0..self.height())
            .flat_map(|y| (0..self.width()).map(move |x| (x, y)))
            .enumerate()
            .map(|(i, (x, y))| (Vector::new(x as i32, y as i32), &self.cells[i]))
    }

    pub fn indices(&self) -> impl Iterator<Item=Vector> {
        let width = self.width;
        let height = self.height;
        (0..height).flat_map(move |y|
            (0..width).map(move |x| Vector::new(x as i32, y as i32)
        ))
    }

    pub fn in_bounds(&self, position: &Vector) -> bool {
        position.in_bounds(&Vector::new(self.width() as i32, self.height() as i32))
    }
}

#[derive(Debug)]
pub enum ParseGridError<E: Debug> {
    LineLengthsInconsistent {
        line_index: usize,
        expected_line_len: usize
    },
    ParseElementError{
        line_index: usize,
        column_index: usize,
        error: E,
    }
}

impl<E: Display + Debug> Display for ParseGridError<E> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ParseGridError::LineLengthsInconsistent { line_index, expected_line_len } => {
                write!(f, "line {} is longer than the previous lines, which have {} characters", line_index, expected_line_len)?;
            },
            ParseGridError::ParseElementError{ line_index, column_index, error } => {
                write!(f, "error parsing character in line {}, column {}: {}", line_index, column_index, error)?;
            }
        }
        Ok(())
    }
}

#[derive(Debug)]
pub struct ParseU8Error(char);

impl Display for ParseU8Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{} is not a digit", self.0)
    }
}

fn from_stdin<T, F, E: Debug>(f: F) -> Result<Grid<T>, ParseGridError<E>>
where
    F: Fn(char) -> Result<T, E>,
{
    let mut lines = io::stdin().lines().map(Result::unwrap).peekable();
    let width = lines.peek().unwrap().len();
    let mut height = 0;
    let mut cells = Vec::new();
    for line in lines {
        for (x, c) in line.chars().enumerate() {
            if x >= width {
                return Err(ParseGridError::LineLengthsInconsistent {
                    line_index: height,
                    expected_line_len: width,
                });
            };
            let element = f(c)
                .map_err(|e| ParseGridError::ParseElementError{
                    line_index: height,
                    column_index: x,
                    error: e
                })?;
            cells.push(element);
        }
        height += 1;
    }
    Ok(Grid {
        cells,
        width,
        height,
    })
}

impl Grid<u8> {
    pub fn from_stdin() -> Result<Self, ParseGridError<ParseU8Error>> {
        from_stdin(|c| {
            if !c.is_numeric() {
                Err(ParseU8Error(c))
            } else {
                Ok(c as u8 - '0' as u8)
            }
        })
    }
}

impl Grid<char> {
    pub fn from_stdin() -> Result<Self, ParseGridError<()>> {
        from_stdin(|c| Ok(c))
    }
}

impl<T> Index<Vector> for Grid<T> {
    type Output = T;

    fn index(&self, index: Vector) -> &Self::Output {
        &self.cells[index[1] as usize * self.width + index[0] as usize]
    }
}

impl<T> IndexMut<Vector> for Grid<T> {
    fn index_mut(&mut self, index: Vector) -> &mut Self::Output {
        &mut self.cells[index[1] as usize * self.width + index[0] as usize]
    }
}