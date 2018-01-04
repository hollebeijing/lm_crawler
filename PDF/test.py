# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# '''
#     Create  : 2017/12/27 下午12:34
#     Author  : Richard Chen
#     File    : test.py
#     Software: IntelliJ IDEA
# '''
#
# #!/usr/bin/env python2
# #-*-encoding:utf-8-*-
# from pdfminer.pdfparser import PDFParser
# from pdfminer.pdfdocument import PDFDocument
# from pdfminer.pdfpage import PDFPage
# from pdfminer.pdfpage import PDFTextExtractionNotAllowed
# from pdfminer.pdfinterp import PDFResourceManager
# from pdfminer.pdfinterp import PDFPageInterpreter
# from pdfminer.pdfdevice import PDFDevice
# from pdfminer.layout import *
# from pdfminer.converter import PDFPageAggregator
# import urllib2
# from cStringIO import StringIO
#
# def Pdf2Txt(DataIO,Save_path):                     #来创建一个pdf文档分析器
#     parser = PDFParser(DataIO)                     #创建一个PDF文档对象存储文档结构
#     document = PDFDocument(parser)
#     if not document.is_extractable:
#         raise PDFTextExtractionNotAllowed
#     else:
#         #创建一个PDF资源管理器对象来存储共赏资源
#         rsrcmgr=PDFResourceManager();            #设定参数进行分析
#         laparams=LAParams();                    #创建一个PDF设备对象
#         #device=PDFDevice(rsrcmgr)
#         device=PDFPageAggregator(rsrcmgr,laparams=laparams);#创建一个PDF解释器对象
#         interpreter=PDFPageInterpreter(rsrcmgr,device)
#         #处理每一页
#         for page in PDFPage.create_pages(document):
#             interpreter.process_page(page);        #接受该页面的LTPage对象
#             layout=device.get_result()
#             for x in layout:
#                 try:
#                     if(isinstance(x,LTTextBoxHorizontal)):
#                         with open('%s'%(Save_path),'a') as f:
#                             f.write(x.get_text().encode('utf-8')+'\n')
#                 except:
#                     print "Failed!"
#
# #convert online pdf
# '''
# url = "pdf url";
# html = urllib2.urlopen(urllib2.Request(url)).read();
# DataIO = StringIO(html.read());
# Pdf2Txt(DataIO,r'C:\workspace\python\converter\resource\b2.txt');
# '''
# #convert local pdf
# with open(r'C:\workspace\python\converter\resource\text.pdf','rb') as html:
#     DataIO = StringIO(html.read())
#     Pdf2Txt(DataIO,r'C:\workspace\python\converter\resource\b3.txt')