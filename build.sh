#!/usr/bin/env bash
# Aether-Nexus Production Build Script
set -o errexit

echo "[*] 开始手动安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[+] 依赖安装完成。"
