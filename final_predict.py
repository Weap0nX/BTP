from bleu import list_bleu
from simpletransformers.t5 import T5Model


model_args = {
    "reprocess_input_data": True,
    "overwrite_output_dir": True,
    "max_seq_length": 128,
    "eval_batch_size": 4,
    "num_train_epochs": 1,
    "save_eval_checkpoints": False,
    "use_multiprocessing": False,
    # "silent": True,
    "num_beams": None,
    "do_sample": True,
    "max_length": 50,
    "top_k": 50,
    "top_p": 0.95,
    "num_return_sequences": 3,
}

model = T5Model("t5", "outputs/best_model", args=model_args)

# Query format
#query = "fluent: " + ""
#When did princess Diana die? + 31 August, 1997
#"""

# User-input query
#ques = input("Question : ")
#fact_ans = input("Factoid answer : ")
#hyp = input("Target: ")

#query = "fluent: " + ques + " + " + fact_ans

#preds = model.predict([query])

#hyp = 'Normans were in normandy during 10th and 11th centuries.'
#result = ''
#max_score = 0

#print(preds)



#for ele in preds[0]:
#	bleu_score = list_bleu([ele], [hyp])
#	print(bleu_score)
#	if bleu_score > max_score:
#		max_score = bleu_score
#		result = ele

#print(result)

# Read query from files
#test_file = open("final_test.tsv", "r")
filenames = ["data/final_test.tsv", "data/freebase_test.tgt"]
pred_file = open("data/output.txt", "w")

files = [open(i, "r") for i in filenames]


cnt = 0

#for line in test_file:
#	print(cnt, " : ")
#	preds = model.predict([line])
#	cnt += 1
#	pred_file.write(preds[0] + "\n")



for rows in zip(*files):
	preds = model.predict([rows[0]])
	hyp = rows[1][:-1]
	result = ''
	max_score = -1

	for ele in preds[0]:
		bleu_score = list_bleu([ele], [hyp])
		if bleu_score > max_score:
			max_score = bleu_score
			result = ele

	cnt += 1
	pred_file.write(result + "\n")
	print(cnt, " : ", max_score, " : ", result)


