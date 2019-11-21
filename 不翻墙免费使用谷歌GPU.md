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

!nvidia-smi
Thu Nov 21 11:04:50 2019       
+-----------------------------------------------------------------------------+

| NVIDIA-SMI 430.50       Driver Version: 418.67       CUDA Version: 10.1     |

|-------------------------------+----------------------+----------------------+

| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |

| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |

|===============================+======================+======================|

|   0  Tesla K80           Off  | 00000000:00:04.0 Off |                    0 |

| N/A   41C    P0    58W / 149W |     69MiB / 11441MiB |      0%      Default |

+-------------------------------+----------------------+----------------------+

                                                                               
+-----------------------------------------------------------------------------+

| Processes:                                                       GPU Memory |

|  GPU       PID   Type   Process name                             Usage      |

|=============================================================================|

+-----------------------------------------------------------------------------+

5. 查看内存信息
!cat /proc/meminfo
