import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jvmpath import java_home
import jpype

if not jpype.isJVMStarted():
    try:
        jpype.startJVM(convertStrings=False)
    except Exception as e:
        print(f"Error starting JVM: {e}")
        sys.exit(1)

from konlpy.tag import Kkma
import re

kkma = Kkma()

def analyze_text(text):
    # Tokenization and POS tagging
    pos_tagged = kkma.pos(text)
    
    # Sentence splitting
    sentences = kkma.sentences(text)
    
    # Grammar checking
    grammar_errors = []
    for i, sentence in enumerate(sentences):
        # Check for subject-object-verb order
        sov_check = check_sov_order(pos_tagged)
        if sov_check:
            grammar_errors.append(f"Sentence {i+1}: {sov_check}")
        
        # Check for particle usage
        particle_check = check_particle_usage(pos_tagged)
        if particle_check:
            grammar_errors.append(f"Sentence {i+1}: {particle_check}")
        
        # Check for conjugation
        conj_check = check_conjugation(pos_tagged)
        if conj_check:
            grammar_errors.append(f"Sentence {i+1}: {conj_check}")
        
        # Check for non-Korean words (except for common exceptions like API)
        non_korean = check_non_korean(sentence)
        if non_korean:
            grammar_errors.append(f"Sentence {i+1}: Contains non-Korean word(s): {', '.join(non_korean)}")
    
    return {
        'pos_tagged': pos_tagged,
        'grammar_errors': grammar_errors
    }

# ... (rest of the helper functions like check_sov_order, check_particle_usage, etc.)