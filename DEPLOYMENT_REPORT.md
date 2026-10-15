GGI1 服务器部署与验证报告

核验时间：2026-10-16T01:12:15+08:00

已部署到 `/root/rwth-ggi1`，目录及内容归 root 所有。本次新增课程目录和当前任务工作区中的源文件副本、审计记录；未安装或升级软件包，未执行服务重启、系统重装或 Docker 操作。

**工具与兼容性**

| 项目 | 实测结果 |
| --- | --- |
| 操作系统与架构 | Ubuntu 24.04.2 LTS，x86_64 / amd64 |
| 内核 | 7.0.0-28-generic |
| GCC / G++ | 13.3.0 / 13.3.0，已安装 |
| GDB | 15.0.50.20240403-git，已安装 |
| Make / CMake | 4.3 / 3.28.3，已安装 |
| Git / build-essential | 2.43.0 / 12.10ubuntu1，已安装 |
| glibc | 2.39 |
| libstdc++ 符号版本 | 包含 GLIBCXX_3.4.33 |
| 基础依赖 | bash、tar、gzip、curl、wget、ca-certificates、libgcc-s1、libstdc++6 已安装 |
| Python（仅验证脚本使用） | 3.12.3 |
| 根分区可用空间（初检） | 236 GiB |
| 可用内存（初检） | 约 24 GiB |
| 文件系统 | ext4，可写，课程目录与 /tmp 所在挂载无 noexec |

本机满足当前 [VS Code Linux 远程端官方要求](https://code.visualstudio.com/docs/remote/linux)：内核至少 4.18、glibc 至少 2.28、GLIBCXX 至少 3.4.25，并具备 OpenSSH、Bash、tar 和下载工具。本次没有安装图形化 VS Code，也没有手工部署 `/root/.vscode-server`；首次连接时由朋友电脑的 Remote-SSH 扩展自动完成。

**SSH 与 Tailscale**

- 地址：`root@100.91.53.76`，端口 `33322`。
- OpenSSH 9.6p1；Tailscale 1.102.2；ssh.service、ssh.socket、tailscaled.service 均为 active。
- `PermitRootLogin without-password`、`PubkeyAuthentication yes`、`PasswordAuthentication no`、`KbdInteractiveAuthentication no`。
- `AllowTcpForwarding yes`、`AllowStreamLocalForwarding yes`、`DisableForwarding no`、`PermitOpen any`、`ForceCommand none`；SFTP 子系统已配置。
- root 的 authorized_keys 有 1 条公钥，未设置限制转发的密钥选项。没有修改该文件或新增密钥。
- Tailscale `RunSSH=false`、`WantRunning=true`、`ShieldsUp=false`；当前使用 Tailscale 网络上的普通 OpenSSH。
- 已观察到来自 `100.106.211.49` 到本机 `100.91.53.76:33322` 的现有 root SSH 会话。本次执行账号取得 sudo 权限后在本机完成部署，没有使用朋友的私钥发起新认证。
- `sshd -t` 返回 0。现有配置有废弃的 `RSAAuthentication` 选项提示，本次保持原样。
- 273 个 SSH、Tailscale 服务配置及 UFW 配置文件的 SHA-256 与部署前一致；三个核心服务的 MainPID/ActiveState/启动时间均一致。
- 初检时运行的服务在结束检查时仍运行；初检已有的 3 个失败服务（claude-remote-probe、mcsm-daemon、xray）状态未改变，未处理这些已有问题。

**实际编译、运行和调试结果**

| 检查 | 结果 |
| --- | --- |
| GCC C11 + G++ C++17，Make 构建 | 成功，无编译警告 |
| C 与 C++ 温度转换 | 各自验证 32→0、212→100、-40→-40、98.6→37，8 项通过 |
| 非法输入 | 两个程序均返回退出码 1，2 项通过 |
| GDB 断点和单步 | 两个程序均停在 fahrenheit_to_celsius，next 执行成功 |
| GDB 变量读取 | 两个程序均读到 fahrenheit=212、celsius=100，随后正常退出 |
| GDB MI2 | 成功加载 C++ 可执行文件、设置 main 断点、退出 |
| 当前文件任务的实际命令 | C、C++ 均成功编译运行，212→100 |
| CMake Debug 构建 | 两个目标均成功；分别运行验证 32→0 |
| 可执行文件 | x86-64 ELF，带 debug_info，未剥离；动态依赖均可解析 |
| VS Code 配置 | JSON 可解析，preLaunchTask 均存在，program 和 GDB 路径正确 |

复验命令：在课程目录执行 `make check`。原始输出见 `build/verification.log`；系统检查见 `build/system-check.json`。

**下载连通性与验证边界**

- VS Code 更新接口获取 JSON 成功，实际服务端下载地址 HEAD 返回 HTTP 200；仅检查连通性，没有安装服务端。
- C/C++ Marketplace 详情页 GET 返回 HTTP 200。
- Marketplace 根路径 HEAD 返回 404，扩展包接口 HEAD 返回 405；这些探测没有完成扩展包下载验证。实际扩展下载安装由朋友电脑连接后执行，原始探测记录在 `build/connectivity.json`。
- 朋友电脑的私钥、OpenSSH 配置、Tailscale 本地状态、Remote-SSH 首次部署、扩展安装、图形界面中的 F5 和变量面板均无法由本次服务器端操作代替验证。

朋友电脑的完整操作步骤见同目录 `README.md`。若下载受限，可按指南使用 `remote.SSH.localServerDownload=always` 从朋友电脑下载并传输服务端；此设置不改变 SSH 登录配置。
