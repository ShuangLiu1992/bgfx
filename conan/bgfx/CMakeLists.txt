cmake_minimum_required(VERSION 3.15)

project(bgfx)
if (IS_MACOS OR IS_IOS)
    enable_language(C CXX OBJCXX)
else()
    enable_language(C CXX)
endif()

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
         ../../src/bgfx.cpp
         ../../src/debug_renderdoc.cpp
         ../../src/dxgi.cpp
         ../../src/glcontext_egl.cpp
         ../../src/glcontext_glx.cpp
         ../../src/glcontext_wgl.cpp
         ../../src/glcontext_html5.cpp
         ../../src/nvapi.cpp
         ../../src/renderer_agc.cpp
         ../../src/renderer_d3d11.cpp
         ../../src/renderer_d3d12.cpp
         ../../src/renderer_d3d9.cpp
         ../../src/renderer_gl.cpp
         ../../src/renderer_gnm.cpp
         ../../src/renderer_noop.cpp
         ../../src/renderer_nvn.cpp
         ../../src/renderer_vk.cpp
         ../../src/renderer_webgpu.cpp
         ../../src/shader.cpp
         ../../src/shader_dx9bc.cpp
         ../../src/shader_dxbc.cpp
         ../../src/shader_spirv.cpp
         ../../src/topology.cpp
         ../../src/vertexlayout.cpp
        )
if (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    target_sources(${PROJECT_NAME} PRIVATE
            ../../src/glcontext_eagl.mm
            ../../src/glcontext_nsgl.mm
            ../../src/renderer_mtl.mm
            )
    set_property(SOURCE ../../src/renderer_vk.cpp PROPERTY LANGUAGE OBJCXX)
endif ()

target_include_directories(${PROJECT_NAME} PUBLIC ../../include)
target_include_directories(${PROJECT_NAME} PUBLIC ../../examples/common)
target_include_directories(${PROJECT_NAME} PUBLIC ../../3rdparty)
target_include_directories(${PROJECT_NAME} PUBLIC ../../3rdparty/khronos/)

find_package(meshoptimizer REQUIRED)
target_link_libraries(${PROJECT_NAME} PUBLIC meshoptimizer::meshoptimizer)
find_package(bx REQUIRED)
target_link_libraries(${PROJECT_NAME} PUBLIC bx::bx)
find_package(bimg REQUIRED)
target_link_libraries(${PROJECT_NAME} PUBLIC bimg::bimg)

if (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    target_include_directories(${PROJECT_NAME} PUBLIC ../../3rdparty/directx-headers/include/directx)
endif ()
if (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    target_compile_definitions(${PROJECT_NAME} PUBLIC -DBGFX_CONFIG_RENDERER_OPENGL_MIN_VERSION=21)
    if (${IS_MACOS})
        target_link_libraries(${PROJECT_NAME} PUBLIC "-framework OpenGL")
        target_link_libraries(${PROJECT_NAME} PUBLIC "-framework Cocoa")
    else()
        target_compile_definitions(${PROJECT_NAME} PUBLIC -DBGFX_CONFIG_RENDERER_OPENGLES_MIN_VERSION=30)
        target_link_libraries(${PROJECT_NAME} PUBLIC "-framework OpenGLES")
        target_link_libraries(${PROJECT_NAME} PUBLIC "-framework UIKit")
        target_link_libraries(${PROJECT_NAME} PUBLIC "-framework CoreFoundation")
        target_link_libraries(${PROJECT_NAME} PUBLIC "-framework Foundation")
    endif()
    target_link_libraries(${PROJECT_NAME} PUBLIC "-framework IOKit")
    target_link_libraries(${PROJECT_NAME} PUBLIC "-framework QuartzCore")
    target_link_libraries(${PROJECT_NAME} PUBLIC "-framework Metal")
    target_link_libraries(${PROJECT_NAME} PUBLIC "-framework MetalKit")
endif ()
if ((${CMAKE_SYSTEM_NAME} MATCHES "Windows") OR ${CMAKE_SYSTEM_NAME} MATCHES "Linux")
    target_compile_definitions(${PROJECT_NAME} PUBLIC -DBGFX_CONFIG_RENDERER_OPENGL_MIN_VERSION=44)
elseif (${CMAKE_SYSTEM_NAME} MATCHES "Android")
    target_compile_definitions(${PROJECT_NAME} PUBLIC -DBGFX_CONFIG_RENDERER_OPENGLES_MIN_VERSION=30)
elseif (${CMAKE_SYSTEM_NAME} MATCHES "Emscripten")
    target_compile_definitions(${PROJECT_NAME} PUBLIC -DBGFX_CONFIG_RENDERER_OPENGLES_MIN_VERSION=20)
    target_link_options(${PROJECT_NAME} PUBLIC "-sMAX_WEBGL_VERSION=2")
    target_link_options(${PROJECT_NAME} PUBLIC "-sFULL_ES3")
endif ()
if (CMAKE_SYSTEM_NAME STREQUAL "Linux")
    find_package(OpenGL REQUIRED)
    target_link_libraries(${PROJECT_NAME} PUBLIC OpenGL::GL)
    target_include_directories(${PROJECT_NAME} PUBLIC ./bx/include/compat/linux)
    target_include_directories(${PROJECT_NAME} PUBLIC ../../3rdparty/directx-headers/include/wsl/stubs)
    target_include_directories(${PROJECT_NAME} PUBLIC ../../3rdparty/directx-headers/include/directx)
endif ()

install(TARGETS ${PROJECT_NAME}
        RUNTIME DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
        )