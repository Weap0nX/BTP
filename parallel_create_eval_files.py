import multiprocessing as mp
import time
from class_tuple import Tuple

tuple = Tuple()
cnt = 0

def my_fun(sentence, rows):
	combined = ""
	find_flag = 0

	print('.')

	srl_dict = tuple.dict(sentence)

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

	output = ""


	if find_flag == 0:
		output = target + "\t" + ques + " + " + ans + "\t" + "fluent\n"
	else:
		output = target + "\t" + combined + "\t" + "srl_fluent\n"

	print(output)

	return output

def add_to_file(sentence):
	global tgt_file
	global count
	print(count, '::')
	count += 1
	tgt_file.write(sentence)


if __name__ == '__main__':

	filenames = ["data/val.tgt", "data/val.ques", "data/val.ans"]
	files = [open(i, "r") for i in filenames]
	tgt_file = open("data/final_eval.tsv", "w")

	count = 0
	tgt_file.write("target_text\tinput_text\tprefix\n")

	pool = mp.Pool(15)
	results = []

	max_len = 0

	for rows in zip(*files):
		#print(count, " : ")
		target = rows[0][:-1]
		ques = rows[1][:-1]
		ans = rows[2][:-2]

		pool.apply_async(my_fun, args=(ques, rows), callback=add_to_file)

	pool.close()
	pool.join()
