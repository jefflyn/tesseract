from sklearn import svm

import zillion.stock.data.lab.predict.data_process as DP

if __name__ == '__main__':
    # ['600069.SH', '002895.SZ', '002923.SZ', '000820.SZ', '002555.SZ'
    stock = '000820.SZ'
    dc = DP.DataCollect(stock, '2010-01-01', '2019-12-06')
    train = dc.data_train
    target = dc.data_target
    test_case = [dc.test_case]
    model = svm.SVC()  # 建模
    model.fit(train, target)  # 训练
    ans2 = model.predict(test_case)  # 预测
    # 输出对第二天的涨跌预测，1表示涨，0表示不涨。
    print(ans2[0])
