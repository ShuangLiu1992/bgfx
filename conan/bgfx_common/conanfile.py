from conan import ConanFile
import conan.tools.files
from conan.tools.cmake import CMake, CMakeToolchain
import embed_shader
import os


class BGFXCOMMONConan(ConanFile):
    name = "bgfx_common"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "backend": [None, "ANY"]}
    default_options = {"shared": False, "fPIC": True, "backend": None}

    generators = "CMakeDeps"
    exports_sources = "CMakeLists.txt", "embed_shader.py", "embed_shader.cmake",
    exports = "embed_shader.py", "embed_shader.cmake",

    def build_requirements(self):
        self.tool_requires(f"bgfx_shaderc/{self.version}@")

    def export_sources(self):
        conan.tools.files.copy(self, "*", os.path.join(self.recipe_folder, "..", ".."), self.export_sources_folder)

    def requirements(self):
        self.requires(f"imgui/{self.version}")
        self.requires(f"bimg/{self.version}")
        self.requires(f"bgfx/{self.version}")
        self.requires(f"meshoptimizer/{self.version}")
        if self.options.backend == "glfw":
            self.requires(f"glfw/{self.version}")
        if self.options.backend == "sdl":
            self.requires(f"sdl/{self.version}")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BGFX_BACKEND"] = self.options.backend
        tc.variables["IS_MACOS"] = self.settings.os == "Macos"
        if self.settings.os == "Emscripten" and self.settings.os.simd:
            tc.preprocessor_definitions["SIMD_WASM"] = 1
        if self.settings.os == "Macos":
            tc.variables["IS_MACOS"] = True
        if self.settings.os == "iOS":
            tc.variables["IS_IOS"] = True
        tc.generate()

    def build(self):
        if self.settings.os in ["Emscripten", "Android", "iOS"]:
            shaderc = self.conf.get("user.bgfx_shaderc.shaderc")
            for shader in ["fs_debugdraw_fill", "fs_debugdraw_fill_lit", "fs_debugdraw_fill_texture",
                           "fs_debugdraw_lines",
                           "fs_debugdraw_lines_stipple"]:
                embed_shader.compile([shaderc,
                                      f"./examples/common/debugdraw/{shader}.sc",
                                      f"./examples/common/debugdraw/{shader}.bin.h",
                                      "fragment",
                                      f"./src/",
                                      f"./examples/common/debugdraw/varying.def.sc",
                                      str(self.settings.os), str(self.settings.arch)])
            for shader in ["vs_debugdraw_fill", "vs_debugdraw_fill_lit", "vs_debugdraw_fill_lit_mesh",
                           "vs_debugdraw_fill_mesh", "vs_debugdraw_fill_texture", "vs_debugdraw_lines",
                           "vs_debugdraw_lines_stipple"]:
                embed_shader.compile([shaderc,
                                      f"./examples/common/debugdraw/{shader}.sc",
                                      f"./examples/common/debugdraw/{shader}.bin.h",
                                      "vertex",
                                      f"./src/",
                                      f"./examples/common/debugdraw/varying.def.sc",
                                      str(self.settings.os), str(self.settings.arch)])

        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        dst_dir = self.package_folder
        src_dir = self.build_folder

        conan.tools.files.copy(self, "embed_shader.cmake", src_dir, os.path.join(dst_dir, "cmake"))
        conan.tools.files.copy(self, "embed_shader.py", src_dir, os.path.join(dst_dir, "bin"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "include"), os.path.join(dst_dir, "include"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "src"), os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "3rdparty"),
                               os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "examples/common"),
                               os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.inl", os.path.join(src_dir, "examples/common"),
                               os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "bx/include"), os.path.join(dst_dir, "include"))
        conan.tools.files.copy(self, "*.inl", os.path.join(src_dir, "bx/include"), os.path.join(dst_dir, "include"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "examples"),
                               os.path.join(dst_dir, "include/bgfx/examples"))
        conan.tools.files.copy(self, "*.sc", os.path.join(src_dir, "examples"), os.path.join(dst_dir, "include/shaders"))
        conan.tools.files.copy(self, "*.sh", os.path.join(src_dir, "examples"), os.path.join(dst_dir, "include/shaders"))
        conan.tools.files.copy(self, "*.sc", os.path.join(src_dir, "src"), os.path.join(dst_dir, "include/shaders"))
        conan.tools.files.copy(self, "*.sh", os.path.join(src_dir, "src"), os.path.join(dst_dir, "include/shaders"))

    def package_info(self):
        self.cpp_info.set_property("cmake_build_modules", [os.path.join("cmake", "embed_shader.cmake")])
        self.cpp_info.libs = conan.tools.files.collect_libs(self)