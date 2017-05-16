import AssemblyKeys._  
assemblySettings

name := "scala_sbt"

version := "1.0"

scalaVersion := "2.11.8"

EclipseKeys.createSrc := EclipseCreateSrc.Default + EclipseCreateSrc.Resource

libraryDependencies ++= Seq(
  "org.json4s" %% "json4s-native" % "3.2.10",
  "org.json4s" %% "json4s-jackson" % "3.2.10",
  "org.apache.spark" %% "spark-core" % "2.1.0",
  "org.apache.spark" %% "spark-mllib" % "2.1.0",
  "ml.dmlc" %% "xgboost4j-spark" % "0.7"
)

resolvers ++= Seq(
	// HTTPS is unavailable for Maven Central  
	"Maven Repository"     at "http://repo.maven.apache.org/maven2",  
	"Apache Repository"    at "https://repository.apache.org/content/repositories/releases",  
	"JBoss Repository"     at "https://repository.jboss.org/nexus/content/repositories/releases/",  
	"MQTT Repository"      at "https://repo.eclipse.org/content/repositories/paho-releases/",  
	"Cloudera Repository"  at "http://repository.cloudera.com/artifactory/cloudera-repos/",
	Resolver.mavenLocal
)