def Utility( data,score):
    Score = 0
    Score -= sum(data[0:6])
    Score += sum(data[6:])
    for i, l in enumerate(data[0:6]):
        if l + i > 6:
            Score -= 1
        elif i + l == 6:
            Score -= 3
    for i, l in enumerate(data[6:]):
        if l + i > 6:
            Score += 1
        elif i + l == 6:
            Score += 4

    return Score + 4 * (score[1] - score[0])
