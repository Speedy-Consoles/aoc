use std::{
    fmt::{
        self,
        Debug,
        Display,
    },
    io,
    ops::{
        Deref,
        Index,
        IndexMut,
    },
};

type Vector = crate::vector::Vector<i32, 2>;

#[derive(Debug)]
pub struct ParseU8Error(char);

impl Display for ParseU8Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{} is not a digit", self.0)
    }
}

pub trait TryFromChar: Sized {
    type Error;

    // Required method
    fn try_from_char(value: char) -> Result<Self, Self::Error>;
}

impl TryFromChar for char {
    type Error = ();

    fn try_from_char(value: char) -> Result<Self, Self::Error> {
        Ok(value)
    }
}

impl TryFromChar for u8 {
    type Error = ParseU8Error;

    fn try_from_char(value: char) -> Result<Self, Self::Error> {
        if !value.is_numeric() {
            Err(ParseU8Error(value))
        } else {
            Ok(value as u8 - '0' as u8)
        }
    }
}

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

    pub fn get(&self, position: &Vector) -> Option<&T> {
        self.in_bounds(position).then(|| &self[*position])
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

    pub fn indices<'a, 'b>(&'a self) -> impl Iterator<Item=Vector> + 'b {
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

impl<T> Grid<T>
where
    T: Eq,
{
    pub fn find(&self, value: &T) -> Option<Vector> {
        self.indexed_iter().find_map(|(k, v)| (v == value).then_some(k))
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

impl<T> Grid<T>
where
    T: TryFromChar,
    <T as TryFromChar>::Error: Debug,
{
    pub fn from_line_iterators<L, I>(lines: L) -> Result<Grid<T>, ParseGridError<<T as TryFromChar>::Error>>
    where
        L: Iterator<Item=I>,
        I: Iterator<Item=char>,
    {
        let mut width = None;
        let mut height = 0;
        let mut cells = Vec::new();
        for line in lines {
            let mut local_width = 0;
            for (x, c) in line.enumerate() {
                if let Some(width) = width {
                    if x >= width {
                        return Err(ParseGridError::LineLengthsInconsistent {
                            line_index: height,
                            expected_line_len: width,
                        });
                    }
                };
                let element = TryFromChar::try_from_char(c)
                    .map_err(|e| ParseGridError::ParseElementError{
                        line_index: height,
                        column_index: x,
                        error: e
                    })?;
                cells.push(element);
                local_width += 1;
            }
            width = Some(local_width);
            height += 1;
        }
        Ok(Grid {
            cells,
            width: width.unwrap(),
            height,
        })
    }

    pub fn from_lines<L, I>(lines: L) -> Result<Grid<T>, ParseGridError<<T as TryFromChar>::Error>>
    where
        L: Iterator<Item=I>,
        I: Deref<Target=str>,
    {
        Self::from_line_iterators(lines.map(|line|
            // collecting into Vec is not nice, but there isn't really a nice way to return
            // an iterator that owns the line string (https://stackoverflow.com/a/43958470)
            line.chars().collect::<Vec<_>>().into_iter()
        ))
    }
    
    pub fn from_stdin() -> Result<Self, ParseGridError<<T as TryFromChar>::Error>> {
        Self::from_lines(io::stdin().lines().map(Result::unwrap))
    }
}

impl<T> Debug for Grid<T>
where
    T: Debug,
{
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for y in 0..self.height {
            for x in 0..self.width {
                write!(f, "{:?}", self.cells[y * self.width + x])?;
            }
            write!(f, "\n")?;
        }
        Ok(())
    }
}

impl<T> Display for Grid<T>
where
    T: Display,
{
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for y in 0..self.height {
            for x in 0..self.width {
                write!(f, "{}", self.cells[y * self.width + x])?;
            }
            write!(f, "\n")?;
        }
        Ok(())
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
