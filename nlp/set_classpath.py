import os
from konlpy.utils import installpath

def set_classpath():
    base_path = os.path.join(installpath, 'java')
    jars = [f for f in os.listdir(base_path) if f.endswith('.jar')]
    classpath = os.pathsep.join([os.path.join(base_path, jar) for jar in jars])
    os.environ['CLASSPATH'] = classpath
    print(f"Classpath set to: {classpath}")

if __name__ == "__main__":
    set_classpath()