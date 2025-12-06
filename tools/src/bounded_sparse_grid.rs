use std::{
    collections::HashMap,
    io:: {
        self,
        BufRead,
    },
    ops::Deref,
};

type Vector =  crate::vector::Vector<i32, 2>;

pub struct BoundedSparseGrid<T> {
    elements: HashMap<Vector, T>,
    width: usize,
    height: usize,
}

impl<T> BoundedSparseGrid<T> {
    pub fn new(width: usize, height: usize) -> Self {
        Self {
            elements: HashMap::new(),
            width,
            height,
        }
    }

    pub fn width(&self) -> usize {
        self.width
    }

    pub fn height(&self) -> usize {
        self.height
    }

    pub fn insert(&mut self, index: Vector, value: T) -> Option<T> {
        self.elements.insert(index, value)
    }

    pub fn get(&self, index: &Vector) -> Option<&T> {
        self.elements.get(index)
    }

    pub fn get_mut(&mut self, index: &Vector) -> Option<&mut T> {
        self.elements.get_mut(index)
    }

    pub fn indexed_iter(&self) -> impl Iterator<Item=(&Vector, &T)> {
        self.elements.iter()
    }

    pub fn indices(&self) -> impl Iterator<Item=Vector> {
        let width = self.width;
        let height = self.height;
        (0..height).flat_map(move |y|
            (0..width).map(move |x| Vector::new(x as i32, y as i32)
        ))
    }

    pub fn in_bounds(&self, position: &Vector) -> bool {
        position.in_bounds(&Vector::new(self.width as i32, self.height as i32))
    }
}

impl BoundedSparseGrid<char> {
    pub fn from_lines<L, I>(lines: L, empty: char) -> Self
    where
        L: Iterator<Item=I>,
        I: Deref<Target=str>,
    {
        let mut lines = lines.peekable();
        let width = lines.peek().unwrap().len();
        let mut height = 0;
        let mut elements = HashMap::new();
        for (y, line) in lines.enumerate() {
            for (x, c) in line.chars().enumerate() {
                assert!(x < width);
                if c != empty {
                    elements.insert(Vector::new(x as i32, y as i32), c);
                }
            }
            height += 1;
        }
        Self {
            elements,
            width,
            height,
        }
    }

    pub fn from_buf_read<B>(buf_read: &mut B, empty: char) -> Self
    where
        B: BufRead,
    {
        Self::from_lines(buf_read.lines().map(Result::unwrap), empty)
    }

    pub fn from_stdin(empty: char) -> Self {
        Self::from_lines(io::stdin().lines().map(Result::unwrap), empty)
    }
}
