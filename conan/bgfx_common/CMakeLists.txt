cmake_minimum_required(VERSION 3.15)

project(bgfx_common)
if (IS_MACOS OR IS_IOS)
    enable_language(C CXX OBJCXX)
else()
    enable_language(C CXX)
endif()

add_library(${PROJECT_NAME})
find_package(imgui REQUIRED)
target_link_libraries(${PROJECT_NAME} PUBLIC imgui::imgui)
find_package(bimg REQUIRED)
target_link_libraries(${PROJECT_NAME} PUBLIC bimg::bimg)
find_package(bx REQUIRED)
target_link_libraries(${PROJECT_NAME} PUBLIC bx::bx)
find_package(bgfx REQUIRED)
target_link_libraries(${PROJECT_NAME} PUBLIC bgfx::bgfx)

target_sources(${PROJECT_NAME} PRIVATE
        ./bgfx/examples/common/bgfx_utils.cpp
        ./bgfx/examples/common/cube_atlas.cpp
        ./bgfx/examples/common/imgui/imgui.cpp
        ./bgfx/examples/common/nanovg/nanovg.cpp
        ./bgfx/examples/common/nanovg/nanovg_bgfx.cpp
        ./bgfx/examples/common/debugdraw/debugdraw.cpp
        ./bgfx/examples/common/entry/cmd.cpp
        ./bgfx/examples/common/entry/dialog.cpp
        ./bgfx/examples/common/entry/entry.cpp
        ./bgfx/examples/common/entry/input.cpp
        )

target_include_directories(${PROJECT_NAME} PUBLIC ./bgfx/examples/common)
if (BGFX_BACKEND STREQUAL "glfw")
    target_compile_definitions(${PROJECT_NAME} PUBLIC -DENTRY_CONFIG_USE_GLFW=1)
    target_sources(${PROJECT_NAME} PRIVATE ./bgfx/examples/common/entry/entry_glfw.cpp)
    find_package(glfw3 REQUIRED)
    target_link_libraries(${PROJECT_NAME} PUBLIC glfw)
elseif (BGFX_BACKEND STREQUAL "sdl")
    target_compile_definitions(${PROJECT_NAME} PUBLIC -DENTRY_CONFIG_USE_SDL=1)
    target_sources(${PROJECT_NAME} PRIVATE ./bgfx/examples/common/entry/entry_sdl.cpp)
    find_package(SDL2 REQUIRED)
    target_link_libraries(${PROJECT_NAME} PUBLIC SDL2::SDL2)
    if (CONAN_SETTINGS_OS STREQUAL "Linux")
        find_package(X11 REQUIRED)
        target_link_libraries(${PROJECT_NAME} PUBLIC ${X11_LIBRARIES})
    endif()
else ()
    if (CMAKE_SYSTEM_NAME STREQUAL "Linux")
        target_sources(${PROJECT_NAME} PRIVATE ./bgfx/examples/common/entry/entry_x11.cpp)
    elseif (CMAKE_SYSTEM_NAME STREQUAL "Darwin")
        if (${IS_MACOS})
            target_sources(${PROJECT_NAME} PRIVATE ./bgfx/examples/common/entry/entry_osx.mm)
        else()
            target_sources(${PROJECT_NAME} PRIVATE ./bgfx/examples/common/entry/entry_ios.mm)
        endif ()
    elseif (CMAKE_SYSTEM_NAME STREQUAL "Windows")
        target_sources(${PROJECT_NAME} PRIVATE ./bgfx/examples/common/entry/entry_windows.cpp)
    elseif (CMAKE_SYSTEM_NAME STREQUAL "Emscripten")
        target_sources(${PROJECT_NAME} PRIVATE ./bgfx/examples/common/entry/entry_html5.cpp)
    elseif (CMAKE_SYSTEM_NAME STREQUAL "Android")
        target_link_libraries(${PROJECT_NAME} PUBLIC android log EGL GLESv2)
        target_include_directories(${PROJECT_NAME} PUBLIC ./bgfx/3rdparty/native_app_glue/)
        target_sources(${PROJECT_NAME} PRIVATE ./bgfx/examples/common/entry/entry_android.cpp)
    endif ()
endif ()
target_compile_definitions(${PROJECT_NAME} PUBLIC -DUSE_ENTRY=1)

install(TARGETS ${PROJECT_NAME}
        RUNTIME DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
        )