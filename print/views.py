from django.shortcuts import render

# Create your views here.
def handle_msg(topic, message):

    if str(topic).endswith("/temperature/tool0"):
        pass
    elif str(topic).endswith("/temperature/bed"):
        pass
    elif str(topic).endswith("/event/ZChange"):
        pass
    elif str(topic).endswith("/event/ZChange"):
        pass
    elif str(topic).endswith("/event/ZChange"):
        pass
    elif str(topic).endswith("/event/ZChange"):
        pass
    elif str(topic).endswith("/event/ZChange"):
        pass
    else:
        return "no input"