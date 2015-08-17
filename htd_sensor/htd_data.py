import sys

htd_data = sys.argv[1].split(',')

print("humidity ....... " + htd_data[0])
print("temp_c ......... " + htd_data[1])
print("temp_f ......... " + htd_data[2])
print("heat_index_c ... " + htd_data[3])
print("heat_index_f ... " + htd_data[4])
print("\n")
