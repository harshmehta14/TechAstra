from Firebase_config import firebase,auth,db
import datetime
import json
def Register_firebase(username,password,name,interests,address):
    try:
        print(username,password,name)
        user = auth.create_user_with_email_and_password(username,password) 
        id= auth.get_account_info(user['idToken'])
        key = id["users"][0]['localId']
        if isinstance(key, str): 
            data={"username":username,"password":password,"name":name,"Registered_on": datetime.datetime.now(),"id":key,"rewards":0,"re":{},"interests":interests,"address":address}
            print(data,key)
            db.collection('users').document(key).set(data)
        return "Success"
    except Exception as e:
        print(e)
        return "Failed"



def Login_firebase(username,password):
    try:
        print(username,password)
        name=""
        user = auth.sign_in_with_email_and_password(username,password)
        id= auth.get_account_info(user['idToken'])
        key = id["users"][0]['localId']
        if isinstance(key, str): 
            data={"last_login": datetime.datetime.now()}
            db.collection('users').document(key).update(data)
            n= db.collection('users').where("username","==" ,username).get()[0]
            name=n.to_dict()['name']
        return name
    except Exception as e:
        print(e)
        return "Failed"


# a= Login_firebase("test@abc.coaa","12345") 
# print(a)
# print(type(id["users"][0]['localId']))
# a= db.collection('users').where("name","==" ,"test").get()[0].id
# print(a)

def get_rewards_firebase(username):
    a = db.collection('users').where("username","==" ,username).get()[0]
    rewards = a.to_dict()['rewards']
    return rewards

def add_rewards_firebase(username,amt,action):
    try:
        a = db.collection('users').where("username","==" ,username).get()[0]
        key=a.to_dict()['id']
        rewards = a.to_dict()['rewards']
        db.collection('users').document(key).update({"rewards":rewards+amt})
        return "Updated"
    except Exception as e:
        print(e)
        return "Failed"

def get_user_info(username):
    user_info = db.collection('users').where("username","==" ,username).get()[0]
    return user_info.to_dict()


