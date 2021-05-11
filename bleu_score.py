from bleu import file_bleu, multi_file_bleu

hyp_file = 'data/freebase_test.tgt'
ref_files = ['data/output.txt']

bleu_scores = file_bleu(ref_files, hyp_file)


print(bleu_scores)
