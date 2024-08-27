import unittest
from grammar_checker import (
    komoran,
    check_sov_order,
    check_sentence_completeness,
    check_proper_ending,
    check_case_particles,
    check_honorific_consistency,
    check_grammar
)

class TestGrammarChecker(unittest.TestCase):

    def test_sov_order(self):
        correct = komoran.pos("나는 사과를 먹었다.")
        self.assertIsNone(check_sov_order(correct))
        
        no_subject = komoran.pos("사과를 먹었다.")
        self.assertIsNotNone(check_sov_order(no_subject))
        
        no_verb = komoran.pos("나는 사과를.")
        self.assertIsNotNone(check_sov_order(no_verb))

    def test_sentence_completeness(self):
        complete = komoran.pos("나는 간다.")
        self.assertIsNone(check_sentence_completeness(complete))
        
        incomplete = komoran.pos("나는.")
        self.assertIsNotNone(check_sentence_completeness(incomplete))

    def test_proper_ending(self):
        proper_ending = komoran.pos("이것은 책이다.")
        self.assertIsNone(check_proper_ending(proper_ending))
        
        improper_ending = komoran.pos("이것은 책")
        self.assertIsNotNone(check_proper_ending(improper_ending))

    def test_case_particles(self):
        with_particles = komoran.pos("나는 책을 읽는다.")
        self.assertIsNone(check_case_particles(with_particles))
        
        without_particles = komoran.pos("나 책 읽는다.")
        self.assertIsNotNone(check_case_particles(without_particles))

    def test_honorific_consistency(self):
        consistent = komoran.pos("제가 갑니다.")
        self.assertIsNone(check_honorific_consistency(consistent))
        
        inconsistent = komoran.pos("제가 간다.")
        self.assertIsNotNone(check_honorific_consistency(inconsistent))

    def test_check_grammar(self):
        correct_sentence = "나는 어제 친구와 함께 영화를 봤어요."
        self.assertEqual(len(check_grammar(correct_sentence)), 0)
        
        incorrect_sentence = "나 어제 친구 영화 봤어"
        self.assertGreater(len(check_grammar(incorrect_sentence)), 0)

if __name__ == '__main__':
    unittest.main()