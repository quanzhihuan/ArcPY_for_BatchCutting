# ArcPY_for_BatchCutting
ArcGIS脚本工具(ArcGIS scripting tools):利用ArcPY，实现按要素属性表进行批量裁剪。（ Using arcpy to realize batch cutting according to element attribute table）<br />
**注意**：该脚本已集成为ArcGIS脚本工具（项目中的Toolbox），需要配合ArcGIS使用。（Note: The script has been integrated into ArcGIS script tool (toolbox in the project) and needs to be used with ArcGIS）</p>
****
**参数说明**：<br />
被裁剪数据：需要被裁剪的数据<br />
裁剪范围数据：用于作为裁剪范围的数据<br />
裁剪分类字段：【裁剪范围数据】中，用于分类的字段，输出时，会以该字段进行批量命名输出数据名称<br />
输出文件夹：批量裁剪后的数据的输出地址<br />
