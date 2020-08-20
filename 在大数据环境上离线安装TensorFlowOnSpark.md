在大数据环境上离线安装TensorFlowOnSpark

方进 2019-04-04 16:40:14

准备条件：

1. 一个已安装好的大数据集群环境，包括HDFS、YARN等

2. 各节点上已安装spark2.4.0

3. 准备好Python安装包

Python-3.6.8.tgz

Tensorflow依赖包，如下：https://pypi.org/

absl-py-0.7.1.tar.gz

astor-0.7.1-py2.py3-none-any.whl 

bleach-3.1.0-py2.py3-none-any.whl  

gast-0.2.2.tar.gz

get-pip.py  

grpcio-1.19.0-cp36-cp36m-manylinux1_x86_64.whl 

h5py-2.9.0-cp36-cp36m-manylinux1_x86_64.whl 

html5lib-1.0.1-py2.py3-none-any.whl  

Keras_Applications-1.0.7-py2.py3-none-any.whl   

Keras_Preprocessing-1.0.9-py2.py3-none-any.whl 

Markdown-3.1-py2.py3-none-any.whl

mock-2.0.0-py2.py3-none-any.whl  

numpy-1.16.2-cp36-cp36m-manylinux1_x86_64.whl

pbr-5.1.3-py2.py3-none-any.whl

protobuf-3.7.1-cp36-cp36m-manylinux1_x86_64.whl

six-1.12.0-py2.py3-none-any.whl

tensorboard-1.13.1-py3-none-any.whl

tensorflow-1.13.1-cp36-cp36m-manylinux1_x86_64.whl

tensorflow_estimator-1.13.0-py2.py3-none-any.whl

termcolor-1.1.0.tar.gz
termcolor2-0.0.3.tar.gz

webencodings-0.5.1-py2.py3-none-any.whl

Werkzeug-0.15.2-py2.py3-none-any.whl

wheel-0.33.1-py2.py3-none-any.whl



安装过程: 

1.  登录大数据集群的Master节点

mkdir -p tfspark/tf-package

2.  上传Python-3.6.8.tgz到tfspark目录下

3.  上传tensorflow依赖包到tfspark/tf-package目录下

4.  sudo su -   #切到root用户

5.  编译安装Python

cd /home/bdapp/tfspark	#进入前面创建的tfspark目录

mkdir Python

export PYTHON_ROOT=/home/bdapp/tfspark/Python	#即刚刚创建的Python目录的绝对路径

tar xvzf Python-3.6.8.tgz

cd Python-3.6.8

./configure --prefix="${PYTHON_ROOT}" --enable-unicode=ucs4

make

make install

cd ../Python/bin

ln -s python3.6 python

ln -s pip3 pip

5. 在每个节点安装glibc-2.17：

wget https://ftp.gnu.org/gnu/glibc/glibc-2.17.tar.gz

tar -xvf glibc-2.17.tar.gz

LD_LIBRARY_PATH=/usr/local/lib

export LD_LIBRARY_PATH

cd glibc-2.17

mkdir build

cd build

../configure --prefix=/usr --disable-profile --enable-add-ons --with-headers=/usr/include --with-binutils=/usr/bin

make && make install

6. 在所有节点上下载libstdc++.so.6.0.18放到/usr/lib64目录下

ln -sf libstdc++.so.6.0.18 libstdc++.so.6  #修改软链接

7. 安装tensorflow：

cd /home/bdapp/tfspark/tf-package	#进入前面创建的tf-package目录

${PYTHON_ROOT}/bin/pip install *.whl 

#如果有报错，检查是否有对应的.tar.gz或.tgz文件，解压安装

tar xvzf XXXX.tgz

cd XXXX

${PYTHON_ROOT}/bin/python setup.py install

cd ..

8. Python打包上传到HDFS

cd ${PYTHON_ROOT}

zip -r Python.zip *

exit	#切回当前用户

export PYTHON_ROOT=/home/bdapp/tfspark/Python	#重新设置一下，环境变量可能没带过来

hadoop fs -put ${PYTHON_ROOT}/Python.zip

9. 制作tfspark.zip

在其他可联网的机器上下载TensorFlowOnSpark并压缩

git clone https://github.com/yahoo/TensorFlowOnSpark

tar cvzf TensorFlowOnSpark.tar.gz TensorFlowOnSpark

将TensorFlowOnSpark.tar.gz上传到/home/bdapp/tfspark，解压

tar xvzf  TensorFlowOnSpark.tar.gz

cd TensorFlowOnSpark

zip -r tfspark.zip tensorflowonspark

10. tensorflow-hadoop-1.10.0.jar编译并上传HDFS

在其他可联网的机器上下载

git clone https://github.com/tensorflow/ecosystem

cd ecosystem/hadoop

mvn clean package

cd target

将tensorflow-hadoop-1.10.0.jar上传到/home/bdapp/tfspark目录

cd /home/bdapp/tfspark

hadoop fs -put tensorflow-hadoop-1.10.0.jar

11. Run MNIST example

mkdir mnist

cd mnist

下载MNIST数据集并上传到/home/bdapp/tfspark/mnist

	train-images-idx3-ubyte.gz
	
	train-labels-idx1-ubyte.gz
	
	t10k-images-idx3-ubyte.gz
	
	t10k-labels-idx1-ubyte.gz
	
zip -r mnist.zip *


运行案例：

设置环境变量（无GPU情况，有GPU的请参考 https://github.com/yahoo/TensorFlowOnSpark/wiki/GetStarted_YARN ）

# set environment variables (if not already done)

export LD_LIBRARY_PATH=${PATH}

export PYSPARK_PYTHON=${PYTHON_ROOT}/bin/python

export SPARK_YARN_USER_ENV="PYSPARK_PYTHON=Python/bin/python"

export PATH=${PYTHON_ROOT}/bin/:$PATH

# set paths to libjvm.so, libhdfs.so, and libcuda*.so

#export LIB_HDFS=/opt/cloudera/parcels/CDH/lib64		 # for CDH (per @wangyum)

export LIB_HDFS=/usr/lib64/             				 # path to libhdfs.so, for TF acccess to HDFS，不确定的话可以find一下

export LIB_JVM=$JAVA_HOME/jre/lib/amd64/server		 # path to libjvm.so

export QUEUE=default	

准备训练数据庥

# save images and labels as CSV files

${SPARK_HOME}/bin/spark-submit \

--master yarn \

--deploy-mode cluster \

--queue ${QUEUE} \

--num-executors 4 \

--executor-memory 4G \

--archives hdfs:///user/${USER}/Python.zip#Python,mnist/mnist.zip#mnist \

TensorFlowOnSpark/examples/mnist/mnist_data_setup.py \

--output mnist/csv \

--format csv

# save images and labels as TFRecords (OPTIONAL)

${SPARK_HOME}/bin/spark-submit \

--master yarn \

--deploy-mode cluster \

--queue ${QUEUE} \

--num-executors 4 \

--executor-memory 4G \

--archives hdfs:///user/${USER}/Python.zip#Python,mnist/mnist.zip#mnist \

--jars hdfs:///user/${USER}/tensorflow-hadoop-1.10.0.jar \

TensorFlowOnSpark/examples/mnist/mnist_data_setup.py \

--output mnist/tfr \

--format tfr

训练

Run distributed MNIST training (using feed_dict)

# hadoop fs -rm -r mnist_model

${SPARK_HOME}/bin/spark-submit \

--master yarn \

--deploy-mode cluster \

--queue ${QUEUE} \

--num-executors 2 \			#环境配置较低，此处设置的比较小

--executor-memory 2G \			#环境配置较低，此处设置的比较小

--py-files TensorFlowOnSpark/tfspark.zip,TensorFlowOnSpark/examples/mnist/spark/mnist_dist.py \

--conf spark.dynamicAllocation.enabled=false \

--conf spark.yarn.maxAppAttempts=1 \

--archives hdfs:///user/${USER}/Python.zip#Python \

--conf spark.executorEnv.LD_LIBRARY_PATH=$LIB_CUDA:$LIB_JVM:$LIB_HDFS \

TensorFlowOnSpark/examples/mnist/spark/mnist_spark.py \

--batch_size 10 \				#环境配置较低，此处设置的比较小

--images mnist/csv/train/images \

--labels mnist/csv/train/labels \

--mode train \

--model mnist_model

测试

Run distributed MNIST inference (using feed_dict)

${SPARK_HOME}/bin/spark-submit \

--master yarn \

--deploy-mode cluster \

--queue ${QUEUE} \

--num-executors 2 \

--executor-memory 2G \

--py-files TensorFlowOnSpark/tfspark.zip,TensorFlowOnSpark/examples/mnist/spark/mnist_dist.py \

--conf spark.dynamicAllocation.enabled=false \

--conf spark.yarn.maxAppAttempts=1 \

--archives hdfs:///user/${USER}/Python.zip#Python \

--conf spark.executorEnv.LD_LIBRARY_PATH=$LIB_JVM:$LIB_HDFS \

TensorFlowOnSpark/examples/mnist/spark/mnist_spark.py \

--images mnist/csv/test/images \

--labels mnist/csv/test/labels \

--mode inference \

--model mnist_model \

--output predictions

使用Spark Streaming进行训练和测试

准备数据集

Convert the MNIST zip files to image-label records

# hadoop fs -rm -r mnist/csv2

${SPARK_HOME}/bin/spark-submit \

--master yarn \

--deploy-mode cluster \

--queue ${QUEUE} \

--num-executors 4 \

--executor-memory 4G \

--archives hdfs:///user/${USER}/Python.zip#Python,mnist/mnist.zip#mnist \

TensorFlowOnSpark/examples/mnist/mnist_data_setup.py \

--output mnist/csv2 \

--format csv2

训练

Run distributed MNIST training (using Spark Streaming)

# create a folder for new streaming data to arrive

hadoop fs -mkdir stream_data

# hadoop fs -rm -r mnist_model stream_data/*

${SPARK_HOME}/bin/spark-submit \

--master yarn \

--deploy-mode cluster \

--queue ${QUEUE} \

--num-executors 2 \

--executor-memory 2G \

--py-files TensorFlowOnSpark/tfspark.zip,TensorFlowOnSpark/examples/mnist/streaming/mnist_dist.py \

--conf spark.dynamicAllocation.enabled=false \

--conf spark.yarn.maxAppAttempts=1 \

--conf spark.streaming.stopGracefullyOnShutdown=true \

--archives hdfs:///user/${USER}/Python.zip#Python \

--conf spark.executorEnv.LD_LIBRARY_PATH=$LIB_JVM:$LIB_HDFS \

TensorFlowOnSpark/examples/mnist/streaming/mnist_spark.py \

--batch_size 10 \

--images stream_data \

--format csv2 \

--mode train \

--model mnist_model

# make a temp copy of the data, so we can atomically move them into the stream_data input dir

hadoop fs -mkdir temp stream_data

hadoop fs -cp mnist/csv2/train/* temp

# drop data into the stream (monitor spark logs after each command to view behavior)

hadoop fs -mv temp/part-00000 stream_data

hadoop fs -mv temp/part-00001 stream_data

hadoop fs -mv temp/part-0000[2-9] stream_data

# shutdown job, since this normally runs forever, waiting for new data to arrive

# the host and port of the reservation server will be in the driver logs, e.g.

# "listening for reservations at ('gpbl191n01.blue.ygrid.yahoo.com', 38254)"

${PYTHON_ROOT}/bin/python TensorFlowOnSpark/com/yahoo/ml/tf/reservation_client.py <host> <port>
	
测试

Run distributed MNIST inference (using Spark Streaming)

# hadoop fs -rm -r -skipTrash predictions/* stream_data/*

${SPARK_HOME}/bin/spark-submit \

--master yarn \

--deploy-mode cluster \

--queue ${QUEUE} \

--num-executors 4 \

--executor-memory 27G \

--py-files TensorFlowOnSpark/tfspark.zip,TensorFlowOnSpark/examples/mnist/streaming/mnist_dist.py \

--conf spark.dynamicAllocation.enabled=false \

--conf spark.yarn.maxAppAttempts=1 \

--conf spark.streaming.stopGracefullyOnShutdown=true \

--archives hdfs:///user/${USER}/Python.zip#Python \

--conf spark.executorEnv.LD_LIBRARY_PATH=$LIB_JVM:$LIB_HDFS \

TensorFlowOnSpark/examples/mnist/streaming/mnist_spark.py \

--images stream_data \

--format csv2 \

--mode inference \

--model mnist_model \

--output predictions/batch

# make a temp copy of the data, so we can atomically move them into the stream_data input dir

hadoop fs -mkdir temp stream_data

hadoop fs -cp mnist/csv2/test/* temp
# drop data into the stream (monitor spark logs after each command to view behavior)

hadoop fs -mv temp/part-00000 stream_data

hadoop fs -mv temp/part-00001 stream_data

hadoop fs -mv temp/part-0000[2-9] stream_data

# shutdown job, since this normally runs forever, waiting for new data to arrive

# Note: the host and port of the reservation server will be in the driver logs, e.g.

# "listening for reservations at ('<host>', <port>)"
	
${PYTHON_ROOT}/bin/python TensorFlowOnSpark/src/com/yahoo/ml/tf/reservation_client.py <host> <port>
	
