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

    def requirements(self):
        self.requires(f"imgui/tag_docking_3.27")
        self.requires(f"bimg/{self.version}")
        self.requires(f"bgfx/{self.version}")
        self.requires(f"meshoptimizer/{self.version}")
        if self.options.backend == "glfw":
            self.requires(f"glfw/{self.version}")
        if self.options.backend == "sdl":
            self.requires(f"sdl/{self.version}")

    def source(self):
        conan.tools.files.get(self,
                              "https://github.com/ShuangLiu1992/bgfx/archive/a77e4bf1c4f5599f7dc44f9946ae4637f516b75d.tar.gz",
                              md5="afe0fa3dfa1f9f2b5ef9bdf6679df855", strip_root=True, destination="bgfx")

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
        if self.settings.os == "Emscripten":
            conan.tools.files.replace_in_file(self,
                                              f"{self.folders.base_build}/bgfx/3rdparty/meshoptimizer/src/vertexfilter.cpp",
                                              '#define SIMD_SSE',
                                              '')
            conan.tools.files.replace_in_file(self,
                                              f"{self.folders.base_build}/bgfx/3rdparty/meshoptimizer/src/vertexcodec.cpp",
                                              '#define SIMD_SSE',
                                              '')
            conan.tools.files.replace_in_file(self,
                                              f"{self.folders.base_build}/bgfx/examples/common/entry/entry_html5.cpp",
                                              'EMSCRIPTEN_CHECK(emscripten_request_fullscreen_strategy(canvas, false, &fullscreenStrategy) );',
                                              '')

        if self.settings.os in ["Emscripten", "Android", "iOS"]:
            shaderc = self.conf.get("user.bgfx_shaderc.shaderc")
            for shader in ["fs_debugdraw_fill", "fs_debugdraw_fill_lit", "fs_debugdraw_fill_texture",
                           "fs_debugdraw_lines",
                           "fs_debugdraw_lines_stipple"]:
                embed_shader.compile([shaderc,
                                      f"{self.build_folder}/bgfx/examples/common/debugdraw/{shader}.sc",
                                      f"{self.build_folder}/bgfx/examples/common/debugdraw/{shader}.bin.h",
                                      "fragment",
                                      f"{self.build_folder}/bgfx/src/",
                                      f"{self.build_folder}/bgfx/examples/common/debugdraw/varying.def.sc",
                                      str(self.settings.os), str(self.settings.arch)])
            for shader in ["vs_debugdraw_fill", "vs_debugdraw_fill_lit", "vs_debugdraw_fill_lit_mesh",
                           "vs_debugdraw_fill_mesh", "vs_debugdraw_fill_texture", "vs_debugdraw_lines",
                           "vs_debugdraw_lines_stipple"]:
                embed_shader.compile([shaderc,
                                      f"{self.build_folder}/bgfx/examples/common/debugdraw/{shader}.sc",
                                      f"{self.build_folder}/bgfx/examples/common/debugdraw/{shader}.bin.h",
                                      "vertex",
                                      f"{self.build_folder}/bgfx/src/",
                                      f"{self.build_folder}/bgfx/examples/common/debugdraw/varying.def.sc",
                                      str(self.settings.os), str(self.settings.arch)])


        conan.tools.files.rmdir(self, f"{self.build_folder}/bgfx/3rdparty/dear-imgui")
        conan.tools.files.rmdir(self, f"{self.build_folder}/bimg/3rdparty/astc-encoder")
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        dst_dir = self.package_folder
        src_dir = self.folders.base_build
        conan.tools.files.copy(self, "embed_shader.cmake", src_dir, os.path.join(dst_dir, "cmake"))
        conan.tools.files.copy(self, "embed_shader.py", src_dir, os.path.join(dst_dir, "bin"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "bgfx/include"), os.path.join(dst_dir, "include"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "bgfx/src"), os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "bgfx/3rdparty"),
                               os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "bgfx/examples/common"),
                               os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.inl", os.path.join(src_dir, "bgfx/examples/common"),
                               os.path.join(dst_dir, "include/bgfx"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "bx/include"), os.path.join(dst_dir, "include"))
        conan.tools.files.copy(self, "*.inl", os.path.join(src_dir, "bx/include"), os.path.join(dst_dir, "include"))
        conan.tools.files.copy(self, "*.h", os.path.join(src_dir, "bgfx/examples"),
                               os.path.join(dst_dir, "include/bgfx/examples"))
        conan.tools.files.copy(self, "*.sc", os.path.join(src_dir, "bgfx/examples"), os.path.join(dst_dir, "include/shaders"))
        conan.tools.files.copy(self, "*.sh", os.path.join(src_dir, "bgfx/examples"), os.path.join(dst_dir, "include/shaders"))
        conan.tools.files.copy(self, "*.sc", os.path.join(src_dir, "bgfx/src"), os.path.join(dst_dir, "include/shaders"))
        conan.tools.files.copy(self, "*.sh", os.path.join(src_dir, "bgfx/src"), os.path.join(dst_dir, "include/shaders"))

    def package_info(self):
        self.cpp_info.set_property("cmake_build_modules", [os.path.join("cmake", "embed_shader.cmake")])
        self.cpp_info.libs = conan.tools.files.collect_libs(self)