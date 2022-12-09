use std::collections::HashMap;

fn main() {
    let dir: Directory = include_str!("input").parse().unwrap();

    let (p1, p2) = solve(&dir);
    println!("part1: {p1}");
    println!("part2: {p2}");
}

fn solve(directory: &Directory) -> (u64, u64) {
    // use a depth first search to perform a kind of topological sort on the directories
    // so that sub-directories are searched before parent ones
    let mut dir_stack = vec![String::from("/")];
    let mut directories = dir_stack.clone();
    while let Some(dir) = dir_stack.pop() {
        directories.push(dir.clone());
        for node in &directory.contents[dir.as_str()] {
            if let FileSystemNode::Directory { name } = node {
                let sub = if dir == "/" {
                    format!("/{name}")
                } else {
                    format!("{dir}/{name}")
                };
                dir_stack.push(sub);
            }
        }
    }

    let mut sizes: HashMap<String, u64> = HashMap::new();
    for dir in directories.iter().rev() {
        let mut total_size = 0;
        for node in &directory.contents[dir] {
            total_size += match node {
                FileSystemNode::Directory { name } => {
                    if dir.ends_with('/') {
                        sizes[&format!("{dir}{name}")]
                    } else {
                        sizes[&format!("{dir}/{name}")]
                    }
                }
                FileSystemNode::File { size, .. } => *size,
            };
        }
        sizes.insert(dir.clone(), total_size);
    }

    let part1 = sizes.values().filter(|size| **size <= 100000).sum();

    const TOTAL_SIZE: u64 = 70000000;
    const NEEDED_SPACE: u64 = 30000000;
    let used_space = sizes["/"];
    let space_needed_to_remove = NEEDED_SPACE - (TOTAL_SIZE - used_space);

    let part2 = *sizes.values().filter(|size| **size >= space_needed_to_remove).min().unwrap();

    (part1, part2)
}

#[derive(Debug, Default)]
struct Directory {
    contents: HashMap<String, Vec<FileSystemNode>>,
}

impl std::str::FromStr for Directory {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut dir = Directory::default();
        let mut curr_path = String::new();
        for line in s.lines() {
            if line.starts_with("$") {
                let command: Command = line.parse()?;
                match command {
                    Command::Cd(dir) => {
                        if dir == ".." {
                            let (base, _) = curr_path.rsplit_once('/').expect("Bad path while building directory.");
                            curr_path = base.to_owned();
                        } else {
                            if dir != "/" && !curr_path.ends_with("/") {
                                curr_path.push('/');
                            }
                            curr_path.push_str(dir.as_str());
                        }

                        if curr_path.is_empty() {
                            curr_path.push('/');
                        }
                    }
                    Command::Ls => {}
                }
            } else {
                let fs_node: FileSystemNode = line.parse()?;
                dir.contents.entry(curr_path.clone()).or_default().push(fs_node);
            }
        }

        Ok(dir)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
enum FileSystemNode {
    Directory {
        name: String
    },
    File {
        name: String,
        size: u64,
    },
}

impl std::str::FromStr for FileSystemNode {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.split_once(' ') {
            Some(("dir", dirname)) => Ok(Self::Directory { name: dirname.to_owned() }),
            Some((size, name)) => {
                match size.parse() {
                    Ok(n) => Ok(Self::File { name: name.to_owned(), size: n }),
                    Err(e) => Err(format!("{e:?}")),
                }
            }
            None => Err(String::from("Invalid file system node format."))
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
enum Command {
    Cd(String),
    Ls,
}

impl std::str::FromStr for Command {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let parts: Vec<_> = s.split_ascii_whitespace().collect();
        match parts.as_slice() {
            &["$", "cd", dir] => Ok(Self::Cd(dir.to_owned())),
            &["$", "ls"] => Ok(Self::Ls),
            _ => Err(String::from("Invalid command format.")),
        }
    }
}
