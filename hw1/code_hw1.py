#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Kamal Giri

COSC 4550-COSC5550 - Introduction to AI - Homework 1
// This python code runs a small dfs algorithm to check all the 
possible states of the game from a given state and return the 
scores according to the requirements defined in the homework.
//
"""


import numpy as np

NETID = "kgiri" # Replace with your NetID!
BLANK = "_"

def state_str(state, prefix=""):
    return "\n".join("%s%s" % (prefix, "".join(row)) for row in state)

def move(state, symbol, row, col):
    if state[row,col] != BLANK: return False
    new_state = state.copy()
    new_state[row,col] = symbol
    return new_state

def score(state):
    """
    Return the score for player X in the given state.
    Use the weights for your NetID as described in written.pdf.
    [2 2 3 1]
    """
    
    inter_score = 0     # to maintain a possibility of multiple scores in a final state.
    w1 = 2
    w2 = 2
    w3 = 3
    w4 = 1
    
  
    for symbol in ['o','x']:
        if symbol == 'o':
            #for loop to go through the row and columns
            for row in range(3):
            
                
                for col in range(3):
                    if col == 0:
                        a = state[row][col]
                        d = state[col][row]
                    elif col == 1:
                        b = state[row][col]
                        e = state[col][row]
                    else:
                        c = state[row][col]
                        f = state[col][row]
                if all(x == 'o' for x in (a,b,c)):
                    inter_score-=w1
                elif all(x == 'o' for x in (d,e,f)):
                    inter_score -=w2
             #Diagonal from top-left to bottom-right
            if all(state[i,i] == 'o' for i in range(3)):
                
                inter_score -= w3
             #Diagonal from bottom-left to top-right
            if all(state[2-i, i] == 'o' for i in range(3)):
                inter_score -= w4
            
        elif symbol == 'x':
            for row in range(3):
                
                for col in range(3):
                    if col == 0:
                        a = state[row][col]
                        d = state[col][row]
                    elif col == 1:
                        b = state[row][col]
                        e = state[col][row]
                    else:
                        c = state[row][col]
                        f = state[col][row]
                if all(x == 'x' for x in (a,b,c)):
                    inter_score+=w1
                elif all(x == 'x' for x in (d,e,f)):
                    inter_score +=w2
             #Diagonal from top-left to bottom-right
            if all(state[i,i] == 'x' for i in range(3)):
                inter_score += w3
             #Diagonal from bottom-left to top-right
            if all(state[2-i, i] == 'x' for i in  range(3)):
                inter_score += w4
            
        
    return inter_score

def dfs(state, symbol):
    """
    Replace the following with your implementation.
    Return the outputs described in instructions.pdf.
    """
    leaf_count = 0
    expected_score = 0
    child_count = 0             # to keep a count of the children
    child_score = 0             # to keep a score of all the children so that their weighted average can be calculated
    

    has_child = False
    for row in range(3):
        for col in range(3):
            child = move(state, symbol, row, col)
            if child is False: continue
            has_child = True
            child_count += 1
            num_leaves, pred_score = dfs(child, "x" if symbol == "o" else "o")
            leaf_count += num_leaves
            child_score += pred_score


    if has_child is False:                                  # if it is a leaf node
        s = score(state)
        return 1 if s > 1 else 0, s
    else:                                                   # if it is not a leaf node
     
        expected_score = child_score/ child_count
        
        return leaf_count, expected_score
 

if __name__ == "__main__":
    
    state0 = np.array([[BLANK]*3]*3)
    
    state1 = move(state0, "x", 2, 2)
    state2 = move(state1, "o", 1, 0)
    state3 = move(state2, "x", 1, 1)
    print(state_str(state0))
    print(state_str(state1))
    print(state2)
    print(state3)
  
    lc, v = dfs(state2, "x")
    print("DFS: leaf count = %d, expected value = %f" % (lc, v))
    
