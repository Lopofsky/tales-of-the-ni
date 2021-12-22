d = {'test':{}}
d['rarity'] = 1/1000
d['test']['true positive'] = 99/100

d['normality'] = 1 - d['rarity']
d['test']['false positive'] = 1 - d['test']['true positive']

# The Event Where You Test Positive And You Actually Have The Disease, Given The Prior Probability:
up = d['test']['true positive'] * d['rarity']
# The Event Where You Test FALSELY Positive And You Don't Actually Have The Disease, Given The Prior Probability:
down = up + (d['normality'] * d['test']['false positive'])
d['Result Actual %'] = up / down

'''
# The Event aka "Tested Positive":
P(E) = P(E|H)*P(H) + P(E|-H)*P(-H)
####### INDEX: ############
    # Actually Have the Disease - aka Prior Probability of Having The Disease:
    # _____This Is The Hardest Part To Quantify & Most Probably A Guess____
        P(H) = d['rarity'] 
    # Probability Of Not Having The Disease:
        P(-H) = 1 - d['rarity']
    # Probability Of Tested Positive IFF You Actually Have The Disease:
        P(E|H) = d['test']['true positive']
    # Probability Of Tested Positive AND NOT Actually Have The Disease:
        P(E|-H) = 1 - d['test']['false positive']
    ***Actual % ***
        P(H|E) = P(E|H)*P(H) / P(E|H)*P(H) + P(E|-H)*P(-H)
'''
def rec(d):
    for k,v in d.items():
        if type(v) == dict: rec(v)
        else:
            if k.lower().startswith('result') > 0: title = ">>>>>> " + k.lower().replace("result", "").strip().title()
            else: title = k.title()
            print(title + " = " + str(round(v,3)*100)+'%')
rec(d)