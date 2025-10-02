@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\VsDevCmd.bat" -arch=x64
cl.exe /EHsc ^
 /I "C:\Users\raman\Downloads\opencv\build\include" ^
 "C:\Users\raman\Downloads\image-analyzer\opencv-project\src\spot_counter.cpp" ^
 /Fe:"C:\Users\raman\Downloads\image-analyzer\opencv-project\src\spot_counter.exe" ^
 /link /MACHINE:X64 /LIBPATH:"C:\Users\raman\Downloads\opencv\build\x64\vc16\lib" opencv_world4120.lib
