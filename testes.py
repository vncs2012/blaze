import pandas as pd
from matplotlib import pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import Adam

file = pd.read_csv('tabela_crash.csv', sep = ';')

lucro = []
for a in file['lucro']:
    lucro.append(a/100)

aposta = []
for a in file['aposta']:
    aposta.append(a)

diff = []
for a in range(len(lucro)):
    diff.append((lucro[a] - aposta[a])/100)


lista = []
total = [0, 0, 0, 0, 0, 0]
total2 = [0, 0, 0, 0, 0, 0]
percent = [0, 0, 0, 0, 0, 0]
for a in file['multiplicador']:
    lista.append(a)
    if len(lista) >= 7:
        num = len(lista)
        if num == 147:
            break
        total.append((lucro[num-1] + lucro[num-2] + lucro[num-3] + lucro[num-4]  + lucro[num-5] + lucro[num-6] + lucro[num-7])/3)
        total2.append((aposta[num-1] + aposta[num-2] + aposta[num-3] + aposta[num-4]  + aposta[num-5] + aposta[num-6] + aposta[num-7])/3)
        percent.append(100*(total[-1]/total2[-1]))
        print("Percentual: ", 100*(total[-1]/total2[-1]), end="")
        print(" Outros: ", total[-1], total2[-1], num)
# plt.plot(lucro, lista, 'o')
# plt.plot(range(len(total)), total)
# plt.plot(range(146), [1.3]*146)

dadosx = total[7:len(lucro)-2]
dadosx2 = percent[7:len(lucro)-2]
dadosy = lista[8:len(lucro)-1]
train_x = []
test_x = []

num_train = 110

for i in range(7, len(lucro)-3):
    if i < num_train+7:
        train_x.append([total[i], percent[i], lista[i+1]])
    else: 
        test_x.append([total[i], percent[i], lista[i+1]])

for a in range(len(dadosy)):
    if dadosy[a] < 1.3:
        dadosy[a] = 0
    else:
        dadosy[a] = 1

train_y = dadosy[:num_train]

test_y = dadosy[num_train+1:]

model = keras.Sequential([
    keras.layers.Dense(25, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer=Adam(learning_rate=0.0001),
              loss='mse',
              metrics=['accuracy'])

result = model.fit(train_x, train_y, 1, epochs=50,shuffle=True,)

result.history.keys()
plt.plot(result.history['accuracy'])

test_loss, test_acc = model.evaluate(test_x,  test_y, verbose=2)

print("Acertou: ", (test_acc*100), "%", sep="")

plt.show()