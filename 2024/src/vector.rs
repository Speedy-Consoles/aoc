use std::ops::{
    Add,
    AddAssign,
    Sub,
    SubAssign,
    Index,
    IndexMut,
    Mul,
    MulAssign,
    Div,
    DivAssign,
};

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
pub struct Vector<T, const N: usize>([T; N]);

impl<T: Ord + Default, const N: usize> Vector<T, N> {
    pub fn in_bounds(&self, size: &Vector<T, N>) -> bool {
        self.0.iter().zip(size.0.iter()).all(|(v, l)| v >= &T::default() && v < l)
    }
}

impl<T> Vector<T, 2> {
    pub const fn new(x: T, y: T) -> Self {
        Vector([x, y])
    }
}

impl<T> Vector<T, 3> {
    pub const fn new(x: T, y: T, z: T) -> Self {
        Vector([x, y, z])
    }
}

impl Vector<i32, 2> {
    pub const DIRECTIONS_4: [Self; 4] = [
        Self::new( 1,  0),
        Self::new( 0,  1),
        Self::new(-1,  0),
        Self::new( 0, -1),
    ];

    pub const DIRECTIONS_8: [Self; 8] = [
        Self::new( 1,  0),
        Self::new( 1,  1),
        Self::new( 0,  1),
        Self::new(-1,  1),
        Self::new(-1,  0),
        Self::new(-1, -1),
        Self::new( 0, -1),
        Self::new( 1, -1),
    ];
}

impl Vector<i32, 3> {
    pub const DIRECTIONS_6: [Self; 6] = [
        Self::new( 1,  0,  0),
        Self::new( 0,  1,  0),
        Self::new( 0,  0,  1),
        Self::new(-1,  0,  0),
        Self::new( 0, -1,  0),
        Self::new( 0,  0, -1),
    ];
}

impl<T, const N: usize> Index<usize> for Vector<T, N> {
    type Output = T;

    fn index(&self, index: usize) -> &Self::Output {
        self.0.index(index)
    }
}

impl<T, const N: usize> IndexMut<usize> for Vector<T, N> {
    fn index_mut(&mut self, index: usize) -> &mut Self::Output {
        self.0.index_mut(index)
    }
}

impl<T: Copy + Add, const N: usize> Add<Self> for Vector<T, N> {
    type Output = Vector<<T as Add>::Output, N>;

    fn add(self, rhs: Self) -> Self::Output {
        Vector(
            self.0.iter().zip(rhs.0.iter())
                .map(|(&a, &b)| a + b)
                .collect::<Vec<_>>()
                .try_into()
                .unwrap_or_else(|_| unreachable!())
        )
    }
}

impl<T: Copy + AddAssign, const N: usize> AddAssign<Self> for Vector<T, N> {
    fn add_assign(&mut self, rhs: Self) {
        self[0] += rhs[0];
        self[1] += rhs[1];
    }
}

impl<T: Copy + Sub, const N: usize> Sub<Self> for Vector<T, N> {
    type Output = Vector<<T as Sub>::Output, N>;

    fn sub(self, rhs: Self) -> Self::Output {
        Vector(
            self.0.iter().zip(rhs.0.iter())
                .map(|(&a, &b)| a - b)
                .collect::<Vec<_>>()
                .try_into()
                .unwrap_or_else(|_| unreachable!())
        )
    }
}
 
impl<T: Copy + SubAssign, const N: usize> SubAssign<Self> for Vector<T, N> {
    fn sub_assign(&mut self, rhs: Self) {
        self[0] -= rhs[0];
        self[1] -= rhs[1];
    }
}

impl<T: Copy + Mul<U>, const N: usize, U: Copy> Mul<U> for Vector<T, N> {
    type Output = Vector<<T as Mul<U>>::Output, N>;

    fn mul(self, rhs: U) -> Self::Output {
        Vector(self.0.map(|v| v * rhs))
    }
}

impl<T: Copy + MulAssign, const N: usize> MulAssign<T> for Vector<T, N> {
    fn mul_assign(&mut self, rhs: T) {
        self[0] *= rhs;
        self[1] *= rhs;
    }
}

impl<T: Copy + Div<U>, const N: usize, U: Copy> Div<U> for Vector<T, N> {
    type Output = Vector<<T as Div<U>>::Output, N>;

    fn div(self, rhs: U) -> Self::Output {
        Vector(self.0.map(|v| v / rhs))
    }
}

impl<T: Copy + DivAssign, const N: usize> DivAssign<T> for Vector<T, N> {
    fn div_assign(&mut self, rhs: T) {
        self[0] /= rhs;
        self[1] /= rhs;
    }
}