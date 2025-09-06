cmake_minimum_required(VERSION 3.16)

project(MedicalSystem VERSION 0.1 LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets)
find_package(Qt${QT_VERSION_MAJOR} COMPONENTS Core Gui Widgets Network REQUIRED)
find_package(Qt6 REQUIRED COMPONENTS Core Sql)

set(PROJECT_SOURCES

        loginwindow.cpp
        loginwindow.h
        loginwindow.ui
        doctormainwindow.h

)

if(${QT_VERSION_MAJOR} GREATER_EQUAL 6)
    qt_add_executable(MedicalSystem
        MANUAL_FINALIZATION
        ${PROJECT_SOURCES}


        main.cpp
        registerwindow.cpp
        resetpasswordwindow.cpp
        doctormainwindow.h
        admissionstatuswindow.cpp
        doctormainwindow.cpp
        patientinfowindow.cpp
        punchleavewindow.cpp
        receptionwindow.cpp
        registrationinfowindow.cpp
        mainwindow_patient.h
        mainwindow_patient.cpp
        mainwindow_patient.ui
        resources.qrc
        databasemanager.h databasemanager.cpp
        sendandreceive.h sendandreceive.cpp
        chatSrc/chatsysteminit.h chatSrc/chatsysteminit.cpp

        chatSrc/messageclient.h chatSrc/messageclient.cpp
        chatSrc/chatinitwindow.h chatSrc/chatinitwindow.cpp chatSrc/chatinitwindow.ui
        chatSrc/chatmainwindow.h chatSrc/chatmainwindow.cpp chatSrc/chatmainwindow.ui
        doctorinfowindow.cpp







    )
# Define target properties for Android with Qt 6 as:
#    set_property(TARGET loginAndRegister APPEND PROPERTY QT_ANDROID_PACKAGE_SOURCE_DIR
#                 ${CMAKE_CURRENT_SOURCE_DIR}/android)
# For more information, see https://doc.qt.io/qt-6/qt-add-executable.html#target-creation
else()
    if(ANDROID)
        add_library(MedicalSystem SHARED
            ${PROJECT_SOURCES}
        )
# Define properties for Android with Qt 5 after find_package() calls as:
#    set(ANDROID_PACKAGE_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/android")
    else()
        add_executable(MedicalSystem
            ${PROJECT_SOURCES}
        )
    endif()
endif()

target_link_libraries(MedicalSystem PRIVATE Qt${QT_VERSION_MAJOR}::Widgets Qt${QT_VERSION_MAJOR}::Network)
target_link_libraries(MedicalSystem PRIVATE Qt6::Core Qt6::Sql)
# Qt for iOS sets MACOSX_BUNDLE_GUI_IDENTIFIER automatically since Qt 6.1.
# If you are developing for iOS or macOS you should consider setting an
# explicit, fixed bundle identifier manually though.
if(${QT_VERSION} VERSION_LESS 6.1.0)
  set(BUNDLE_ID_OPTION MACOSX_BUNDLE_GUI_IDENTIFIER com.example.MedicalSystem)
endif()
set_target_properties(MedicalSystem PROPERTIES
    ${BUNDLE_ID_OPTION}
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

include(GNUInstallDirs)
install(TARGETS MedicalSystem
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

if(QT_VERSION_MAJOR EQUAL 6)
    qt_finalize_executable(MedicalSystem)
endif()
