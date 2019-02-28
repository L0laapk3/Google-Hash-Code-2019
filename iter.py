import sys
import itertools
import multiprocessing as mp
from collections.abc import Iterable

if len(sys.argv) > 1:
	infile = sys.argv[1] + ".txt"
else:
	infile = "a.txt"
	
	
	
	
A = []
H = []
V = []
T = []

with open(infile, 'r') as inf:

	nlines = int(inf.readline())

	for i, line in enumerate(inf):
		line = line.rstrip("\n").split(" ")

		ori = line[0]
		ntags = int(line[1])
		tags = line[2:]


		photo = (i, set(tags), ori)

		A.append(photo)
		if ori == "H":
			H.append(photo)
		else:
			V.append(photo)
		



S = []

with open("out" + infile, 'r') as inf:

	nlines = int(inf.readline())

	for i, line in enumerate(inf):
		line = line.rstrip("\n").split(" ")


		if len(line) == 1:
			S.append(A[int(line[0])])
		else:
			p1 = A[int(line[0])]
			p2 = A[int(line[1])]
			S.append(((p1[0], p2[0]), p1[1] | p2[1], "V"))
		




def calcScore(photo1, photo2):
    score1 = len(photo1[1] & photo2[1])
    score2 = len(photo1[1]) - score1
    score3 = len(photo2[1]) - score1

    return min(score1, score2, score3)

while True:
	changed = False
	for j in range(1, len(S) - 2):
		sChanged = False
		while True:
			for i in range(1, len(S) - 2):
				score = calcScore(S[i - 1], S[i + 1]) - calcScore(S[i - 1], S[i]) - calcScore(S[i + 1], S[i]) \
					- calcScore(S[j - 1], S[j]) + calcScore(S[j - 1], S[i]) + calcScore(S[j], S[i])
				if score > 0:
					S.insert(j, S.pop(i))
					sChanged = True
					changed = True
			if not sChanged:
				break

	if not changed:
		break



first = True
with open("out" + infile, 'w') as outf:
	outf.write(str(len(S)))
	for slide in S:
		if isinstance(slide[0], Iterable):
			outf.write("\n" + str(slide[0][0]) + " " + str(slide[0][1]))
		else:
			outf.write("\n" + str(slide[0]))
