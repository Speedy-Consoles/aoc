use std::{
    io,
    ops::{
        Index,
        IndexMut,
    }
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

impl Grid<char> {
    pub fn from_stdin() -> Self {
        let mut lines = io::stdin().lines().map(Result::unwrap).peekable();
        let width = lines.peek().unwrap().len();
        let mut height = 0;
        let mut cells = Vec::new();
        for line in lines {
            for (x, c) in line.chars().enumerate() {
                assert!(x < width);
                cells.push(c);
            }
            height += 1;
        }
        Self {
            cells,
            width,
            height,
        }
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