# README
该项目使用docker-compose部署集群，其中使用的镜像adamlv/ubuntu-hadoop:2.0已公开上传至dockerhub，可直接使用。
项目中包括了一个Hadoop HelloWorld程序和一个Hadoop WordCount程序，位于包pers.hadoop.helloworld中。镜像中
已经添加了maven构建工具，可以通过maven管理项目。

## 1. 集群规模
所有节点均使用镜像adamlv/ubuntu-hadoop:2.0构建，使用docker-compose部署，包括一个master节点和四个slave节点，其中master节点上部署了
namenode、datanode、resourcemanager，所有slave节点上各自部署了datanode、nodemanager，额外在slave1节点上部署了secondarynamenode。
所有节点使用相同的配置文件，位于项目`hadoop-config`目录中。

## 2. 环境配置与集群启动
可以使用任意操作系统，但需要安装并开启docker服务，并且保证docker-compose可用、网络端口9870、8088空闲。
1. 在项目根目录下执行`docker-compose up -d`启动集群。
2. 进入master节点终端，执行`hdfs namenode -format`格式化namenode。途中输入`Y`确认重新格式化。
3. 执行`start-all.sh`启动集群。

## 3. WordCount程序构建与运行
项目使用maven构建，在master节点`/project`目录下使用`mvn package`命令构建jar包。

之后进入`target`目录，使用以下命令运行WordCount程序：
```shell
hadoop jar HelloWorld-1.0.jar pers.hadoop.helloworld.WordCount <input-file> <output-dir>
```
其中`<input-file>`为输入文件的hdfs路径，`<output-dir>`为输出目录的hdfs路径。

在初始化hdfs文件系统后，文件系统中没有任何文件，需要使用`hdfs dfs -put <local-file> <input-file>`将本地文件上传至hdfs。代码提供了一个样例
输入文件`src/main/resources/words.txt`，经过maven构建后，位于`target/classes/words.txt`，可以使用以下命令上传至hdfs：
```shell
hdfs dfs -put target/classes/words.txt /words.txt
```
之后使用以下命令运行WordCount程序：
```shell
hadoop jar HelloWorld-1.0.jar pers.hadoop.helloworld.WordCount /words.txt /output
```

可以使用`hdfs dfs -cat <output-dir>/part-r-00000`查看输出结果。若使用如上命令上传文件，则可以使用
`hdfs dfs -cat /output/part-r-00000`查看输出结果。

另外，当集群启动后，可以在宿主机通过`http://localhost:9870`访问HDFS管理界面，通过`http://localhost:8088`访问YARN管理界面。

## 4. 可能出现的问题
1. docker镜像基于x86_64架构，在arm架构的处理器上运行速度十分缓慢。
2. 若出现"Pool overlaps with other one on this address space"报错提示，请对docker-compose.yml文件中的networks配置进行如下修改：
   - 删除所有节点的IP地址分配，将`hadoop:`更改为`- hadoop`。
   - 删除networks配置中的`ipam`配置（文件的最后四行）。