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
    pos_tagged = komoran.pos(sentence)
    pos_tagged = [(str(word), str(tag)) for word, tag in pos_tagged]
    
    morphs = komoran.morphs(sentence)
    morphs = [str(morph) for morph in morphs]
    
    nouns = komoran.nouns(sentence)
    nouns = [str(noun) for noun in nouns]
    
    return {
        'pos_tagged': pos_tagged,
        'morphs': morphs,
        'nouns': nouns
    }