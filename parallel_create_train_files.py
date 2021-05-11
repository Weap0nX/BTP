import multiprocessing as mp
from multiprocessing import Queue
import time
from class_tuple import Tuple

tuple = Tuple()

def my_fun(sentence, rows, cnt):
	combined = ""
	find_flag = 0
	output = ""

	print('.')
	print("count ",cnt)

	global queue

	gpu_id = queue.get()


	print("gpu ", gpu_id)
	srl_dict = tuple.dict(sentence, gpu_id)


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

	time.sleep(0.1)
	queue.put(gpu_id)

	if find_flag == 0:
		output = target + "\t" + ques + " + " + ans + "\t" + "fluent\n"
	else:
		output = target + "\t" + combined + "\t" + "srl_fluent\n"


	print(output)

	return output

def add_to_file(sentence):
	global tgt_file
	global count
	global ts
	print("time ", time.time()-ts)
	print(count, '::')
	count += 1
	tgt_file.write(sentence)


if __name__ == '__main__':

	filenames = ["data/train.tgt", "data/train.ques", "data/train.ans"]
	files = [open(i, "r") for i in filenames]
	tgt_file = open("data/final_train.tsv", "w")

	count = 0
	cnt = 0
	ts = time.time()
	tgt_file.write("target_text\tinput_text\tprefix\n")

	NUM_GPUS = 3
	PROC_PER_GPU = 3

	queue = Queue()
	for i in range(3):
		queue.put(0)
	for i in range(3):
		queue.put(1)
	for i in range(3):
		queue.put(2)

#	for gpu_ids in range(NUM_GPUS):
#		for _ in range(PROC_PER_GPU):
#			queue.put(gpu_ids)

	pool = mp.Pool(processes=9)
	results = []

	max_len = 0

	for rows in zip(*files):
		#print(count, " : ")
		target = rows[0][:-1]
		ques = rows[1][:-1]
		ans = rows[2][:-2]
		cnt += 1
		if cnt > 103500:
			pool.apply_async(my_fun, args=(ques, rows, cnt), callback=add_to_file)

	pool.close()
	pool.join()
