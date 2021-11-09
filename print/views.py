

from django.shortcuts import render
import django
django.setup()
from ast import literal_eval
import json
from print.models import Machine, PrintJob , PrintTemperatureHistory
from django.utils import timezone
def handle_msg(topic, message):
    printer = topic.split("/")[2]
    p_id = Machine.objects.get(Name=printer).id
    m = message.decode("Utf-8")
    try:
        print(json.loads(m)["_timestamp"])
    except:
        print("no json")
    try:
        PrintJob.objects.get(Machine_id=p_id)
        if PrintJob.objects.get(Machine_id=p_id).State == 1:
            # PrintTemperatureHistory.objects.create(PrintJob_id=p_id, ToolTarget=message.)
            pass
    except:
        pass
        # print("does not exist")
        # PrintJob.objects.create(Start=timezone.now(), End=timezone.now(), GCode_id=None,State=1, Machine_id=p_id,User_id=1)
