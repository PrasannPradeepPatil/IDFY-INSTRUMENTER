import uuid

'''
  Takes str,ch(optional) ; replace `.` with `+` char for routing key. Also replaces nil with "null" and returns string 

  ## Examples
      make_routing_key_safe("ab.c.d")
      "ab+c+d"

      make_routing_key_safe(nil)
      "null"

'''
def make_routing_key_safe(s,ch="+"):
    if(isinstance(s, str)):
        if(str == None):
            return "null"
        return s.replace(".",ch)
    else:
        return "make_routing_key_safe Takes (String , char='+' ) as arguement"

    
"""
  Takes events which are string and return event_source in case of custom source else return "null" for RMQ routing key

  ## Examples

      event_source_routing_key("Capture")
      "Capture"

      event_source_routing_key("(ms_connection_check) lib/ms_connection_check/media_server.ex:150: Elixir.MsConnectionCheck.MediaServer.attempt_room_creation/4")
      "null"
"""
def event_source_routing_key(events):
    if(isinstance(events, str)):
        if(events.startswith("(")):
            return "null"
        else:
            return events    
    else:
        return "event_source_routing_key takes (String) as arguement"


"""
 Takes no arg and generate a new UUID v4. 

  ## Examples
       uuid4()
      "fb49a0ec-d60c-4d20-9264-3b4cfe272106"

"""
def uuid4():
    id = str(uuid.uuid4())
    print(id)












