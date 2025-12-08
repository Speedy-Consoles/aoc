use std::{
    collections::HashSet,
    iter,
    mem,
};

#[derive(Debug)]
enum SetOrRef {
    Set(HashSet<usize>),
    Ref(usize),
}

impl SetOrRef {
    fn as_set(&self) -> Option<&HashSet<usize>> {
        match *self {
            SetOrRef::Set(ref set) => Some(set),
            SetOrRef::Ref(_) => None,
        }
    }

    fn as_mut_set(&mut self) -> Option<&mut HashSet<usize>> {
        match *self {
            SetOrRef::Set(ref mut set) => Some(set),
            SetOrRef::Ref(_) => None,
        }
    }

    fn into_set(self) -> Option<HashSet<usize>> {
        match self {
            SetOrRef::Set(set) => Some(set),
            SetOrRef::Ref(_) => None,
        }
    }
}

pub struct DisjointSets {
    size: usize,
    sets_by_element: Vec<SetOrRef>,
}

impl DisjointSets {
    pub fn new(size: usize) -> Self {
        let sets_by_element = (0..size)
            .map(|i| SetOrRef::Set(iter::once(i).collect()))
            .collect();
        DisjointSets {
            size,
            sets_by_element,
        }
    }

    pub fn join(&mut self, first_index: usize, second_index: usize) {
        let mut r1 = self.get_representative(first_index);
        let mut r2 = self.get_representative(second_index);
        if r1 == r2 {
            return;
        }
        let mut set_or_ref_1 = SetOrRef::Ref(r2);
        let mut set_or_ref_2 = SetOrRef::Ref(r1);
        mem::swap(&mut self.sets_by_element[r1], &mut set_or_ref_1);
        mem::swap(&mut self.sets_by_element[r2], &mut set_or_ref_2);
        let set_1 = set_or_ref_1.as_mut_set().unwrap();
        let mut set_2 = set_or_ref_2.into_set().unwrap();
        if set_1.len() < set_2.len() {
            // for better performance
            mem::swap(set_1, &mut set_2);
            mem::swap(&mut r1, &mut r2);
        }
        for &i in set_2.iter() {
            self.sets_by_element[i] = SetOrRef::Ref(r1);
        }
        set_1.extend(set_2);
        mem::swap(&mut set_or_ref_1, &mut self.sets_by_element[r1]);
        self.size -= 1;
    }

    pub fn len(&self) -> usize {
        self.size
    }

    pub fn iter(&self) -> impl Iterator<Item=&HashSet<usize>> {
        self.sets_by_element.iter().filter_map(|set_or_ref| set_or_ref.as_set())
    }

    fn get_representative(&self, index: usize) -> usize {
        match self.sets_by_element[index] {
            SetOrRef::Set(_) => index,
            SetOrRef::Ref(representative) => representative,
        }
    }
}
