import matplotlib.pyplot as plt

with open('transfer_time_logs.txt') as infile:
    transfer_time = [[int(i) for i in line.strip().split('/n')] for line in infile]

suma = 0
for t in transfer_time:
    suma = suma + t[0]

print(suma / len(transfer_time))

transfer_number = range(len(transfer_time))

plt.plot(transfer_number, transfer_time, color='g')

plt.xlabel('Broj prijenosa')
plt.ylabel('Proteklo vrijeme izvršavanja u ms')
plt.title('Proteklo vrijeme prijenosa podataka između vozila i računala')
plt.show()