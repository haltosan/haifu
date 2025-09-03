from syllables import estimate
import cmudict

c_dict = cmudict.dict()

def count(w: str) -> int:
    '''Count syllables in a word'''
    # based on https://datascience.stackexchange.com/a/24865
    if w in c_dict:
        return [len(list(y for y in x if y[-1].isdigit())) for x in c_dict[w.lower()]][0]
    return estimate(w)


if __name__ == '__main__':
    # testing
    runner_f = count
    show_fails = True

    t_simple = {'bucket':2, 'expectations':4, 'happiness':3, 'summer':2, 'day':1, 'amplified':3, 'angel':2}
    t_dip = {'house':1, 'joy':1, 'food':1, 'see':1, 'foolish':2}
    t_trip = {'anxious':2, 'precious':2, 'beautiful':3, 'malicious':3}
    t_silent = {'close':1, 'made':1, 'cheese':1, 'silence':2, 'extreme':2, 'turpentine':3, 'ore':1}
    t_non_silent = {'angle':2, 'tickle':2, 'bottle':2}
    t_misc = {'announcement':3, 'columbia':4, 'tried':1, 'course':1}
    t_regres = {}
    test_words = [t_simple, t_dip, t_trip, t_silent, t_non_silent, t_misc, t_regres]

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
