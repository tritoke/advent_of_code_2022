use chumsky::prelude::*;
use std::cmp::Ordering;
use std::fmt::{self, Write};


fn main() {
    let input = Input::parser().parse(include_str!("../input")).unwrap();

    let p1 = part1(&input);
    println!("part 1: {p1}");

    let p2 = part2(&input);
    println!("part 2: {p2}");
}

fn part1(input: &Input) -> u64 {
    input
        .pairs
        .iter()
        .enumerate()
        .filter(|(_, (a, b))| *a < *b)
        .map(|(i, _)| (i + 1) as u64)
        .sum()
}

// originally used for testing but used for part 2 as well
macro_rules! list {
    ( $( $elem:expr ),* ) => {
        Packet::List(vec![$($elem),*])
    }
}

macro_rules! vlist {
    ( $( $elem:expr ),* ) => {
        Packet::List(vec![$(val!($elem)),*])
    }
}

macro_rules! val {
    ($v:literal) => {
        Packet::Value($v)
    };
}

fn part2(input: &Input) -> u64 {
    let mut all_packets = Vec::new();
    for (l, r) in &input.pairs {
        all_packets.push(l);
        all_packets.push(r);
    }

    // push the divider packets
    let div1 = list![vlist![2]];
    let div2 = list![vlist![6]];
    all_packets.push(&div1);
    all_packets.push(&div2);

    all_packets.sort_unstable();

    all_packets
        .into_iter()
        .enumerate()
        .filter_map(|(i, p)| (p == &div1 || p == &div2).then_some(i))
        .fold(1, |acc, x| acc * (x as u64 + 1))
}

#[derive(Debug)]
struct Input {
    pairs: Vec<(Packet, Packet)>,
}

impl Input {
    fn parser() -> impl Parser<char, Self, Error = Simple<char>> {
        Packet::parser()
            .then_ignore(just('\n'))
            .then(Packet::parser())
            .separated_by(just("\n\n"))
            .map(|pairs| Input { pairs })
    }
}

#[derive(Debug, Clone, Eq, PartialEq)]
enum Packet {
    List(Vec<Packet>),
    Value(i8),
}

impl fmt::Display for Packet {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Packet::List(elems) => {
                f.write_char('[')?;
                let mut first = true;
                for e in elems {
                    if first {
                        first = false;
                        write!(f, "{e}")?;
                    } else {
                        write!(f, ",{e}")?;
                    }
                }
                f.write_char(']')
            }
            Packet::Value(v) => write!(f, "{v}"),
        }
    }
}

impl Packet {
    fn parser() -> impl Parser<char, Self, Error = Simple<char>> {
        recursive(|tree| {
            tree.separated_by(just(','))
                .delimited_by(just('['), just(']'))
                .map(Packet::List)
                .or(text::int(10)
                    .from_str::<i8>()
                    .unwrapped()
                    .map(Packet::Value))
        })
    }
}

impl PartialOrd for Packet {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        use Ordering::*;
        use Packet::*;

        let cmp = match (self, other) {
            (Value(l), Value(r)) => l.partial_cmp(&r),
            (List(left), List(right)) => {
                let body_comparison =
                    left.iter()
                        .zip(right.iter())
                        .fold(Equal, |mut acc, (l, r)| {
                            if acc == Equal {
                                acc = l.cmp(&r);
                            };

                            acc
                        });

                match body_comparison {
                    Equal => left.len().cmp(&right.len()),
                    cmp => cmp,
                }
            }
            .into(),
            (l, List(_)) => List(vec![l.clone()]).partial_cmp(other),
            (List(_), r) => self.partial_cmp(&List(vec![r.clone()])),
        };
        cmp
    }
}

impl Ord for Packet {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test1() {
        let a = vlist![1, 1, 3, 1, 1];
        let b = vlist![1, 1, 5, 1, 1];
        assert!(a < b);
    }

    #[test]
    fn test2() {
        // [[1],[2,3,4]] vs [[1],4]
        let a = list![vlist![1], vlist![2, 3, 4]];
        let b = list![vlist![1], val!(4)];
        assert!(a < b);
    }

    #[test]
    fn test3() {
        // [9] vs [[8,7,6]]
        let a = vlist![9];
        let b = list![vlist![8, 7, 6]];
        assert!(a > b);
    }

    #[test]
    fn test4() {
        // [[4,4],4,4] vs [[4,4],4,4,4]
        let a = list![vlist![4, 4], val!(4), val!(4)];
        let b = list![vlist![4, 4], val!(4), val!(4), val!(4)];
        assert!(a <= b);
    }

    #[test]
    fn test5() {
        // [7,7,7,7] vs [7,7,7]
        let a = vlist![7, 7, 7, 7];
        let b = vlist![7, 7, 7];
        assert!(a > b);
    }

    #[test]
    fn test6() {
        // [] vs [3]
        let a = list![];
        let b = vlist![3];
        assert!(a <= b);
    }

    #[test]
    fn test7() {
        // [[[]]] vs [[]]
        let a = list![list![list![]]];
        let b = list![list![]];
        assert!(a > b);
    }

    // an extra test case because my thing couldn't cope
    #[test]
    fn test8() {
        // [1,[2,[3,[4,[5,6,7]]]],8,9] vs [1,[2,[3,[4,[5,6,0]]]],8,9]
        let a = list![
            val!(1),
            list![val!(2), list![val!(3), list![val!(4), vlist![5, 6, 7]]]],
            val!(8),
            val!(9)
        ];
        let b = list![
            val!(1),
            list![val!(2), list![val!(3), list![val!(4), vlist![5, 6, 0]]]],
            val!(8),
            val!(9)
        ];
        assert!(a > b);
    }

    // an extra test case because my thing couldn't cope
    #[test]
    fn test9() {
        // [[[],8],[9]] vs [[8,[7],[],7,9],[1,[[1,8,6,1,9]],2,8,[]],[],[3,4,[0,[4]],5],[]]
        let a = list![list![list![], val!(9)], vlist![9]];
        let b = list![
            list![val!(8), vlist![7], list![], val!(7), val!(9)],
            list![
                val!(1),
                list![vlist![1, 8, 6, 1, 9]],
                val!(2),
                val!(8),
                list![]
            ],
            list![],
            list![val!(3), val!(4), list![val!(0), vlist![4]], val!(5)],
            list![]
        ];

        assert!(a < b);
    }

    #[test]
    fn test10() {
        // [[[[9],5]],[[[7,7,4],8,9,[0,10,2,0,9]],[[1,0],[6],4],6],[[[7,8],8,9,[],[]],5,[],9],[10]] vs [[[9,[],6],[[7,8,8,1],[]],[4,[],[8,4,9,3,5],3],[0,[0,5,3,4],0,1],[4,9,4,7]],[[0,[10,0]],[[1,1,8,10],9,1,[7,6]],4]]

        let a = list![
            list![list![vlist![9], val!(5)]],
            list![
                list![vlist![7, 7, 4], val!(8), val!(9), vlist![0, 10, 2, 0, 9]],
                list![vlist![1, 0], vlist![6], val!(4)],
                val!(6)
            ],
            list![
                list![vlist![7, 8], val!(8), val!(9), list![], list![]],
                val!(5),
                list![],
                val!(9)
            ],
            vlist![10]
        ];
        let b = list![
            list![
                list![val!(9), list![], val!(6)],
                list![vlist![7, 8, 8, 1], list![]],
                list![val!(4), list![], vlist![8, 4, 9, 3, 5], val!(3)],
                list![val!(0), vlist![0, 5, 3, 4], val!(0), val!(1)],
                vlist![4, 9, 4, 7]
            ],
            list![
                list![val!(0), vlist![10, 0]],
                list![vlist![1, 1, 8, 10], val!(9), val!(1), vlist![7, 6]],
                val!(4)
            ]
        ];

        assert!(a > b);
    }
}
