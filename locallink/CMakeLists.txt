cmake_minimum_required(VERSION 3.16)
project(MyQtApp)

set(CMAKE_CXX_STANDARD 20)

# 指定 Qt 安装路径
set(CMAKE_PREFIX_PATH "/opt/homebrew/Cellar/qt/6.9.1")

find_package(Qt6 COMPONENTS Core Widgets Gui Network REQUIRED)

add_executable(MyQtApp main.cpp)
add_executable(QtJsonClient qt_client.cpp)

target_link_libraries(MyQtApp Qt6::Core Qt6::Widgets Qt6::Gui Qt6::Network)
target_link_libraries(QtJsonClient Qt6::Core Qt6::Network)
