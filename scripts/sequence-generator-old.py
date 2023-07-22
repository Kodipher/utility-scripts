from traceback import format_exc


DEBUG = True
ROUND_DECIMALS = 6


# Sequqnces
class Sequence:

	def get_comments_contents(self):
		yield "Unknown"

	def generator(self):
		return
		yield

	def write_to_file(self, file):
		for comment in self.get_comments_contents():
			file.write(f"// {comment}\n")
		file.write("!")
		for val in self.generator():
   			file.write(f"{val} ")
		file.write("\n\n")


class SeqConstnat(Sequence):

	def __init__(self, count, value):
		super().__init__()
		self.count = count
		self.value = value

	def get_comments_contents(self):
		yield f"Constant; count {self.count}; value {self.value}"

	def generator(self):
		for i in range(self.count):
			yield round(self.value, ROUND_DECIMALS)


class SeqLinear(Sequence):

	def __init__(self, count, start, shift):
		super().__init__()
		self.count = count
		self.start = start
		self.shift = shift

	def get_comments_contents(self):
		yield f"Linear; count {self.count}; start {self.start}, shift {self.shift}"

	def generator(self):
		val = self.start
		for i in range(self.count):
			yield val
			val = round(val + self.shift, ROUND_DECIMALS)


class SeqMult(Sequence):

	def __init__(self, count, start, mult):
		super().__init__()
		self.count = count
		self.start = start
		self.mult = mult

	def get_comments_contents(self):
		yield f"Multiplication; count {self.count}; start {self.start}, mult {self.mult}"

	def generator(self):
		val = self.start
		for i in range(self.count):
			yield val
			val = round(val * self.mult, ROUND_DECIMALS)


class SeqPower(Sequence):

	def __init__(self, count, base, exp_start=0, exp_shift=1):
		super().__init__()
		self.count = count
		self.base = base
		self.exp_start = exp_start
		self.exp_shift = exp_shift

	def get_comments_contents(self):
		yield f"Power; count {self.count}; base {self.base}, exponent start {self.exp_start}, exponent shift {self.exp_shift}"

	def generator(self):
		exp = self.exp_shift
		for i in range(self.count):
			yield self.base**exp
			exp = round(exp + self.exp_shift, ROUND_DECIMALS)


class SeqLucas(Sequence):

	def __init__(self, count, first, second):
		super().__init__()
		self.count = count
		self.first = first
		self.second = second

	def get_comments_contents(self):
		yield f"Lucas/Fibonachi; count {self.count}; first {self.first}, second {self.second}"

	def generator(self):
		first = self.first
		second = self.second
		yield first
		yield second
		for i in range(self.count):
			thrid = round(first + second, ROUND_DECIMALS)
			yield thrid
			first = second
			second = thrid


class SeqModAltSign(Sequence):

	def __init__(self, seq, is_start_negative):
		super().__init__()
		self.seq = seq
		self.is_start_negative = is_start_negative

	def get_comments_contents(self):
		yield from self.seq.get_comments_contents()
		yield f"With alternating sign; start {'negative' if self.is_start_negative else 'positive'}"

	def generator(self):
		is_negative = self.is_start_negative
		for val in self.seq.generator():
			yield -val if is_negative else val
			is_negative = not is_negative

class SeqModAltSeq(Sequence):

	def __init__(self, seq1, seq2):
		super().__init__()
		self.seq1 = seq1
		self.seq2 = seq2

	def get_comments_contents(self):
		yield f"Alternating sequences"
		yield from self.seq1.get_comments_contents()
		yield f"and"
		yield from self.seq2.get_comments_contents()

	def generator(self):
		for val1, val2 in zip(self.seq1.generator(), self.seq2.generator()):
			yield val1
			yield val2

# Main
def main():

	print("This script will generate some sequences.")

	filename = input("Filename: ")

	doOverwriteString = input("Overwrite contents? [Y/n]: ") 
	doOverwrite = len(doOverwriteString) == 0 or doOverwriteString[0] in ["Y", 'y']

	count = int(input("Sequences' length: "))

	sequences = [

		SeqConstnat(count=count, value=0),

		SeqLinear(count=count, start=0, shift=10),
		SeqLinear(count=count, start=20, shift=-2.2),

		SeqMult(count=count, start=2, mult=2),
		SeqMult(count=count, start=-1000, mult=-0.75),

		SeqPower(count=count, base=2, exp_start=0, exp_shift=1),

		SeqLucas(count=count, first=0, second=1),
		SeqLucas(count=count, first=2, second=1),

		SeqModAltSign(
			seq=SeqConstnat(count=count, value=1),
			is_start_negative=True
		),
		
		SeqModAltSign(
			seq=SeqLinear(count=count, start=5, shift=2),
			is_start_negative=False
		),

		SeqModAltSeq(
			SeqConstnat(count=count, value=0),
			SeqLucas(count=count, first=2, second=1),
		)
	]

	with open(filename, 'w' if doOverwrite else 'a') as f:

		for sequence in sequences:
			sequence.write_to_file(f)

	input("Done. Press enter to exit")


if (__name__ == '__main__'):
	if not DEBUG:
		main()
	else:
		try:
			main()
		except Exception:
			print("An error has occured:")
			print(format_exc())
			input("Press enter to exit")
