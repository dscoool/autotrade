import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil


class TestService(win32serviceutil.ServiceFramework):
    _svc_name_ = "AutoTrade"
    _svc_display_name_ = "Python Auto Trade"
    _svc_description_ = "Web Server receiving signal and writing log from tradingview.com"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        rc = None
        while rc != win32event.WAIT_OBJECT_0:
            self.main()

            with open('TestService.log', 'a') as f:
                f.write('test service running...\n')
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
            
    def main(self):
        # run here 
        return

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(TestService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(TestService)
