import pytest
from nlp.grammar_checker import (
    check_sov_order,
    check_sentence_completeness,
    check_proper_ending,
    check_case_particles,
    check_honorific_consistency,
    check_grammar
)
from nlp.language_model import initialize_komoran

@pytest.fixture(scope="module")
def komoran():
    return initialize_komoran()

def test_sov_order(komoran):
    correct = komoran.pos("나는 사과를 먹었다.")
    assert check_sov_order(correct) is None
    
    no_subject = komoran.pos("사과를 먹었다.")
    assert check_sov_order(no_subject) is not None
    
    no_verb = komoran.pos("나는 사과를.")
    assert check_sov_order(no_verb) is not None

def test_sentence_completeness(komoran):
    complete = komoran.pos("나는 간다.")
    assert check_sentence_completeness(complete) is None
    
    incomplete = komoran.pos("나는.")
    assert check_sentence_completeness(incomplete) is not None

def test_proper_ending(komoran):
    proper_ending = komoran.pos("이것은 책이다.")
    assert check_proper_ending(proper_ending) is None
    
    improper_ending = komoran.pos("이것은 책")
    assert check_proper_ending(improper_ending) is not None

def test_case_particles(komoran):
    with_particles = komoran.pos("나는 책을 읽는다.")
    assert check_case_particles(with_particles) is None
    
    without_particles = komoran.pos("나 책 읽는다.")
    assert check_case_particles(without_particles) is not None

def test_honorific_consistency(komoran):
    consistent = komoran.pos("제가 갑니다.")
    assert check_honorific_consistency(consistent) is None
    
    inconsistent = komoran.pos("제가 간다.")
    assert check_honorific_consistency(inconsistent) is not None

def test_check_grammar(komoran):
    correct_sentence = komoran.pos("나는 어제 친구와 함께 영화를 봤어요.")
    assert len(check_grammar(correct_sentence)) == 0
    
    incorrect_sentence = komoran.pos("나 어제 친구 영화 봤어")
    assert len(check_grammar(incorrect_sentence)) > 0