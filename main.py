import sys
import itertools
import multiprocessing as mp
from collections.abc import Iterable

if len(sys.argv) > 1:
	infile = sys.argv[1] + ".txt"
else:
	infile = "b.txt"



#all, horizontal, vertical
A = []
H = []
V = []
T = {}
TV = {}

with open(infile, 'r') as inf:

	nlines = int(inf.readline())

	for i, line in enumerate(inf):
		line = line.rstrip("\n").split(" ")

		ori = line[0]
		ntags = int(line[1])
		tags = line[2:]

		tags.sort()
		for tag in tags:
			if tag in T:
				T[tag] += 1
			else:
				T[tag] = 1

			if ori == "V":
				if tag in TV:
					TV[tag] += 1
				else:
					TV[tag] = 1


		photo = (i, set(tags), ori)

		A.append(photo)
		if ori == "H":
			H.append(photo)
		else:
			V.append(photo)
		


# vb:  H[0] = (id, [tag1, tag2, ..], "H")
# inputs zijn nu H en V
# T is hoeveel tags voorkomen
# S zijn slideshows
S = []



def calcScore(photo1, photo2):
    score1 = len(photo1[1] & photo2[1])
    score2 = photo1[1].size - score1
    score3 = photo2[1].size - score1

    return min(score1, score2, score3)













# print(H)
# print(V)
# print(T)

Trev = []
for k, v in TV.items():
	Trev.append((v, k))
Trev.sort(reverse=True)
#print(Trev)


def photoToCommon(photo):
	return importantTags & photo[1]
def invertCommonTags(tags):
	return importantTags - tags
def tagsToKey(tags):
	return "".join(sorted(tags))



IMPORTANTCOUNT = 4

importantTags = set(map(lambda x: x[1], Trev[0:IMPORTANTCOUNT]))
commonTagCombinations = []
for i in range(IMPORTANTCOUNT+1):
	commonTagCombinations.extend(map(set, itertools.combinations(importantTags, i)))
commonTagCombinations = tuple(commonTagCombinations)
commonTagCombinationsKeys = tuple(map(tagsToKey, commonTagCombinations))




indexV = {}
for tagCombKey in commonTagCombinationsKeys:
	indexV[tagCombKey] = []

for photo in V:
	indexV[tagsToKey(photoToCommon(photo))].append(photo)
	







# BEGIN PAIRING OF V

if len(V) > 0:
	pairedKeys = []
	for tags in commonTagCombinations:
		pairedKeys.append([tagsToKey(tags), tagsToKey(importantTags - tags)])



	remainingV = []
	Vslides = []
	for n in range(2**(IMPORTANTCOUNT-1)):
		V1List = indexV.get(pairedKeys[n][0])
		V2List = indexV.get(pairedKeys[n][1])

		while ((len(V1List) > 0) and (len(V2List) > 0)):
			V1 = V1List.pop(0)
			V2 = V2List.pop(0)
			slide = ((V1[0], V2[0]), V1[1] | V2[1], "V")
			Vslides.append(slide)

		if (len(V1List) > 0):
			remainingV.append((pairedKeys[n][0], V1List))
		if (len(V2List) > 0):
			remainingV.append((pairedKeys[n][1], V2List))

	lastVs = []
	lenRemaining = len(remainingV)
	for i in range(lenRemaining):
		for j in range(i + 1, lenRemaining):
			key1, VList1 = remainingV[i]
			key2, VList2 = remainingV[j]
			if (key1 != key2):
				while ((len(VList1) > 0) and (len(VList2) > 0)):
					V1 = VList1.pop(0)
					V2 = VList2.pop(0)
					slide = ((V1[0], V2[0]), V1[1] | V2[1], "V")
					Vslides.append(slide)

	for _, VList in remainingV:
		lastVs.extend(VList)

	while (len(lastVs) > 1):
		V1 = lastVs.pop(0)
		V2 = lastVs.pop(0)
		slide = ((V1[0], V2[0]), V1[1] | V2[1], "V")
		Vslides.append(slide)


	#END PAIRING OF V

	H.extend(Vslides)
	A = H

#print(A)



# print(H)
# print(V)
# print(T)

Trev = []
for k, v in T.items():
	Trev.append((v, k))
Trev.sort(reverse=True)
#print(Trev)


def photoToCommon(photo):
	return importantTags & photo[1]
def invertCommonTags(tags):
	return importantTags - tags
def tagsToKey(tags):
	return "".join(sorted(tags))




importantTags = set(map(lambda x: x[1], Trev[0:IMPORTANTCOUNT]))
commonTagCombinations = []
for i in range(IMPORTANTCOUNT+1):
	commonTagCombinations.extend(map(set, itertools.combinations(importantTags, i)))
commonTagCombinations = tuple(commonTagCombinations)
commonTagCombinationsKeys = tuple(map(tagsToKey, commonTagCombinations))



index = {}
for tagCombKey in commonTagCombinationsKeys:
	index[tagCombKey] = []

for photo in A:
	index[tagsToKey(photoToCommon(photo))].append(photo)
	
for tagCombKey in commonTagCombinationsKeys:
	if len(index[tagCombKey]) == 0:
		index[tagCombKey] = None

print(f"indexes: {len(commonTagCombinations)}")
print(f"max length in index: {max(map(len, index))}")


# print(f"V= {V}")
# print(f"commonTagCombinations= {commonTagCombinations}")
#print(f"index= {index}")
# print(f"T= {T}")
# print(f"Trev= {Trev}")

#print(list(commonTagCombinations))
	








#PAK GWN EFFE EEN RANDOM FOTO AS EERSTE
startPhoto = A.pop()
invTagsKey = tagsToKey(photoToCommon(startPhoto))
currIndex = index[invTagsKey]
currIndex.remove(startPhoto)
if len(currIndex) == 0:
	index[invTagsKey] = None
currPhoto = startPhoto
S.append(currPhoto)
for i in range(len(A)):
	invTagsFirst = importantTags - currPhoto[1]
	
	for i in range(IMPORTANTCOUNT+1):
		for offsetSet in map(set, itertools.combinations(importantTags, i)):
			invTagsKey = tagsToKey(invTagsFirst ^ offsetSet)
			currIndex = index[invTagsKey]

			if currIndex is not None:
				break	
		if currIndex is not None:
			break


	
	maxScore = -1
	nextImage = None
	currOtherTags = currPhoto[1] - importantTags
	for potentialNext in currIndex:
		score = len(currOtherTags & potentialNext[1])
		if score > maxScore:
			maxScore = score
			nextImage = potentialNext

	

	S.append(nextImage)
	currIndex.remove(nextImage)
	if len(currIndex) == 0:
		index[invTagsKey] = None
	currPhoto = nextImage






#print(S)


first = True
with open("out" + infile, 'w') as outf:
	outf.write(str(len(S)))
	for slide in S:
		if isinstance(slide[0], Iterable):
			outf.write("\n" + str(slide[0][0]) + " " + str(slide[0][1]))
		else:
			outf.write("\n" + str(slide[0]))
