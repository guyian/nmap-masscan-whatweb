##### 当前内容参考自：https://github.com/hellogoldsnakeman/masnmapscan-V1.0

# nmap-masscan-whatweb
masscan扫描端口，nmap扫描端口对应服务

原内容
> 整合了masscan和nmap两款扫描器，masscan扫描端口，nmap扫描端口对应服务，二者结合起来实现了又快又好地扫描。
> 并且加入了针对目标资产有防火墙的应对措施
> 首先pip install -r requirements.txt安装所需插件，然后将ip地址每行一个保存到txt文本里，与本程序放在同一目录下，masscan安装完成后也与本程序放> 在同一目录下，运行程序即可。
> 最终会在当前目录下生成一个scan_url_port.txt的扫描结果

修改
> 使用 gl = globals() 作为引用全局变量 <br>
> 由于设计之初是多线程实现，导致同时对同一资源进行竞争使用，ip与端口号不对应，故修改，<br>
> 由被扫描ip作为主要因素，即由ip绑定端口号，由ip作为masscan输出文件的名称<br>
> 然后把取出的port放入变量ip中 即变量名定义如下 <br>
> gl['ip' + ''.join(scan_ip.split('.'))] = temp_ports<br>
> 变量名为  ('ip' + ''.join(scan_ip.split('.'))) <br>
> 每次取变量都会取ip对应的变量，都会选择ip对应文件进行读取<br>

```
masscan 和 nmap 配置
python2.7
pip install chardet urllib3 python-nmap
pip install requests==2.14.2
```

```
whatweb 配置
ruby 版本修改到 2.3.0
rvm install 2.3.0
gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
curl -sSL https://get.rvm.io | bash -s stable
source /etc/profile.d/rvm.sh
rvm list known
rvm install 2.3.0
gem install bundler
bundler install
```