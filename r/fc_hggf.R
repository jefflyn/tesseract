library(quantmod)
setSymbolLookup(HGGF=list(name='600570.ss',src='yahoo'))
getSymbols("HGGF")
View(HGGF)
#head(HGGF)
#chartSeries(HGGF)

ORIG=data.frame(HGGF)
N0=nrow(ORIG)
#print(N0)
HGGF=na.omit(ORIG)
N=nrow(HGGF)
print(N)
subdata=HGGF[1:(N-30),1:4]
#print(subdata)
#由于后面需要对误差进行累加，此处对所有指标，按均值和标准差进行标准化处理
subdata=scale(subdata)
center.back=attr(subdata,"scaled:center")
scale.back=attr(subdata,"scaled:scale")

#ADF verify
# library(fUnitRoots)
# for(i in 1:ncol(subdata)){
#   pValue=adfTest(subdata[,i])@test$p.value
#   print(paster("target ",colnames(subdata)[i]," unit roots verify p value:",pValue))
# }

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
for(i in 1:30){
  predData=as.vector(subdata[(n+i-1):(n+i-p),])
  a=t(predData)
  b=a[,1]
  c=c(1,b)
  d=c(1,t(predData)[,1])
  e=lmList[[p]]
  
  predVals=d%*%e
  #使用均值和标准差，还原预测值
  predVals=predVals*scale.back+center.back
  preddf=rbind(preddf,predVals)
  
  subdata=rbind(subdata,(HGGF[n+i,1:4]-center.back)/scale.back)
}
rownames(preddf)=NULL
subdata.test=HGGF[(N-30+1):N,1:4]
summary(as.vector(abs(preddf-subdata.test)*100/subdata.test))

print(preddf[,4])
print(subdata.test[,4])

#plot
par(mfrow=c(2,2))
plot(preddf[,1],type='l',ylab='Open')
lines(subdata.test[,1],lty=2,col='red')

plot(preddf[,2],type='l',ylab='High')
lines(subdata.test[,2],lty=2,col='red')
plot(preddf[,3],type='l',ylab='Low')
lines(subdata.test[,3],lty=2,col='red')
plot(preddf[,4],type='l',ylab='Close')
lines(subdata.test[,4],lty=2,col='red')
par(mfrow=c(1,1))

