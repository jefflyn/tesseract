package com.guru.chaos

/**
 * object作为Scala中的一个关键字，相当于Java中的public static class这样的一个修饰符，也就说object中的成员都是静态的！
 * 所以我们在这个例子中的main方法是静态的，不需要类的实例就可以直接被虚拟机调用，而这正是作为JVM平台上程序入口的必备
 * 条件；
 * 疑问：object是不是一个对象（此时，你肯定是从Java的角度是考虑），事实是object是Scala中的静态类，不是对象
 * 从Spark的Master和Worker的源码中我们都发现了其入口的main方法是在object中的；
 */
object HelloScala {
  /**
   * 1,def是什么，def是scala的关键字，所有用def定义的内容都是函数或者方法；
   * 2，这里的main是方法，因为被def定义且不具有函数特征；
   * 3，main是Scala语言中规定的Scala的应用程序的入口，一个运行的Scala应用程序只能有一个Main入口
   * 4，args: Array[String] 其中args是参数名称，Array[String]表面应用程序运行时候的传入参数集合
   * 5,: Unit 表明main入口方面的类型是Unit，也就是说执行main方法后返回的Unit类型；
   * 6，Unit是什么类型呢？相当于Java中Void类型
   * 7，=是什么？是表明main方法执行的结果是由谁来赋值的，或者或main方法的方法体在哪里？在“=“的右面！
   * 8，方法体一般有{}来封装，里面可以有很多条语句
   * 9，{}语句块默认情况下最后一条语句的结果类型就是{}的返回类型
   * 10，跟踪println的源代码的一个额外的收获是发现Scala的println的IO操作是借助了Java的IO操作，
   * 也就是说Scala调用了Java！！！
   * 11，如果方法或者函数的类型或者返回类型是Unit的话，
   * 就可以直接把“:Unit = ”去掉，其他的非Unit类型则不可去掉
   * 12，关于println打印出内容到控制台，底层借助了Java IO的功能，一个事实情况是Scala在做很多比较底层的实现的时候经常会
   * 使用Java的实现来缩短开发时间，例如说操作数据源（DB、NoSQL（Cassandra、HBase）等）的JDBC，再例如关于线程Thread的操作，Scala往往也会直接使用Java中的Thread；
   * 13，按照当今OS的原理，程序的main入口方法都是运行在主线程中的，OS的运行分为Kernel Space和User Space
   * ，应用程序是运行在User Space中，应用程序Scala所在的进程一般都是透过OS Fork出来，被Fork出来的应用程序进程默认会有主线程
   * 而我们的main方法就是默认在主线程中的；
   */
  def main(args: Array[String]) {
    println("Hello Scala!!!") //在Console上打印出"Hello Scala!!!"这个字符串并且换行
    //println(args.length)
  }
}
