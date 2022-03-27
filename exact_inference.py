# Exact Inference in Bayes Nets Implementation

# DO NOT DELETE - THIS NEEDS TO BE INCLUDED TO BE ABLE TO READ LINES LONGER THAN 1024 BYTES
# OTHERWISE LONG INPUTS WILL FAIL
import readline

# Global variables for convenience
nodeList = []
evidenceData = None
decisionData = None
# Class for holding decision data - this was used more extensively but has been optimized out, copying was slow


class Decision:
    def __init__(self, decisionD) -> None:
        self.decisions = []
        for i in range(len(decisionD)):
            vals = decisionD[i].split()
            vals[0] = int(vals[0])
            vals[1] = int(vals[1])
            vals[2] = float(vals[2])
            self.decisions.append(vals)
# Class for holding evidence data - this was used more extensively but has been optimized out, copying was slow


class Evidence:
    def __init__(self, evidenceD) -> None:
        self.evidences = []
        for i in range(len(evidenceD)):
            vals = evidenceD[i].split()
            for i in range(len(vals)):
                vals[i] = int(vals[i])
            self.evidences.append(vals)

# Class for holding the nodes of the Bayes net


class Node:

    # Init all the values after reading it
    def __init__(self, nodeData, index) -> None:
        self.idx = index
        self.numOfValues = int(nodeData[0])
        self.numOfParents = int(nodeData[1])
        self.parents = []
        self.parentValues = 0
        self.probValues = []
        for i in range(self.numOfParents):
            if(self.parentValues == 0):
                self.parentValues = nodeList[int(nodeData[2 + i])].numOfValues
            else:
                self.parentValues *= nodeList[int(nodeData[2 + i])].numOfValues
            self.parents.append(nodeList[int(nodeData[2 + i])])

        if(self.parentValues == 0):
            vals = nodeData[2].split(',')
            for i in range(len(vals)):
                vals[i] = float(vals[i])
            self.probValues.extend(vals)
        else:
            for i in range(self.parentValues):
                vals = nodeData[2 + self.numOfParents + i].split(':', 1)

                vals[0] = vals[0].split(',')
                vals[1] = vals[1].split(',')

                index = ''
                for i in range(len(vals[0])):
                    index += vals[0][i]
                vals[0] = index
                for i in range(len(vals[1])):
                    vals[1][i] = float(vals[1][i])

                self.probValues.append(vals)

    # Finding the probability given the parents of the node, or if it does not have parents then just return
    # the corresponding value
    def probValue(self, e, valIndex) -> float:
        if(self.numOfParents <= 0):
            return self.probValues[valIndex]
        else:
            index = ''
            parentids = []
            for i in range(len(self.parents)):
                parentids.append(self.parents[i].idx)

            for i in range(len(parentids)):
                for j in range(len(e)):
                    if(parentids[i] == e[j][0]):
                        index += str(e[j][1])

            for i in range(len(self.probValues)):
                if(self.probValues[i][0] == index):
                    return self.probValues[i][1][valIndex]

# Pop the first valus of the variables list after copying it


def popFirstCopied(variables):
    copyvar = variables.copy()
    copyvar.pop(0)
    return copyvar

# Perform enumeration


def enumerateAll(variables, e) -> float:
    if(len(variables) <= 0):
        return 1.0
    y = nodeList[variables[0]]
    variables = popFirstCopied(variables)

    contains = -1

    for i in range(len(e)):
        if(e[i][0] == y.idx):
            contains = i
            break

    if(contains != -1):
        return y.probValue(e, e[contains][1]) * enumerateAll(variables, e)
    else:
        prob = 0.0
        for i in range(y.numOfValues):
            prob += y.probValue(e, i) * enumerateAll(variables,
                                                     addEvidenceCopied(e, [y.idx, i]))
        return prob

# Normalize all the values


def normalize(distribution):
    length = 0.0
    for i in range(len(distribution)):
        length += distribution[i]
    for i in range(len(distribution)):
        distribution[i] /= length
    return distribution

# Adding evidence after copying the values


def addEvidenceCopied(e, val):
    ecopy = e.copy()
    ecopy.append(val)
    return ecopy

# Perform enumeration for each possible value of the target node and construct it`s distribution


def enumerationAsk(X: Node, e, bn):
    distribution = []
    for i in range(nodeList[X].numOfValues):
        distribution.append(enumerateAll(bn, addEvidenceCopied(e, [X, i])))
    return normalize(distribution)

# Calculate the best decision based on the utilities and distribution


def bestDecision(distribution, numOfDecisions, decisionData):
    utility = [0.0] * numOfDecisions
    for i in range(len(distribution) * numOfDecisions):
        utility[i % numOfDecisions] += distribution[decisionData.decisions[i]
                                                    [0]] * decisionData.decisions[i][2]
    return utility.index(max(utility))
# Reading input, setting up structures and calling enumeration


def main():
    numOfNodes = int(input())
    nodes = []
    for i in range(numOfNodes):
        nodes.append(str(input()))

    numOfEvidenceNodes = int(input())

    evidenceNodes = []
    for i in range(numOfEvidenceNodes):
        evidenceNodes.append(str(input()))

    targetNodeIndex = int(input())

    numOfDecisions = int(input())

    decisions = []
    for i in range(int(nodes[targetNodeIndex][0]) * numOfDecisions):
        decisions.append(str(input()))

    for i in range(numOfNodes):
        nodeList.append(Node(nodes[i].split(), i))

    evidenceData = Evidence(evidenceNodes)

    decisionData = Decision(decisions)

    nodeListIndexes = []

    for i in range(len(nodeList)):
        nodeListIndexes.append(nodeList[i].idx)

    evidenceList = []

    for i in range(len(evidenceData.evidences)):
        evidenceList.append(evidenceData.evidences[i])

    distribution = enumerationAsk(
        nodeList[targetNodeIndex].idx, evidenceList, nodeListIndexes)

    for i in range(len(distribution)):
        print(str(distribution[i]))

    print(bestDecision(distribution, numOfDecisions, decisionData))

    return 0


if __name__ == "__main__":
    main()
