1. 先安装谷歌浏览器

2. 下载谷歌访问助手并安装（当前目录下有安装包，解压后通过chrome扩展程序安装）

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


补充一个重要内容：

8. 在google colab中执行 !nohup python .... &时会报找不到某些python lib的问题，原因是因为nohup中用的python path不一样。

解决方法：

先执行 !which python3

/usr/bin/python3

然后用 /usr/bin/python3 替换 !nohup python .... & 中的python，即

!nohup /usr/bin/python3 train.py --epochs 30 --batch_size 8 --device 0 --raw --train_mmi >nohup.log 2>&1 &

输出的日志文件nohup.log可在google colab左边的目录树中找到，下载即可

9. google colab断线自动重连（防止其页面90分钟不操作退出）

打开浏览器F12，找到console将下面代码粘贴到控制台回车即可。若刷新了页面请重新执行上述步骤

setInterval(()=>{
	if(Array.from(document.getElementById("connect").children[0].children[2].innerHTML).splice(3,4).toString() === '重,新,连,接'){
		document.getElementById("connect").children[0].children[2].click()
	}
},1000)


