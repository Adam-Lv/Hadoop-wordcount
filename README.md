# README
该项目使用docker-compose部署集群，其中使用的镜像adamlv/ubuntu-hadoop:1.7已公开上传至dockerhub，可直接使用。
项目中包括了一个Hadoop HelloWorld程序和一个Hadoop WordCount程序，位于包pers.hadoop.helloworld中。

## 1. 集群规模
所有节点均使用镜像adamlv/ubuntu-hadoop:1.7构建，使用docker-compose部署，包括一个master节点和四个slave节点，其中master节点上部署了
namenode、datanode、resourcemanager，所有slave节点上各自部署了datanode、nodemanager，额外在slave1节点上部署了secondarynamenode。
所有节点使用相同的配置文件，位于项目`hadoop-config`目录中。

## 2. 环境配置与集群启动
可以使用任意操作系统，但需要安装并开启docker服务，并且保证docker-compose可用、网络端口9870、8088空闲。
1. 在项目根目录下执行`docker-compose up -d`启动集群。
2. 进入master节点终端，执行`hdfs namenode -format`格式化namenode。
3. 执行`start-all.sh`启动集群。

## 3. WordCount程序运行
在master节点`/project/target`目录下执行
```shell
hadoop jar helloworld.jar pers.hadoop.helloworld.WordCount <input-file> <output-dir>
```
其中`<input-file>`为输入文件的hdfs路径，`<output-dir>`为输出目录的hdfs路径。
可以使用`hdfs dfs -put <local-file> <input-file>`将本地文件上传至hdfs，使用
`hdfs dfs -cat <output-dir>/part-r-00000`查看输出结果。

另外，当集群启动后，可以在宿主机通过`http://localhost:9870`访问HDFS管理界面，通过`http://localhost:8088`访问YARN管理界面。