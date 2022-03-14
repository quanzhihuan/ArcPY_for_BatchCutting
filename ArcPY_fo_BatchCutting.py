# -*- coding: cp936 -*-
#
#根据要素属性表，进行批量裁剪。该工具已写成ArcGIS脚本，需要配合Toolbox使用
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
    #print(path)
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


if __name__=='__main__':
    try:
        #被裁剪要素
        sc_Input=arcpy.GetParameterAsText(0)
        #裁剪范围要素
        cf_Input=arcpy.GetParameterAsText(1)

        now = datetime.datetime.now()
        ts = now.strftime('%m-%d-%H-%M-%S')

        #上两级目录
        envPath = os.path.dirname(os.path.dirname(cf_Input))
        arcpy.env.workspace = envPath
        outputClipLayerDirPath=envPath+"\\"+ts+"re\\clipLayer"
        mkdir(outputClipLayerDirPath)

        #maindir:目录 subdir:目录下的子目录  file_name_list:文件名
        fileArr=[]
        for maindir, subdir, file_name_list in os.walk(envPath):
            for fn in file_name_list:
                getfn = fn.split(".")
                if len(getfn) == 2 and "shp" in getfn:
                   fileArr.append(fn)
        arcpy.AddMessage('========获取裁剪要素...=========')
        clipFeature_mainDir=envPath + "\\"+ts+"re\\clipLayer"
        # 输出文件的路径（文件夹路径）
        clip_mainDir=arcpy.GetParameterAsText(3)
        #选择的裁剪字段，这里为文本型字段
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

