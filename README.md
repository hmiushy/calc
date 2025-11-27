# README.md（最小 gRPC チュートリアル）

## gRPC Minimal Example（Python）

本プロジェクトは，Python を用いた最小構成の gRPC サンプルです．

クライアントがサーバに対して Add(x， y) を呼び出し，サーバが計算結果を返します．

## 1．uv のインストールと仮想環境

### 1．1 uv のインストール

uv は高速な Python パッケージ管理・仮想環境ツールです．

以下のコマンドでインストールできます．

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

### 1．2 .venv 仮想環境の作成

プロジェクトディレクトリで次を実行します．

```bash
uv venv .venv
```

### 1．3 仮想環境を有効化

**Linux / macOS：**

```bash
source .venv/bin/activate
```

**Windows：**

```powershell
.venv\Scripts\activate
```

有効化確認：

```bash
which python
```

## 2．gRPC のインストール

仮想環境が有効な状態で，次を実行します．

```bash
uv pip install grpcio grpcio-tools
```

## 3．.proto ファイル

calc.proto を用意します．

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

## 4．コード生成

以下のコマンドを，calc.proto と同じディレクトリで実行します．

```bash
python -m grpc_tools.protoc \
  -I . \
  --python_out=. \
  --grpc_python_out=. \
  calc.proto
```

これにより次が生成されます．

- calc_pb2.py
- calc_pb2_grpc.py

## 5．サーバ実装

server.py

```python
import grpc
from concurrent import futures
import calc_pb2
import calc_pb2_grpc

class CalcService(calc_pb2_grpc.CalcServiceServicer):
    def Add(self, request, context):
        result = request.x + request.y
        return calc_pb2.AddResponse(result=result)

def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        calc_pb2_grpc.add_CalcServiceServicer_to_server(CalcService(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        print("Server started at :50051")
        server.wait_for_termination()

if __name__ == "__main__":
    serve()
```

## 6．クライアント実装

client.py

```python
import grpc
import calc_pb2
import calc_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calc_pb2_grpc.CalcServiceStub(channel)
        resp = stub.Add(calc_pb2.AddRequest(x=10, y=20))
        print("Result:", resp.result)

if __name__ == "__main__":
    run()
```

## 7．実行方法

### 7．1 サーバ起動

```bash
python server.py
```

### 7．2 クライアント実行

```bash
python client.py
```

出力例：

```
Result: 30
```

## 8．フォルダ構成例

```
gRPC-minimal/
├── calc.proto
├── calc_pb2.py
├── calc_pb2_grpc.py
├── server.py
├── client.py
└── README.md
```

## 9．補足：protoc について

Python 版 gRPC（grpcio-tools）には protoc が同梱されているため，Python の場合は OS に protoc を別途インストールする必要はありません．

Python 以外の言語（C++，Go，Rust）で使用する場合は，OS 向けの protoc を追加でインストールする必要があります．

