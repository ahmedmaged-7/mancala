def Utility(data):

    Score = 0
    Score -= sum(data.data[0:6])
    Score += sum(data.data[6:])

    for i, l in enumerate(data.data[0:6]):
        if l + i > 6:
            Score -= 1

    for i, l in enumerate(data.data[6:]):
        if l + i > 6:
            Score += 1

    return Score + 4 * (data.score[1] - data.score[0])
