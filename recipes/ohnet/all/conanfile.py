from conan import ConanFile
from conan.tools.microsoft import is_msvc
from conan.tools.files import get, copy, rm, rmdir
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
import os


required_conan_version = ">=1.54.0"

class OhNetConan(ConanFile):
    name = "ohnet"
    description = "ohNet is a library for the discovery, monitoring, manipulation and implementation of UPnP devices, generalized to be extensible to other similar protocols."
    license = "MIT"
    url = ""
    homepage = "https://github.com/openhome/ohNet"
    topics = ("networking", "openhome", "upnp")
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

    def layout(self):
        cmake_layout(self, src_folder="OpenHome")

    def requirements(self):
        self.requires("b64/1.2.1")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        
        cd = CMakeDeps(self)
        cd.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, pattern="LICENSE", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)
        copy(self, "*.h",
            src=os.path.join(self.build_folder, "Temp"),
            dst=os.path.join(self.package_folder, "include"))
            
        # copy(self, "*.a", keep_path=False,
        #     src=self.build_folder,
        #     dst=os.path.join(self.package_folder, "lib"))
        copy(self, "*.so", keep_path=False,
            src=self.build_folder,
            dst=os.path.join(self.package_folder, "lib"))

        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "share"))
        rm(self, "*.la", os.path.join(self.package_folder, "lib"))
        rm(self, "*.pdb", os.path.join(self.package_folder, "lib"))
        rm(self, "*.pdb", os.path.join(self.package_folder, "bin"))
        
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["ohNet"]

        # self.cpp_info.set_property("cmake_module_file_name", "ohNet")
        # self.cpp_info.set_property("cmake_module_target_name", "ohNet::ohNet")
        # self.cpp_info.set_property("cmake_file_name", "ohNet")
        # self.cpp_info.set_property("cmake_target_name", "ohNet::ohNet")

        # If they are needed on Linux, m, pthread and dl are usually needed on FreeBSD too
        # if self.settings.os in ["Linux", "FreeBSD"]:
        #     self.cpp_info.system_libs.append("m")
        #     self.cpp_info.system_libs.append("pthread")
        #     self.cpp_info.system_libs.append("dl")
