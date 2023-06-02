cmake_minimum_required(VERSION 3.15)

project(bgfx_shaderc)

add_executable(${PROJECT_NAME})

target_compile_definitions(${PROJECT_NAME} PUBLIC -DNINCLUDE=64)
target_compile_definitions(${PROJECT_NAME} PUBLIC -DNWORK=65536)
target_compile_definitions(${PROJECT_NAME} PUBLIC -DNBUFF=65536)
target_compile_definitions(${PROJECT_NAME} PUBLIC -DOLD_PREPROCESSOR=0)
if ((${CONAN_SETTINGS_OS} MATCHES "Windows"))
    # no matching operator delete found; memory will not be freed if initialization throws an exception
    target_compile_options(${PROJECT_NAME} PUBLIC /wd4291)
endif ()
target_sources(${PROJECT_NAME} PRIVATE
        ../../3rdparty/fcpp/cpp6.c
        ../../3rdparty/fcpp/cpp5.c
        ../../3rdparty/fcpp/cpp4.c
        ../../3rdparty/fcpp/cpp3.c
        ../../3rdparty/fcpp/cpp2.c
        ../../3rdparty/fcpp/cpp1.c
        ../../tools/shaderc/shaderc_spirv.cpp
        ../../tools/shaderc/shaderc_pssl.cpp
        ../../tools/shaderc/shaderc_metal.cpp
        ../../tools/shaderc/shaderc_hlsl.cpp
        ../../tools/shaderc/shaderc_glsl.cpp
        ../../tools/shaderc/shaderc.cpp
        )

find_package(bx REQUIRED)
target_link_libraries(${PROJECT_NAME} PUBLIC bx::bx)
find_package(bgfx REQUIRED)
target_link_libraries(${PROJECT_NAME} PUBLIC bgfx::bgfx)
find_package(Threads REQUIRED)
find_package(SPIRV-Tools REQUIRED)
find_package(SPIRV-Tools-opt REQUIRED)
target_link_libraries(${PROJECT_NAME} PUBLIC SPIRV-Tools-static SPIRV-Tools-opt)
find_package(glsl_optimizer REQUIRED)
target_link_libraries(${PROJECT_NAME} PUBLIC glsl_optimizer::glsl_optimizer)
target_include_directories(${PROJECT_NAME} PUBLIC ${glsl_optimizer_INC})
target_link_libraries(${PROJECT_NAME} PUBLIC ${CONAN_LIBS_GLSL_OPTIMIZER})
find_package(spirv_cross_core REQUIRED)
find_package(spirv_cross_glsl REQUIRED)
find_package(spirv_cross_hlsl REQUIRED)
find_package(spirv_cross_msl REQUIRED)
find_package(spirv_cross_cpp REQUIRED)
find_package(spirv_cross_reflect REQUIRED)
find_package(spirv_cross_c REQUIRED)
target_link_libraries(${PROJECT_NAME} PUBLIC spirv-cross-c)
find_package(glslang REQUIRED)
target_link_libraries(${PROJECT_NAME} PUBLIC glslang::glslang glslang::SPIRV)
target_include_directories(${PROJECT_NAME} PUBLIC ${glslang_INC}/Public)
target_include_directories(${PROJECT_NAME} PUBLIC ${glslang_INC})

install(TARGETS ${PROJECT_NAME}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
        )