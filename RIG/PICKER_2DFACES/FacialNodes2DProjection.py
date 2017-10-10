def dirs_files_dic ( mypath , filterExtension ):
    '''
    Returns a dic { Dir : files in Dir }. A dictonary with subdirectories and files inside them from a directory input.
    Example:
        dirs_files_dic('O:\\EMPRESAS\\RIG_FACE2D\\ScriptingGuideRig\\Maps','png')
    '''
    
    from glob import glob
    from os import listdir
    from os.path import isfile, join

    returnDic = {}
    for subdir in glob ( mypath+"//*/" ) :
        onlyfiles = [f for f in listdir(subdir) if ( isfile(join(subdir, f)) and os.path.splitext(f)[1]=='.'+filterExtension)]
        returnDic[subdir]= onlyfiles
    return returnDic
