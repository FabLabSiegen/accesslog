
import django
import pytz

django.setup()
import json
from datetime import datetime
from print.models import Machine, PrintJob, BedTemperatureHistory, ToolTemperatureHistory
from django.utils import timezone
def handle_msg(topic, message):
    printer = topic.split("/")[2]
    p_id = Machine.objects.get(Name=printer).id
    m = message.decode("Utf-8")

    # Check if topic is PrintDone
    try:
        done = topic.split("/")[4]
        if done != "PrintDone":
            done = None
    except:
        done = None

    # Check if topic is Temperature and if tool or bed temp is sent
    try:
        temp = topic.split("/")[3]
        toolbed = topic.split("/")[4]
        if temp != "temperature":
            temp = None
            toolbed = None
    except:
        toolbed = None
        temp = None

    if done == "PrintDone":
        # Event: Printer is done with PrintJob
        print("Print Done")
    elif temp == "temperature":
        # Temperature is sent
        target = None
        actual = None
        timestamp = None

        # Set Temperature Data
        try:
            timestamp = datetime.fromtimestamp(json.loads(m)["_timestamp"], tz=pytz.timezone('Europe/Berlin'))
            actual = json.loads(m)["actual"]
            target = json.loads(m)["target"]
        except Exception as e:
            print(e)

        # Check if Machine has related PrintJob
        try:
            PrintJob.objects.get(Machine_id=p_id)
            p_exists = True
        except:
            p_exists = False

        # Create PrintJob if no PrintJob has State 1 or none exists
        if p_exists and PrintJob.objects.get(Machine_id=p_id).State == 0:
            PrintJob.objects.create(Start=timezone.now(), End=timezone.now(), GCode_id=None,State=1, Machine_id=p_id,User_id=1)
        elif not p_exists:
            PrintJob.objects.create(Start=timezone.now(), End=timezone.now(), GCode_id=None,State=1, Machine_id=p_id,User_id=1)

        # If Temperature is bed info
        if toolbed == "bed":
            try:
                BedTemperatureHistory.objects.create(PrintJob_id=PrintJob.objects.get(Machine_id=p_id, State=1).id, Target=target, Actual=actual, TimeStamp=timestamp)
                print(timestamp)
            except Exception as e:
                print(e)

        # If Temperature is tool info
        elif toolbed == "tool0":
            try:
                ToolTemperatureHistory.objects.create(PrintJob_id=PrintJob.objects.get(Machine_id=p_id, State=1).id, Target=target, Actual=actual, TimeStamp=timestamp)
            except Exception as e:
                print(e)




