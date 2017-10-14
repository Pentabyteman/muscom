## user-server
Upvote
{ "action" : "upvote", "value": #songid<Int> }


Music
{ "action" : "volumeadjust", "value" : #volume<Int> }
#int between 1 and 100

## server-user
{ "title" : [#title<String>], "votes" : [#votes<Int>] }
