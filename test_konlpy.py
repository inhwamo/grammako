import os
import sys
import jpype
import platform
from konlpy.utils import installpath
from konlpy.tag import Komoran
from set_classpath import set_classpath

set_classpath()

print(f"Python version: {sys.version}")
print(f"Python architecture: {platform.machine()}")
print(f"sys.prefix: {sys.prefix}")

java_home = os.environ.get('JAVA_HOME')
if not java_home:
    raise ValueError("JAVA_HOME is not set")

print(f"JAVA_HOME: {java_home}")

jvmpath = f"{java_home}/lib/server/libjvm.dylib"
print(f"JVM path: {jvmpath}")
print(f"JVM path exists: {os.path.exists(jvmpath)}")

konlpy_jar = os.path.join(installpath, 'java', 'komoran-3.0.jar')
print(f"KoNLPy JAR path: {konlpy_jar}")
print(f"KoNLPy JAR exists: {os.path.exists(konlpy_jar)}")

if not jpype.isJVMStarted():
    try:
        jpype.startJVM(jvmpath, "-Djava.class.path=" + os.environ.get('CLASSPATH', ''), convertStrings=False)
        print("JVM started successfully")
    except Exception as e:
        print(f"Failed to start JVM: {e}")
        raise

komoran = Komoran()
print("KoNLPy Komoran initialized successfully")

def check_grammar(sentence):
    issues = []
    pos_tagged = komoran.pos(sentence)
    
    # Convert Java strings to Python strings
    pos_tagged = [(str(word), str(tag)) for word, tag in pos_tagged]

    # Rule 1: Check if the sentence ends with a proper ending (EF or SF)
    if pos_tagged[-1][1] not in ['EF', 'SF']:
        issues.append("Sentence may be missing a proper ending.")

    # Rule 2: Check for subject-object-verb order
    has_subject = any(tag in ['NP', 'NNG', 'NNP'] for _, tag in pos_tagged)
    has_object = any(tag == 'JKO' for _, tag in pos_tagged)  # Object particle
    has_verb = any(tag.startswith('V') for _, tag in pos_tagged)
    if has_verb and not has_subject:
        issues.append("Sentence may be missing a subject.")
    if has_object and not has_verb:
        issues.append("Sentence has an object but may be missing a verb.")

    # Rule 3: Check for repeated particles
    particle_count = sum(1 for _, tag in pos_tagged if tag.startswith('J'))
    if particle_count > len(set(tag for _, tag in pos_tagged if tag.startswith('J'))):
        issues.append("There may be unnecessary repetition of particles.")

    # Rule 4: Check for proper use of honorific forms
    if any(word == '저' for word, _ in pos_tagged) and not any(tag == 'EP' for _, tag in pos_tagged):
        issues.append("When using the humble form '저', consider using an honorific verb ending.")

    return issues

def analyze_sentence(sentence):
    print(f"\nAnalyzing: {sentence}")
    pos_tagged = komoran.pos(sentence)
    print("POS Tagged:")
    for word, pos in pos_tagged:
        # Convert Java strings to Python strings
        word = str(word)
        pos = str(pos)
        print(f"  {word:<10} {pos}")
    
    morphs = komoran.morphs(sentence)
    print("Morphemes:", [str(morph) for morph in morphs])
    
    # Modified nouns extraction to handle Java String objects
    tagged = komoran.pos(sentence)
    nouns = [str(s) for s, t in tagged if str(t).startswith('NN')]
    print("Nouns:", nouns)

test_sentences = [
    "안녕하세요. KoNLPy 테스트입니다.",
    "나는 어제 친구와 함께 영화를 봤어요.",
    "그녀는 내일 아침 일찍 학교에 갈 거예요.",
    "이 책은 정말 재미있네요!",
    "우리는 매일 열심히 공부해야 합니다."
]

for sentence in test_sentences:
    analyze_sentence(sentence)
    print("\nGrammar Check:")
    issues = check_grammar(sentence)
    if issues:
        for issue in issues:
            print(f"- {issue}")
    else:
        print("No grammar issues detected.")
    print("\n" + "="*50)
# NNP: Proper Noun
# NNG: Common Noun
# VV: Verb
# JX: Auxiliary Particle
# MAG: Adverb
# EF: Sentence-ending Suffix