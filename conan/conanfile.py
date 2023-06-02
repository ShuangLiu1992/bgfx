from conan import ConanFile
from conan.tools.system.package_manager import Apt
import conan.tools.files
from conan.tools.cmake import CMake, CMakeToolchain
import os


class BGFXConan(ConanFile):
    name = "bgfx"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    generators = "CMakeDeps"
    exports_sources = "CMakeLists.txt"

    def requirements(self):
        self.requires(f"bimg/{self.version}", transitive_headers=True)
        self.requires(f"bx/{self.version}", transitive_headers=True)
        self.requires(f"meshoptimizer/{self.version}")

    def system_requirements(self):
        if self.settings.os == "Linux":
            Apt(self).install(["libgl1-mesa-dev", "libx11-dev", "libxrandr-dev"])

    def source(self):
        conan.tools.files.get(self,
                              "https://github.com/ShuangLiu1992/bgfx/archive/a77e4bf1c4f5599f7dc44f9946ae4637f516b75d.tar.gz",
                              md5="afe0fa3dfa1f9f2b5ef9bdf6679df855", strip_root=True, destination="bgfx")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["IS_MACOS"] = self.settings.os == "Macos"
        if self.settings.os == "Emscripten" and self.settings.os.simd:
            tc.preprocessor_definitions["SIMD_WASM"] = 1
        if self.settings.os == "Macos":
            tc.variables["IS_MACOS"] = True
        if self.settings.os == "iOS":
            tc.variables["IS_IOS"] = True
        tc.generate()

    def build(self):
        if self.settings.os == "Emscripten":
            conan.tools.files.replace_in_file(self,
                                              f"{self.folders.base_build}/bgfx/3rdparty/meshoptimizer/src/vertexfilter.cpp",
                                              '#define SIMD_SSE',
                                              '')
            conan.tools.files.replace_in_file(self,
                                              f"{self.folders.base_build}/bgfx/3rdparty/meshoptimizer/src/vertexcodec.cpp",
                                              '#define SIMD_SSE',
                                              '')

        conan.tools.files.rmdir(self, f"{self.build_folder}/bgfx/3rdparty/dear-imgui")
        conan.tools.files.rmdir(self, f"{self.build_folder}/bimg/3rdparty/astc-encoder")
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        dst_dir = self.package_folder
        src_dir = self.folders.base_build
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "bgfx/include"), os.path.join(dst_dir, "include"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "bgfx/src"), os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "bgfx/3rdparty"),
                               os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "bgfx/examples/common"),
                               os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.inl", os.path.join(src_dir, "bgfx/examples/common"),
                               os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "bgfx/examples"),
                               os.path.join("include/bgfx/examples"))
        conan.tools.files.copy(self, "*.sc", os.path.join(src_dir, "bgfx/examples"), os.path.join(dst_dir, "shaders"))
        conan.tools.files.copy(self, "*.sh", os.path.join(src_dir, "bgfx/examples"), os.path.join(dst_dir, "shaders"))
        conan.tools.files.copy(self, "*.sc", os.path.join(src_dir, "bgfx/src"), os.path.join(dst_dir, "shaders"))
        conan.tools.files.copy(self, "*.sh", os.path.join(src_dir, "bgfx/src"), os.path.join(dst_dir, "shaders"))

    def package_info(self):
        self.cpp_info.includedirs = ['include', 'include/bgfx', 'include/bgfx/fcpp', 'include/bgfx/webgpu/include']

        self.cpp_info.libs = conan.tools.files.collect_libs(self)

        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["rt", "dl", "X11", "GL", "pthread"]

        if self.settings.os == "Android":
            self.cpp_info.system_libs = ["android", "log", "EGL", "GLESv2"]
            self.cpp_info.sharedlinkflags += ['-u ANativeActivity_onCreate']
        if self.settings.os == "Emscripten":
            self.cpp_info.defines += ["BGFX_CONFIG_RENDERER_OPENGLES_MIN_VERSION=30"]
            self.cpp_info.sharedlinkflags += ['-sMAX_WEBGL_VERSION=2']
            self.cpp_info.sharedlinkflags += ['-sFULL_ES3']

        if self.settings.os in ["Macos", "iOS"]:
            if self.settings.os == "Macos":
                self.cpp_info.frameworks += ['Cocoa', 'OpenGL', 'IOKit']
            if self.settings.os == "iOS":
                self.cpp_info.frameworks += [
                    'Foundation',
                    'CoreFoundation',
                    'UIKit',
                    'OpenGLES']
            self.cpp_info.frameworks += [
                'QuartzCore',
                'Metal',
                'MetalKit']
