from thefuzz import fuzz


def readfile_no_strip(filepath):
    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()
    return lines


def writefile(filepath, lines):  # need to have \n's inserted already
    f = open(filepath, 'w')
    f.writelines(lines)
    f.close()
    return


def match_names(name, list):
    min_match = 75
    matches = []
    for i, list_name in enumerate(list):
        score = fuzz.ratio(name, list_name)
        if score > min_match:
            matches.append([list_name, score])
    return matches
