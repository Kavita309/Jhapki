from twilio.rest import Client
# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACbbc0add8b0c9821500ebef3164b07884'
auth_token = 'b7497199ab5af1e2c2783759f4ea279a'
client = Client(account_sid, auth_token)

message = client.messages.create(
                              from_='+15077246172',
                              body='Ho gaya Mansi!',
                              to='+918860243261'
                          )
print(message.sid)
