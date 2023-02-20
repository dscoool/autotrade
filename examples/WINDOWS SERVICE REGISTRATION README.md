# TestService

Windows Service with Python 3.5 and pyinstaller

## Requirements

  * Python 3.5.x
  * [Visual C++ Build Tools 2015](http://go.microsoft.com/fwlink/?LinkId=691126)
  * PyInstaller 3.2

## Check
    
    (env)$ python -V
    Python 3.5.2
    
    (env)$ pip freeze
    PyInstaller==3.2

## Build

    (env)$ pyinstaller -F --hidden-import=win32timezone WindowsService.py
    
## Run

    (env) dist\WindowsService.exe install
    Installing service TestService
    Service installed
    
    (env) dist\WindowsService.exe start
    Starting service TestService

## Clean

    (env) dist\WindowsService.exe stop
    (env) dist\WindowsService.exe remove
