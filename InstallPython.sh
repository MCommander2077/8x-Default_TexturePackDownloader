    # coding=utf-8

    import os
    import sys

    if os.getuid()==0:
        pass
    else:
        print "当前用户不是root用户,请登录root用户执行脚本"
        sys.exit(1)

    version = raw_input('是否安装python版本3.9.9？(y/n)')
    if version == 'y':
        url = 'https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz'
    else:
        print '退出程序'
        sys.exit(1)

    cmd = 'wget '+url
    res = os.system(cmd)
    if res != 0:
        print '下载源码包失败，请检查网络'
        sys.exit(1)

    package_name = 'Python-3.9.9'

    cmd = 'tar xf '+package_name+'.tgz'
    res = os.system(cmd)
    if res != 0:
        os.system('rm '+package_name+'.tgz')
        print '解压源码包失败，请重新运行这个脚本'
        sys.exit(1)

    cmd = 'cd '+package_name+'&& ./configure --prefix=/usr/local/python && make && make install'
    res = os.system(cmd)
    if res !=0:
        print '编译python源码失败，请检查是否缺少依赖库'
        sys.exit(1)
