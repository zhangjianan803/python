#!/usr/bin/env python
# coding: utf-8

# In[ ]:


{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib as mpl\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\n",
    "from sklearn.decomposition import TruncatedSVD\n",
    "from sklearn.naive_bayes import BernoulliNB\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.metrics import f1_score,precision_score, recall_score"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "## 设置字符集，防止中文乱码\n",
    "mpl.rcParams['font.sans-serif']=[u'simHei']\n",
    "mpl.rcParams['axes.unicode_minus']=False"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "# jupyter展示图片，非内嵌显示\n",
    "# tk: 显示出来，inline：内嵌显示，默认为inline\n",
    "%matplotlib tk"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>label</th>\n",
       "      <th>has_date</th>\n",
       "      <th>jieba_cut_content</th>\n",
       "      <th>content_sema</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1.0</td>\n",
       "      <td>1</td>\n",
       "      <td>非  财务  纠淼  牟  莆  窆  芾  -  （  沙盘  模拟  ）  -  -  ...</td>\n",
       "      <td>8.456151</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>0.0</td>\n",
       "      <td>1</td>\n",
       "      <td>讲  的  是  孔子  后人  的  故事  。  一个  老  领导  回到  家乡  ...</td>\n",
       "      <td>7.486084</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>1.0</td>\n",
       "      <td>1</td>\n",
       "      <td>尊敬  的  贵  公司  (  财务  /  经理  )  负责人  您好  ！  我  ...</td>\n",
       "      <td>7.175171</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>1.0</td>\n",
       "      <td>1</td>\n",
       "      <td>贵  公司  负责人  (  经理  /  财务  ）  您好  ：  深圳市  华龙  公...</td>\n",
       "      <td>7.565682</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>1.0</td>\n",
       "      <td>1</td>\n",
       "      <td>这是  一封  HTML  格式  信件  ！  -  -  -  -  -  -  -  ...</td>\n",
       "      <td>2.063409</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>1.0</td>\n",
       "      <td>1</td>\n",
       "      <td>TO  ：  贵  公司  经理  、  财务  您好  ！  深圳市  春洋  贸易  有...</td>\n",
       "      <td>7.143747</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6</th>\n",
       "      <td>0.0</td>\n",
       "      <td>1</td>\n",
       "      <td>那  他  为什么  不  愿意  起诉  ，  既然  这样  了  ！  起诉  后  ...</td>\n",
       "      <td>4.807568</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7</th>\n",
       "      <td>1.0</td>\n",
       "      <td>1</td>\n",
       "      <td>尊敬  的  负责人  （  经理  ／  财务  ）  ：  您好  ！  我  是  深...</td>\n",
       "      <td>6.593684</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>8</th>\n",
       "      <td>1.0</td>\n",
       "      <td>1</td>\n",
       "      <td>您好     以下  是  特别  为  阁下  发  的  香港  信息  (  图片  ...</td>\n",
       "      <td>7.611074</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>9</th>\n",
       "      <td>0.0</td>\n",
       "      <td>1</td>\n",
       "      <td>我  觉得  ，  负债  不要紧  ，  最  重要  的  是  能  负得起  这个 ...</td>\n",
       "      <td>7.041340</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   label  has_date                                  jieba_cut_content  \\\n",
       "0    1.0         1  非  财务  纠淼  牟  莆  窆  芾  -  （  沙盘  模拟  ）  -  -  ...   \n",
       "1    0.0         1  讲  的  是  孔子  后人  的  故事  。  一个  老  领导  回到  家乡  ...   \n",
       "2    1.0         1  尊敬  的  贵  公司  (  财务  /  经理  )  负责人  您好  ！  我  ...   \n",
       "3    1.0         1  贵  公司  负责人  (  经理  /  财务  ）  您好  ：  深圳市  华龙  公...   \n",
       "4    1.0         1  这是  一封  HTML  格式  信件  ！  -  -  -  -  -  -  -  ...   \n",
       "5    1.0         1  TO  ：  贵  公司  经理  、  财务  您好  ！  深圳市  春洋  贸易  有...   \n",
       "6    0.0         1  那  他  为什么  不  愿意  起诉  ，  既然  这样  了  ！  起诉  后  ...   \n",
       "7    1.0         1  尊敬  的  负责人  （  经理  ／  财务  ）  ：  您好  ！  我  是  深...   \n",
       "8    1.0         1  您好     以下  是  特别  为  阁下  发  的  香港  信息  (  图片  ...   \n",
       "9    0.0         1  我  觉得  ，  负债  不要紧  ，  最  重要  的  是  能  负得起  这个 ...   \n",
       "\n",
       "   content_sema  \n",
       "0      8.456151  \n",
       "1      7.486084  \n",
       "2      7.175171  \n",
       "3      7.565682  \n",
       "4      2.063409  \n",
       "5      7.143747  \n",
       "6      4.807568  \n",
       "7      6.593684  \n",
       "8      7.611074  \n",
       "9      7.041340  "
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# 1. 文件数据读取\n",
    "df = pd.read_csv('../data/result_process02', sep=',')\n",
    "# 如果有某值为nan，进行删除操作\n",
    "df.dropna(axis=0, how='any', inplace=True)\n",
    "df.head(10)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "Int64Index: 64284 entries, 0 to 64619\n",
      "Data columns (total 4 columns):\n",
      "label                64284 non-null float64\n",
      "has_date             64284 non-null int64\n",
      "jieba_cut_content    64284 non-null object\n",
      "content_sema         64284 non-null float64\n",
      "dtypes: float64(2), int64(1), object(1)\n",
      "memory usage: 2.5+ MB\n"
     ]
    }
   ],
   "source": [
    "df.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "训练数据集大小:51427\n",
      "测试数据集大小:12857\n"
     ]
    }
   ],
   "source": [
    "# 2. 数据分割\n",
    "x_train, x_test, y_train, y_test = train_test_split(df[['has_date','jieba_cut_content','content_sema']], df['label'], test_size=0.2, random_state=0)\n",
    "print(\"训练数据集大小:%d\" % x_train.shape[0])\n",
    "print(\"测试数据集大小:%d\" % x_test.shape[0])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>has_date</th>\n",
       "      <th>jieba_cut_content</th>\n",
       "      <th>content_sema</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>18810</th>\n",
       "      <td>1</td>\n",
       "      <td>尊敬  的  公司  （  工厂  ）  经理  负责人  你好  ：  我  公司  是 ...</td>\n",
       "      <td>6.849239</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>61632</th>\n",
       "      <td>1</td>\n",
       "      <td>声音  变换器  ：  适用  于  不同  型号  的  手机  ，  电话  ，  网络...</td>\n",
       "      <td>7.242064</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5822</th>\n",
       "      <td>1</td>\n",
       "      <td>http  :  /  /  tengyingge  .  blogchina  .  co...</td>\n",
       "      <td>8.289843</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5881</th>\n",
       "      <td>1</td>\n",
       "      <td>刚  开始  ，  是  会  有点  不  习惯  的  。  慢慢来  。  ps  ：...</td>\n",
       "      <td>7.063309</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>26338</th>\n",
       "      <td>1</td>\n",
       "      <td>尊敬  的  公司  （  工厂  ）  经理  负责人  你好  ：  我  公司  是 ...</td>\n",
       "      <td>6.700159</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "       has_date                                  jieba_cut_content  \\\n",
       "18810         1  尊敬  的  公司  （  工厂  ）  经理  负责人  你好  ：  我  公司  是 ...   \n",
       "61632         1  声音  变换器  ：  适用  于  不同  型号  的  手机  ，  电话  ，  网络...   \n",
       "5822          1  http  :  /  /  tengyingge  .  blogchina  .  co...   \n",
       "5881          1  刚  开始  ，  是  会  有点  不  习惯  的  。  慢慢来  。  ps  ：...   \n",
       "26338         1  尊敬  的  公司  （  工厂  ）  经理  负责人  你好  ：  我  公司  是 ...   \n",
       "\n",
       "       content_sema  \n",
       "18810      6.849239  \n",
       "61632      7.242064  \n",
       "5822       8.289843  \n",
       "5881       7.063309  \n",
       "26338      6.700159  "
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "x_train.head(5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {
    "collapsed": false,
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "         0         1         2         3         4         5         6   \\\n",
      "0  0.340289  0.220012 -0.237481 -0.039929 -0.070163  0.002505 -0.160855   \n",
      "1  0.014968  0.064739  0.027002 -0.004669  0.008162  0.007429  0.016378   \n",
      "2  0.011862  0.072032  0.047006  0.001432 -0.002097  0.035910  0.009125   \n",
      "3  0.019714  0.117439  0.132445  0.060406 -0.103514 -0.074868 -0.012198   \n",
      "4  0.346257  0.215336 -0.234033 -0.043106 -0.071078 -0.000055 -0.162685   \n",
      "\n",
      "         7         8         9         10        11        12        13  \\\n",
      "0 -0.009606  0.201680 -0.010785 -0.199526  0.039608 -0.065746  0.430054   \n",
      "1  0.045969  0.029438  0.000047  0.007738  0.023426  0.041738 -0.011230   \n",
      "2 -0.012129 -0.016859  0.000085  0.001073 -0.003870 -0.002272 -0.003785   \n",
      "3 -0.005375 -0.027441  0.000119 -0.016805 -0.013143 -0.003589  0.016023   \n",
      "4 -0.008875  0.198958 -0.010605 -0.195275  0.037906 -0.062235  0.417887   \n",
      "\n",
      "         14        15        16        17        18        19  \n",
      "0 -0.475845  0.202106  0.095477 -0.253731 -0.173659  0.113119  \n",
      "1  0.013240  0.000197 -0.003748 -0.019631 -0.010597  0.011071  \n",
      "2 -0.003157 -0.003701  0.001942  0.002019  0.025398  0.005097  \n",
      "3  0.002182  0.007932 -0.027776 -0.007399  0.013613 -0.003093  \n",
      "4 -0.466218  0.195439  0.104274 -0.252845 -0.170476  0.112635  \n",
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 51427 entries, 0 to 51426\n",
      "Data columns (total 20 columns):\n",
      "0     51427 non-null float64\n",
      "1     51427 non-null float64\n",
      "2     51427 non-null float64\n",
      "3     51427 non-null float64\n",
      "4     51427 non-null float64\n",
      "5     51427 non-null float64\n",
      "6     51427 non-null float64\n",
      "7     51427 non-null float64\n",
      "8     51427 non-null float64\n",
      "9     51427 non-null float64\n",
      "10    51427 non-null float64\n",
      "11    51427 non-null float64\n",
      "12    51427 non-null float64\n",
      "13    51427 non-null float64\n",
      "14    51427 non-null float64\n",
      "15    51427 non-null float64\n",
      "16    51427 non-null float64\n",
      "17    51427 non-null float64\n",
      "18    51427 non-null float64\n",
      "19    51427 non-null float64\n",
      "dtypes: float64(20)\n",
      "memory usage: 7.8 MB\n",
      "None\n"
     ]
    }
   ],
   "source": [
    "# 3. 开始模型训练\n",
    "# 3.1 特征工程，将文本数据转换为数值型数据\n",
    "transfromer = TfidfVectorizer(norm='l2', use_idf=True)\n",
    "svd = TruncatedSVD(n_components=20)\n",
    "jieba_cut_content = list(x_train['jieba_cut_content'].astype('str'))\n",
    "transfromer_model = transfromer.fit(jieba_cut_content)\n",
    "df1 = transfromer_model.transform(jieba_cut_content)\n",
    "svd_model = svd.fit(df1)\n",
    "df2 = svd_model.transform(df1)\n",
    "\n",
    "data = pd.DataFrame(df2)\n",
    "print(data.head(5))\n",
    "print(data.info())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {
    "collapsed": false,
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "          0         1         2         3         4         5         6  \\\n",
      "0  0.340289  0.220012 -0.237481 -0.039929 -0.070163  0.002505 -0.160855   \n",
      "1  0.014968  0.064739  0.027002 -0.004669  0.008162  0.007429  0.016378   \n",
      "2  0.011862  0.072032  0.047006  0.001432 -0.002097  0.035910  0.009125   \n",
      "3  0.019714  0.117439  0.132445  0.060406 -0.103514 -0.074868 -0.012198   \n",
      "4  0.346257  0.215336 -0.234033 -0.043106 -0.071078 -0.000055 -0.162685   \n",
      "\n",
      "          7         8         9      ...             12        13        14  \\\n",
      "0 -0.009606  0.201680 -0.010785      ...      -0.065746  0.430054 -0.475845   \n",
      "1  0.045969  0.029438  0.000047      ...       0.041738 -0.011230  0.013240   \n",
      "2 -0.012129 -0.016859  0.000085      ...      -0.002272 -0.003785 -0.003157   \n",
      "3 -0.005375 -0.027441  0.000119      ...      -0.003589  0.016023  0.002182   \n",
      "4 -0.008875  0.198958 -0.010605      ...      -0.062235  0.417887 -0.466218   \n",
      "\n",
      "         15        16        17        18        19  has_date  content_sema  \n",
      "0  0.202106  0.095477 -0.253731 -0.173659  0.113119         1      6.849239  \n",
      "1  0.000197 -0.003748 -0.019631 -0.010597  0.011071         1      7.242064  \n",
      "2 -0.003701  0.001942  0.002019  0.025398  0.005097         1      8.289843  \n",
      "3  0.007932 -0.027776 -0.007399  0.013613 -0.003093         1      7.063309  \n",
      "4  0.195439  0.104274 -0.252845 -0.170476  0.112635         1      6.700159  \n",
      "\n",
      "[5 rows x 22 columns]\n",
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 51427 entries, 0 to 51426\n",
      "Data columns (total 22 columns):\n",
      "0               51427 non-null float64\n",
      "1               51427 non-null float64\n",
      "2               51427 non-null float64\n",
      "3               51427 non-null float64\n",
      "4               51427 non-null float64\n",
      "5               51427 non-null float64\n",
      "6               51427 non-null float64\n",
      "7               51427 non-null float64\n",
      "8               51427 non-null float64\n",
      "9               51427 non-null float64\n",
      "10              51427 non-null float64\n",
      "11              51427 non-null float64\n",
      "12              51427 non-null float64\n",
      "13              51427 non-null float64\n",
      "14              51427 non-null float64\n",
      "15              51427 non-null float64\n",
      "16              51427 non-null float64\n",
      "17              51427 non-null float64\n",
      "18              51427 non-null float64\n",
      "19              51427 non-null float64\n",
      "has_date        51427 non-null int64\n",
      "content_sema    51427 non-null float64\n",
      "dtypes: float64(21), int64(1)\n",
      "memory usage: 8.6 MB\n",
      "None\n"
     ]
    }
   ],
   "source": [
    "# 3.2 数据合并\n",
    "data['has_date'] = list(x_train['has_date'])\n",
    "data['content_sema'] = list(x_train['content_sema'])\n",
    "print(data.head(5))\n",
    "print(data.info())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Wall time: 58.2 ms\n"
     ]
    }
   ],
   "source": [
    "%%time\n",
    "nb = BernoulliNB(alpha=1.0,binarize=0.0005)\n",
    "model = nb.fit(data, y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "collapsed": false,
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "          0         1         2         3         4         5         6  \\\n",
      "0  0.537283  0.009048 -0.087600  0.028966  0.000837 -0.032717 -0.157714   \n",
      "1  0.210902  0.131676 -0.090071 -0.086932 -0.033320  0.039651  0.006967   \n",
      "2  0.045151  0.277282  0.233901  0.051111 -0.073998 -0.016321  0.010456   \n",
      "3  0.032907  0.163066  0.113489  0.002482  0.053748  0.008246  0.004315   \n",
      "4  0.035278  0.065204  0.026075 -0.023748  0.072922 -0.005953 -0.003272   \n",
      "\n",
      "          7         8         9      ...             12        13        14  \\\n",
      "0  0.009387 -0.134471  0.009602      ...       0.079591  0.000773 -0.017332   \n",
      "1 -0.008212  0.011706  0.000151      ...      -0.025829  0.082517 -0.056400   \n",
      "2 -0.014928  0.100495 -0.002823      ...      -0.066454 -0.036709 -0.030789   \n",
      "3 -0.020574  0.118087 -0.002192      ...      -0.061132 -0.056873 -0.012746   \n",
      "4 -0.007937  0.007662  0.000563      ...      -0.002760 -0.007197 -0.004672   \n",
      "\n",
      "         15        16        17        18        19  has_date  content_sema  \n",
      "0 -0.116241  0.078559 -0.089024  0.071154 -0.072376         1      6.773350  \n",
      "1  0.023345 -0.053967  0.013307 -0.004725 -0.011376         1      6.747166  \n",
      "2  0.013226  0.176416  0.091783  0.030968 -0.059508         1      8.568723  \n",
      "3 -0.019935  0.062044  0.021720 -0.027836 -0.027865         1      7.120973  \n",
      "4 -0.008747 -0.002713  0.018357  0.101063  0.351306         1      5.434929  \n",
      "\n",
      "[5 rows x 22 columns]\n",
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 12857 entries, 0 to 12856\n",
      "Data columns (total 22 columns):\n",
      "0               12857 non-null float64\n",
      "1               12857 non-null float64\n",
      "2               12857 non-null float64\n",
      "3               12857 non-null float64\n",
      "4               12857 non-null float64\n",
      "5               12857 non-null float64\n",
      "6               12857 non-null float64\n",
      "7               12857 non-null float64\n",
      "8               12857 non-null float64\n",
      "9               12857 non-null float64\n",
      "10              12857 non-null float64\n",
      "11              12857 non-null float64\n",
      "12              12857 non-null float64\n",
      "13              12857 non-null float64\n",
      "14              12857 non-null float64\n",
      "15              12857 non-null float64\n",
      "16              12857 non-null float64\n",
      "17              12857 non-null float64\n",
      "18              12857 non-null float64\n",
      "19              12857 non-null float64\n",
      "has_date        12857 non-null int64\n",
      "content_sema    12857 non-null float64\n",
      "dtypes: float64(21), int64(1)\n",
      "memory usage: 2.2 MB\n",
      "None\n"
     ]
    }
   ],
   "source": [
    "# 4.1 对测试数据进行特征转换\n",
    "jieba_cut_content_test = list(x_test['jieba_cut_content'].astype('str'))\n",
    "data_test = pd.DataFrame(svd_model.transform(transfromer_model.transform(jieba_cut_content_test)))\n",
    "data_test['has_date'] = list(x_test['has_date'])\n",
    "data_test['content_sema'] = list(x_test['content_sema'])\n",
    "print(data_test.head(5))\n",
    "print(data_test.info())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "# 4.2 对测试数据进行预测\n",
    "y_predict = model.predict(data_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "准确率为:0.94667\n",
      "召回率为:0.98937\n",
      "F1值为:0.96755\n"
     ]
    }
   ],
   "source": [
    "# 5. 效果评估\n",
    "print(\"准确率为:%.5f\" % precision_score(y_test, y_predict))\n",
    "print(\"召回率为:%.5f\" % recall_score(y_test, y_predict))\n",
    "print(\"F1值为:%.5f\" % f1_score(y_test, y_predict))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

