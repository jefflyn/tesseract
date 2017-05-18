package com.guru.xgboost

import ml.dmlc.xgboost4j.scala.spark.{ DataUtils, XGBoost }
import ml.dmlc.xgboost4j.scala.spark.XGBoost
import ml.dmlc.xgboost4j.scala.DMatrix
import org.apache.spark.{ SparkConf, SparkContext }
import org.apache.log4j.{ Level, Logger }
import org.apache.spark.sql.{ SparkSession, Row }
import org.apache.spark.mllib.util.MLUtils
import org.apache.spark.ml.feature.LabeledPoint
import org.apache.spark.ml.linalg.Vectors

object XGBoostScalaExample {
  def main(args: Array[String]) {

     //read trainining data, available at xgboost/demo/data
        val trainData =
          new DMatrix("src/main/resources/data/agaricus.txt.train")
        // define parameters
        val paramMap = List(
          "eta" -> 0.1,
          "max_depth" -> 2,
          "objective" -> "binary:logistic").toMap
        // number of iterations
        val round = 2
        // train the model
        val model = ml.dmlc.xgboost4j.scala.XGBoost.train(trainData, paramMap, round)
        // run prediction
        val predTrain = model.predict(trainData)
        // save model to the file.
        model.saveModel("model")
  }

}