from konlpy.tag import Kkma

kkma = Kkma()

def analyze_text(text):
    # Tokenize and perform POS tagging
    pos_tagged = kkma.pos(text)
    
    # Simple grammar check (example: check if sentences end with proper endings)
    sentences = kkma.sentences(text)
    grammar_errors = []
    for i, sentence in enumerate(sentences):
        if not sentence.endswith(('다', '까', '요', '니다')):
            grammar_errors.append(f"Sentence {i+1} may be missing a proper ending.")
    
    return {
        'pos_tagged': pos_tagged,
        'grammar_errors': grammar_errors
    }