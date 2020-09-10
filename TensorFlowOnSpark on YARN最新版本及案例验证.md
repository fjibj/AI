TensorflowOnSpark mnist案例 On Yarn

方进 写于2020.9.10


由于TensorFlowOnSpark版本及案例有较大变动，但官方wiki https://github.com/yahoo/TensorFlowOnSpark/wiki/GetStarted_YARN 未做调整，经过几番调度，终于将mnist案例在yarn集群上跑起来，特记录如下

1. python编译过程如同wiki，无变化，但需要添加对bzip2的手工编译

下载bzip2-1.0.6.tar.gz

tar xvzf bzip2-1.0.6.tar.gz

cd bzip2-1.0.6

make -f Makefile-libbz2_so

make

make install PREFIX="${PYTHON_ROOT}"

2. 升级pip3到20.3，并安装tensorflow和tensorflow_datasets

${PYTHON_ROOT}/bin/pip3 install --upgrade pip

${PYTHON_ROOT}/bin/pip3 install tensorflow

${PYTHON_ROOT}/bin/pip3 install tensorflow_datasets

之后打包Python.zip并上传到HDFS上步骤同wiki

3. 下载mnist/3.0.1,并打包上传到HDFS上（此外可以先在google colab上运行一下tfds.load('mnist', with_info=True)下载下来，注意下载下来的3.0.0，可以将目录名称改为3.0.1）

mnist.zip内部结构如下:

mnist

   └── 3.0.1
   
       ├── dataset_info.json
       
       ├── image.image.json
       
       ├── mnist-test.tfrecord-00000-of-00001
       
       └── mnist-train.tfrecord-00000-of-00001
       
 hadoop fs -put mnist.zip .  (.表示hdfs:///user/yarn目录，当前用户是yarn)
 
 4. 修改TensorFlowOnSpark/examples/mnist/mnist_data_setup.py文件
 
 mnist, info = tfds.load('mnist', data_dir='datasets', download=False, try_gcs=False, with_info=True)  #此处data_dir批定的是mnist所在目录的上层目录）
 
 5. 设置各个环境变更（参考wiki)
 
 6. 提交spark-submit命令
 
 /home/yarn/spark-2.4.5-bin-hadoop2.6/bin/spark-submit \
 
--master yarn \

--deploy-mode cluster \

--queue ${QUEUE} \

--num-executors 4 \

--executor-memory 4G \

--conf spark.yarn.dist.archives=hdfs:///user/yarn/Python.zip#Python,hdfs:///user/yarn/mnist.zip#datasets \  （此外#datasets即为指定mnist.zip的解压到的目录）

--conf spark.pyspark.python=Python/bin/python3 \

--conf spark.executorEnv.PYSPARK_PYTHON=Python/bin/python3 \

--conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=Python/bin/python3 \

--conf spark.yarn.appMasterEnv.PYSPARK_DRIVER_PYTHON=Python/bin/python3 \

--jars /mnt/TensorFlowOnSpark/TensorFlowOnSpark-master/lib/tensorflow-hadoop-1.0-SNAPSHOT.jar \

/mnt/TensorFlowOnSpark/TensorFlowOnSpark-master/examples/mnist/mnist_data_setup.py \

--num_partitions 10 \

--output mnist1        (mnist1是HDFS上的结果输出目录）

7. 以下步骤同wiki，不再赘述
       
       
       




