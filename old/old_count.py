'''
sources
https://www.yourdictionary.com/articles/words-end-silent-e
https://www.howmanysyllables.com/syllable_rules/howtocountsyllables
'''


def count_1(word):
    '''https://stackoverflow.com/a/46759549'''
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    if word[0] in vowels:
        count += 1
    for i in range(1, len(word)):
        if word[i] in vowels and word[i-1] not in vowels:
            count += 1
    if word[-1] == 'e':
        count -= 1
    if count == 0:
        count += 1
    return count

def count_2(w):
    '''https://stackoverflow.com/a/50851189'''
    if len(w) <= 3:
        return 1

    if w[-2:] in ['es', 'ed'] and w[-3:] not in ['ted', 'tes', 'ses', 'ied', 'ies']:
        # find double vowels
        # find [vowel][cons]
        # if doubles or vc > 1, discard
        pass

def count_3(w):
    '''each syllable needs a vowel'''
    pass


runner_f = count_1
show_fails = True

t_simple = {'bucket':2, 'expectations':4, 'happiness':3, 'summer':2, 'day':1, 'amplified':3, 'angel':2}
t_dip = {'house':1, 'joy':1, 'food':1, 'see':1, 'foolish':2}
t_trip = {'anxious':2, 'precious':2, 'beautiful':3, 'malicious':3}
t_silent = {'close':1, 'made':1, 'cheese':1, 'silence':2, 'extreme':2, 'turpentine':3, 'ore':1}
t_non_silent = {'angle':2, 'tickle':2, 'bottle':2}
t_misc = {'announcement':3, 'columbia':4, 'tried':1, 'course':1}
t_regres = {}
test_words = [t_simple, t_dip, t_trip, t_silent, t_non_silent, t_misc. t_regres]

fails = []
for test in test_words:
    fail = 0
    for w in test.keys():
        count = runner_f(w)
        if count != test[w]:
            if show_fails:
                print(w, test[w], count)
            fail += 1
    fails.append(fail)
print('\n', fails)
