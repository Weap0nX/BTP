from bleu import list_bleu
from simpletransformers.t5 import T5Model
from class_tuple import Tuple
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

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
    "num_return_sequences": 1
}

model = T5Model("t5", "outputs/best_model", args=model_args)

tuple = Tuple()

# Query format
query = "fluent: " + """
When did princess Diana die? + 31 August, 1997
"""

# User-input query
ques = input("Question : ")
ans = input("Factoid answer : ")

srl_dict = tuple.dict(ques)
print(srl_dict)
find_flag = 0
combined = ""

for phrase, tags in srl_dict.items():
	if find_flag == 0:
		for words in tuple.ques_words:
			if (phrase.lower()).find(words) != -1:
				find_flag = 1
				phrase = ans
				break
	combined += " " + phrase

if find_flag == 0:
	query = "fluent: " + ques + " + " + ans + "\n"
else:
	query = "srl_fluent: " + combined + "\n"

print(query)

preds = model.predict([query])

print("Full-length answer is :")
print(preds[0])
