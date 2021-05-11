import multiprocessing as mp
from multiprocessing import Queue
import time
from class_tuple import Tuple

tuple = Tuple()



if __name__ == '__main__':

	filenames = ["data/train.tgt", "data/train.ques", "data/train.ans"]
	files = [open(i, "r") for i in filenames]
	tgt_file = open("data/final_train.tsv", "w")

	cnt = 0
	ts = time.time()
	tgt_file.write("target_text\tinput_text\tprefix\n")


	max_len = 0

	for rows in zip(*files):
		#print(count, " : ")
		target = rows[0][:-1]
		ques = rows[1][:-1]
		ans = rows[2][:-2]
		cnt += 1

		combined = ""
		find_flag = 0
		output = ""

		srl_dict = tuple.dict(ques)

		target = rows[0][:-1]
		ques = rows[1][:-1]
		ans= rows[2][:-2]

		for phrase, tags in srl_dict.items():
			if find_flag == 0:
				for words in tuple.ques_words:
					if (phrase.lower()).find(words) != -1:
						find_flag = 1
						phrase = ans
						break
			combined += " " + phrase

		if find_flag == 0:
			output = target + "\t" + ques + " + " + ans + "\t" + "fluent\n"
		else:
			output = target + "\t" + combined + "\t" + "srl_fluent\n"

		print("time ", time.time()-ts)
		print(cnt, '::')
		tgt_file.write(output)



