C/C++ 学习文件自动上传

学习项目：`/root/rwth-ggi1`，日常练习目录：`/root/rwth-ggi1/rwth`。
GitHub 私有仓库：https://github.com/dingyuzhong720/c-c-
分支：`main`；提交署名：`dingyuzhong720`。

在 VS Code 打开项目后，新建或修改 C/C++ 文件，按 Ctrl+S 保存。
后台约每 15 秒检查一次变化，自动创建提交并上传 GitHub；网络传输另需少量时间。
未保存的编辑内容不会上传。无需每次运行 git add / commit / push。

课程源码、文档、VS Code 配置会上传。`build/` 和常见编译产物不上传；
直接编译到源码旁的 Linux ELF 可执行文件也会自动排除。
源码保存时即会同步，不要求它已经编译成功。删除文件也会在下一次同步时提交删除，历史版本仍可从 GitHub 提交记录查看。

后台同步固定使用 GitHub CLI 中 dingyuzhong720 的授权，切换 CLI 当前账号不影响这个项目。
其他目录的 Git 提交署名配置不受影响。服务已设为开机启动，关闭 VS Code 后仍会运行。

查看同步状态（在服务器终端执行）：

```bash
systemctl status rwth-ggi1-sync.timer
journalctl -u rwth-ggi1-sync.service -n 30 --no-pager
cd /root/rwth-ggi1
git status --short --branch
git log -3 --oneline
```

暂停和恢复自动上传：

```bash
systemctl stop rwth-ggi1-sync.timer
systemctl start rwth-ggi1-sync.timer
```

这是从服务器学习目录到 GitHub 的自动上传，不会自动下载 GitHub 网页上的修改。
如果远程分支产生了冲突改动，上传会保留本地提交并记录错误，不会强制覆盖远程历史。
断网或暂时失败会在后续周期重试。
