@echo off
setlocal
set JAVA8_HOME=C:\Program Files\Java\jdk1.8.0_202
if not defined JAVA_HOME (set JAVA_HOME=%JAVA8_HOME%)
set javac="%JAVA_HOME%"\bin\javac -encoding UTF-8 -g:none -deprecation -Xlint:unchecked ^
    -source 1.8 -target 1.8 -bootclasspath "%JAVA8_HOME%\jre\lib\rt.jar"
pushd "%~dp0"\src\jt\rubicon\_java
set py=C:\Windows\py.exe -3.7 -B
%javac% ^
    ..\..\..\..\..\jtypes.jvm\src\jt\jvm\java\com\jt\reflect\*.java ^
    org\pybee\rubicon\*.java
%py% -m class2py org\pybee\rubicon\Python.class
del /F/Q ^
    ..\..\..\..\..\jtypes.jvm\src\jt\jvm\java\com\jt\reflect\*.class ^
    org\pybee\rubicon\*.class
popd
pushd "%~dp0"\tests
rmdir /Q/S java\classes 2> nul & mkdir java\classes
dir /S/B/O:N ^
    ..\..\jtypes.jvm\src\jt\jvm\java\com\jt\reflect\*.java ^
    ..\src\jt\rubicon\_java\org\pybee\rubicon\*.java ^
    java\org\pybee\rubicon\test\*.java ^
    2> nul > build.fil
%javac% -d java/classes -classpath java/lib/* @build.fil
del /F/Q build.fil
popd
endlocal
