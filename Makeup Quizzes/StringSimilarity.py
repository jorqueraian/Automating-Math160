import numpy as np


def align_strings(x, y, c_insert, c_delete, c_sub):
    nx = len(x) + 1
    ny = len(y) + 1

    S = np.array([[0 for _ in range(ny)] for _ in range(nx)])

    for i in range(nx):
        for j in range(ny):
            # Iterate through matrix
            if i > 0 and j > 0:
                if x[i-1] in y[j-1]:  # is or in?
                    # This checks if we can do a no-op
                    # Min(no-op, inset, del)
                    S[i, j] = min(S[i-1, j-1], S[i, j-1]+c_insert, S[i-1, j]+c_delete)
                else:
                    # Min(sub, insert, del)
                    S[i, j] = min(S[i - 1, j - 1] + c_sub, S[i, j - 1] + c_insert, S[i - 1, j] + c_delete)
            elif j is 0 and i is 0:
                # when an empty string is compared with an empty string
                S[i, j] = 0
            elif i is 0:
                # This builds up our base cases when one of the strings in empty
                S[i, j] = S[i, j - 1] + c_insert
            else:  # j is 0
                S[i, j] = S[i - 1, j] + c_delete
    return S


def cost_of_alignment(x, y, c_insert, c_delete, c_sub):
    alignment_matrix = align_strings(x, y, c_insert, c_delete, c_sub)
    return alignment_matrix[len(x), len(y)]


def extract_alignment(S, x, y, c_insert, c_delete, c_sub):
    i = len(x)
    j = len(y)

    alignments = []

    while i > 0 and j > 0:
        # We want tp check each possibility. If one of the paths, or the parent plus the cost is equal to S[i,j] we
        # know that's a possible move we can make
        if x[i-1] in y[j-1] and S[i, j] == S[i-1, j-1]:
            alignments.append('No-op')
            i -= 1
            j -= 1
            continue
        elif S[i, j] == S[i-1, j-1] + c_sub:
            alignments.append('Sub')
            i -= 1
            j -= 1
            continue
        elif S[i, j] == S[i, j-1] + c_insert:
            alignments.append('Insert')
            j -= 1
            continue
        else:
            # We can put an else her because we know there must be a parent node
            alignments.append('Delete')
            i -= 1
            continue
    # At the end our algorithm might stop at [2,0] meaning its missing 2 additional deletions
    if i > 0:
        for _ in range(i):
            alignments.append('Delete')
    if j > 0:
        for _ in range(j):
            alignments.append('Insert')

    return list(reversed(alignments))


def common_substrings(x, L, a):
    i = 0
    subsequences = []
    sequence = []
    for j in a:
        if j == 'No-op':
            sequence.append(x[i])
        elif len(sequence) > 0:
            subsequences.append(sequence)
            sequence = []
        if j == 'Insert':
            continue
        i += 1
    subsequences.append(sequence)
    return [("".join(s), len(s)) for s in subsequences if len(s) >= L]



