读入图片-> 边缘检测->二值化->轮廓检测->筛选结果融合->定位->数据集制作->模型训练->识别


增值税发票OCR

1. 识别文字方向，并做相应旋转，得到正面水平方向图片

2. 识别正面水平方向图片中的近似水平直线（Hough直线检测）

参考：(38条消息) OpenCV霍夫变换直线检测，Python_Zhang Phil-CSDN博客

https://blog.csdn.net/zhangphil/article/details/106288089?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~sobaiduend~default-1-106288089.nonecase&utm_term=opencv%E7%9B%B4%E7%BA%BF%E6%A3%80%E6%B5%8Bpython&spm=1000.2123.3001.4430

3. 旋转图片使得近似水平直线变成水平直线

phoebushe/invoice_OCR

https://github.com/phoebushe/invoice_OCR

4. 运用invoice_OCR进行图片切割，切出发票各部分


5. 对切出的发票部分进行文字识别（paddleOCR)

