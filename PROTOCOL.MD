## user-server
Upvote

{ "action" : "upvote", "value": #songid<Int> }


Music

{ "action" : "volumeadjust", "value" : #volume<Int> }
  
#int between 1 and 100

## server-user
Receive Data       

{ "action" : "receive_updates", "data": "["title": <String>, "votes" : #votes<Int>, "songid": #songid"},{}]" } 
  
  
Receive Currently Playing
  
{ "action" : "currently_playing", "data": "title" }
