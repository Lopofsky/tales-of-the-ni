# Init Source: http://blog.javascriptroom.com/2013/01/21/markov-chains/
# StackOverflow Post that the original author of the article helped me to make the js2py "translation":
# https://stackoverflow.com/questions/14816100/convert-text-prediction-script-markov-chain-from-javascript-to-python

from collections import defaultdict
from random import choice as rand_choice

class Markov:
    memory = defaultdict(list)
    separator = ' '

    def learn(self, txt):
        for part in self.breakText(txt):
            key = part[0]
            value = part[1]
            self.memory[key].append(value)

    def ask(self, seed=()):
        ret = []
        if not seed:
            seed = self.getInitial()
        while True:
            link = self.step(seed)
            if link is None:
                break
            ret.append(link[0])
            seed = link[1]
        return self.separator.join(ret)

    def breakText(self, txt):
        #our very own (ε,ε)
        prev = self.getInitial()
        for word in txt.split(self.separator):
            yield prev, word
            prev = (prev[1], word)
        #end-of-sentence, prev->ε
        yield (prev, '')

    def step(self, state):
        choice = rand_choice(self.memory[state] or [''])
        if not choice:
            return None
        nextState = (state[1], choice)
        return choice, nextState

    def getInitial(self):
        return ('', '')


bob = Markov()
bob.learn('Mary had a little lamb')
print(bob.ask())
bob.learn('Bob had a giant crab')
print(bob.ask(('Mary', 'had')))
bob.learn('Mary had a ball')
print(bob.ask(('Bob', 'had')))
bob.learn('Jack had a supercalafrazelistic lazer')
print(bob.ask(('Jack', 'had')))
bob.learn('Jack had a supercalafrazelistic bazooka')
bob.learn('Jack had a supercalafrazelistic starship')
print(bob.ask())