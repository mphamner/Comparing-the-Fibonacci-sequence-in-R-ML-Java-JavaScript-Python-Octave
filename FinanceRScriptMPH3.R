## Utilize quantmod to load the security symbols
##  require(quantmod)
##
## symbols <- c("AMZN", "QQQ")
## getSymbols(symbols)
##
## quantmod isn't quite right so go directly to Yahoo Finance and get the data
## also QQQQ doesn't exist any more.  It is now QQQ.

library(xts)
library(xlsx)
library(openair)
library(quantmod)
library(lubridate)

sym1 <- readline(prompt = "Enter the stock ticker symbol for the first stock:  ")

sym2 <- readline(prompt = "Enter the stock ticker symbol for the second stock:  ")


a <- "https://www.google.com/finance/historical?output=csv&q="
b <- "&startdate=January+01%2C+2007&enddate=December+31%2C+2016"
url1 <- paste(a, sym1, b, sep = "")
print(url1)

d <- "https://www.google.com/finance/historical?output=csv&q="
e <- "&startdate=January+01%2C+2007&enddate=December+31%2C+2016"
url2 <- paste(d, sym2, e, sep = "")
print(url2)


g <- "~/MyRWork/"
h <- ".xlsx"
dfile1 <- paste(g, sym1, h, sep = "")
print(dfile1)

m <- "~/MyRWork/"
n <- ".xlsx"
dfile2 <- paste(m, sym2, n, sep = "")
print(dfile2)

download.file(url1, dfile1)
sym1Data <- read.csv(dfile1, sep = ",", header = T, quote = "")
names(sym1Data) <- c("Date", "Open", "High", "Low", "Close", "Volume")
sym1Data$Date <- as.Date(sym1Data$Date, "%d-%b-%y")
str(sym1Data)
sym1Data <- sym1Data[order(sym1Data$Date),]


download.file(url2, dfile2)
sym2Data <- read.csv(dfile2, sep = ",", header = T, quote = "")
names(sym2Data) <- c("Date", "Open", "High", "Low", "Close", "Volume")
sym2Data$Date <- as.Date(sym2Data$Date, "%d-%b-%y")
str(sym2Data)
sym2Data <- sym2Data[order(sym2Data$Date),]


## Align the time series data
##

mData <- merge(sym1Data, sym2Data, by="Date")
## data <- na.locf(data)

sym1Data <- mData[, 1:6]
str(sym1Data)
sym2Data <- mData[, c(1,7:11)]
str(sym1Data)

sym1DataXts <- xts(sym1Data[,-1], order.by = sym1Data$Date)
str(sym1DataXts)
sym2DataXts <- xts(sym2Data[,-1], order.by = sym2Data$Date)
str(sym2DataXts)


##
## Finished reading in data
##
## Subset data for in sample processing


startT <- min(sym1Data$Date)
endT <- max(sym1Data$Date)
rangeT <- paste(startT, "::", endT, sep = "")
cat("Date range is: ",rangeT)

tsym1 <- sym1DataXts[,5][rangeT]
tsym2 <- sym2DataXts[,5][rangeT]

##
## Subset data for out of sample processing
##


print("I am ready to plot data.")
##Explore the data
chartSeries(sym1DataXts)
chartSeries(sym2DataXts)


#compute price differences on in-sample data
pdtsym1 <- diff(tsym1[-1])
pdtsym2 <- diff(tsym2[-1])

#build the model
model  <- lm(pdtsym1 ~ pdtsym2 - 1)
print(summary(model))

mpdtsym1 <- as.numeric(pdtsym1)
mpdtsym2 <- as.numeric(pdtsym2)

xlab1 <- paste(sym2, "Adjusted Close Diff")
ylab1 <- paste(sym1, "Adjusted Close Diff")
plot(mpdtsym1, mpdtsym2, xlab = xlab1, ylab = ylab1)
abline(lm(pdtsym1 ~ pdtsym2 -1), col="red", lwd=2)


#extract the hedge ratio
hr <- as.numeric(model$coefficients[1])

#calc spread price (in-sample)
spreadT <- tsym1 - (hr * tsym2)

#compute statistics of the spread
meanT    <- as.numeric(mean(spreadT,na.rm=TRUE))
sdT      <- as.numeric(sd(spreadT,na.rm=TRUE))
upperThr <- meanT + 1 * sdT
lowerThr <- meanT - 1 * sdT

#visualize the in-sample spread + stats
main1 <- paste(sym1, "vs.", sym2, "spread (in-sample period)")
plot(spreadT, main = main1)
abline(h = meanT, col = "red", lwd =2)
abline(h = meanT + 1 * sdT, col = "blue", lwd=2)
abline(h = meanT - 1 * sdT, col = "blue", lwd=2)

main2 <- paste("Spread Histogram(", sym1, "vs.", sym2, ")")
hist(spreadT, col = "blue", breaks = 100, main = main2)
abline(v = meanT, col = "red", lwd = 2)

indSell <- which(spreadT >= meanT + sdT)
indBuy  <- which(spreadT <= meanT - sdT)

spreadL  <- length(spreadT)
pricesB  <- c(rep(NA,spreadL))
pricesS  <- c(rep(NA,spreadL))
sp       <- as.numeric(spreadT)
tradeQty <- 100
totalP   <- 0

for(i in 1:spreadL) {
    spTemp <- sp[i]
    if(spTemp < lowerThr) {
        if(totalP <= 0){
            totalP     <- totalP + tradeQty
            pricesB[i] <- spTemp
        }
    } else if(spTemp > upperThr) {
        if(totalP >= 0){
            totalP <- totalP - tradeQty
            pricesS[i] <- spTemp
        }
    }
}

main3 <- paste(sym1, "vs.", sym2, "spread (in-sample period)")
plot(spreadT, main = main3)
abline(h = meanT, col = "red", lwd =2)
abline(h = meanT + 1 * sdT, col = "blue", lwd = 2)
abline(h = meanT - 1 * sdT, col = "blue", lwd = 2)
points(xts(pricesB,index(spreadT)), col="green", cex=1.9, pch=19)
points(xts(pricesS,index(spreadT)), col="red", cex=1.9, pch=19)

##
#build a separate lm for the calendar year 2016
##

startR <- min(sym1Data$Date)
endR <- max(sym1Data$Date)
rangeR <- paste(startR, "::", endR, sep = "")
cat("The range R is: ", rangeR)

##
#subset the data for this date range
##

rsym1 <- sym1DataXts[,5][rangeR]
rsym2 <- sym2DataXts[,5][rangeR]

##
#build the linear model
##

model2 <- lm(rsym1 ~ rsym2)
print(summary(model2))

##
#create a scatterplot with trend line 
##

jsym1 <- as.numeric(rsym1)
jsym2 <- as.numeric(rsym2)


xlab2 <- paste("2016", sym2, "Adjusted Close Diff")
ylab2 <- paste("2016", sym1, "Adjusted Close Diff")
plot(jsym2, jsym1, xlab = xlab2, ylab = ylab2)
abline(lm(rsym1 ~ rsym2), col='red', lwd=2)


