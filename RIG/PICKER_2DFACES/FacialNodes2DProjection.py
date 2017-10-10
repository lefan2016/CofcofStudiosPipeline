def dirs_files_dic ( mypath , filterExtension ):
    '''
    Returns a dic { Dir : files in Dir }. A dictonary with subdirectories and files inside them from a directory input.
    Example:
        dirs_files_dic('O:\EMPRESAS\RIG_FACE2D\ScriptingGuideRig\Maps','png')
    
    '''
    from os import listdir
    from os.path import isfile, join
    returnDic = {}
    dirs= [f for f in os.listdir(mypath) if not isfile(join(mypath, f))]
    for subdir in dirs:
        subdir = mypath+'\\'+subdir
        onlyfiles = [f for f in listdir(subdir) if ( isfile(join(subdir, f)) and os.path.splitext(f)[1]=='.'+filterExtension)]
        returnDic[subdir]= onlyfiles
    return returnDic
