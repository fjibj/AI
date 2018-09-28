1. pip install jupyter

2. 生成配置文件：
jupyter notebook --generate-config
生成的配置文件位于 ~/.jupyter/jupyter_notebook_config.py。

3. 生成密码
python -c "import IPython;print(IPython.lib.passwd())"
类似'sha1:dd093ab45c4a:8ba6ce96abd70c10e0dc937078ff9dfbf5074f4e'   #fj123

4. 编辑配置文件：
vim ~/jupyter/jupyter_notebook_config.py
c = get_config()
c.NotebookApp.password = u'sha1:dd093ab45c4a:8ba6ce96abd70c10e0dc937078ff9dfbf5074f4e' --上一步生成的密码
c.NotebookApp.allow_remote_access = True
c.NotebookApp.allow_origin = '*'
c.NotebookApp.ip = '*'
c.NotebookApp.port = 6789 --默认8888
c.NotebookApp.open_browser = False

5. 再次启动Notebook：
jupyter notebook 
如果是以root用户启动，还需要加上--allow-root

6. 使用浏览器访问：https://your_domain_or_IP:6789(如果是virtualbox且采用NAT网络模式，则需要设置端口转发：设置->网络->网卡->高级->端口转发）




