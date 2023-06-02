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
        self.requires("bimg/local", transitive_headers=True)
        self.requires("bx/local", transitive_headers=True)
        self.requires("meshoptimizer/local")

    def system_requirements(self):
        if self.settings.os == "Linux":
            Apt(self).install(["libgl1-mesa-dev", "libx11-dev", "libxrandr-dev"])

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

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()
        dst_dir = self.package_folder
        src_dir = os.path.join(self.folders.base_source, "..", "..")
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "include"), os.path.join(dst_dir, "include"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "src"), os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "3rdparty"),
                               os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "examples/common"),
                               os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.inl", os.path.join(src_dir, "examples/common"),
                               os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "examples"),
                               os.path.join("include/examples"))
        conan.tools.files.copy(self, "*.sc", os.path.join(src_dir, "examples"), os.path.join(dst_dir, "shaders"))
        conan.tools.files.copy(self, "*.sh", os.path.join(src_dir, "examples"), os.path.join(dst_dir, "shaders"))
        conan.tools.files.copy(self, "*.sc", os.path.join(src_dir, "src"), os.path.join(dst_dir, "shaders"))
        conan.tools.files.copy(self, "*.sh", os.path.join(src_dir, "src"), os.path.join(dst_dir, "shaders"))

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
