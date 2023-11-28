import numpy as np
import unittest as ut
import code_hw1
from test_results import test_results

def scores_equal(score1, score2):
    return np.fabs(score1 - score2) < 1e-6

class HW1TestCase(ut.TestCase):

    def test_score1(self):
        netid = code_hw1.NETID
        
        state = np.array([
            ["x","o","x"],
            ["x","o","o"],
            ["x","x","o"]])
        
        self.assertTrue(scores_equal(code_hw1.score(state), test_results[netid]["test_score1"]))
        self.assertTrue(scores_equal(code_hw1.score(np.rot90(state)), test_results[netid]["test_score1rot"]))

    def test_score2(self):
        netid = code_hw1.NETID
        
        state = np.array([
            ["x","o","x"],
            ["o","x","o"],
            ["x","o","x"]])
        
        self.assertTrue(scores_equal(code_hw1.score(state), test_results[netid]["test_score2"]))

    def test_score3(self):
        netid = code_hw1.NETID
        
        state = np.array([
            ["x","o","o"],
            ["x","x","o"],
            ["x","o","x"]])
        
        self.assertTrue(scores_equal(code_hw1.score(state), test_results[netid]["test_score3"]))

    def test_leaves1(self):
        netid = code_hw1.NETID

        state = np.array([
            ["x","o","o"],
            ["x","x","o"],
            ["x","_","_"]])
        
        leaf_count, exp_score = code_hw1.dfs(state,"x")
        self.assertTrue(leaf_count == test_results[netid]["test_leaves1"][0])
        self.assertTrue(scores_equal(exp_score, test_results[netid]["test_leaves1"][1]))

    def test_leaves2(self):
        netid = code_hw1.NETID
        
        state = np.array([
            ["x","o","x"],
            ["o","_","_"],
            ["x","_","_"]])

        leaf_count, exp_score = code_hw1.dfs(state,"x")
        self.assertTrue(leaf_count == test_results[netid]["test_leaves2"][0])
        self.assertTrue(scores_equal(exp_score, test_results[netid]["test_leaves2"][1]))

def do_tests():

    test_suite = ut.TestLoader().loadTestsFromTestCase(HW1TestCase)
    results = ut.TextTestRunner(verbosity=2).run(test_suite)
    total, errors, fails = results.testsRun, len(results.errors), len(results.failures)
    return total, errors, fails


if __name__ == "__main__":    
    
    total, errors, fails = do_tests()
    print("Score = %d out of %d (%d errors, %d failed assertions)" % (
        total - (errors + fails), total, errors, fails))




