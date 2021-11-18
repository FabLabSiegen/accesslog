
import django

django.setup()
import pytz
import json, requests
from rest_framework.response import Response
from datetime import datetime
import urllib.request
from print.models import Machine, PrintJob, BedTemperatureHistory, ToolTemperatureHistory, PrintMediaFile
from django.utils import timezone
from django.core.files import File

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
    elif event == "PrinterStateChanged":
        return event
    elif event == "plugin_octolapse_movie_done":
        return event
    elif temp == "temperature":
        return temp



def handle_msg(topic, message):
    p_exists = None
    printer = topic.split("/")[2]
    printer_id = Machine.objects.get(Name=printer).id
    m = message.decode("Utf-8")

    # Check event of topic
    event = check_topic(topic)
    
    if event == "PrinterStateChanged":
        # Event: Printer is done with PrintJob
        print("Print state changed")
        state = json.loads(m)["state_id"]
        if state == "OPERATIONAL":
            # Check if Printer is already set as operational
            try:
                PrintJob.objects.get(Machine_id=printer_id, State=1)
                p_exists = True
            except PrintJob.DoesNotExist:
                p_exists = False
            except Exception as e:
                print(e)

            try:
                if p_exists:
                    pj = PrintJob.objects.get(Machine_id=printer_id, State=1)
                    pj.State = 0
                    pj.End = timezone.now()
                    pj.save()
                    print("PrintJob ended -> State 0")
            except Exception as e:
                print(e)
        elif state == "PRINTING":
            # Check if Printer is already set printing
            try:
                PrintJob.objects.get(Machine_id=printer_id, State=1)
                p_exists = True
            except PrintJob.DoesNotExist:
                p_exists = False
            except Exception as e:
                print(e)

            try:
                if not p_exists:
                    PrintJob.objects.create(Start=timezone.now(), End=timezone.now(), GCode_id=None,State=1, Machine_id=printer_id,User_id=1)
                    print("PrintJob created")
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
        except PrintJob.DoesNotExist:
            p_exists = False
        except Exception as e:
            print(e)

        try:
            if p_exists:
                # If Temperature is bed info
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
        except Exception as e:
            print(e)

    elif event == "plugin_octolapse_movie_done":
        # remove in production
        if printer == "chaos":
            print(printer)
            try:
                # Change name in production to be variable based on topic -> printer
                host = Machine.objects.get(Name="chaos").DomainName
                apikey = Machine.objects.get(Name="chaos").ApiKey
                printjob_id = PrintJob.objects.latest('id').id
                latest_url = get_latest_timelapse_url(apikey, host)['url']
                latest_name = get_latest_timelapse_url(apikey, host)['name']

                file = download_from_path(apikey, host, latest_url, latest_name)

                try:
                    PrintMediaFile.objects.get(PrintJob_id=printjob_id, Description='timelapse')
                except:
                    PrintMediaFile.objects.create(File=file, Owner_id=1,Description='timelapse', PrintJob_id=printjob_id)
            except Exception as e:
                print(e)




def date_from_entry(entry):
    return datetime.strptime(entry['date'], '%Y-%m-%d %H:%M')

def get_latest_timelapse_url(api_key, host):
    hed = {'Authorization': 'Bearer ' + api_key, 'content-type': 'application/json'}
    data = []

    url = 'http://'+host+'/api/timelapse'
    try:
        response = requests.post(url,data=json.dumps(data), headers=hed)
        latest = max(json.loads(response.text)['files'], key=date_from_entry)
        return latest
    except requests.exceptions.RequestException as e:
        response = {'error':str(e)}
        return response

def download_from_path(api_key, host, path, name):
    hed = {'Authorization': 'Bearer ' + api_key, 'content-type': 'application/json'}

    url = 'http://'+host+ path
    try:
        response = requests.get(url, headers=hed)
        print(response)
        f=open(name,'wb')
        for chunk in response.iter_content(chunk_size=255):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
        f.close()
        f=open(name,'rb')
        return File(f)
    except requests.exceptions.RequestException as e:
        response = {'error':str(e)}
        return response