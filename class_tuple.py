from allennlp.predictors.predictor import Predictor
from contextlib import ExitStack
import allennlp_models.tagging

class Tuple:

	def __init__(self):
		self.sentence = "John broke the window"
		self.predictor_srl = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz", cuda_device=2)

	ques_words = ['what', 'where', 'which', 'who', 'how', 'when']

	def create_tuple(self, tags, words):
		temp_tok=[]
		count=1
		class_label=0
		class_begin=0
		final_dic={}
		flag=0
		flag2=0

	#	print(tags)
	#	print(words)
		for i,j in zip(tags,words):
			count+=1
			if i !='O':
				if i.split('-')[0]=='B':
					if class_label!=i.split('-')[-1] and class_begin!='B' and len(temp_tok)!=0:
						# print('1',temp_tok)
						final_dic[' '.join(temp_tok)]=class_label
					elif len(temp_tok)!=0:
						# print('2',temp_tok)
						final_dic[' '.join(temp_tok)]=class_label
					temp_tok=[]
					class_label=0
					class_begin=i.split('-')[0]
					class_label=i.split('-')[-1]
					temp_tok.append(j)
				elif i.split('-')[0]=='I':
					temp_tok.append(j)
					class_begin=i.split('-')[0]
				if count>len(words):
					# print('3',temp_tok)
					final_dic[' '.join(temp_tok)]=class_label
					temp_tok=[]
			else :
				if len(temp_tok)!=0:
					final_dic[' '.join(temp_tok)] = class_label
				temp_tok = []
				class_label = 0
				class_begin= 0
				final_dic[j] = i
			if count>len(words) and len(temp_tok)!=0:
				# print('4',temp_tok)
				final_dic[' '.join(temp_tok)]=class_label
				temp_tok=[]
		return(final_dic)


	def dict(self, sentence):
		# predictor_srl = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/bert-base-srl-2020.03.24.tar.gz")
#		predictor_srl = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz", cuda_device=2)
		# predictor_srl = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/bert-base-srl-2019.06.17.tar.gz")


		value_srl = self.predictor_srl.predict(sentence.rstrip('\n'))
		#print("\n\nValue SRL:= ", value_srl)
		# print("value_srl['verbs']:= ", value_srl['verbs'])

		temp_dic = {}
		if len(value_srl['verbs'])!=0:
			for verbs in value_srl['verbs']:
				# print("verbs[tags]:= ", verbs['tags'])
				final_dic = {}
				final_dic['fuck'] = 'off'
				final_dic = self.create_tuple(verbs['tags'],value_srl['words'])
				if len(temp_dic) == 0:
					temp_dic = final_dic
				if len(final_dic) < len(temp_dic):
					temp_dic = final_dic
		#print("Sentence= ", sentence)
		#print("Final dictionary= ", temp_dic)


		return (temp_dic)



