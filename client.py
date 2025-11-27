import grpc
import calc_pb2
import calc_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calc_pb2_grpc.CalcServiceStub(channel)
        resp = stub.Add(calc_pb2.AddRequest(x=101, y=20))
        print("Result:", resp.result)

if __name__ == "__main__":
    run()
