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
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
