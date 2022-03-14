# -*- coding: cp936 -*-
#
#根据字段，从【分类要素】中批量导出用来分类的要素，并按要这些要素裁剪【源要素】。
# 后续可增加：对结果进行统计分析
#
import os
import sys
import arcpy
import shutil
import traceback
import datetime
import time
reload(sys)
sys.setdefaultencoding('utf-8')
#创建文件夹
def mkdir(path):
    print(path)
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径

#通过文件名称获取文件名及后缀
#def getNameAndEXName(filename):

if __name__=='__main__':
    try:
        #print('========脚本启动=========')
        #p = sys.argv[1]  # cmd 执行代码的结构是：python test.py 2 所以：argv[0]=test.py，argv[1]=2
        #源要素
        sc_Input=arcpy.GetParameterAsText(0)
        #分类要素：用来分类的要素
        cf_Input=arcpy.GetParameterAsText(1)

        now = datetime.datetime.now()
        ts = now.strftime('%m-%d-%H-%M-%S')

        #上两级目录
        envPath = os.path.dirname(os.path.dirname(cf_Input))
        arcpy.env.workspace = envPath
        outputClipLayerDirPath=envPath+"\\"+ts+"re\\clipLayer"
        #outputExcelDirPath=envPath+"\\"+ts+"re\\excel"
        mkdir(outputClipLayerDirPath)
        #mkdir(outputExcelDirPath)
        #print(inpath)

        #maindir:目录 subdir:目录下的子目录  file_name_list:文件名
        fileArr=[]
        for maindir, subdir, file_name_list in os.walk(envPath):
            # print(maindir)
            # print(subdir)
            # print(file_name_list)
            for fn in file_name_list:
                getfn = fn.split(".")
                if len(getfn) == 2 and "shp" in getfn:
                   fileArr.append(fn)
        arcpy.AddMessage('========获取裁剪要素...=========')
        clipFeature_mainDir=envPath + "\\"+ts+"re\\clipLayer"
        clip_mainDir=arcpy.GetParameterAsText(3)
        #clip_mainDir = envPath + "\\" + ts + "re"
        # 裁剪要素字段名称
        # theFields = arcpy.ListFields(sc_Input)
        # FieldsArray = []  # 全部字段名
        # for Field in theFields:
        #     FieldsArray.append(Field.name)
        # if "FID" in FieldsArray:
        #     clipFieldName = ["FID"]
        # else:
        #     clipFieldName = ["OBJECTID"]
        FieldsName=arcpy.GetParameterAsText(2)
        clipFieldName=[]
        clipFieldName.append(FieldsName)
        with arcpy.da.SearchCursor(cf_Input,clipFieldName) as cursor:
            for row in cursor:
                clip_layerName=r"裁剪范围_"+str(row[0])
                clip_OutPath = clipFeature_mainDir+"\\"+ clip_layerName+ r".shp"
                # 创建临时图层,第一参数为临时图层路径，第二个参数为临时图层名称
                featureLayer=arcpy.MakeFeatureLayer_management(cf_Input,"temp_"+clip_layerName)
                sql=clipFieldName[0]+r" = "+"'"+str(row[0])+"'"
                #print sql
                arcpy.SelectLayerByAttribute_management(featureLayer, "NEW_SELECTION",sql )
                #导出裁剪要素
                arcpy.CopyFeatures_management(featureLayer, clip_OutPath)
            #关闭，否则shutil报错
            del cursor, row

            arcpy.AddMessage('========进行裁剪...=========')
        for maindir, subdir, file_name_list in os.walk(clipFeature_mainDir):
            for fn in file_name_list:
                getfn = fn.split(".")
                if len(getfn) == 2 and "shp" in getfn:
                    # 裁剪
                    arcpy.Clip_analysis(sc_Input, maindir+'\\'+fn, clip_mainDir+"\\完成的"+fn)
        shutil.rmtree(envPath+"\\"+ts+"re")
    except:
        arcpy.AddError(traceback.format_exc())
        shutil.rmtree(envPath+"\\"+ts+"re")

