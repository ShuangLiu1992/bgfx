import subprocess
import pathlib
import sys
import os


def compile(argv):
    shaderc, shader_src, output_path, shader_type, include_path, varying_path, target_platform, target_arch = argv

    languages = {
        "glsl": "130",
        "spv": "spirv",
        "essl": "300_es",
        "mtl": "metal"
    }
    if target_platform == "Windows":
        languages["dx11"] = "s_4_0" if shader_type == "vertex" else "s_4_0"

    platforms = {
        "mtl": "ios",
        "glsl": "linux",
        "spv": "linux",
        "essl": "android",
        "dx11": "windows",
        "dx9": "windows"
    }
    if target_platform == "Emscripten":
        platforms["essl"] = "asm.js"
    if target_platform == "Windows":
        platforms["essl"] = "windows"
        platforms["glsl"] = "windows"
    if target_platform == "Macos":
        platforms["glsl"] = "osx"
    if target_platform == "Android":
        if target_arch in ["x86", "x86_64"]:
            languages["essl"] = "100_es"
            languages["glsl"] = "120"

    out_parent = pathlib.Path(output_path).parent
    os.makedirs(out_parent, exist_ok=True)

    combined = ""
    for language in languages:
        name = pathlib.Path(shader_src).stem
        out_name = f"{out_parent}/{name}_{language}.h"
        cmd = [shaderc,
               "-i", include_path,
               "--type", shader_type,
               "--platform", platforms[language],
               "-p", languages[language],
               "-f", shader_src,
               "-o", out_name,
               "--bin2c", f"{name}_{language}",
               "--varyingdef", varying_path
               ]
        subprocess.run(cmd)
        f = open(out_name)
        combined += str(f.read())
        f.close()
    output_file = open(output_path, "w")
    output_file.write(combined)
    output_file.close()


if __name__ == "__main__":
    compile(sys.argv[1:])
