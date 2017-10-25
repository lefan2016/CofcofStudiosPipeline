# @Date:   2017-10-25T16:33:52-03:00
# @Last modified time: 2017-10-25T16:34:01-03:00
import maya.cmds as cmds
import maya.OpenMaya as om

def openImgTemp(*args):
    CurrentProject = cmds.workspace(q=1,fullName=1)
    path = CurrentProject + '/images/tmp/'
    os.startfile(path)


fileNodes = cmds.ls(type='file')

width = 100
height = 100
image = om.MImage()

for i in fileNodes:
    filePath = cmds.getAttr(i+'.fileTextureName')
    image.readFromFile ( filePath )
    image.resize( width, height, False )
    image.writeToFile( filePath.split(".")[0] +'_resized.png', 'png')
    # replace file textures with resized images
    cmds.setAttr(i+'.fileTextureName', filePath.split(".")[0]+'_resized.png', type='string')
