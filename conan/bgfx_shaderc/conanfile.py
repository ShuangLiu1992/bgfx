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

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.conf_info.define("user.bgfx_shaderc.shaderc", os.path.join(self.package_folder, "bin", "bgfx_shaderc").replace(os.path.sep, '/'))
