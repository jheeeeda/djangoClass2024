from django.shortcuts import render
from django.http import JsonResponse
from pymodbus.client import ModbusTcpClient
import json

# Create your views here.

def modbus(request):
    return render( request, 'modbus/modbus.html')

def modbus_data(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        receiveData = json.loads(request.body)
        mod = receiveData.get("mod")
        ipAddress = receiveData.get("ipAddress")
        ipAddress = ipAddress.strip()

        client = ModbusTcpClient(ipAddress)
        client.connect()

        result = None
        response_data = {}

        if mod == "writeRegister":
            registerAddress = receiveData.get("registerAddress")
            registerValue = receiveData.get("registerValue")

            client.write_register(int(registerAddress)-1, int(registerValue))
        
        elif mod == "readRegister":
            registerAddress = receiveData.get("registerAddress")

            result = client.read_holding_registers(int(registerAddress)-1, count=1)
            if not result.isError():
                response_data["register"] = str(result.registers[0])

        elif mod == "writeCoil":
            coilAddress = receiveData.get("coilAddress")
            coilValue = receiveData.get("coilValue")

            client.write_coil(int(coilAddress)-1, coilValue == "True")
        
        elif mod == "readCoil":
            firstAddress = receiveData.get("firstAddress")
            lastAddress = receiveData.get("lastAddress")
            readCount = int(lastAddress)-int(firstAddress)+1

            result = client.read_coils(int(firstAddress)-1, readCount)
            if not result.isError():
                resultCoils = ",".join(list(map(str, result.bits[:readCount])))
                response_data["coils"] = resultCoils
        
        client.close()

        response_data["message"] = "Modbus 통신이 완료되었습니다."
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "잘못된 요청입니다."}, status=400)