# gRPC Minimal Example (Python)

Python を用いた最小構成の gRPC サンプルプロジェクトです。クライアントがサーバに対して `Add(x, y)` を呼び出し、サーバが計算結果を返すシンプルな例を提供します。

## 📋 目次

- [概要](#概要)
- [機能](#機能)
- [要件](#要件)
- [セットアップ](#セットアップ)
- [使い方](#使い方)
- [プロジェクト構造](#プロジェクト構造)
- [補足情報](#補足情報)

## 概要

このプロジェクトは、gRPC を初めて学ぶ方のための最小構成のサンプルです。以下の要素を含んでいます：

- Protocol Buffers (`.proto`) ファイルの定義
- gRPC サーバの実装
- gRPC クライアントの実装
- 基本的な RPC 呼び出しの例

## 機能

- 2つの整数を受け取り、その合計を返す `Add` RPC メソッド
- シンプルで理解しやすいコード構造
- 最小限の依存関係

## 要件

- Python 3.7 以上
- [uv](https://github.com/astral-sh/uv)（パッケージ管理ツール）

## セットアップ

### 1. uv のインストール

uv は高速な Python パッケージ管理・仮想環境ツールです。

**Linux / macOS：**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows（PowerShell）：**

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

インストール確認：

```bash
uv --version
```

### 2. 仮想環境の作成と有効化

プロジェクトディレクトリで以下を実行します：

```bash
# 仮想環境の作成
uv venv .venv

# 仮想環境の有効化（Linux / macOS）
source .venv/bin/activate

# 仮想環境の有効化（Windows）
.venv\Scripts\activate
```

### 3. gRPC のインストール

仮想環境が有効な状態で、以下を実行します：

```bash
uv pip install grpcio grpcio-tools
```

### 4. コード生成

`.proto` ファイルから Python コードを生成します：

```bash
python -m grpc_tools.protoc \
  -I . \
  --python_out=. \
  --grpc_python_out=. \
  calc.proto
```

これにより以下のファイルが生成されます：

- `calc_pb2.py` - メッセージクラス
- `calc_pb2_grpc.py` - サービスとスタブクラス

## 使い方

### サーバの起動

ターミナルで以下を実行します：

```bash
python server.py
```

サーバが起動すると、以下のメッセージが表示されます：

```
Server started at :50051
```

### クライアントの実行

別のターミナルで以下を実行します：

```bash
python client.py
```

出力例：

```
Result: 30
```

## プロジェクト構造

```
calc/
├── calc.proto          # Protocol Buffers 定義ファイル
├── calc_pb2.py         # 生成されたメッセージクラス
├── calc_pb2_grpc.py    # 生成されたサービスとスタブクラス
├── server.py           # gRPC サーバ実装
├── client.py           # gRPC クライアント実装
├── .gitignore          # Git 除外設定
└── README.md           # このファイル
```

## 補足情報

### protoc について

Python 版 gRPC（`grpcio-tools`）には `protoc` が同梱されているため、Python の場合は OS に `protoc` を別途インストールする必要はありません。

Python 以外の言語（C++、Go、Rust など）で使用する場合は、OS 向けの `protoc` を追加でインストールする必要があります。

### .proto ファイルの内容

```proto
syntax = "proto3";

package calc;

service CalcService {
  rpc Add (AddRequest) returns (AddResponse);
}

message AddRequest {
  int32 x = 1;
  int32 y = 2;
}

message AddResponse {
  int32 result = 1;
}
```

### サーバ実装の要点

```python
class CalcService(calc_pb2_grpc.CalcServiceServicer):
    def Add(self, request, context):
        result = request.x + request.y
        return calc_pb2.AddResponse(result=result)
```

### クライアント実装の要点

```python
with grpc.insecure_channel('localhost:50051') as channel:
    stub = calc_pb2_grpc.CalcServiceStub(channel)
    resp = stub.Add(calc_pb2.AddRequest(x=10, y=20))
    print("Result:", resp.result)
```
