FROM ubuntu:latest

MAINTAINER jlsche <jlsche@lingtelli.com.com>

RUN apt-get update -y
RUN apt-get install -y locales locales-all
RUN apt-get install python3 -y 
RUN apt-get install python3-pip -y
RUN pip3 install --upgrade pip


ENV LC_ALL zh_TW.UTF-8
ENV LANGUAGE zh_TW.UTF-8
ENV LANG zh_TW.UTF-8

#RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple requests
#RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple emoji
#RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple jieba
#RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy
#RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple scipy
#RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple scikit-learn
#RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pymysql
#RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas

RUN pip3 install requests
RUN pip3 install emoji
RUN pip3 install jieba
RUN pip3 install numpy
RUN pip3 install scipy
RUN pip3 install scikit-learn
RUN pip3 install pymysql
RUN pip3 install pandas


ADD volume /code	
WORKDIR /code


