def calibrate_digits(line):
    lptr = 0
    rptr = len(line) - 1
    
    while not line[lptr].isdigit() and lptr < len(line) - 1:
        lptr += 1

    numstr = ''.join(line[lptr])

    while not line[rptr].isdigit() and rptr > -1:
        rptr -= 1

    numstr = ''.join([numstr, line[rptr]])

    return (numstr, lptr, rptr)

def calibrate_words(line):
    lptr = 0
    ldig = None
    lfound = False
    rptr = len(line) - 1
    rdig = None
    rfound = False
    words_to_digits = {'one': 1,
                       'two': 2,
                       'three': 3,
                       'four': 4,
                       'five': 5,
                       'six': 6,
                       'seven': 7,
                       'eight': 8,
                       'nine': 9}
    
    while not lfound and lptr < len(line):
        for (word, digit) in words_to_digits.items():
            if line[lptr:].startswith(word):
                ldig = digit
                lfound = True
                lptr -= 1
                break

        lptr += 1

    while not rfound and rptr > -1:
        for (word, digit) in words_to_digits.items():
            if line[rptr:].startswith(word):
                rdig = digit
                rfound = True
                rptr += 1
                break
        
        rptr -= 1

    numstr = ''.join([str(ldig), str(rdig)])

    return (numstr, lptr, rptr)


def get_correct_calibration(c1, c2):
    dig_pair1, l1, r1 = c1
    dig_pair2, l2, r2 = c2

    if l1 < l2 and r1 < r2:
        return int(''.join([dig_pair1[0], dig_pair2[1]]))
    elif l1 < l2 and r1 > r2:
        return int(dig_pair1)
    elif l1 > l2 and r1 < r2:
        return int(dig_pair2)
    elif l1 > l2 and r1 > r2:
        return int(''.join([dig_pair2[0], dig_pair1[1]]))


def get_correct_calibrations(c1s, c2s):
    return [get_correct_calibration(c1s[i], c2s[i]) for i in range(len(c1s))]


def sum_calibrate(text):
    lines = text.split('\n')
    lines = [line.lstrip() for line in lines]

    calibrate_only_digits = [calibrate_digits(line) for line in lines]
    calibrate_only_words = [calibrate_words(line) for line in lines]
    
    correct_calibrations = get_correct_calibrations(calibrate_only_digits, calibrate_only_words)

    return sum(correct_calibrations)
    
if __name__ == '__main__':
    test1 = """1abc2
               pqr3stu8vwx
               a1b2c3d4e5f
               treb7uchet"""

    assert(sum_calibrate(test1) == 142)

