#include <stdlib.h>
#include <stdio.h>

typedef struct pair {
	unsigned char a: 4;
	unsigned char b: 4;
} pair_t;

typedef struct input {
	pair_t* pairs;
	size_t num_pairs;
} input_t;

typedef struct answer {
	unsigned int part1;
	unsigned int part2;
} answer_t;

input_t load(const char*);
answer_t solve(input_t);

int main() {
	input_t input = load("input");
	answer_t answer = solve(input);

	printf("part 1: %u\n", answer.part1);
	printf("part 2: %u\n", answer.part2);

	free(input.pairs);

	return 0;
}

input_t load(const char* fname) {
	FILE* fp = fopen(fname, "r");
	if (!fp) {
		perror("fopen");
		exit(EXIT_FAILURE);
	}

	fseek(fp, 0, SEEK_END);
	long size = ftell(fp);
	rewind(fp);

	char* buf = malloc(size * sizeof(char));
	if (!buf) {
		perror("malloc");
		exit(EXIT_FAILURE);
	}

	fread(buf, sizeof(char), size, fp);

	struct pair* pairs = (struct pair*) malloc(size * sizeof(struct pair) / 4);
	if (!pairs) {
		perror("malloc");
		exit(EXIT_FAILURE);
	}

	for (int i = 0; i < size; i += 4) {
		pairs[i >> 2].a = buf[i] - 'A';
		pairs[i >> 2].b = buf[i + 2] - 'X';
	}
	
	free(buf);

	return (input_t) {
		.pairs = pairs,
		.num_pairs = size / 4,
	};
}

answer_t solve(input_t input) {
	unsigned int part1 = 0, part2 = 0;
  unsigned char score_table[9] = {3, 6, 0, 0, 3, 6, 6, 0, 3};
  unsigned char move_table[9] = {3, 1, 2, 1, 2, 3, 2, 3, 1};

	for (size_t i = 0; i < input.num_pairs; i++) {
		pair_t pair = input.pairs[i];
		size_t index = pair.a * 3 + pair.b;
		part1 += score_table[index] + pair.b + 1;
		part2 += move_table[index] + pair.b * 3;
	}

	return (answer_t) { part1, part2 };
}
