"""
NEXTGEN AI — Standalone Android APK Builder
Developer: Shohjahon Abdullayev
"""
import os
import sys
import subprocess
import shutil
import zipfile

def find_java():
    candidates = [
        r"C:\Users\Admin\.jre17",
        r"C:\Users\Admin\.jdk17",
        os.environ.get("JAVA_HOME", "")
    ]
    for c in candidates:
        if not c or not os.path.exists(c):
            continue
        for root, dirs, files in os.walk(c):
            if "java.exe" in files:
                java_exe = os.path.join(root, "java.exe")
                keytool_exe = os.path.join(root, "keytool.exe")
                javac_exe = os.path.join(root, "javac.exe") if "javac.exe" in files else None
                return {
                    "home": os.path.dirname(root) if os.path.basename(root).lower() == "bin" else root,
                    "bin": root,
                    "java": java_exe,
                    "keytool": keytool_exe,
                    "javac": javac_exe
                }
    return None

def build():
    print("=" * 60)
    print("⚡ NEXTGEN AI — Standalone Android APK Builder")
    print("👨‍💻 Developer: Shohjahon Abdullayev")
    print("=" * 60)

    j = find_java()
    if not j:
        print("Waiting: Java environment is still downloading/extracting...")
        sys.exit(1)

    print(f"Using Java Home: {j['home']}")
    print(f"Java binary: {j['java']}")

    sdk_dir = r"C:\Users\Admin\AppData\Local\Android\Sdk"
    build_tools = os.path.join(sdk_dir, "build-tools", "34.0.0")
    android_jar = os.path.join(sdk_dir, "platforms", "android-34", "android.jar")

    aapt2 = os.path.join(build_tools, "aapt2.exe")
    d8 = os.path.join(build_tools, "d8.bat")
    zipalign = os.path.join(build_tools, "zipalign.exe")
    apksigner = os.path.join(build_tools, "apksigner.bat")

    os.environ["JAVA_HOME"] = j["home"]
    os.environ["PATH"] = j["bin"] + os.pathsep + build_tools + os.pathsep + os.environ["PATH"]

    work_dir = os.path.abspath("android_standalone")
    bin_dir = os.path.join(work_dir, "bin")
    os.makedirs(bin_dir, exist_ok=True)

    # 1. Generate debug keystore if not exists
    keystore = os.path.join(work_dir, "debug.keystore")
    if not os.path.exists(keystore):
        print("1. Generating debug signing key...")
        cmd_key = [
            j["keytool"], "-genkeypair", "-v",
            "-keystore", keystore,
            "-alias", "androiddebugkey",
            "-keyalg", "RSA", "-keysize", "2048",
            "-validity", "10000",
            "-storepass", "android", "-keypass", "android",
            "-dname", "CN=Shohjahon Abdullayev, OU=NEXTGEN, O=NEXTGEN AI, C=UZ"
        ]
        subprocess.run(cmd_key, check=True)

    # 2. Compile resources with aapt2
    print("2. Compiling Android resources with AAPT2...")
    res_dir = os.path.join(work_dir, "res")
    compiled_res = os.path.join(work_dir, "compiled_res.zip")
    if os.path.exists(compiled_res):
        os.remove(compiled_res)
    subprocess.run([aapt2, "compile", "--dir", res_dir, "-o", compiled_res], check=True)

    # 3. Link resources and AndroidManifest with aapt2
    print("3. Linking APK package with AAPT2...")
    manifest = os.path.join(work_dir, "AndroidManifest.xml")
    unaligned_apk = os.path.join(work_dir, "unaligned.apk")
    if os.path.exists(unaligned_apk):
        os.remove(unaligned_apk)
    subprocess.run([
        aapt2, "link",
        "-I", android_jar,
        "--manifest", manifest,
        "-o", unaligned_apk,
        "--auto-add-overlay",
        compiled_res
    ], check=True)

    # 4. Compile Java code (using javac if available, or ecj.jar)
    print("4. Compiling Java source code...")
    java_src = os.path.join(work_dir, "src", "uz", "nextgen", "ai", "MainActivity.java")
    ecj_jar = os.path.join(work_dir, "ecj.jar")
    if j["javac"]:
        print("   Using javac.exe...")
        subprocess.run([j["javac"], "-cp", android_jar, "-d", bin_dir, java_src], check=True)
    elif os.path.exists(ecj_jar):
        print("   Using Eclipse Java Compiler (ecj.jar)...")
        subprocess.run([
            j["java"], "-jar", ecj_jar,
            "-cp", android_jar,
            "-d", bin_dir,
            "-7",
            java_src
        ], check=True)
    else:
        raise RuntimeError("No Java compiler found (neither javac nor ecj.jar)")

    # 5. Convert bytecode to Dalvik dex with d8
    print("5. Converting bytecode to Dalvik DEX format with D8...")
    class_files = []
    for root, dirs, files in os.walk(bin_dir):
        for f in files:
            if f.endswith(".class"):
                class_files.append(os.path.join(root, f))
    if not class_files:
        raise RuntimeError("No compiled .class files found in bin!")

    subprocess.run([d8, "--lib", android_jar, "--output", bin_dir, *class_files], check=True)

    # 6. Add classes.dex into unaligned.apk
    print("6. Packaging classes.dex into APK...")
    dex_path = os.path.join(bin_dir, "classes.dex")
    with zipfile.ZipFile(unaligned_apk, "a") as z:
        z.write(dex_path, "classes.dex")

    # 7. ZipAlign APK
    print("7. Optimizing 4-byte page alignment with zipalign...")
    aligned_apk = os.path.join(work_dir, "aligned.apk")
    if os.path.exists(aligned_apk):
        os.remove(aligned_apk)
    subprocess.run([zipalign, "-p", "-f", "4", unaligned_apk, aligned_apk], check=True)

    # 8. Sign APK with apksigner (v2 + v3 scheme)
    print("8. Cryptographically signing APK with apksigner...")
    final_apk = os.path.abspath("NEXTGEN-AI.apk")
    if os.path.exists(final_apk):
        os.remove(final_apk)
    subprocess.run([
        apksigner, "sign",
        "--ks", keystore,
        "--ks-pass", "pass:android",
        "--ks-key-alias", "androiddebugkey",
        "--key-pass", "pass:android",
        "--out", final_apk,
        aligned_apk
    ], check=True)

    # Verify signature
    print("9. Verifying APK signature...")
    subprocess.run([apksigner, "verify", final_apk], check=True)

    size_mb = os.path.getsize(final_apk) / (1024 * 1024)
    print("=" * 60)
    print(f"🎉 SUCCESS! Android APK successfully generated:")
    print(f"📁 Path: {final_apk}")
    print(f"📦 Size: {size_mb:.2f} MB")
    print(f"🚀 Application ID: uz.nextgen.ai")
    print(f"👨‍💻 Developer: Shohjahon Abdullayev")
    print("=" * 60)
    return final_apk

if __name__ == "__main__":
    build()
