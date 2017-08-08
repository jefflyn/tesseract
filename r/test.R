library(quantmod)
setSymbolLookup(TARGET=list(name="600126.SS",src="yahoo"))
getSymbols("TARGET")

TARGET=data.frame(TARGET)
print(nrow(TARGET))

TARGET=na.omit(TARGET)
N=nrow(TARGET)
print(N)

# subdata=TARGET[1:(N-30),1:4]
subdata=TARGET
print(nrow(subdata))

print(paste("TARGET start from ",min(row.names(TARGET))," to ",max(row.names(TARGET))))
print(paste("subdata start from ",min(row.names(subdata))," to ",max(row.names(subdata))))

subdata=scale(subdata)
center.back=attr(subdata,"scaled:center")
scale.back=attr(subdata,"scaled:scale")

#ADF verify
library(tseries)
for(i in 1:ncol(subdata)){
  pValue=adf.test(subdata[,i])$p.value
  print(paste("target ",colnames(subdata)[i]," unit roots verify p value:",pValue))
}

#Vector Autoregression 
rowCol=dim(subdata)
#print(rowCol[2])
aicList=NULL
lmList=list()
for(p in 1:10){
  baseData=NULL
  
  for(i in (p+1):rowCol[1]){
    baseData=rbind(baseData,c(as.vector(subdata[i,]),as.vector(subdata[(i-1):(i-p),])))
  }
  
  X=cbind(1,baseData[,(rowCol[2]+1):ncol(baseData)])
  Y=baseData[,1:rowCol[2]]
  #print(Y)
  coefMatrix=solve(t(X)%*%X)%*%t(X)%*%Y
  #print(coefMatrix)
  aic=log(det(cov(Y-X%*%coefMatrix)))+2*(nrow(coefMatrix)-1)^2*p/nrow(baseData)
  #print(aic)
  aicList=c(aicList,aic)
  lmList=c(lmList,list(coefMatrix))
}
data.frame(p=1:10,aicList)

#predict and validation
p=which.min(aicList)
p=1
print(p)
n=nrow(subdata)
preddf=NULL
subdata=data.frame(subdata)
print(nrow(subdata))

###
# predData=as.vector(subdata[(507+1-1):(507+1-1),])
# print(predData)
# a=t(predData)
# b=a[,1]
# c=c(1,b)
# d=c(1,t(predData)[,1])
# e=lmList[[p]]
# 
# predVals=d%*%e
# print(predVals)
# #使用均值和标准差，还原预测值
# fiPredVals=predVals*scale.back+center.back
# print(fiPredVals)
# preddf=rbind(preddf,fiPredVals)
# subdata=rbind(subdata,as.vector(predVals))

for(i in 1:30){
  predData=as.vector(subdata[(n+i-1):(n+i-p),])
  a=t(predData)
  b=a[,1]
  c=c(1,b)
  d=c(1,t(predData)[,1])
  e=lmList[[p]]
  
  predVals=d%*%e
  #使用均值和标准差，还原预测值
  finalPredVals=predVals*scale.back+center.back
  
  preddf=rbind(preddf,finalPredVals)
  
  #subdata=rbind(subdata,(TARGET[n+i,1:4]-center.back)/scale.back)
  #把预测值加进数据，预测下一期
  subdata=rbind(subdata,as.vector(predVals))
}
print(preddf)
rownames(preddf)=NULL

#plot
par(mfrow=c(2,2))
plot(preddf[,1],type='l',ylab='Open')
#lines(subdata.test[,1],lty=2,col='red')
plot(preddf[,2],type='l',ylab='High')
#lines(subdata.test[,2],lty=2,col='red')
plot(preddf[,3],type='l',ylab='Low')
#lines(subdata.test[,3],lty=2,col='red')
plot(preddf[,4],type='l',ylab='Close')
#lines(subdata.test[,4],lty=2,col='red')
par(mfrow=c(1,1))

