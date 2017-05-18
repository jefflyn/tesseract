package com.guru.chaos.spark

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext

object WordCount {
  def main(args: Array[String]): Unit = {
    /**
     * 1.创建Spark的配置对象SparkConf，设置Spark程序的运行时的配置信息，
     * 例如：通过setMaster来设置程序要链接的Spark集群的Master的URL,如果设置为local,
     * 则代表Spark程序在本地运行，特别适合于机器配置条件非常差的情况。
     */
    //创建SparkConf对象  
    val conf = new SparkConf()
    //设置应用程序名称，在程序运行的监控界面可以看到名称  
    conf.setAppName("My First Spark App!")
    //设置local使程序在本地运行，不需要安装Spark集群  
    conf.setMaster("local[2]")
    //conf.setMaster("spark://10.240.177.66:4040")
    /**
     * 2.创建SparkContext对象
     * SparkContext是spark程序所有功能的唯一入口，无论是采用Scala,java,python,R等都必须有一个SprakContext
     * SparkContext核心作用：初始化spark应用程序运行所需要的核心组件，包括DAGScheduler,TaskScheduler,SchedulerBackend
     * 同时还会负责Spark程序往Master注册程序等；
     * SparkContext是整个应用程序中最为至关重要的一个对象；
     */
    //通过创建SparkContext对象，通过传入SparkConf实例定制Spark运行的具体参数和配置信息  
    val sc = new SparkContext(conf)

    /**
     * 3.根据具体数据的来源（HDFS,HBase,Local,FS,DB,S3等）通过SparkContext来创建RDD；
     * RDD的创建基本有三种方式：根据外部的数据来源（例如HDFS）、根据Scala集合、由其他的RDD操作；
     * 数据会被RDD划分成为一系列的Partitions,分配到每个Partition的数据属于一个Task的处理范畴；
     */
    //读取本地文件，并设置一个partition  
    val lines = sc.textFile("src/main/resources/data/NOTICE", 1)

    /**
     * 4.对初始的RDD进行Transformation级别的处理，例如map,filter等高阶函数的变成，来进行具体的数据计算
     * 4.1.将每一行的字符串拆分成单个单词
     */
    //对每一行的字符串进行拆分并把所有行的拆分结果通过flat合并成一个大的集合  
    val words = lines.flatMap { line => line.split(" ") }
    /**
     * 4.2.在单词拆分的基础上对每个单词实例计数为1，也就是word => (word,1)
     */
    val pairs = words.map { word => (word, 1) }

    /**
     * 4.3.在每个单词实例计数为1基础上统计每个单词在文件中出现的总次数
     */
    //对相同的key进行value的累积（包括Local和Reducer级别同时Reduce）  
    val wordCounts = pairs.reduceByKey(_ + _)
    //打印输出  
    wordCounts.foreach(pair => println(pair._1 + ":" + pair._2))
    sc.stop()
  }
}