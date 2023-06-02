find_package(Python3 COMPONENTS Interpreter)
function(EmbedShader target_name shader_path shader_type varying)
    add_custom_command(
            OUTPUT ${CMAKE_BINARY_DIR}/Shaders/${shader_path}.h
            DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${shader_path}
            ${CMAKE_CURRENT_SOURCE_DIR}/${varying}
            COMMAND ${Python3_EXECUTABLE}
            ${BGFX_EMBED_SHADER_PATH}
            ${BGFX_SHADERC_PATH}
            ${CMAKE_CURRENT_SOURCE_DIR}/${shader_path}
            ${CMAKE_BINARY_DIR}/Shaders/${shader_path}.h
            ${shader_type}
            ${BGFX_SHADERC_INC_PATH}
            ${CMAKE_CURRENT_SOURCE_DIR}/${varying}
            ${CMAKE_SYSTEM_NAME}
            ${CMAKE_SYSTEM_PROCESSOR}
    )
    add_custom_target(${shader_path}_mkdir ALL COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/Shaders/)
    add_custom_target(${shader_path} ALL DEPENDS ${CMAKE_BINARY_DIR}/Shaders/${shader_path}.h)
    add_dependencies(${target_name} ${shader_path}_mkdir ${shader_path})
endfunction()
