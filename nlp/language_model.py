import os
import jpype
from konlpy.utils import installpath
from konlpy.tag import Komoran

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
            print("JVM started successfully")
        except Exception as e:
            print(f"Failed to start JVM: {e}")
            raise

    return Komoran()


def analyze_sentence(komoran, sentence):
    # POS tagging
    pos_tagged = komoran.pos(sentence)
    pos_tagged = [(str(word), str(tag)) for word, tag in pos_tagged]
    
    # Morpheme analysis
    morphs = komoran.morphs(sentence)
    morphs = [str(morph) for morph in morphs]
    
    # Noun extraction
    nouns = [str(s) for s, t in pos_tagged if str(t).startswith('NN')]
    
    # Phrase extraction
    phrases = komoran.phrases(sentence)
    
    # Keyword extraction (based on noun frequency)
    noun_freq = Counter(nouns)
    keywords = noun_freq.most_common(5)  # Top 5 most frequent nouns
    
    # Sentence structure
    sentence_structure = [tag for _, tag in pos_tagged]
    
    return {
        'pos_tagged': pos_tagged,
        'morphs': morphs,
        'nouns': nouns,
        'phrases': phrases,
        'keywords': keywords,
        'sentence_structure': sentence_structure
    }