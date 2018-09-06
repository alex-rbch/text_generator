from random import randint
import re
import pickle

reg = re.compile('[^a-zA-Z ]')


class Model:
    def __init__(self):
        try:
            open('maps.pickle')
        except IOError:
            print(10)
            maps = {}
            with open('maps.pickle', 'wb') as handle:
                pickle.dump(maps, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('maps.pickle', 'rb') as handle:
            self.maps = pickle.load(handle)

    def fit(self, file_name):
        try:
            f = open(file_name, "r")
        except IOError:
            print("No such file")
            return
        for line in f:
            line = reg.sub('', line)
            words = line.split()
            length = len(words)
            if length != 0:
                words[0] = words[0].lower()
            for i in range(length - 1):
                words[i + 1] = words[i + 1].lower()
                if self.maps.get(words[i], -1) == -1:
                    self.maps[words[i]] = [0, {words[i + 1]: 0}]
                else:
                    if self.maps[words[i]][1].get(words[i + 1], -1) == -1:
                        self.maps[words[i]][1][words[i + 1]] = 0
                self.maps[words[i]][1][words[i + 1]] += 1
                self.maps[words[i]][0] += 1

        with open('maps.pickle', 'wb') as handle:
            pickle.dump(self.maps, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def generate(self, first_word, n):
        stop = False
        number_of_words = n
        word = first_word
        while not stop and (number_of_words > 0):
            number_of_words -= 1
            print(word, end=" ")
            if self.maps.get(word, -1) != -1:
                ran = randint(1, self.maps[word][0])
                loc = 0
                for x, y in self.maps[word][1].items():
                    loc += y
                    if loc >= ran:
                        word = x
                        break
            else:
                stop = True
        print("")


model = Model()
print(model.maps)
print("Insert the number of expected operations:")
number_of_operations = int(input())
print("For education of model type 0 and filename")
print("In order to generate your own text, type 1, number of words and first word")

for i in range(number_of_operations):
    type_of_operation = int(input())
    if type_of_operation == 0:
        filename = input()
        model.fit(filename)
        print(model.maps)
    else:
        text_length = int(input())
        first_word = input()
        model.generate(first_word, text_length)




