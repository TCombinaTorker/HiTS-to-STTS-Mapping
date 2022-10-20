#!/usr/bin/python3

import sys
import re
import fileinput

hits_to_stts = {
    'ADJN': 'ADJA',
    'ADJS': 'ADJA',
    'AVD': 'ADV',
    'AVNEG': 'ADV',
    'AVG': 'PWAV',
    'AVW': 'PWAV',
    'APPR': 'APPR',
    'APPO': 'APPO',
    'CARDA': 'CARD',
    'CARDD': 'CARD',
    'CARDN': 'CARD',
    'CARDS': 'CARD',
    'DDART': 'ART',
    'DDA': 'PDAT',
    'DDS': 'PDS',
    'DDN': 'PDAT',
    'DDD': 'PDAT',
    'DIA': 'PIAT',
    'DIART': 'ART',
    'DID': 'PDAT',
    'DIN': 'PDAT',
    'DRELS': 'PRELS',
    'DPOSA': 'PPOSAT',
    'DPOSN': 'PPOSAT',
    'DPOSD': 'PPOSS',
    'DPOSGEN': 'PPOSAT',
    'DPOSS': 'NN',
    'DWA': 'PWAT',
    'DWN': 'PWAT',
    'DWS': 'PWS',
    'DWD': 'PWS',
    'KO*': 'KOUS',
    'NA': 'NN',
    'PAVAP': 'PAV',
    'PAVD': 'PAV',
    'PAVG': 'PAV',
    'PAVREL': 'PWAV',
    'PAVW': 'PWAV',
    'VVPS': 'ADJA',
    'VAPS': 'ADJA',
    'VMPS': 'ADJA',
    # TODO: ASK 'PW', 'PI', 'DIS', 'DGA', 'PGA', 'DGS', 'PG', 'VAIMP'
    # Andere Wortarte
    'PI':'PIS',
    'VVFIN': 'VVFIN',
    'NE': 'NE',
    'VVIMP': 'VVIMP',
    'PPER': 'PPER',
    'VAFIN':'VAFIN',
    'VAIMP':'VAIMP',
    'VMFIN':'VMFIN',
    'ADJA':'ADJA',
    'VMINF': 'VMINF',
    'ADJD' : 'ADJD',
    #externe
    'PW' : 'PWS',
    'PI'  : 'PIS',
    'DIS' : 'PIS',
    'DGA' : 'PWAT',
    'DGS' : 'PWS',
    'PG'  : 'PWS',
    'PGA' : 'PWAT',
}

unknown_pos = set()

def get_pos(tag):
    return tag.split('.', 1)[0]

def convert(pos):
    if pos in hits_to_stts.keys():
        return hits_to_stts[pos]
    elif pos in hits_to_stts.values():
        return pos
    else:
        global unknown_pos
        unknown_pos.add(pos)
        return pos

# Diese Mapping-Funktion können Sie in anderen Programmen verwenden:
def map_tag(tag):
    # Mehrdeutige Merkmale durch * ersetzen
    tag = tag.replace("Masc,Neut", "*").replace("Fem,Masc", "*").replace("Fem,Neut", "*").replace("Masc,Fem","*")
    # ADVERB
    match = re.match(r'(AVG)', tag)
    if match:
        return convert(tag)

    # Adjektive
    match = re.match(r'(ADJA|ADJD|ADJN|ADJS)\.?(Pos|Comp|Sup|\*)?\.?(Masc|Fem|Neut|\*)?\.?(Nom|Gen|Dat|Akk|\*)?\.?(Sg|Pl|\*)?\.?(st|wk|\*)?', tag)
    if match:
        pos, degree, gender, case, number, strength = match.group(1,2,3,4,5,6)
        if case == 'Akk':
            case = 'Acc'
        return '.'.join(filter(lambda x : x, [convert(pos), degree, case, number, gender]))
        
    # Nomen
    match = re.match(r'(NA|CARDD|CARDA|CARDN|CARDS|DDA|DDART|DDD|DDN|DDS|DGA|DGS|DIA|DIART|DID|DIN|DIS|DPOSA|DPOSN|DPOSS|DRELS|DWA|DWD|DWS|NA|NE|PG|PI|PW)\.?(Masc|Fem|Neut|\*)?\.?(Nom|Gen|Dat|Akk|\*)?\.?(Sg|Pl|\*)?\.?(st|wk|\*)?', tag)
    if match:
        pos, gender, case, number, strength = match.group(1,2,3,4,5)
        if case == 'Akk':
            case = 'Acc'
        return '.'.join(filter(lambda x : x, [convert(pos), case, number, gender]))
    # PPER
    match = re.match(r'(PPER)\.?(Masc|Fem|Neut|\*)?\.?(Nom|Gen|Dat|Akk|\*)?\.?(Sg|Pl|\*)?\.?(st|wk|\*)?(1|2|3|\*)?', tag)
    if match:
        pos, gender, case, number, strength, person = match.group(1,2,3,4,5,6)
        if case == 'Akk':
            case = 'Acc'
        return '.'.join(filter(lambda x : x, [convert(pos), person, case, number, gender]))
    # Verb
    match = re.match(r'(VAFIN|VAIMP|VMFIN|VVFIN|VVIMP)\.?(Ind|Subj|\*)?\.?(Past|Pres\*)?\.?(Sg|Pl|\*)?\.?(1|2|3|\*)?', tag)
    if match:
        pos, mood, tense, number, person = match.group(1,2,3,4,5)
        return '.'.join(filter(lambda x : x, [convert(pos), person, number,tense, mood]))
    
    # alles andere
    return tag



with open('HiTS-tagset.txt') as f:
    hits = f.read().splitlines()


with open('Tiger_v8_tagset.txt') as f:
    stts = f.read().splitlines()



mapped =list (map(map_tag, hits))
hits = set(hits)
stts = set(stts)

# Hier werden die Tags aus der Argumentdatei eingelesen,
# abgebildet, und sortiert ausgegeben.


print((set(mapped)-stts))
print('fehler: ',len(set(mapped)-stts))
print('Unknown POS list:', unknown_pos)
