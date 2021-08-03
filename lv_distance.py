'''
https://xo.dev/hacking-command-recommendation/

Levenshtein distance 
'''
import numpy as np

def levenshtein(source: str, target: str) -> int:
    dist = np.zeros((len(source)+1, len(target)+1))

    for i in range(len(source)+1):
        dist[i,0] = i
    for i in range(len(target)+1):
        dist[0,i] = i
    ### calculate levenshtein distance for source
    for i in range(1,len(source)+1):
        for j in range(1,len(target)+1):
            #substitutionCost = abs(ord(source[i-1]) - ord(target[j-1]))
            substitutionCost = int(source[i-1] != target[j-1])
            dist[i,j] = min(dist[i-1,j] + 1,
                            dist[i,j-1] + 1,
                            dist[i-1,j-1] + substitutionCost)
    return dist[len(source),len(target)]

def didYouMean(command : str, commands : list, limit = 5) -> list:
    candidates = []
    minDist = np.inf

    for candidate in commands:
        dist = levenshtein(command, candidate)
        if len(candidate) == dist:
            dist = np.inf
        if candidate.startswith(command):
            dist = 0
        candidates.append( {'dist' : dist, 'command' : candidate} )
        minDist = min(minDist, dist)
    sorted_candidates = sorted(candidates, 
                               key=lambda k : k['dist'])

    out = list(d['command'] for d in sorted_candidates if d['dist'] <= minDist+2)
    #return list({'key': d['dist'], 'command': d['command']} for d in sorted_candidates if d['dist'] <= minDist)
    return out[:5]



if __name__ == "__main__":
    available_commands = [
      "add",
      "am",
      "bisect",
      "branch",
      "checkout",
      "cherry-pick",
      "clean",
      "commit",
      "diff",
      "fsck",
      "init",
      "mv",
      "push",
      "rebase",
      "reset",
      "restore",
      "revert",
      "rm",
      "show",
      "sparse-checkout",
      "stage",
      "stash",
      "status",
      "svn",
      "switch",
      "tag",
    ]

    a = didYouMean('st', available_commands)
    print(a)

