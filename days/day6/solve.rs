#![feature(array_windows)]

const TESTING: bool = false;

fn main() {
    if TESTING {
        let inputs: Vec<(String, u32, u32)> = include_str!("test_inputs")
            .lines()
            .map(|line| {
                let bits = line.split(' ').collect::<Vec<_>>();
                (bits[0].to_string(), bits[1].parse().unwrap(), bits[2].parse().unwrap())
            })
            .collect();

        for (inp, p1ans, p2ans) in inputs {
            assert_eq!(part1(inp.as_str()), p1ans);
            assert_eq!(part2(inp.as_str()), p2ans);
        }
        println!("all tests passed!");
    } else {
        let input = include_str!("input").trim();
        let p1 = part1(input);
        let p2 = part2(input);
        println!("part1: {p1}");
        println!("part2: {p2}");
    }
}

fn part1(s: &str) -> u32 {
    part::<4>(s.as_bytes()) as u32
}

fn part2(s: &str) -> u32 {
    part::<14>(s.as_bytes()) as u32
}

fn part<const N: usize>(b: &[u8]) -> usize {
    b.array_windows::<N>()
        .position(|array| {
            let alpha_positions = array.map(|x| 1 << (x - b'A'));
            let position_bits: u64 = alpha_positions.into_iter().fold(0, |acc, x| acc | x);
            position_bits.count_ones() == N as u32
        }).unwrap() + N
}
