#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:11:38 2017

@author: charles
"""
import os
import os.path
import json
import ast
class HandleClass:
    def __init__(self,path):
        self.__path = path
        
    def __get_py(path,json_path):      
        fileList = os.listdir(path)
        for filename in fileList:
            file_path = os.path.join(path,filename)
            if os.path.isdir(file_path):
                get_py(file_path,json_path)
            elif filename[-5:].upper()=='.JSON':
                json_path.append(file_path)              
        return json_path

    def ParseJson(self):
        json_path=[]
        json_path = get_py(self.__path,json_path)
        print(len(json_path))
        for json_file in json_path:
            data=[]
            with open(json_file,'r',encoding="utf-8",errors="ignore") as f:
                for line in f:
                    json_data = json.loads(line)
                    data.append(json_data['text'])
            filename = json_file.split("/")[-1]
            filename = filename[:-5]+'.txt'
            txt_file = os.path.join(self.__path,"txt",filename)
            
            with open(txt_file,'w',encoding="utf-8",errors="ignore") as f:
                f.write(str(data))
        
        print("Finish")
        
        
        
        
           
        
        
    

if __name__ == '__main__':
    positive = HandleClass("/home/charles/tool/tweet-ubuntu/negative-undepressed")
    positive.ParseJson()
    ''' 
    path = "/home/charles/tool/tweet-ubuntu/positive-depressed/txt/_JasmineRakhracreated_at-907409179.txt"
    with open(path,'r',encoding="utf-8",errors="ignore") as f:
        data = ast.literal_eval(f.read())
        print(len(data))
    '''
        
    
    