#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 00:15:32 2024

@author: h.chou
"""

import numpy as np
import numpy
import pandas as pd
import math 
from scipy.stats import norm
import scipy.optimize as opt
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from operator import length_hint
import scipy
import seaborn as sns
import sympy
from sympy import *     
from pandas import Series,DataFrame
from datetime import datetime
from scipy import stats
import heapq
from scipy import interpolate
from scipy.optimize import fsolve
from sklearn.metrics import roc_curve, auc
#1
Name1 = "5172_ENE"       #標的1 SIC code+ticker
Name2 = "5172_SUN"         #標的2 SIC code+ticker
TIME = 30            #破產前幾天
Time = 20111010         #從幾號的資料開始抓
#選出我們要的公司及選擇權種類
#Data1 = Company.loc[Company["issuer"] == "ARCH COAL INC"]
#Data1 = Data1.loc[Data1["cp_flag"] == "P"]
#c = [] 
#for i in range(Data1.shape[0]):
#    if Data1.iloc[i,2][3]!=" ":
#        c.append(i)
#Data1 = Data1.drop(Data1.index[c])
#Company = pd.read_csv('~/Documents/Data/delisted_nomomax/6211_LEH_option_new_t.csv')
Company = pd.read_csv('~/Documents/Data/delisted_new_t/6211_LEH_option.csv')
Data1 = Company
#這裡選取倒數N天
Mark=Data1.iloc[-1,0]
list=[]
count=1
for i in range(Data1.shape[0]):
    if Mark!=Data1.iloc[-(i+1),0]:
        count=count+1
        Mark=Data1.iloc[-(i+1),0]
    if count==TIME+1:
        break
    list.append(-(i+1))
Data2 =Data1.loc[Data1.index[list],:]
Data2=Data2.iloc[::-1]
#-----------------------------------------------------------------------------
# 判斷 C 或 P 並且過濾價內資料
K = Data2.iloc[:, 2]
S = Data2.iloc[:, 4]
# 判斷 C 或 P 並且過濾價內資料
def remove_in_the_money_options(Data2):
    # 確保第2列和第4列的數據為數值類型，如果無法轉換則會變為 NaN
    Data2.iloc[:, 2] = pd.to_numeric(Data2.iloc[:, 2], errors='coerce')  # 行權價 K
    Data2.iloc[:, 4] = pd.to_numeric(Data2.iloc[:, 4], errors='coerce')  # 標的資產現價 S

    # 分別取出第2列的行權價 (K) 和第4列的標的資產現價 (S)
    K = Data2.iloc[:, 2]
    S = Data2.iloc[:, 4]
    
    # 取出第8列的權證類型 (C for call, P for put)
    option_type = Data2.iloc[:, 8]
    
    # 條件1: 買權（Call）且 S > K (價內)
    condition_call = (option_type == 'C') & (S > K)
    
    # 條件2: 賣權（Put）且 S < K (價內)
    condition_put = (option_type == 'P') & (S < K)
    
    # 將符合以上兩個條件的資料列刪除
    Data3 = Data2[~(condition_call | condition_put)]
    
    return Data3

# 執行函數
Data3 = remove_in_the_money_options(Data2)
#-----------------------------------------------------------------------------
for i in range(Data3.shape[0]):
    if Data3.iloc[i, 8] == 'C':  # 如果第8欄為C（買權）
        # 提取S、K、r、T值
        S = Data3.iloc[i, 4]  # 第4欄的S
        K = Data3.iloc[i, 2]  # 第2欄的K
        r = Data3.iloc[i, 5]  # 第5欄的r
        T = Data3.iloc[i, 3]  # 第3欄的T
        
        # 計算賣權價格（轉換）
        P_converted = K * np.exp(-r * T) - S
        
        # 更新該行的第9欄位為轉換後的賣權價格
        Data3.iloc[i, 9] = P_converted
#-----------------------------------------------------------------------------
T = Data2.iloc[:,3]
R = Data2.iloc[:,5]
F = Data2.iloc[:,6]
S = Data2.iloc[:,4]
date=Data1.iloc[0,0]
#Del=S[S["date"]<Time].index
#S = S.drop(index=Del)
#紀錄日期最後繪圖用
#Datelist = S.iloc[len(S)-TIME:len(S),1].tolist()
#for i in range(len(Datelist)):
#    Datelist[i] = datetime.strptime(str(Datelist[i]), '%Y%m%d')

#S = Series(S["close"].tolist())
Variable = pd.concat([R,T,S,F], axis=1)
Variable.columns = ['Rate','Time','Stock Price','Future Price']
Variable=Variable.iloc[len(Variable)-TIME:len(Variable),:]
S1 = pd.read_csv('~/Documents/Data/Stock_delisted/1311_GPOR_stock.csv')
#S1 = pd.read_csv('~/Documents/Data/Archive_de_stock/4911_FE_stock.csv')
Del=S1[S1["date"]<Time].index
S1 = S1.drop(index=Del)
#紀錄日期最後繪圖用
Datelist = S1.iloc[len(S1)-TIME:len(S1),1].tolist() 
for i in range(len(Datelist)):
    Datelist[i] = datetime.strptime(str(Datelist[i]), '%Y%m%d')
S1 = Series(S1["close"].tolist())
#-----------------------------------------------------------------------------
T = Data2.iloc[:,3]
R = Data2.iloc[:,5]
F = Data2.iloc[:,6]
S = Data2.iloc[:,4]
date=Data1.iloc[0,0]

#Test version
Variable = pd.concat([R,T,S,F], axis=1)
Variable.columns = ['Rate','Time','Stock Price','Future Price']
Variable = Variable.drop_duplicates(subset=['Rate', 'Time', 'Stock Price', 'Future Price'])





Variable = pd.concat([R,T,S,F], axis=1)
Variable.columns = ['Rate','Time','Stock Price','Future Price']
Variable=Variable.iloc[len(Variable)-TIME:len(Variable),:]
#S1 = pd.read_csv('~/Documents/Data/Stock_delisted/1311_LINE_stock.csv')
S1 = pd.read_csv('~/Documents/Data/Archive_de_stock/6211_LEH_stock.csv')
#S1 = pd.read_csv('~/Documents/Data/Stock_delisted_new/2834_MNK_stock.csv')
# 設定 Time 為 datetime 類型
Time = datetime(2001, 9, 3)
# 轉換 S1["date"] 為 datetime 類型
S1['date'] = pd.to_datetime(S1['date'], format='%Y/%m/%d', errors='coerce')
# 正確比較日期，篩掉太早的資料
S1 = S1[S1["date"] >= Time].reset_index(drop=True)
Datelist = S1["date"].iloc[-TIME:].tolist()
S1 = Series(S1["close"].tolist())
#-----------------------------------------------------------------------------
# 找最長的履約價
Num = []
date = Data3.iloc[0, 0]
A = 0
for i in range(Data3.shape[0]):
    if Data3.iloc[i, 0] == date:
        A = A + 1
    else:
        date = Data3.iloc[i, 0]
        Num.append(A)
        A = 1
Num.append(A)
Strike = max(Num)

# 確認變數 Strike 和 Variable.shape[0] 的值
print("Strike:", Strike)
print("Variable.shape[0]:", Variable.shape[0])

# 整理 K
K = pd.DataFrame(columns=range(Variable.shape[0]), index=range(Strike))  # 創建一個 DataFrame，行數是 Strike，列數是 Variable 的行數
date = Data3.iloc[0, 0]  # 初始化第一個交易日的日期
row = 0  # 用來標記當前的列索引（即哪一天）
Column = 0  # 用來標記當前的行索引（即當天的履約價數量）

for i in range(Data3.shape[0]):  # 遍歷 Data2 中的每一行
    if Data3.iloc[i, 0] == date:  # 如果當前行的日期和前一行相同
        if Column < Strike and row < Variable.shape[0]:  # 檢查當前的行和列索引是否超出範圍
            K.iloc[Column, row] = Data3.iloc[i, 2]  # 將 Data2 中的履約價填入 K
        Column = Column + 1  # 增加當前履約價的行索引
    else:  # 當遇到新的一天
        date = Data3.iloc[i, 0]  # 更新交易日期
        row = row + 1  # 切換到下一列（新的一天）
        Column = 0  # 重置行索引，因為新的一天從頭開始計算履約價
        if Column < Strike and row < Variable.shape[0]:  # 檢查範圍
            K.iloc[Column, row] = Data3.iloc[i, 2]  # 將履約價填入 K
        Column = Column + 1  # 增加行索引

# 整理 Price
P = pd.DataFrame(columns=range(Variable.shape[0]), index=range(Strike))
date = Data3.iloc[0, 0]
row = 0
Column = 0
for i in range(Data3.shape[0]):
    if Data3.iloc[i, 0] == date:
        if Column < Strike and row < Variable.shape[0]:
            P.iloc[Column, row] = Data3.iloc[i, 9]
        Column = Column + 1
    else:
        date = Data3.iloc[i, 0]
        row = row + 1
        Column = 0
        if Column < Strike and row < Variable.shape[0]:
            P.iloc[Column, row] = Data3.iloc[i, 9]
        Column = Column + 1
#-----------------------------------------------------------------------------
Problist_delisted = []
MSErecord_delisted=0
MAPErecord_delisted = []
for i in range(len(Variable)):
    #將選擇權資料重新排列
    Option_data = pd.DataFrame(zip(K.iloc[:,i],P.iloc[:,i]), columns = ['Strike price','Price']).dropna(axis=0)
    Option_data = Option_data.sort_values(by=['Strike price'], ascending=True)
    Opt_len = Option_data.shape[0]
    dz=0.4
    h=2*dz
    Z=numpy.arange(Option_data.iloc[0,0],Option_data.iloc[Opt_len-1,0]+dz,dz).tolist()
    Z.insert(0,0)
    dis=length_hint(Z) 
    PCA_1 = pd.DataFrame(columns=Option_data.iloc[:,0],index=Z)
    for k in range(Opt_len):
        for j in range(dis):
            PCA_1.iloc[j,k]=(Option_data.iloc[k,0]-Z[j])/h
    
    #做PCA
    PCA_2= pd.DataFrame(columns=Option_data.iloc[:,0],index=Z)
    for k in range(Opt_len):
        for j in range(dis):
            PCA_2.iloc[j,k]=(math.exp(-0.5*(PCA_1.iloc[j,k])**2)/math.sqrt(2*math.pi)+PCA_1.iloc[j,k]*norm.cdf(PCA_1.iloc[j,k]))/h
  
    #做最佳化
    def PCA_fnc(a):
        PCA=0
        for k in range(Opt_len):
            Sum=0
            for j in range(dis):
                Sum=Sum+a[j]*PCA_2.iloc[j,k]
            PCA=PCA+abs((Option_data.iloc[k,1]-Sum)/Option_data.iloc[k,1])
        return PCA

    def con(a):
        A=np.sum(a)
        return A-1
    def con_F(a):
        B=0
        for j in range(dis):
            B=B+a[j]*Z[j]
        return B-F.iloc[i]
    cons = [{'type':'eq', 'fun': con},
            {'type':'eq', 'fun': con_F}]
    a0=[1/dis]*dis
    PCA_fnc(a=a0)
    bounds = [(0,1)]*dis
    res = opt.minimize(PCA_fnc,a0,bounds=bounds,constraints=cons)
    
    #印出預測誤差及分配
    print("破產前", len(Variable)-i ,"天破產機率預測")
    print("適配MAPE為",np.round(res['fun']/Opt_len,decimals=4))
    MSErecord_delisted = MSErecord_delisted+np.round(res['fun']/Opt_len,decimals=4)
    MAPErecord_delisted.append(np.round(res['fun'] / Opt_len, decimals=4))
    def PCA(x):
        SUM_RND=0
        for j in range(dis):
            SUM_RND=SUM_RND+res['x'][j]*(sympy.exp(-0.5*((x-Z[j])/h)**2)/(2*sympy.pi)**0.5)/h
        return(SUM_RND)  
    x = symbols('x')
    Prob = integrate(PCA(x), (x,-float("inf"),0)).simplify()
    Problist_delisted.append(np.round(float(Prob),decimals=4))
    Prob = np.round(float(Prob)*100,decimals=4)
    print("破產機率為: ", Prob,"%")
    print("係數為 : ")
    print(np.round(res['x'],decimals=4))
    print("--------------------------------------------------------------------")
    #畫出破產機率時間序列圖
    
    #繪圖
    x=np.linspace(min(Option_data.iloc[:,0])-30,max(Option_data.iloc[:,0])+20,10000)
    y=[]
    for S in x:
        SUM_RND=0
        for j in range(dis):
            SUM_RND=SUM_RND+res['x'][j]*(math.exp(-0.5*((S-Z[j])/h)**2)/math.sqrt(2*math.pi))/h
        y.append(SUM_RND)
    high=np.argmax(y)+1
    print(x[high])
    #plt.subplot(2, 3, i+1) 
    plt.figure(1)
    plt.plot(x,y)
    plt.title(Name1[5:]+" RND model")
    plt.xlabel("Stock price")
    plt.ylabel("Risk Neutral Distribution")
    plt.axvline(x=x[high],linewidth=2,linestyle="--",color="r")
    
    plt.figure(2)
    z=[]
    cdf = 0
    for S in x:
        SUM_RND=0
        for j in range(dis):
            SUM_RND=SUM_RND+res['x'][j]*(math.exp(-0.5*((S-Z[j])/h)**2)/math.sqrt(2*math.pi))/h
        cdf = cdf + SUM_RND/10000*(max(Option_data.iloc[:,0])-min(Option_data.iloc[:,0])+4)
        z.append(cdf)
        
    plt.plot(x,z)
    plt.title("PCA CDF model")
    plt.xlabel("Stock price")
    plt.ylabel("Cumulative Distribution Function")
    
plt.figure(3)
plt.plot(Datelist,Problist_delisted)
plt.xticks(rotation=45)
plt.title("Delisted company Bankruptcy prob")
plt.xlabel("Time")
plt.ylabel("Bankrupty probability")
print("平均破產機率為:",np.round(np.mean(Problist_delisted)*100,decimals=2),"%")
print("破產機率標準差為:",np.round(np.std(Problist_delisted),decimals=2))
print("平均適配MAPE為:",np.round(MSErecord_delisted/TIME,decimals=4)*100,"%")
print("平均每日選擇權資料量為",np.round(Data3.shape[0]/TIME,decimals=2))

print("平均破產機率為:", np.round(np.mean(Problist_delisted[:30]) * 100, decimals=2), "%")
print("破產機率標準差為:", np.round(np.std(Problist_delisted[:30]), decimals=2))
total_mape = sum(MAPErecord_delisted[:30])
print("平均適配MAPE為:", np.round(total_mape / 30, decimals=4) * 100, "%")
#-----------------------------------------------------------------------------
#listing company
#Company = pd.read_csv('~/Documents/Data/Option_listing_convert/6331_RE_option_new_t.csv')
Company = pd.read_csv('~/Documents/Data/listing_new_t/6211_GS_LEH_result.csv')
#Company = pd.read_csv('~/Documents/Data/listing_nomomax/3519_ENPH_result.csv')
Data1 = Company
#這裡選取倒數N天
Mark=Data1.iloc[-1,0]
list=[]
count=1
for i in range(Data1.shape[0]):
    if Mark!=Data1.iloc[-(i+1),0]:
        count=count+1
        Mark=Data1.iloc[-(i+1),0]
    if count==TIME+1:
        break
    list.append(-(i+1))
Data2 =Data1.loc[Data1.index[list],:]
Data2=Data2.iloc[::-1]
#-----------------------------------------------------------------------------
# 判斷 C 或 P 並且過濾價內資料
K = Data2.iloc[:, 2]
S = Data2.iloc[:, 4]
# 判斷 C 或 P 並且過濾價內資料
def remove_in_the_money_options(Data2):
    # 確保第2列和第4列的數據為數值類型，如果無法轉換則會變為 NaN
    Data2.iloc[:, 2] = pd.to_numeric(Data2.iloc[:, 2], errors='coerce')  # 行權價 K
    Data2.iloc[:, 4] = pd.to_numeric(Data2.iloc[:, 4], errors='coerce')  # 標的資產現價 S

    # 分別取出第2列的行權價 (K) 和第4列的標的資產現價 (S)
    K = Data2.iloc[:, 2]
    S = Data2.iloc[:, 4]
    
    # 取出第8列的權證類型 (C for call, P for put)
    option_type = Data2.iloc[:, 8]
    
    # 條件1: 買權（Call）且 S > K (價內)
    condition_call = (option_type == 'C') & (S > K)
    
    # 條件2: 賣權（Put）且 S < K (價內)
    condition_put = (option_type == 'P') & (S < K)
    
    # 將符合以上兩個條件的資料列刪除
    Data3 = Data2[~(condition_call | condition_put)]
    
    return Data3

# 執行函數
Data3 = remove_in_the_money_options(Data2)
#-----------------------------------------------------------------------------
for i in range(Data3.shape[0]):
    if Data3.iloc[i, 8] == 'C':  # 如果第8欄為C（買權）
        # 提取S、K、r、T值
        S = Data3.iloc[i, 4]  # 第4欄的S
        K = Data3.iloc[i, 2]  # 第2欄的K
        r = Data3.iloc[i, 5]  # 第5欄的r
        T = Data3.iloc[i, 3]  # 第3欄的T
        
        # 計算賣權價格（轉換）
        P_converted = K * np.exp(-r * T) - S
        
        # 更新該行的第9欄位為轉換後的賣權價格
        Data3.iloc[i, 9] = P_converted
#-----------------------------------------------------------------------------
T = Data2.iloc[:,3]
R = Data2.iloc[:,5]
F = Data2.iloc[:,6]
S = Data2.iloc[:,4]
date=Data1.iloc[0,0]
#Del=S[S["date"]<Time].index
#S = S.drop(index=Del)
#紀錄日期最後繪圖用
#Datelist = S.iloc[len(S)-TIME:len(S),1].tolist() 
#for i in range(len(Datelist)):
#    Datelist[i] = datetime.strptime(str(Datelist[i]), '%Y%m%d')

#S = Series(S["close"].tolist())
Variable = pd.concat([R,T,S,F], axis=1)
Variable.columns = ['Rate','Time','Stock Price','Future Price']
Variable=Variable.iloc[len(Variable)-TIME:len(Variable),:]
S1 = pd.read_csv('~/Documents/Data/Stock_listing/3519_ENPH_stock.csv')
#S1 = pd.read_csv('~/Documents/Data/Archive_de_stock/5122_NUS_stock.csv')
#S1 = pd.read_csv('~/Documents/Data/listing2020new/Stock_listing_new/1311_ROCC_stock.csv')
Del=S1[S1["date"]<Time].index
S1 = S1.drop(index=Del)
#紀錄日期最後繪圖用
Datelist = S1.iloc[len(S1)-TIME:len(S1),1].tolist() 
for i in range(len(Datelist)):
    Datelist[i] = datetime.strptime(str(Datelist[i]), '%Y%m%d')
S1 = Series(S1["close"].tolist())
#-----------------------------------------------------------------------------
T = Data2.iloc[:,3]
R = Data2.iloc[:,5]
F = Data2.iloc[:,6]
S = Data2.iloc[:,4]
date=Data1.iloc[0,0]

#Test version
Variable = pd.concat([R,T,S,F], axis=1)
Variable.columns = ['Rate','Time','Stock Price','Future Price']
Variable = Variable.drop_duplicates(subset=['Rate', 'Time', 'Stock Price', 'Future Price'])




Variable = pd.concat([R,T,S,F], axis=1)
Variable.columns = ['Rate','Time','Stock Price','Future Price']
Variable=Variable.iloc[len(Variable)-TIME:len(Variable),:]
#S1 = pd.read_csv('~/Documents/Data/Stock_listing/3825_ITRI_stock.csv')
S1 = pd.read_csv('~/Documents/Data/Archive_li_stock/6211_GS_LEH_stock.csv')
#S1 = pd.read_csv('~/Documents/Data/listing2020new/Stock_listing_new/1311_MTDR_stock.csv')

# 設定 Time 為 datetime 類型
Time = datetime(2001, 9, 3)
# 轉換 S1["date"] 為 datetime 類型
S1['date'] = pd.to_datetime(S1['date'], format='%Y/%m/%d', errors='coerce')
# 正確比較日期，篩掉太早的資料
S1 = S1[S1["date"] >= Time].reset_index(drop=True)
Datelist = S1["date"].iloc[-TIME:].tolist()
S1 = Series(S1["close"].tolist())
#-----------------------------------------------------------------------------
# 找最長的履約價
Num = []
date = Data3.iloc[0, 0]
A = 0
for i in range(Data3.shape[0]):
    if Data3.iloc[i, 0] == date:
        A = A + 1
    else:
        date = Data3.iloc[i, 0]
        Num.append(A)
        A = 1
Num.append(A)
Strike = max(Num)

# 確認變數 Strike 和 Variable.shape[0] 的值
print("Strike:", Strike)
print("Variable.shape[0]:", Variable.shape[0])

# 整理 K
K = pd.DataFrame(columns=range(Variable.shape[0]), index=range(Strike))  # 創建一個 DataFrame，行數是 Strike，列數是 Variable 的行數
date = Data3.iloc[0, 0]  # 初始化第一個交易日的日期
row = 0  # 用來標記當前的列索引（即哪一天）
Column = 0  # 用來標記當前的行索引（即當天的履約價數量）

for i in range(Data3.shape[0]):  # 遍歷 Data2 中的每一行
    if Data3.iloc[i, 0] == date:  # 如果當前行的日期和前一行相同
        if Column < Strike and row < Variable.shape[0]:  # 檢查當前的行和列索引是否超出範圍
            K.iloc[Column, row] = Data3.iloc[i, 2]  # 將 Data2 中的履約價填入 K
        Column = Column + 1  # 增加當前履約價的行索引
    else:  # 當遇到新的一天
        date = Data3.iloc[i, 0]  # 更新交易日期
        row = row + 1  # 切換到下一列（新的一天）
        Column = 0  # 重置行索引，因為新的一天從頭開始計算履約價
        if Column < Strike and row < Variable.shape[0]:  # 檢查範圍
            K.iloc[Column, row] = Data3.iloc[i, 2]  # 將履約價填入 K
        Column = Column + 1  # 增加行索引

# 整理 Price
P = pd.DataFrame(columns=range(Variable.shape[0]), index=range(Strike))
date = Data3.iloc[0, 0]
row = 0
Column = 0
for i in range(Data3.shape[0]):
    if Data3.iloc[i, 0] == date:
        if Column < Strike and row < Variable.shape[0]:
            P.iloc[Column, row] = Data3.iloc[i, 9]
        Column = Column + 1
    else:
        date = Data3.iloc[i, 0]
        row = row + 1
        Column = 0
        if Column < Strike and row < Variable.shape[0]:
            P.iloc[Column, row] = Data3.iloc[i, 9]
        Column = Column + 1

Problist_listing = []
MSErecord_listing=0
MAPErecord_listing = []
for i in range(len(Variable)):
    #將選擇權資料重新排列
    Option_data = pd.DataFrame(zip(K.iloc[:,i],P.iloc[:,i]), columns = ['Strike price','Price']).dropna(axis=0)
    Option_data = Option_data.sort_values(by=['Strike price'], ascending=True)
    Opt_len = Option_data.shape[0]
    dz=0.5
    h=2*dz
    Z=numpy.arange(Option_data.iloc[0,0],Option_data.iloc[Opt_len-1,0]+dz,dz).tolist()
    Z.insert(0,0)
    dis=length_hint(Z) 
    PCA_1 = pd.DataFrame(columns=Option_data.iloc[:,0],index=Z)
    for k in range(Opt_len):
        for j in range(dis):
            PCA_1.iloc[j,k]=(Option_data.iloc[k,0]-Z[j])/h
    
    #做PCA
    PCA_2= pd.DataFrame(columns=Option_data.iloc[:,0],index=Z)
    for k in range(Opt_len):
        for j in range(dis):
            PCA_2.iloc[j,k]=(math.exp(-0.5*(PCA_1.iloc[j,k])**2)/math.sqrt(2*math.pi)+PCA_1.iloc[j,k]*norm.cdf(PCA_1.iloc[j,k]))/h
  
    #做最佳化
    def PCA_fnc(a):
        PCA=0
        for k in range(Opt_len):
            Sum=0
            for j in range(dis):
                Sum=Sum+a[j]*PCA_2.iloc[j,k]
            PCA=PCA+abs((Option_data.iloc[k,1]-Sum)/Option_data.iloc[k,1])
        return PCA

    def con(a):
        A=np.sum(a)
        return A-1
    def con_F(a):
        B=0
        for j in range(dis):
            B=B+a[j]*Z[j]
        return B-F.iloc[i]
    cons = [{'type':'eq', 'fun': con},
            {'type':'eq', 'fun': con_F}]
    a0=[1/dis]*dis
    PCA_fnc(a=a0)
    bounds = [(0,1)]*dis
    res = opt.minimize(PCA_fnc,a0,bounds=bounds,constraints=cons)

    #印出預測誤差及分配
    print("破產前", len(Variable)-i ,"天破產機率預測")
    print("適配MAPE為",np.round(res['fun']/Opt_len,decimals=4))
    MSErecord_listing = MSErecord_listing+np.round(res['fun']/Opt_len,decimals=4)
    MAPErecord_listing.append(np.round(res['fun'] / Opt_len, decimals=4))
    def PCA(x):
        SUM_RND=0
        for j in range(dis):
            SUM_RND=SUM_RND+res['x'][j]*(sympy.exp(-0.5*((x-Z[j])/h)**2)/(2*sympy.pi)**0.5)/h
        return(SUM_RND)  
    x = symbols('x')
    Prob = integrate(PCA(x), (x,-float("inf"),0)).simplify()
    Problist_listing.append(np.round(float(Prob),decimals=4))
    Prob = np.round(float(Prob)*100,decimals=4)
    print("破產機率為: ", Prob,"%")
    print("係數為 : ")
    print(np.round(res['x'],decimals=4))
    print("--------------------------------------------------------------------")
    #畫出破產機率時間序列圖
    
    
    #繪圖
    x=np.linspace(min(Option_data.iloc[:,0])-10,max(Option_data.iloc[:,0])+5,10000)
    y=[]
    for S in x:
        SUM_RND=0
        for j in range(dis):
            SUM_RND=SUM_RND+res['x'][j]*(math.exp(-0.5*((S-Z[j])/h)**2)/math.sqrt(2*math.pi))/h
        y.append(SUM_RND)
    high=np.argmax(y)+1
    print(x[high])
    #plt.subplot(2, 3, i+1) 
    plt.figure(1)
    plt.plot(x,y)
    plt.title(Name2[5:]+" RND model")
    plt.xlabel("Stock price")
    plt.ylabel("Risk Neutral Distribution")
    plt.axvline(x=x[high],linewidth=2,linestyle="--",color="r")
    
    plt.figure(2)
    z=[]
    cdf = 0
    for S in x:
        SUM_RND=0
        for j in range(dis):
            SUM_RND=SUM_RND+res['x'][j]*(math.exp(-0.5*((S-Z[j])/h)**2)/math.sqrt(2*math.pi))/h
        cdf = cdf + SUM_RND/10000*(max(Option_data.iloc[:,0])-min(Option_data.iloc[:,0])+4)
        z.append(cdf)
        
    plt.plot(x,z)
    plt.title("PCA CDF model")
    plt.xlabel("Stock price")
    plt.ylabel("Cumulative Distribution Function")
    
plt.figure(3)
plt.plot(Datelist,Problist_listing)
plt.xticks(rotation=45)
plt.title("Listing company bankruptcy prob")
plt.xlabel("Time")
plt.ylabel("Bankrupty probability")
#MDTR
print("平均破產機率為:", np.round(np.mean(Problist_listing[:30]) * 100, decimals=2), "%")
print("破產機率標準差為:", np.round(np.std(Problist_listing[:30]), decimals=2))
total_mape = sum(MAPErecord_listing[:30])
print("平均適配MAPE為:", np.round(total_mape / 30, decimals=4) * 100, "%")

print("平均破產機率為:",np.round(np.mean(Problist_listing)*100,decimals=2),"%")
print("破產機率標準差為:",np.round(np.std(Problist_listing),decimals=2))
print("平均適配MAPE為:",np.round(MSErecord_listing/TIME,decimals=4)*100,"%")
print("平均每日選擇權資料量為",np.round(Data3.shape[0]/TIME,decimals=2))


plt.figure(5)
plt.plot(Datelist,Problist_delisted, 'tomato', label=Name1)
plt.plot(Datelist,Problist_listing, 'royalblue',linestyle="--", label=Name2)
plt.title("Bankruptcy probability comparison chart",fontsize=14,y = 1.01)
plt.xticks(rotation=45)
plt.xlabel("Time",fontsize=12)
plt.ylabel("Bankrupty probability",fontsize=12)
plt.legend(loc="best")
plt.show()
def get_p_value(arrA, arrB):
  a = np.array(arrA)
  b = np.array(arrB)
  t, p = stats.ttest_ind(a,b,alternative='greater')
  return p
p_value=get_p_value(Problist_delisted, Problist_listing)
print("兩組數據做T-test後的p-value為",p_value)
if p_value<0.05:
    print("破產公司破產預測機率顯著大於對照公司")
else:
    print("破產公司破產預測機率並無顯著大於對照公司")
    
std_price = Option_data.iloc[:, 1].std()
std_price
#findh
x = np.linspace(min(Option_data['Strike price']) - 10, max(Option_data['Strike price']) + 5, 10000)
y = [np.sum([res['x'][j] * (math.exp(-0.5 * ((S - Z[j]) / h) ** 2) / math.sqrt(2 * math.pi)) / h for j in range(dis)]) for S in x]
# Find the Mode of RND
mode = x[np.argmax(y)]
print("Mode of RND:", mode)
xm=mode
m=PCA(xm)
#calculate m1 for w1, m2 for w2
m1=0.75*PCA(xm)
m2=0.5*PCA(xm)
# Define the objective function to minimize
def objective(vars):
    x1, x2 = vars
    return x2 - x1  # Objective function to minimize

# Define the constraints
def constraint1(vars):
    x1, x2 = vars
    return PCA(x1) - m1  # Constraint 1: PCA(x1) = m1

def constraint2(vars):
    x1, x2 = vars
    return PCA(x2) - m1  # Constraint 2: PCA(x2) = m1

def constraint3(vars):
    x1, x2 = vars
    return x1 - xm  # Constraint 3: x1 < xm

def constraint4(vars):
    x1, x2 = vars
    return x2 - xm  # Constraint 4: x2 > xm

# Initial guess
initial_guess = [22, 23]

# Define the constraints as a list of dictionaries
constraints = ({'type': 'eq', 'fun': constraint1},
               {'type': 'eq', 'fun': constraint2},
               {'type': 'ineq', 'fun': constraint3},
               {'type': 'ineq', 'fun': constraint4})

# Perform the optimization
result = minimize(objective, initial_guess, constraints=constraints, method='SLSQP')
# Print the result
print(result.x)
#w1=x1-x2
x1=20.27559836
x2=24.9724014
w1=x1-x2
w1
#Define the objective function to minimize
def objective(vars):
    x3, x4 = vars
    return x4 - x3  # Objective function to minimize

# Define the constraints
def constraint1(vars):
    x3, x4 = vars
    return PCA(x3) - m2  # Constraint 1: PCA(x3) = m2

def constraint2(vars):
    x3, x4 = vars
    return PCA(x4) - m2  # Constraint 2: PCA(x4) = m2

def constraint3(vars):
    x3, x4 = vars
    return x3 - xm  # Constraint 3: x3 < xm

def constraint4(vars):
    x3, x4 = vars
    return x4 - xm  # Constraint 4: x4 > xm

# Initial guess
initial_guess = [22, 23]

# Define the constraints as a list of dictionaries
constraints = ({'type': 'eq', 'fun': constraint1},
               {'type': 'eq', 'fun': constraint2},
               {'type': 'ineq', 'fun': constraint3},
               {'type': 'ineq', 'fun': constraint4})

# Perform the optimization
result = minimize(objective, initial_guess, constraints=constraints, method='SLSQP')

# Print the result
print(result.x)
#w2=x3-x4
x3=18.97873841
x4=26.26926134
w2=x3-x4
w2
#Find h0
h0 = min(abs(w1 / 0.7585), abs(w2 / 1.1774))
h0
h1=0.95*h0
h1
dz=0.5*h1
dz
#-----------------------------------------------------------------------------
#CAP&ROC曲線
#ROC 2m
y_true = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])  # 1 表示破產，0 表示非破產
y_scores = np.array([0.006, 0.0148, 0.0073, 0.00165, 0.00186, 0.0058, 0.0094, 0.0009, 0.0006, 0.0006, 0.0012, 0.015, 0.0801, 0.0045, 0.0103, 0.1361, 0.002, 0.0055, 0.2089, 0.0026, 0.0046, 0.0121, 0.0563, 0.2525, 0.2648, 0.0294, 0.0024, 0.0075, 0.0291, 0.0146, 0.0024, 0.0034, 0.0024, 0.0082,
                     0.011, 0.0092, 0.0065, 0.0057, 0.4505, 0.0049, 0.012, 0.0164, 0.121, 0.2104, 0.4828, 0.42, 0.0006, 0.4222, 0.0032, 0.1376, 0.30,0.0227, 0.1941, 0.4666, 0.1392, 0.385,
                     0.4552, 0.47, 0.2845, 0.3888, 0.3754, 0.1366, 0.444, 0.0261, 0.2546, 0.463, 0.4198, 0.2845])  # 破產機率
# 計算 ROC 曲線
fpr, tpr, thresholds = roc_curve(y_true, y_scores)

# 計算 AUC
roc_auc = auc(fpr, tpr)

# 繪製 ROC 曲線
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')

# 添加隨機分類基準線（灰色虛線）
plt.plot([0, 1], [0, 1], color='gray', linestyle='--', lw=2, label='Random guess')

# 設定圖表細節
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.grid()

# 顯示圖表
plt.show()

#ROC 1m
y_true = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])  # 1 表示破產，0 表示非破產
y_scores = np.array([0.0076, 0.0863, 0.01, 0.0146, 0.0162, 0.0069, 0.008, 0.001, 0.0007, 0.0008, 0.0011, 0.0088, 0.0871, 0.0036, 0.0075, 0.0018, 0.003, 0.0053, 0.1609, 0.0027, 0.0016, 0.0042, 0.0148, 0.055, 0.2071, 0.1129, 0.0067, 0.0017, 0.0071, 0.0134, 0.0104, 0.0022, 0.0033, 0.0042, 0.0082, 0.0122, 0.0096, 0.0073, 0.0049,
                     0.1426, 0.3439, 0.024, 0.1213, 0.475, 0.2417, 0.4702, 0.3924, 0.0006, 0.4492, 0.0053, 0.1445, 0.3679, 0.1054, 0.4236, 0.465, 0.1207, 0.3315, 0.4777, 0.0446, 0.3693, 0.3208, 0.4266, 0.4046, 0.1177, 0.4746, 0.0146, 0.2602, 0.4778, 0.4309, 0.3208])  # 破產機率
#-----------------------------------------------------------------------------
#CAP 2m
y_scores = np.array([0.006, 0.0148, 0.0073, 0.00165, 0.00186, 0.0058, 0.0094, 0.0009, 0.0006, 0.0006, 0.0012, 0.015, 0.0801, 0.0045, 0.0103, 0.1361, 0.002, 0.0055, 0.2089, 0.0026, 0.0046, 0.0121, 0.0563, 0.2525, 0.2648, 0.0294, 0.0024, 0.0075, 0.0291, 0.0146, 0.0024, 0.0034, 0.0024, 0.0082,
                     0.011, 0.0092, 0.0065, 0.0057, 0.4505, 0.0049, 0.012, 0.0164, 0.121, 0.2104, 0.4828, 0.42, 0.0006, 0.4222, 0.0032, 0.1376, 0.30,0.0227, 0.1941, 0.4666, 0.1392, 0.385,
                     0.4552, 0.47, 0.2845, 0.3888, 0.3754, 0.1366, 0.444, 0.0261, 0.2546, 0.463, 0.4198, 0.2845])  # 破產機率
y_true = np.array([0]*38 + [1]*30)
# 按預測機率從高到低排序
sorted_indices = np.argsort(y_scores)[::-1]
y_true_sorted = y_true[sorted_indices]

# 計算累積命中率
cum_good = np.cumsum(y_true_sorted) / sum(y_true)  # 真正類別為 1 的累積比例
cum_total = np.arange(1, len(y_true) + 1) / len(y_true)  # 全體累積比例

# 隨機分類基準線
random_line = cum_total  # 45 度對角線（隨機分類）

# 完美分類基準線
perfect_model = np.concatenate([[0], np.ones(sum(y_true)) / sum(y_true), np.ones(len(y_true) - sum(y_true))])
perfect_model = np.cumsum(perfect_model)

# 畫 CAP 曲線
plt.figure()
plt.plot(cum_total, cum_good, label="Model CAP", color="blue", lw=2)
plt.plot(cum_total, random_line, label="Random Model", color="gray", linestyle="--")
plt.plot(np.linspace(0, 1, len(perfect_model)), perfect_model, label="Perfect Model", color="green", linestyle="dotted")

plt.xlabel("Sample Percentage")
plt.ylabel("Cumulative Positive Rate")
plt.title("Cumulative Accuracy Profile (CAP)")
plt.legend(loc="lower right")
plt.show()

sorted_indices = np.argsort(y_scores)[::-1]  # 破產機率由高到低排序
y_true_sorted = y_true[sorted_indices]
y_scores_sorted = y_scores[sorted_indices]
print(y_true_sorted[:10])

# 計算累積命中率
cum_good = np.cumsum(y_true_sorted) / sum(y_true)  # 累積真正的破產數
sample_percentage = np.arange(1, len(y_true) + 1) / len(y_true)  # 樣本比例

# 計算隨機模型 (Random Model) 
random_model = sample_percentage

# 計算完美模型 (Perfect Model)
perfect_model = np.concatenate([
    np.linspace(0, 1, sum(y_true)),  # 前 30% 內累積所有 1
    np.ones(len(y_true) - sum(y_true))  # 之後保持 100%
])

plt.figure(figsize=(6, 4))
plt.plot(sample_percentage, cum_good, label="Model CAP", color="blue")
plt.plot(sample_percentage, random_model, label="Random Model", linestyle="--", color="gray")
plt.plot(sample_percentage, perfect_model, label="Perfect Model", linestyle="dotted", color="green")

plt.xlabel("Sample Percentage")
plt.ylabel("Cumulative Positive Rate")
plt.title("Cumulative Accuracy Profile (CAP)")
plt.legend()
plt.show()

#CAP 1m
y_true = np.array([0]*39 + [1]*31)
y_scores = np.array([0.0076, 0.0863, 0.01, 0.0146, 0.0162, 0.0069, 0.008, 0.001, 0.0007, 0.0008, 0.0011, 0.0088, 0.0871, 0.0036, 0.0075, 0.0018, 0.003, 0.0053, 0.1609, 0.0027, 0.0016, 0.0042, 0.0148, 0.055, 0.2071, 0.1129, 0.0067, 0.0017, 0.0071, 0.0134, 0.0104, 0.0022, 0.0033, 0.0042, 0.0082, 0.0122, 0.0096, 0.0073, 0.0049,
                     0.1426, 0.3439, 0.024, 0.1213, 0.475, 0.2417, 0.4702, 0.3924, 0.0006, 0.4492, 0.0053, 0.1445, 0.3679, 0.1054, 0.4236, 0.465, 0.1207, 0.3315, 0.4777, 0.0446, 0.3693, 0.3208, 0.4266, 0.4046, 0.1177, 0.4746, 0.0146, 0.2602, 0.4778, 0.4309, 0.3208])  # 破產機率
