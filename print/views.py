
import django
django.setup()
import pytz
import json
from datetime import datetime
from print.models import Machine, PrintJob, BedTemperatureHistory, ToolTemperatureHistory
from django.utils import timezone

def check_topic(topic):
    temp = None
    event = None
    
    try:
        event = topic.split("/")[4]
    except:
        pass

    try:
        temp = topic.split("/")[3]
    except:
        pass
        
    if event == "PrintDone":
        return event
    elif event == "PrintStarted":
        return event
    elif event == "PrintStarted":
        return event
    elif temp == "temperature":
        return temp


def handle_msg(topic, message):
    printer = topic.split("/")[2]
    printer_id = Machine.objects.get(Name=printer).id
    m = message.decode("Utf-8")

    # Check event of topic
    event = check_topic(topic)
    
    if event == "PrintStarted":
        # Event: Printer is done with PrintJob
        print("Print started")
        # Check if PrintJob already exists
        try:
            PrintJob.objects.get(Machine_id=printer_id, State=1)
            p_exists = True
        except:
            p_exists = False

        try:
            if p_exists:
                print("PrintJob already exists")
            else:
                PrintJob.objects.create(Start=timezone.now(), End=timezone.now(), GCode_id=None,State=1, Machine_id=printer_id,User_id=1)
                print("PrintJob created")
        except Exception as e:
            print(e)

    elif event == "PrintDone":
        # Event: Printer is done with PrintJob
        print("Print Done")

        # Check if PrintJob exists
        try:
            PrintJob.objects.get(Machine_id=printer_id, State=1)
            p_exists = True
        except:
            p_exists = False

        try:
            if p_exists:
                pj = PrintJob.objects.get(Machine_id=printer_id, State=1)
                pj.State = 0
                pj.save()
                print("PrintJob State = 0")
        except Exception as e:
            print(e)

    elif event == "temperature":
        # Event: Temperature is sent
        target = None
        actual = None
        timestamp = None
        tool_bed = topic.split("/")[4]
        # Set Temperature Data
        try:
            timestamp = datetime.fromtimestamp(json.loads(m)["_timestamp"], tz=pytz.timezone('Europe/Berlin'))
            actual = json.loads(m)["actual"]
            target = json.loads(m)["target"]
        except Exception as e:
            print(e)

        # Check if Machine has related PrintJob
        try:
            PrintJob.objects.get(Machine_id=printer_id, State=1)
            p_exists = True
        except:
            p_exists = False

        # If Temperature is bed info
        if p_exists:
            if tool_bed == "bed":
                try:
                    BedTemperatureHistory.objects.create(PrintJob_id=PrintJob.objects.get(Machine_id=printer_id, State=1).id, Target=target, Actual=actual, TimeStamp=timestamp)
                except Exception as e:
                    print(e)

            # If Temperature is tool info
            elif tool_bed == "tool0":
                try:
                    ToolTemperatureHistory.objects.create(PrintJob_id=PrintJob.objects.get(Machine_id=printer_id, State=1).id, Target=target, Actual=actual, TimeStamp=timestamp)
                except Exception as e:
                    print(e)