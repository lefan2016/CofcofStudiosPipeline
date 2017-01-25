## Define maya commands
import maya.cmds as cmds
## Load our window and put it into a variable.
qtWin = cmds.loadUI(uiFile=r'P:\LOCAL\ES_SCRIPTS\RIG\pistonRigUI.ui')
## Open our window
cmds.showWindow(qtWin)
## Create dock layout and tell it where it can go
dockLayout = cmds.paneLayout(configuration='single', parent=qtWin)
cmds.dockControl(allowedArea='all', area='right', floating=True, content=dockLayout, label='Custom Dock')
## parent our window underneath the dock layout
cmds.control(qtWin, e=True, parent=dockLayout)
