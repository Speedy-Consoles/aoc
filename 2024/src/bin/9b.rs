use std::{
    cell::RefCell,
    rc::Rc,
};

use itertools::Itertools;
use lib::nine::parse_input;

// Linked list cursors in rust are still experimental, so we build our own.
struct SectionInner {
    file_id: usize,
    size: usize,
    space: usize,
    prev: Option<Section>,
    next: Option<Section>,
}

#[derive(Clone)]
struct Section {
    inner: Rc<RefCell<SectionInner>>,
}

impl Section {
    fn new(file_id: usize, size: usize, space: usize, prev: Option<Section>) -> Self {
        Self {
            inner: Rc::new(RefCell::new(SectionInner {
                file_id,
                size,
                space,
                prev,
                next: None,
            })),
        }
    }

    fn file_id(&self) -> usize {
        self.inner.borrow().file_id
    }

    fn size(&self) -> usize {
        self.inner.borrow().size
    }

    fn space(&self) -> usize {
        self.inner.borrow().space
    }

    fn size_and_space(&self) -> usize {
        let inner = self.inner.borrow();
        inner.size + inner.space
    }

    fn prev(&self) -> Option<Section> {
        self.inner.borrow().prev.clone()
    }

    fn next(&self) -> Option<Section> {
        self.inner.borrow().next.clone()
    }

    fn set_space(&mut self, space: usize) {
        self.inner.borrow_mut().space = space;
    }

    fn set_prev(&mut self, prev: Option<Section>) {
        self.inner.borrow_mut().prev = prev;
    }

    fn set_next(&mut self, next: Option<Section>) {
        self.inner.borrow_mut().next = next;
    }
}

// fn print_memory(head: Option<Section>) {
//     let mut cursor = head;
//     while let Some(current) = cursor {
//         cursor = current.next();
//         for _ in 0..current.size() {
//             eprint!("{}", current.file_id());
//         }
//         for _ in 0..current.space() {
//             eprint!(".");
//         }
//     }
//     eprintln!();
// }

fn main() {
    let memory = parse_input();

    let num_files = (memory.len() + 1) / 2;

    let (head, tail) = memory.iter()
        .chain([0].iter())
        .tuples()
        .enumerate()
        .fold((None, None), |(mut head, mut tail), (file_id, (&size, &space))| {
            let section = Section::new(file_id, size, space, tail.clone());
            head = head.or(Some(section.clone()));
            if let Some(mut tail) = tail.replace(section.clone()) {
                tail.set_next(Some(section.clone()));
            }
            (head, tail)
        });

    let mut next = tail;
    for current_id in (0..num_files).rev() {
        // print_memory(head.clone());

        let mut current = next.unwrap();
        while current.file_id() != current_id {
            current = current.prev().unwrap();
        }
        next = current.prev();

        let mut cursor = head.clone().unwrap();
        while cursor.file_id() != current_id {
            if cursor.space() >= current.size() {
                // remove
                let mut current_prev = current.prev().unwrap();
                current_prev.set_space(current_prev.space() + current.size_and_space());
                current_prev.set_next(current.next());

                // insert
                current.set_space(cursor.space() - current.size());
                cursor.set_space(0);
                current.set_next(cursor.next());
                current.set_prev(Some(cursor.clone()));
                if let Some(mut next) = cursor.next() {
                    next.set_prev(Some(current.clone()));
                }
                cursor.set_next(Some(current.clone()));

                break;
            }
            cursor = cursor.next().unwrap();
        }
    }

    let mut cursor = head;
    let mut block_index = 0;
    let mut result = 0;
    while let Some(current) = cursor {
        result += (
            block_index * current.size()
            + (current.size() - 1) * current.size() / 2
        ) * current.file_id();
        block_index += current.size() + current.space();
        cursor = current.next();
    }
    println!("{result}");
}
