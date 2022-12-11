#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <x86intrin.h>

typedef struct {
	// using bitfields for this is 100% necessary I promise
	enum {
		NOOP = 0,
		ADDX,
	} op:2;
	int arg:30;
} instr_t;

typedef struct {
	instr_t *instrs;
	size_t num_instrs;
} program_t;

void die(const char*);
int num_newlines_in_block(const char*);
program_t read_program(FILE*);
long part1(const program_t*);
void part2(const program_t*);
void debug_128(__m128i);

int main(void) {
	FILE* fp = fopen("input", "r");
	if (!fp) die("fopen");

	program_t prog = read_program(fp);
	fclose(fp);

	long p1 = part1(&prog);
	printf("part1: %ld\n", p1);
	part2(&prog);

	free(prog.instrs);

	return 0;
}

long part1(const program_t* prog) {
	long tc = 0;
	long x = 1;
	long signal_strength = 0;

	for (size_t i = 0; i < prog->num_instrs; i++) {
		instr_t instr = prog->instrs[i];
		long cycles = 1;
		if (instr.op == ADDX) {
				cycles++;
		}

		for (; cycles > 0; cycles--) {
			switch (++tc) {
				case 20:
				case 60:
				case 100:
				case 140:
				case 180:
					signal_strength += tc * x;
					break;
				case 220:
					signal_strength += tc * x;
					return signal_strength;
			}
		}

		if (instr.op == ADDX) {
			x += instr.arg;
		}
	}

	return signal_strength;
}

void part2(const program_t *prog) {
	char screen[240] = { 0 };
	memset(screen, '.', 240);

	// run program
	long tc = 0;
	long x = 1;
	long signal_strength = 0;

	for (size_t i = 0; i < prog->num_instrs; i++) {
		instr_t instr = prog->instrs[i];
		long cycles = 1;
		if (instr.op == ADDX) {
				cycles++;
		}

		for (; cycles > 0; cycles--) {
			if (labs((tc++) % 40 - x) < 2) {
				screen[tc - 1] = '#';
			}
		}

		if (instr.op == ADDX) {
			x += instr.arg;
		}
	}

	// display the screen
	for (int i = 0; i < 240; i++) {
		putchar(screen[i]);
		if ((i + 1) % 40 == 0) {
			putchar('\n');
		}
	}
}

program_t read_program(FILE* fp) {
	// find the size of the file
	fseek(fp, 0, SEEK_END);
	long fsz = ftell(fp);
	rewind(fp);

	// read the whole file
	char* bytes = malloc(fsz * sizeof(char));
	if (!bytes) die("malloc");
	fread(bytes, sizeof(char), fsz, fp);

	// find the number of newlines using SIMD :D cos lmao why not
	unsigned int no_newlines = 0, i;
	for (i = 0; i < (fsz - 16); i += 16) {
		no_newlines += num_newlines_in_block(&bytes[i]);
	}
	for (; i < fsz; i++) {
		no_newlines += bytes[i] == '\n';
	}

	// allocate the space for the instructions
	// using calloc here to default initialise the array as a zero-d instruction is just NOOP
	instr_t* instructions = calloc(no_newlines, sizeof(instr_t));
	if (!instructions) die("calloc");

	// parse the instructions
	long arg;
	char* buf = bytes;
	char* end = NULL;
	for (unsigned int i = 0; i < no_newlines; i++) {
		if (buf[0] == 'n') {
			// on NOOP, skip 5
			buf = buf + 5;
			instructions[i].op = NOOP;
		} else {
			// skip to arg
			buf = buf + 5;

			// parse arg
			arg = strtol(buf, &end, 10);
			instructions[i].op = ADDX;
			instructions[i].arg = arg;
			// skip to end + 1 to get to next instr
			buf = end + 1;
		}
	}

	// free memory from file
	free(bytes);

	return (program_t) {
		.instrs = instructions,
		.num_instrs = no_newlines,
	};
}

int num_newlines_in_block(const char* block) {
	// load the input into a 128 bit register
	__m128i n = _mm_loadu_si128((__m128i_u*) block);

	// splat out newline into 8 newlines
	__m128i MASK = _mm_set1_epi8('\n');

	// compare for equality with the mask
	n = _mm_cmpeq_epi8(n, MASK);

	// take the MSB of each 8 bit block and pack it into the lowest 16
	unsigned int lsb16 = _mm_movemask_epi8(n);

	// use popcnt to determine the number of set bits
	// this corresponds directly to the number of characters which were '\n'
	return _mm_popcnt_u32(lsb16);
}

void die(const char * reason) {
	perror(reason);
	exit(EXIT_FAILURE);
}

void debug_128(__m128i n) {
	// extract to two 64 bit values
	unsigned long halves[2] = {0};
	_mm_storeu_si128((__m128i_u*) halves, n);
	printf("%016lx%016lx\n", halves[0], halves[1]);
}
