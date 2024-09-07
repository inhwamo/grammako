import os
import jpype
import logging
from konlpy.utils import installpath
from konlpy.tag import Komoran
from collections import Counter
from .pos_tags import POS_TAG_TRANSLATIONS, SIMPLIFIED_POS_TAGS
import nltk

def initialize_komoran():
    java_home = os.environ.get('JAVA_HOME')
    if not java_home:
        raise ValueError("JAVA_HOME is not set")

    jvmpath = f"{java_home}/lib/server/libjvm.dylib"
    if not os.path.exists(jvmpath):
        raise FileNotFoundError(f"JVM not found at {jvmpath}")

    if not jpype.isJVMStarted():
        try:
            jpype.startJVM(jvmpath, "-Djava.class.path=" + os.environ.get('CLASSPATH', ''), convertStrings=False)
            logging.info("JVM started successfully")
        except Exception as e:
            logging.error(f"Failed to start JVM: {e}")
            raise

    return Komoran()

def analyze_sentence(komoran, sentence):
    logging.debug(f"Analyzing sentence: {sentence[:50]}...")  # Log first 50 chars
    
    try:
        # POS tagging
        pos_tagged = komoran.pos(sentence)
        pos_tagged = [(str(word), str(tag)) for word, tag in pos_tagged]
        simplified_pos_tagged = [(word, SIMPLIFIED_POS_TAGS.get(tag, tag)) for word, tag in pos_tagged]
        
        # Morpheme analysis
        morphs = komoran.morphs(sentence)
        morphs = [str(morph) for morph in morphs]
        
        # Custom noun extraction
        nouns = [word for word, tag in pos_tagged if tag.startswith('NN')]
        
        # Keyword extraction (based on noun frequency)
        noun_freq = Counter(nouns)
        keywords = noun_freq.most_common(5)  # Top 5 most frequent nouns
        
        # Sentence structure
        sentence_structure = [tag for _, tag in pos_tagged]
        
        # Phrasal Chunking
        chunks = chunk_sentence(pos_tagged)
        
        return {
            'original_text': sentence,
            'pos_tagged': pos_tagged,
            'simplified_pos_tagged': simplified_pos_tagged,
            'morphs': morphs,
            'nouns': nouns,
            'keywords': keywords,
            'sentence_structure': sentence_structure,
            'chunks': chunks
        }
    except Exception as e:
        logging.error(f"Error in analyze_sentence: {str(e)}", exc_info=True)
        raise

def chunk_sentence(pos_tagged):
    grammar = """
    NP: {<N.*>*<Suffix>?}   # Noun phrase
    VP: {<V.*>*}            # Verb phrase
    AP: {<A.*>*}            # Adjective phrase
    SP: {<NP><Josa>?}       # Subject phrase
    """
    parser = nltk.RegexpParser(grammar)
    tree = parser.parse(pos_tagged)
    
    chunks = {
        'noun_phrases': [],
        'verb_phrases': [],
        'adjective_phrases': [],
        'subject_phrases': []
    }
    
    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            chunks['noun_phrases'].append(' '.join(word for word, tag in subtree.leaves()))
        elif subtree.label() == 'VP':
            chunks['verb_phrases'].append(' '.join(word for word, tag in subtree.leaves()))
        elif subtree.label() == 'AP':
            chunks['adjective_phrases'].append(' '.join(word for word, tag in subtree.leaves()))
        elif subtree.label() == 'SP':
            chunks['subject_phrases'].append(' '.join(word for word, tag in subtree.leaves()))
    
    return chunks