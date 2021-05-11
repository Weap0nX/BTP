filename =  input("filename: ")
file = open(filename, "r")
cnt = 0

for line in file:
	cnt += 1
	if (cnt>=245500) and (cnt<=245510):
		print(line)

print(cnt)

file.close()
