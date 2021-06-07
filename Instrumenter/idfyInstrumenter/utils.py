import uuid

'''
  Takes str,ch(optional) ; replace `.` with `+` char for routing key. Also replaces nil with "null" and returns string 

  ## Examples
      makeRoutingKeySafe("ab.c.d")
      "ab+c+d"

      makeRoutingKeySafe(nil)
      "null"

'''
def makeRoutingKeySafe(s,ch="+"):
    if(isinstance(s, str)):
        if(str == None):
            return "null"
        return s.replace(".",ch)
    else:
        return "makeRoutingKeySafe Takes (String , char='+' ) as arguement"

    
"""
  Takes events which are string and return event_source in case of custom source else return "null" for RMQ routing key

  ## Examples

      eventSourceRoutingKey("Capture")
      "Capture"

      eventSourceRoutingKey("(ms_connection_check) lib/ms_connection_check/media_server.ex:150: Elixir.MsConnectionCheck.MediaServer.attempt_room_creation/4")
      "null"
"""
def eventSourceRoutingKey(events):
    if(isinstance(events, str)):
        if(events.startswith("(")):
            return "null"
        else:
            return events    
    else:
        return "eventSourceRoutingKey takes (String) as arguement"


"""
 Takes no arg and generate a new UUID v4. 

  ## Examples
       uuid4()
      "fb49a0ec-d60c-4d20-9264-3b4cfe272106"

"""
def uuid4():
    id = str(uuid.uuid4())
    print(id)












