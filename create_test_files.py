import multiprocessing as mp
from multiprocessing import Queue
import time
from class_tuple import Tuple

tuple = Tuple()



if __name__ == '__main__':

	filenames = ["data/freebase_test.ques", "data/freebase_test.ans"]
	files = [open(i, "r") for i in filenames]
	tgt_file = open("data/final_test.tsv", "w")

	cnt = 0
	ts = time.time()


	max_len = 0

	for rows in zip(*files):
		ques = rows[0][:-1]
		ans = rows[1][:-2]
		cnt += 1

		combined = ""
		find_flag = 0
		output = ""

		srl_dict = tuple.dict(ques)

		ques = rows[0][:-1]
		ans= rows[1][:-2]

		for phrase, tags in srl_dict.items():
			if find_flag == 0:
				for words in tuple.ques_words:
					if (phrase.lower()).find(words) != -1:
						find_flag = 1
						phrase = ans
						break
			combined += " " + phrase

		if find_flag == 0:
			output = "fluent: " + ques + " + " + ans + "\n"
		else:
			output = "srl_fluent: " + combined + "\n"

		print("time ", time.time()-ts)
		print(cnt, '::')
		tgt_file.write(output)



