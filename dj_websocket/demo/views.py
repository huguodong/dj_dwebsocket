from django.shortcuts import render
from dwebsocket.decorators import accept_websocket,require_websocket
from django.http import HttpResponse

import threading

# Create your views here.

clients = []


def index(request):
    return render(request, 'index.html')

def index2(request):
    return render(request, 'index2.html')
# @accept_websocket
# def echo(request):
#     if request.is_websocket:#如果是webvsocket
#         lock = threading.RLock() #rlock线程锁
#         try:
#             lock.acquire()#抢占资源
#             clients.append(request.websocket)#把websocket加入到clients
#             print(clients)
#             for message in request.websocket:
#                 if not message:
#                     break
#                 for client in clients:
#                     client.send(message)
#         finally:
#             clients.remove(request.websocket)
#             lock.release()#释放锁

def modify_message(message):
    return message.lower()


@accept_websocket
def echo(request):
    if not request.is_websocket():#判断是不是websocket连接
        try:#如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request,'index.html')
    else:
        for message in request.websocket:
            request.websocket.send(message)#发送消息到客户端

@require_websocket
def echo_once(request):
    message = request.websocket.wait()
    request.websocket.send(message)