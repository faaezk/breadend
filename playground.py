

last_file_update = 8391736193721

last_file_update = str(last_file_update)[:-3]

last_num = int(str(last_file_update)[-1])
last_num += 1
last_file_update = int(str(last_file_update)[:-1] + str(last_num))

print(last_num)
print(last_file_update)