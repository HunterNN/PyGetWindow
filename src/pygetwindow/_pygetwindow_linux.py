from pygetwindow import PyGetWindowException, pointInRect, BaseWindow, Rect, Point, Size
import subprocess

def getActiveWindow():
    """Returns a Window object of the currently active (focused) Window."""
    x_id = subprocess.check_output(['xprop', '-root', '_NET_ACTIVE_WINDOW']).decode('utf-8').split(" ")[-1]
    return LinuxWindow(x_id)

def getActiveWindowTitle():
    """Returns a string of the title text of the currently active (focused) Window."""
    return getActiveWindow().title

class LinuxWindow(BaseWindow):
    def __init__(self, x_id):
        self.x_id = x_id
        self._setupRectProperties()

    def _getWindowRect(self):
        wininfos = subprocess.check_output(['xwininfo', '-id', str(self.x_id)]).decode('utf8')
        left = 0
        top = 0
        width = 0
        height = 0
        for info in wininfos.split("\n"):
            if "Absolute upper-left X" in info:
                left = int(info.split(": ")[1])
            elif "Absolute upper-left Y" in info:
                top = int(info.split(": ")[1])
            elif "Width" in info:
                width = int(info.split(": ")[1])
            elif "Height" in info:
                height = int(info.split(": ")[1])
        right = left + width
        bottom = top + height
        return Rect(left, top, right, bottom)

    @property
    def title(self):
        """Returns the window title as a string."""
        title = subprocess.check_output(['xprop', '-id', str(self.x_id), '_NET_WM_NAME']).decode('utf8')
        title = title.split("= ")[1] 
        return title

    @property
    def isMaximized(self):
        """Returns ``True`` if the window is currently maximized."""
        state = subprocess.check_output(['xprop', '-id', str(self.x_id), '_NET_WM_STATE']).decode('utf8')
        return "_NET_WM_STATE_MAXIMIZED_VERT" in state and "_NET_WM_STATE_MAXIMIZED_HORZ" in state

    @property
    def isActive(self):
        """Returns ``True`` if the window is currently the active, foreground window."""
        state = subprocess.check_output(['xprop', '-id', str(self.x_id), '_NET_WM_STATE']).decode('utf8')
        return "_NET_WM_STATE_FOCUSED" in state

    @property
    def isMinimized(self):
        """Returns ``True`` if the window is currently minimized."""
        state = subprocess.check_output(['xprop', '-id', str(self.x_id), '_NET_WM_STATE']).decode('utf8')
        return "_NET_WM_STATE_HIDDEN" in state