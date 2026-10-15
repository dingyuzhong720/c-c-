RWTH Aachen GGI1 远程 C/C++ 开发环境

服务器课程目录：`/root/rwth-ggi1`。C 使用 C11，C++ 使用 C++17；编译启用 `-Wall -Wextra -Wpedantic -g3 -O0`，方便发现问题、设置断点和查看变量。这里的华氏度转换程序是为本次环境验证编写的教学示例，不是学校发布的作业答案。

**1. 朋友电脑上的准备**

- 启动已有的 Tailscale，确保能访问服务器 `100.91.53.76`。
- 保留现有 VS Code，在本机安装 Microsoft 的 **Remote - SSH** 扩展，ID：`ms-vscode-remote.remote-ssh`。
- 在本机 PowerShell 或终端运行 `ssh -V`。Windows 如果找不到命令，在“设置 → 可选功能”中安装 **OpenSSH 客户端**。FinalShell 自带的连接功能不能代替 VS Code 所调用的 OpenSSH 客户端。
- 在 FinalShell 现有连接设置中确认使用的私钥文件。服务器目前 `PasswordAuthentication no`，root 允许公钥登录；这里需要复用原有私钥，不能仅填写 root 密码。若私钥带口令，SSH 提示的是该私钥的口令。

**2. 填写本机 SSH Config**

VS Code 按 `Ctrl+Shift+P`，执行 `Remote-SSH: Open SSH Configuration File...`，选择本机用户配置。Windows 通常是 `C:\Users\你的用户名\.ssh\config`；macOS/Linux 是 `~/.ssh/config`。将下面这一段追加到文件中，不覆盖已有主机配置：

```sshconfig
Host rwth-ggi1
    HostName 100.91.53.76
    User root
    Port 33322
    IdentityFile "C:/Users/你的用户名/.ssh/已有私钥文件"
    IdentitiesOnly yes
    ServerAliveInterval 30
    ServerAliveCountMax 3
```

`IdentityFile` 必须换成朋友电脑上现有私钥的真实路径，指向私钥本身，不是 `.pub` 公钥文件。macOS/Linux 可以写成 `IdentityFile ~/.ssh/已有私钥文件`。本次检查确认 SSH 端口是 **33322**。

先在朋友电脑的 PowerShell/终端测试：

```text
ssh rwth-ggi1
```

首次连接如提示 ED25519 主机指纹，可与本次服务器读取的值核对：

```text
SHA256:qpEnF9/imKv2MD5kfrBZfN0Ao5NbtCy/iyvQUeuRsRs
```

登录后运行 `whoami`，应为 `root`；运行 `ls /root/rwth-ggi1`，应看到 `src`、`Makefile`、`CMakeLists.txt` 等。用 `exit` 退出此次测试连接。

**3. 在 VS Code 打开远程项目**

1. 按 `Ctrl+Shift+P` → `Remote-SSH: Connect to Host...` → 选择 `rwth-ggi1`。
2. 如果要求选择平台，选 **Linux**。等待 Remote-SSH 自动部署匹配本机 VS Code 版本的服务端组件；不需要在服务器安装图形化 VS Code。
3. 确认左下角出现 `SSH: rwth-ggi1`，然后“文件 → 打开文件夹”，填写 `/root/rwth-ggi1`。首次询问工作区信任时，确认这是刚部署的课程项目后信任它。
4. 在扩展视图安装 Microsoft **C/C++**（`ms-vscode.cpptools`），确保显示已安装在 **SSH: rwth-ggi1**。仅装在本机的 C/C++ 扩展不足以调试远程程序。
5. **CMake Tools**（`ms-vscode.cmake-tools`）可选，也应装在远程端。现成的一键任务使用 GCC/G++ 与 Make；不依赖该扩展。

Remote-SSH 的远程组件部署与扩展位置遵循 [Microsoft 官方连接说明](https://code.visualstudio.com/docs/remote/ssh)。

**4. 编译和运行**

先打开 `src/fahrenheit.c` 或 `src/fahrenheit.cpp`，按 `Ctrl+S` 保存，并保持该源文件为当前活动编辑器。

| 操作 | 使用方法 |
| --- | --- |
| 编译当前 C/C++ 文件 | `Ctrl+Shift+B`，默认任务 `GGI1: Build active file` |
| 编译并运行当前文件 | 在“运行和调试”下拉框选 `GGI1: Debug active file`，按 `Ctrl+F5` |
| 通过任务运行当前文件 | 命令面板 `Tasks: Run Task` → `GGI1: Run active file` |
| 编译两个示例 | `Tasks: Run Task` → `GGI1: Build examples` |
| 运行固定 C / C++ 示例 | `GGI1: Run C example` / `GGI1: Run C++ example` |
| 重做自动验证 | `GGI1: Verify examples`，或远程终端 `make check` |

运行后在下方 **终端 Terminal** 输入 `212` 并回车，应看到 `212.00 F = 100.00 C`。标准输入在终端中输入，不是在“调试控制台 Debug Console”中输入。

也可以在 VS Code 的远程终端执行：

```bash
cd /root/rwth-ggi1
make
./build/fahrenheit-c
./build/fahrenheit-cpp
make check
```

两个可执行程序分别等待一次输入。新作业可保存为项目内的 `.c`、`.cpp`、`.cc` 或 `.cxx` 文件，打开该文件后继续使用相同的快捷键。当前文件任务一次编译一个源文件；需要多个源文件共同链接时，在 Makefile/CMakeLists.txt 中添加对应目标。两个人同时练习时，使用各自的源码文件；相同文件名的“当前文件”构建会共用 `build/active/` 下对应的可执行文件。

**5. F5 断点调试和查看变量**

1. 打开 `src/fahrenheit.c`，在第 7 行 `return celsius;` 左侧点击，出现红色断点。
2. 在“运行和调试”下拉框中选 `GGI1: Debug C example`，按 `F5`。启动前会自动编译。
3. 在下方终端输入 `212` 并回车，程序会停在断点。
4. 在左侧 **变量 Variables** 中查看 `fahrenheit = 212`、`celsius = 100`；也可悬停变量，或在 **监视 Watch** 中添加这两个名称。
5. `F10` 单步跳过，`F11` 单步进入，`Shift+F11` 跳出函数，`F5` 继续，`Shift+F5` 停止。变量仅在其所在作用域有效。
6. C++ 示例同理：在 `src/fahrenheit.cpp` 第 10 行设置断点，选择 `GGI1: Debug C++ example`。新作业则使用 `GGI1: Debug active file`，并保持对应源码为活动编辑器。

调试器配置为 `cppdbg`、`gdb`、`/usr/bin/gdb`，输入输出使用 VS Code 集成终端；配置含义见 [Microsoft C/C++ 调试配置文档](https://code.visualstudio.com/docs/cpp/launch-json-reference)。

**6. 可选的 CMake 构建**

```bash
cd /root/rwth-ggi1
cmake -S . -B build/cmake -DCMAKE_BUILD_TYPE=Debug
cmake --build build/cmake --parallel 2
./build/cmake/fahrenheit_c
./build/cmake/fahrenheit_cpp
```

**7. 连接问题排查**

- `Permission denied (publickey)`：检查 Config 中的私钥是否确实是 FinalShell 使用的同一把密钥、用户名是否是 root、端口是否是 33322。若 FinalShell 使用的是另一台主机或另一个入口，应先核对连接信息。
- 找不到 `ssh`：安装本机 OpenSSH 客户端后重新打开 VS Code。
- 无法连接：在 Windows PowerShell 运行 `Test-NetConnection 100.91.53.76 -Port 33322`，检查 Tailscale 是否在线。它只能测试端口连通性，不能替代 SSH 认证测试。
- 卡在服务端下载：打开“查看 → 输出 → Remote - SSH”查看错误。如果服务器侧下载受限，可在朋友电脑的 VS Code 用户设置中合并 `"remote.SSH.localServerDownload": "always"`，由本机下载并经 SSH 传输。朋友电脑需要能访问微软更新和下载站点；扩展下载另需要 Marketplace/CDN。该设置的行为见 [官方网络要求](https://code.visualstudio.com/docs/remote/ssh#_what-are-the-connectivity-requirements-for-the-vs-code-server-when-it-is-running-on-a-remote-machine-vm)。
- `cppdbg` 无法识别：检查 C/C++ 扩展是否安装在当前 SSH 远程端。
- 断点灰色或不停止：确认调试下拉框选对了程序，源码已保存；如果用“当前文件”，确认活动编辑器是对应的 C/C++ 源文件。这里的构建参数已包含调试符号并关闭优化。

**8. 已验证范围**

服务器端已实际完成 C11/C++17 编译、温度转换、非法输入、GDB 断点/单步/变量、GDB MI、当前文件任务命令以及 CMake 构建验证。原始日志在 `build/verification.log`，部署结果见 `DEPLOYMENT_REPORT.md`。

朋友电脑上的 OpenSSH 配置、私钥可用性、Remote-SSH 首次下载、远程扩展安装、VS Code 图形界面中的 F5 和变量面板仍需按本指南在该电脑验证。服务器端测试不能替代这些客户端操作。
