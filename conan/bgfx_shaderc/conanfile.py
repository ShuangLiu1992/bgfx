from conan import ConanFile
import conan.tools.files
from conan.tools.cmake import CMake, CMakeToolchain
from conan.tools.env import VirtualBuildEnv
import os
import shutil


class BGFXSHADERCConan(ConanFile):
    name = "bgfx_shaderc"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"
    exports_sources = "CMakeLists.txt"

    def requirements(self):
        self.requires(f"bx/{self.version}@")
        self.requires(f"bgfx/{self.version}@")
        self.requires(f"glslang/{self.version}@")
        self.requires(f"spirv_tools/{self.version}@")
        self.requires(f"spirv_cross/{self.version}@")
        self.requires(f"glsl_optimizer/{self.version}@")

    def generate(self):
        glslang_INC = os.path.join(VirtualBuildEnv(self).vars()["glslang_DIR"], "include", "glslang").replace(os.sep,
                                                                                                              '/')
        glsl_optimizer_INC = os.path.join(VirtualBuildEnv(self).vars()["glsl_optimizer_DIR"], "include").replace(os.sep,
                                                                                                                 '/')
        tc = CMakeToolchain(self)
        tc.variables["glslang_INC"] = glslang_INC
        tc.variables["glsl_optimizer_INC"] = glsl_optimizer_INC
        tc.generate()

    def source(self):
        conan.tools.files.get(self,
                              "https://github.com/ShuangLiu1992/bgfx/archive/1566847bf660a8badcbea7db5f79130d9dbc0e3a.tar.gz",
                              md5="e6c836e031b08a319fcccd15181dd7a9", strip_root=True, destination="bgfx")
        shutil.rmtree(os.path.join(self.source_folder, "bgfx/3rdparty/glslang"))
        shutil.rmtree(os.path.join(self.source_folder, "bgfx/3rdparty/spirv-tools"))
        shutil.rmtree(os.path.join(self.source_folder, "bgfx/3rdparty/spirv-headers"))
        shutil.rmtree(os.path.join(self.source_folder, "bgfx/3rdparty/spirv-cross"))
        shutil.rmtree(os.path.join(self.source_folder, "bgfx/3rdparty/glsl-optimizer"))

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.conf_info.define("user.bgfx_shaderc.shaderc", os.path.join(self.package_folder, "bin", "bgfx_shaderc").replace(os.path.sep, '/'))
