from conan import ConanFile
from conan.tools.microsoft import is_msvc
from conan.tools.files import get, copy, rm, rmdir
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout

import os


required_conan_version = ">=1.54.0"

class OhPipelineConan(ConanFile):
    name = "ohpipeline"
    description = "ohMediaPlayer provides a software av.openhome media renderer."
    license = "MIT"
    url = ""
    homepage = "https://github.com/openhome/ohPipeline"
    topics = ("sound", "openhome", "player")
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def requirements(self):
        self.requires("libressl/2.9.2")
        self.requires("flac/1.3.3")
        self.requires("ogg/1.3.5")
        self.requires("alac/cci.20121212")
        self.requires("libfdk_aac/2.0.2")
        self.requires("libmad/0.15.1b")
        self.requires("ohnet/wip_conan")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        
        cd = CMakeDeps(self)
        cd.generate()

        print("libki:")
        print(self.deps_cpp_info)
        deps = self.deps_cpp_info.deps
        print(deps)

        copy(self, "*.py", self.deps_cpp_info["ohnet"].bin_paths[0], self.build_folder)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, pattern="License.txt", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)

        copy(self, "*.h",
            src=os.path.join(self.source_folder, "OpenHome"),
            dst=os.path.join(self.package_folder, "include", "OpenHome"))
        copy(self, "*.a", keep_path=False,
            src=self.build_folder,
            dst=os.path.join(self.package_folder, "lib"))

        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["ohPipeline"]
