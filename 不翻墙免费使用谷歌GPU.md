1. 先安装谷歌浏览器

2. 下载谷歌访问助手并安装，参考
https://segmentfault.com/a/1190000020548973?utm_source=tag-newest

3. 使用谷歌云端硬盘，可用QQ帐号注册，参考
http://www.sohu.com/a/332938797_787107

注1：看到有小伙伴即使关联本应用（Colaboratory），在谷歌云端硬盘的新建目录下仍然看不到它。我的办法是：

1） 转到页面：https://colab.research.google.com/notebooks/welcome.ipynb

2） 单击菜单栏偏下方的“复制到云端硬盘”

3） 进入自己的谷歌云端硬盘(drive.google.com)，可以看到出现一个黄色的文件夹，叫做Colab Notebooks，双击打开，里面有文件名为'“欢迎使用Colaboratory”的副本‘

4）这时候再单击云端硬盘的“新建”-“更多”，就能看到“Google Colaboratory”项了。

注2：如果查找自己的工作目录？

执行!find . -name test0.ipynb， 其中test0.ipynb是你当前正在编辑的文件

4. 查看GPU信息

import tensorflow as tf

tf.test.gpu_device_name()

from tensorflow.python.client import device_lib

device_lib.list_local_devices()

!nvidia-smi（配置好象还不错）

5. 查看内存信息

!cat /proc/meminfo

6. 每新建一个xxxx.ipynb文件，设置好“修改”->"笔记本设置”->“硬件加速器”，选择GPU后，就拥有了一个12G内存、300G存储和GPU（>12G显存,Tesla系统）的环境，真的很爽！

7. 安装Open in Colab（谷歌浏览器插件），则可以在谷歌浏览器浏览到某个.ipynb文件时，点击浏览器右上角的横8字（colaboratory图标）按钮，就可以在colaboratory中直接打开该文件（根据需要在“笔记本设置”中设置“硬件加速器”），这种方法无需打开google云硬盘！！！
