use std::{
    cmp::Ordering,
    iter::{
        self,
        Sum,
    },
    ops::{
        self,
        Sub,
    },
};

#[derive(Debug)]
struct Range<T> {
    start: T,
    end: T,
}

impl<T> Range<T>
where
    T: Sub + Copy,
{
    fn len(&self) -> <T as Sub>::Output {
        self.end - self.start
    }
}

#[derive(Debug)]
pub struct RangeSet<T> {
    ranges: Vec<Range<T>>,
}

impl<T> RangeSet<T> {
    pub fn new() -> Self {
        RangeSet {
            ranges: Vec::new(),
        }
    }
}

impl<T> RangeSet<T>
where
    T: Sub + Copy
{
    pub fn count<S>(&self) -> S
    where
        S: Sum<<T as Sub>::Output>
    {
        self.ranges.iter().map(Range::len).sum()
    }
}

impl<T> RangeSet<T>
where
    T: PartialOrd + Copy
{
    pub fn add(&mut self, mut range: ops::Range<T>) {
        let start_result = self.ranges.binary_search_by(|other_range|
            if range.start < other_range.start {
                Ordering::Greater
            } else if range.start <= other_range.end {
                Ordering::Equal
            } else {
                Ordering::Less
            }
        );
        let end_result = self.ranges.binary_search_by(|other_range|
            if range.end <= other_range.start {
                Ordering::Greater
            } else if range.end <= other_range.end {
                Ordering::Equal
            } else {
                Ordering::Less
            }
        );
        let start = match start_result {
            Ok(index) => {
                range.start = self.ranges[index].start;
                index
            },
            Err(index) => index,
        };
        let end = match end_result {
            Ok(index) => {
                range.end = self.ranges[index].end;
                index + 1
            },
            Err(index) => index,
        };
        self.ranges.splice(start..end, iter::once(Range { start: range.start, end: range.end }));
    }
}

impl<T> RangeSet<T>
where
    T: PartialOrd
{
    pub fn contains<U>(&self, item: &U) -> bool
    where
        T: PartialOrd<U>,
        U: PartialOrd<T> + ?Sized,
    {
        self.ranges.binary_search_by(|range|
            if *item < range.start {
                Ordering::Greater
            } else if *item < range.end {
                Ordering::Equal
            } else {
                Ordering::Less
            }
        ).is_ok()
    }
}
