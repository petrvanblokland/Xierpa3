# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    fileio.py
#
import os

class FileIO:

    @classmethod
    def filesOfPath(cls, path):
        paths = []
        for file in os.listdir(path):
            if file.startswith('.'):
                continue
            filePath = path + '/' + file
            if os.path.isdir(filePath):
                continue
            paths.append(filePath)
        return paths
    
    @classmethod
    def foldersOfPath(cls, path):
        paths = []
        for file in os.listdir(path):
            if file.startswith('.'):
                continue
            filePath = path + '/' + file
            if os.path.isdir(filePath):
                paths.append(filePath)
        return paths
    