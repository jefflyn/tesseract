package com.guru.gbdt

import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.tree.GradientBoostedTrees
import org.apache.spark.mllib.tree.configuration.BoostingStrategy
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.{ SparkConf, SparkContext }

object GBDTRegression {
  val conf = new SparkConf() //创建环境变量
    .setMaster("local[*]") //设置本地化处理
    .setAppName("GBDTRegression") //设定名称
  val sc = new SparkContext(conf) //创建环境变量实例
  def main(args: Array[String]) {
    val data = sc.textFile("src/main/resources/data/sku_data.csv") //获取数据集路径
    
    val parsedData = data.map { line => //开始对数据集处理
      val parts = line.split("\t") //根据tab进行分列
      val data_length = parts.length //文件列数
      println("data_length: " + data_length)
      val label = parts(data_length - 2)
       println("label: " + label)
      val features = parts.slice(0, data_length - 1).map(_.toDouble)
      LabeledPoint(label.toDouble, Vectors.dense(features))
    }.randomSplit(Array(0.7, 0.3)) //分成训练集、测试集

    val (trainingData, testData) = (parsedData(0), parsedData(1))
    val boostingStrategy = BoostingStrategy.defaultParams("Regression")
    boostingStrategy.numIterations = Integer.parseInt("20") // Note: Use more iterations in practice.
    boostingStrategy.treeStrategy.maxDepth = Integer.parseInt("10")
    boostingStrategy.treeStrategy.categoricalFeaturesInfo = Map[Int, Int]()
    val model = GradientBoostedTrees.train(trainingData, boostingStrategy)

    val predict_result = testData.map { p =>
      (p.label, model.predict(p.features))
    }

    // 模型保存
    model.save(sc, "models/GBDTRegressionModel")
    //val sameModel = LinearRegressionModel.load(sc, "target/tmp/scalaLinearRegressionWithSGDModel") 

    // 模型评价
    val MSE = predict_result.map(value =>
      {
        (value._1 - value._2) * (value._1 - value._2)
      }).mean()

    val RMSPE_TEMP = predict_result.filter(_._1 != 0).map(value =>
      {
        math.pow((value._1 - value._2) / value._1, 2)
      }).mean()
    val RMSPE = math.pow(RMSPE_TEMP, 0.5)

    val RMSLE = predict_result.map(value =>
      {
        math.pow(math.log(value._1 + 1) - math.log(value._2 + 1), 2)
      }).mean()

    println(predict_result.collect().mkString(",")) //打印预测结果
    println("MSE:" + MSE)
    println("RMSPE:" + RMSPE)
    println("RMSLE:" + RMSLE)
  }
}
