import os
import subprocess

def get_java_home():
    try:
        return subprocess.check_output(['/usr/libexec/java_home']).decode().strip()
    except:
        return os.environ.get('JAVA_HOME')

java_home = get_java_home()

if not java_home:
    raise ValueError("JAVA_HOME is not set and couldn't be determined automatically.")

print(f"JAVA_HOME: {java_home}")

# We're not setting jvmpath directly anymore
# jpype will use JAVA_HOME to find the JVM