from flask import*
import pyrebase
from datetime import datetime
from datetime import datetime,timedelta
import urllib.request
import time
import smtplib
#import openai #dis_abled_openai_key=True
#from bardapi import Bard
#pip install bardapi
#pip install torch
#from transformers import AutoModelForCausalLM, AutoTokenizer
#import torch
import cohere


# used for development ----not used in actual  build----
'''firebaseConfig = {
  "apiKey": "AIzaSyB-JHJrL3p6V-MlsitkgoWnN4HZ4eQuCHs",
  "authDomain": "picsta-9b3d0.firebaseapp.com",
  "databaseURL": "https://picsta-9b3d0-default-rtdb.firebaseio.com",
  "projectId": "picsta-9b3d0",
  "storageBucket": "picsta-9b3d0.appspot.com",
  "messagingSenderId": "908730701999",
  "appId": "1:908730701999:web:aeb59ed18e7dd68e8a1c5a",
  "measurementId": "G-TVQM8LZC49"
}'''

#original picstanew db
firebaseConfig = {
 "apiKey": "AIzaSyC0fzM9LaUtydwHrPS1N0gtJcvu-Ff_bvI",
  "authDomain": "picstanew.firebaseapp.com",
  "databaseURL": "https://picstanew-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "picstanew",
  "storageBucket": "picstanew.appspot.com",
  "messagingSenderId": "690459338329",
  "appId": "1:690459338329:web:12414949439a77dca53348",
  "measurementId": "G-54JM47BZEW"
}

firebase= pyrebase.initialize_app(firebaseConfig)

auth=firebase.auth()

data=firebase.database()
storage=firebase.storage()

app=Flask(__name__)


app.secret_key = "123abc"

@app.route('/')
def landing():
    return render_template("loading.html")
    
   
    

    
    
   
    
    

@app.route("/🍪")    
def realanding():
    
    user_token = request.cookies.get("user_id")
   
    if user_token:
        cookie=data.child(user_token).child("cookies").get().val()
        if cookie:
            
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login"))
            
    else:
            return redirect(url_for("login"))
            
   
    
    
    
    
        
    
    
    
   
        
   
    

@app.route("/Login",methods=["POST","GET"])
def login():
    error=None
    if request.method=="POST":
        email=request.form["email"]
        passw=request.form["password"]

        if not email or not passw:
            return "Please enter your email and password"
        else:
            try:
                user=auth.sign_in_with_email_and_password(email,passw)
                user_id=user["localId"]
                session["userid"] = user_id
                max_age_in_years = 500
                max_age_in_seconds = max_age_in_years * 365.25 * 24 * 60 * 60 

               
                response = make_response(redirect(url_for('index')))
                
                response.set_cookie('user_id', value=user_id, max_age=int(max_age_in_seconds))
                data.child(user_id).child("cookies").set(True)
                return response
               
                #return redirect(url_for("index"))
                

            except:
                error="Invalid email or password"
                

                
                
     
            
    
    return render_template("login.html",error=error)
@app.route("/Home",methods=["POST","GET"])
def index():
          idu=request.cookies.get("user_id")
          datasus=data.child(idu).get().val()
          now = datetime.now()
          dt = now.strftime("%a %b %d, %Y")
          dtt = now.strftime("%I:%M %p")
           
          time=f"Last seen on {dt} at {dtt}"

          #print(time)

          data.child(idu).child("active").push(time)
          sus=datasus.get("suspended",False)
          wallpaper=data.child(idu).child("wallpaper").get().val()
          if wallpaper is not None:
              b=data.child(idu).child("wallpaper").get()
              for imgc in b.each():
                     wall=imgc.val()
          else:
                         wall= "https://garden.spoonflower.com/c/13653066/p/f/l/2ew2IlKxO3d7zoMLO3NiUxf6MkJT7aeURreXyo89kPIiZJSXwkA5mAE/Solid%20nero%20grey.jpg"
            
          
    

          
              

                 
           
         
          '''storiesresp=data.get("stories")
          stories=storiesresp.val()
          story=[]

          if stories is not None :
              for post_id, postcontent in reversed(stories.items()):
                   if isinstance(postcontent, dict):
                           postsdata = postcontent.get("stories")
                           if postsdata is not None:
                               for postin in postsdata.values():
                                   story.append({"postid":post_id,"verified":postin["verified"],"userid":postin["userid"],"userdp": postin["userdp"], "username": postin["username"], "time": postin["time"],"image_url": postin["image_url"] })


          else:
              p=" " '''

                          
              

          
          
          response = data.get("posts")
          post =response.val()
          images = []
          if post is not None:
              timestamps = []
              for postid, postcontent in post.items():
                  if isinstance(postcontent, dict):
                      postsdata = postcontent.get("posts")
                      if postsdata is not None:
                          for postin in postsdata.values():
                              timestamps.append(postin["time"])
              sorted_timestamps = sorted(timestamps, reverse=True)
              images = []
              for timestamp in sorted_timestamps:
                   for postid, postcontent in post.items():
                       if isinstance(postcontent, dict):
                           postsdata = postcontent.get("posts")
                           if postsdata is not None:
                               for postin in postsdata.values():
                                   if postin["time"] == timestamp:
                                       images.append({"os":postin["os"],"postid":postid,"verified":postin["verified"],"userid":postin["userid"],"userdp": postin["userdp"], "username": postin["username"], "time": postin["time"], "caption": postin["caption"],"image_url": postin["image_url"] })
        

        
       
          return  render_template("index.html",images=images,wall=wall)#story=story)
@app.route("/Search")
def search():
    idu=request.cookies.get("user_id")
    now = datetime.now()
    dt = now.strftime("%a %b %d, %Y")
    dtt = now.strftime("%I:%M %p")
           
    time=f"Last seen on {dt} at {dtt}"

         

    data.child(idu).child("active").push(time)

   
   
    
    wallpaper=data.child(idu).child("wallpaper").get().val()
    if wallpaper is not None:
         b=data.child(idu).child("wallpaper").get()
         for imgc in b.each():
                     wall=imgc.val()
    else:
                         wall= "https://garden.spoonflower.com/c/13653066/p/f/l/2ew2IlKxO3d7zoMLO3NiUxf6MkJT7aeURreXyo89kPIiZJSXwkA5mAE/Solid%20nero%20grey.jpg"
            
          
    
    allu=data.get()
    resa=[]
    userdp=None
    for ush in allu.each():
        user_data=ush.val()
        if isinstance(user_data,dict):
            idu=request.cookies.get("user_id")
            k=ush.val().get("Handle")
            abc=ush.val().get("ID")
            verified=ush.val().get("verified",True)
            if verified:
                     url="https://media2.giphy.com/media/xmOMPI63SsyZyKz2Tx/giphy.gif"
            else:
                     url="https://upload.wikimedia.org/wikipedia/commons/4/48/BLANK_ICON.png"
            ni=ush.val().get("Images")
            if ni:
                 for key, value in ni.items():
                     userdp = value 
                      
            else:
                      userdp="https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"

            suspen=data.child(idu).get().val()
            verified=suspen.get("verified",True)
            if verified:
                actived=ush.val().get("active")
                if actived:
                    for key,value in actived.items():
                        da=value
                else:
                    pass
                        
            else:
                     #iu=ush.val().get("Handle")
                     da=""


        
           
           
           
            if k:
                resa.append({"handle":[k],"id":[abc],"url":[url],"dp":[userdp],"active":[da]})
    
    return render_template("search.html",resa=resa,wall=wall)
@app.route("/Forgot",methods=["POST","GET"])
def forgot():
    error=None
    success=None
    if request.method=="POST":
        email=request.form["email"]

        try:
             auth.send_password_reset_email(email)
             success=f"Password reset link has been successfully sent to  {email}!"
        except:
            error="Invalid email address"
    return render_template("forgot.html",error=error,success=success)
@app.route("/Upload",methods=["POST","GET"])
def upload():
     e=None
     user=None
     user_id=request.cookies.get("user_id")

     
     
   
     datasus=data.child(user_id).get().val()

     sus=datasus.get("suspended",False)
     
     
     if sus:
         return render_template("uploadsus.html")
         
        
     else:
         user_id=request.cookies.get("user_id")
         resa=[]
         wallpaper=data.child(user_id).child("wallpaper").get().val()
         if wallpaper is not None:
              b=data.child(user_id).child("wallpaper").get()
              for imgc in b.each():
                     wall=imgc.val()
         else:
                         wall= "https://garden.spoonflower.com/c/13653066/p/f/l/2ew2IlKxO3d7zoMLO3NiUxf6MkJT7aeURreXyo89kPIiZJSXwkA5mAE/Solid%20nero%20grey.jpg"
         k=data.child(user_id).child("Handle").get().val()
        
         datasus=data.child(user_id).get().val()
         verified=datasus.get("verified",True)
     
         if verified:
                     url="https://media2.giphy.com/media/xmOMPI63SsyZyKz2Tx/giphy.gif"
         else:
                     url="https://upload.wikimedia.org/wikipedia/commons/4/48/BLANK_ICON.png"
            
         nimg=data.child(user_id).child("Images").get().val()
         if nimg is not None:
            v=data.child(user_id).child("Images").get()
            for img in v.each():
                         imgc=img.val()
                         userdp=imgc
         else:
                      userdp="https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"


         resa.append({"handle":[k],"url":[url],"dp":[userdp]})
         
            
          
         error=None
         success=None
         userdp=None
         if request.method=="POST":
             caption=request.form["caption"]
             image=request.files["filename"]
             if image:
                      image_path = f"images/{image.filename}"
                      storage.child(image_path).put(image)
             else:
                      wall = "https://img.icons8.com/material-outlined/1/full-stop.png"
                      response = urllib.request.urlopen(wall)
                      image_path = f"images/image.jpg"
                      storage.child(image_path).put(response.read())
                  
            
                  

            
             userdata = data.child(user_id).child('Handle').get().val()

             nimg=data.child(user_id).child("Images").get().val()
             if nimg is not None:
                      v=data.child(user_id).child("Images").get()
                      for img in v.each():
                         imgc=img.val()
                         userdp=imgc
             else:
                      userdp="https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"
             now = datetime.now()
             dt = now.strftime("%d / %m / %y")
             dtt = now.strftime("%I:%M %p")
             captiondata = f"{caption}"
             time=f"Shared on: {dt} at {dtt}"
             suspen=data.child(user_id).get().val()
             verified=suspen.get("verified",True)
             if verified:
                     url="https://media2.giphy.com/media/xmOMPI63SsyZyKz2Tx/giphy.gif"
             else:
                     url="https://upload.wikimedia.org/wikipedia/commons/4/48/BLANK_ICON.png"
            
             def useridget(userdevice):
                 if "Windows" in userdevice:
                     return"💻 Posted from Windows device"
                 if "Android" in userdevice:
                     return"📱Posted from Android device"
                 elif 'iPhone' in userdevice or 'iPad' in userdevice:
                     return"📱Posted from Ios   device"
                 elif "Macintosh" in userdevice:
                     return "💻 Posted from Macos device"
                 else:
                     return"❌ Can't determine device"
              
             userdevice=request.headers.get("user-agent")
             useros=useridget(userdevice)
             post_data = {"verified":url,"userid":user_id,"userdp":userdp,"username":userdata,"caption": captiondata, "image_url": storage.child(image_path).get_url(None),"time":time,"os":useros}
             data.child(user_id).child("posts").push(post_data)
             return redirect(url_for("index"))
                  
              
         return render_template("upload.html",error=error,success=success,wall=wall,userdp=userdp,resa=resa)


@app.route("/Id")
def id():

    nop=None
    wall=None
    url=None
    delete=None
    deleteno=None
    idu=request.cookies.get("user_id")
   
    now = datetime.now()
    dt = now.strftime("%a %b %d, %Y")
    dtt = now.strftime("%I:%M %p")
           
    time=f"Last seen on {dt} at {dtt}"

         

    data.child(idu).child("active").push(time)
    
    idofu=data.child(idu).child("Handle").get().val()


    wallpaper=data.child(idu).child("wallpaper").get().val()
    if wallpaper is not None:
          b=data.child(idu).child("wallpaper").get()
          for imgc in b.each():
                     wall=imgc.val()
    else:
                         wall= "https://garden.spoonflower.com/c/13653066/p/f/l/2ew2IlKxO3d7zoMLO3NiUxf6MkJT7aeURreXyo89kPIiZJSXwkA5mAE/Solid%20nero%20grey.jpg"
            

    bio=data.child(idu).child("bio").get().val()
    if bio is not None:
        bio=data.child(idu).child("bio").get()
        for bio in bio.each():
            bio=bio.val()
    

    bday=data.child(idu).child("birthday").get()
    for bday in bday.each():
            bday=bday.val()

    
    date=data.child(idu).child("date").get()
    for date in date.each():
            date=date.val()

    nimg=data.child(idu).child("Images").get().val()
    if nimg is not None:
       v=data.child(idu).child("Images").get()
       for img in v.each():
           userdp=img.val()
    else:
        userdp = "https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"
                 
    response = data.child(idu).child("posts").get()
    posta = response.val()
    images = []


    datasus=data.child(idu).get().val()

    ver=datasus.get("verified",True)
     
     
    if ver:
         url="https://media2.giphy.com/media/xmOMPI63SsyZyKz2Tx/giphy.gif"

    else:
                     url="https://upload.wikimedia.org/wikipedia/commons/4/48/BLANK_ICON.png"
    vere=datasus.get("verified",True)
     
     
    if vere:
         delete="delete"

    else:
         deleteno="deleteno"



    if posta:
        for post_id, post_content in reversed(posta.items()):
            images.append({"os":post_content.get("os"),"postid":post_id,"verified":post_content.get("verified",""),"userid":post_content.get("userid",""),"userdp": post_content.get("userdp", ""),"username": post_content.get("username", ""), "time": post_content.get("time", ""),"caption": post_content.get("caption", ""),"image_url": post_content.get("image_url", "")})

    else:
        nop="No pic's yet"

   

    
         
        
    return render_template("id.html",ido=idofu,userdp=userdp,images=images,bd=bday,d=date,nop=nop,bio=bio,wall=wall,url=url,delete=delete,deleteno=deleteno)
    
   
@app.route("/Register",methods=["POST","GET"])
def register():
    error=None
    if request.method=="POST":
        email=request.form["email"]
        passw=request.form["password"]
        handle=request.form["name"]
        bd=request.form["birthday"]
        password=request.form["password"]
       

        if not email or not passw:
            return "Please enter your email and password"
        else:
            try:
               
                user=auth.create_user_with_email_and_password(email,passw)
                data.child(user["localId"]).child("Handle").set(handle)
                data.child(user["localId"]).child("ID").set(user["localId"])
                dateofjoin = datetime.now().strftime("%d-%m-%y")
                dateofjoinadd="Joined on :"+dateofjoin
                data.child(user["localId"]).child("date").push(dateofjoinadd)
                bd=bd
                dateofbday="Birthday 🎂:"+bd
                data.child(user["localId"]).child("birthday").push(dateofbday)
                data.child(user["localId"]).child("suspended").set(False)

                data.child(user["localId"]).child("password").push(password)
                data.child(user["localId"]).child("verified").set(False)
                data.child(user["localId"]).child("email").push(email)

                

                
                
                
                

                return redirect(url_for("login"))
                

            except:
                error="Invalid email or user already exists"
    return render_template("register.html",error=error)

@app.route("/Id/<profile>")
def profile(profile):
    nop=None
    idu=profile
    wall=None
    url=None

    myid=request.cookies.get("user_id")

    now = datetime.now()
    dt = now.strftime("%a %b %d, %Y")
    dtt = now.strftime("%I:%M %p")
           
    time=f"Last seen on {dt} at {dtt}"

         

    data.child(myid).child("active").push(time)

    
    
    
    idofu=data.child(idu).child("Handle").get().val()

    datasus=data.child(idu).get().val()

    sus=datasus.get("suspended",False)


    if sus:
        return render_template("useridsus.html",idofu=idofu)
    else:
        wallpaper=data.child(idu).child("wallpaper").get().val()
        if wallpaper is not None:
          b=data.child(idu).child("wallpaper").get()
          for imgc in b.each():
                     wall=imgc.val()
        else:
                         wall= "https://garden.spoonflower.com/c/13653066/p/f/l/2ew2IlKxO3d7zoMLO3NiUxf6MkJT7aeURreXyo89kPIiZJSXwkA5mAE/Solid%20nero%20grey.jpg"

        bio=data.child(idu).child("bio").get().val()
        if bio is not None:
            bio=data.child(idu).child("bio").get()
            for bio in bio.each():
                bio=bio.val()

        bday=data.child(idu).child("birthday").get()
        for bday in bday.each():
            bday=bday.val()

        date=data.child(idu).child("date").get()
        for date in date.each():
            date=date.val()


        nimg=data.child(idu).child("Images").get().val()
        if nimg is not None:
            v=data.child(idu).child("Images").get()
            for img in v.each():
                userdp=img.val()
        else:
            userdp = "https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"

    
        response = data.child(idu).child("posts").get()
        posta = response.val()
        images = []
        datasus=data.child(idu).get().val()
        ver=datasus.get("verified",True)

        if ver:
         url="https://media2.giphy.com/media/xmOMPI63SsyZyKz2Tx/giphy.gif"
         actived=data.child(idu).child("active").get()
         for actived in actived.each():
            da=actived.val()
         
        else:
                     url="https://upload.wikimedia.org/wikipedia/commons/4/48/BLANK_ICON.png"
                     da="To see last seen of {{idofu}} you need to be verified first"
        datasus=data.child(myid).get().val()
        vere=datasus.get("verified",True)

        if vere:
        
         actived=data.child(idu).child("active").get()
         for actived in actived.each():
            da=actived.val()
         
        else:
                     iu=data.child(idu).child("Handle").get().val()
                     da=f"To see '{iu}'s' last seen, verify first."
        if posta:
            for post_id, post_content in reversed(posta.items()):
                images.append({"os":post_content.get("os",""),"verified":post_content.get("verified",""),"userid":post_content.get("userid",""),"userdp": post_content.get("userdp", ""),"username": post_content.get("username", ""), "time": post_content.get("time", ""),"caption": post_content.get("caption", ""),"image_url": post_content.get("image_url", "")})
        else:
            nop="No pic's yet"

        isb=None
        nob=None
        buddy=data.child(myid).child("buddy").get().val()
       
       
     
       

        
        
        myid=request.cookies.get("user_id") 

        idofme=data.child(myid).child("Handle").get().val()
        idofu=data.child(idu).child("Handle").get().val()
        

        info=[]
        info.append({"iduo":idu,"their":idofu})

       


        if buddy is not None :
            v=data.child(myid).child("buddy").get()
            for idm in v.each():
               bud=idm.val()
               if idofu==bud:
                       
                        isb=" "
               else:
                   pass
                        
      
   
        else:
            pass
        info=[]
        info.append({"iduo":idu,"handle":idofu,"their":idofu})

        
        return render_template("userid.html",ido=idofu,userdp=userdp,images=images,bd=bday,d=date,nop=nop,bio=bio,wall=wall,url=url,da=da,isb=isb,nob=nob,info=info)

@app.route("/Seebuddiesof/<idbo>")
def seebuddy(idbo):
    bud=idbo

    lis=data.child(bud).child("buddy").get().val()


    lism=[]

    name=data.child(bud).child("Handle").get().val()

    nimg=data.child(bud).child("Images").get().val()
    if nimg is not None:
       v=data.child(bud).child("Images").get()
       for img in v.each():
           userdp=img.val()
    else:
        userdp = "https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"

    

    lism.append({"idd":bud,"hn":name})

    buddylist=[]
    
    if lis :
            #v=data.child(bud).child("buddy").get().val()

            #if v:
                for n,cont in reversed(lis.items()):
                    
                    buddylist.append({"buddyval":cont,"idh":n[1:]})
                
                      
    else:
                  pass
      

    return render_template("buddylist.html",buddyl=buddylist,liso=lism,userdp=userdp)
    
    

@app.route("/addingbuddy<idb>")
def addb(idb):
    myid=request.cookies.get("user_id")
    bi=idb

    binfo=data.child(bi).child("Handle").get().val()
    minfo=data.child(myid).child("Handle").get().val()

 

    

    data.child(myid).child("buddy").push(binfo)
    
    data.child(bi).child("buddy").push(minfo)#infomy

    mail=data.child(bi).child("email").get().val()
    if mail is not None:
                 mail=data.child(bi).child("email").get()
                 for mail in mail.each():
                     mail=mail.val()
    myidinfo=data.child(myid).child("Handle").get().val()
             
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("picsta218@gmail.com", "baud wuit yaif ilzo")
    message = f"""Subject:You have got a new buddy

             {myidinfo} is your buddy now  here,https://picsta.up.railway.app/Id/{myid}"""
    s.sendmail("noreply@picstanew.firebaseapp.com", f"{mail}", message)
    s.quit()
            

    #data.child(myid).child("buddylist").push(bi)
    
    #data.child(bi).child("buddylist").push(myid)
    
    return redirect(url_for("profile",profile=bi))
    
    
@app.route("/Settings",methods=["POST","GET"])
def settings():
     
      userdp=None
      success=None
      wall=None
      
      user_id=request.cookies.get("user_id")

      now = datetime.now()
      dt = now.strftime("%a %b %d, %Y")
      dtt = now.strftime("%I:%M %p")
      time=f"Last seen on {dt} at {dtt}"

      data.child(user_id).child("active").push(time)
      nimg=data.child(user_id).child("Images").get().val()
      if nimg is not None:
          v=data.child(user_id).child("Images").get()
          for img in v.each():
                     userdp=img.val()
      else:
                         userdp = "https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"

      wallpaper=data.child(user_id).child("wallpaper").get().val()
      if wallpaper is not None:
          b=data.child(user_id).child("wallpaper").get()
          for imgc in b.each():
                     wall=imgc.val()
      else:
                         wall= "https://garden.spoonflower.com/c/13653066/p/f/l/2ew2IlKxO3d7zoMLO3NiUxf6MkJT7aeURreXyo89kPIiZJSXwkA5mAE/Solid%20nero%20grey.jpg"
            
      if request.method=="POST":
           

            
             image=request.files["filename"]
            
             try:
                  dataup=storage.child(user_id).put(image)
                  aimgdata=storage.child(user_id).get_url(dataup["downloadTokens"])

                  data.child(user_id).child("Images").push(aimgdata)
                  success="Bio,dp and wallpaper successfully updated"

                 

                 
             except Exception as e:
                 pass
             bio=request.form["bio"]
             try:

                 data.child(user_id).child("bio").push(bio)
                 success="Bio,dp and wallpaper successfully updated"
                 
             except Exception as e:
                 pass

             wallpaper=request.form["wallpaper"]


             try:
                  
                  data.child(user_id).child("wallpaper").push(wallpaper)
                  

                 
                  success="Bio,dp and wallpaper successfully updated"
             except Exception as e:
                 pass
             
                 
      return render_template("settings.html",userdp=userdp,success=success,wall=wall)
@app.route("/Settings-dp",methods=["POST","GET"])
def dp():
     userdp=None
     success=None
     
     user_id=request.cookies.get("user_id")
     nimg=data.child(user_id).child("Images").get().val()
     if nimg is not None:
          v=data.child(user_id).child("Images").get()
          for img in v.each():
                     userdp=img.val()
     else:
                         userdp = "https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"
     if request.method=="POST":
           

            
             image=request.files["filename"]
            
             try:
                  dataup=storage.child(user_id).put(image)
                  aimgdata=storage.child(user_id).get_url(dataup["downloadTokens"])

                  data.child(user_id).child("Images").push(aimgdata)
                  success="Dp successfully updated"
             except Exception as e:
                 pass
             

     return render_template("changedp.html",userdp=userdp,success=success)
@app.route("/delete-dp")
def deledp():
    idu=request.cookies.get("user_id")
    userdp="https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"
   
  
    data.child(idu).child("Images").push(userdp)

    return redirect(url_for("dp"))
    
@app.route("/Settings-bio",methods=["POST","GET"])
def bio():
      
     
      success=None
      user_id=request.cookies.get("user_id")
     
    
      if request.method=="POST":
           

            
           
             bio=request.form["bio"]
             try:

                 data.child(user_id).child("bio").push(bio)
                 success="Bio successfully updated"
                 
             except Exception as e:
                 pass

           
             
                 
      return render_template("changebio.html",success=success)



@app.route("/Settings-wallpaper",methods=["POST","GET"])
def wallpaper():
    idu=request.cookies.get("user_id")
    datasus=data.child(idu).get().val()

    ver=datasus.get("verified",True)
    

    
     
     
    if ver:
        wall=None
        success=None
        wallpaper=data.child(idu).child("wallpaper").get().val()
        if wallpaper is not None:
            b=data.child(idu).child("wallpaper").get()
            for imgc in b.each():
                wall=imgc.val()
        else:
                         wall= "https://garden.spoonflower.com/c/13653066/p/f/l/2ew2IlKxO3d7zoMLO3NiUxf6MkJT7aeURreXyo89kPIiZJSXwkA5mAE/Solid%20nero%20grey.jpg"
        if request.method=="POST":
            wallpaperurl=request.form["wallpaper"]
            try:
                  data.child(idu).child("wallpaper").push(wallpaperurl)
                  

                 
                  success="wallpaper successfully updated"
            except Exception as e:
                 pass
        return render_template("changewall.html",success=success,wall=wall)
             
        
    

    else:
        return render_template("verified.html")

@app.route("/delete-wallpaper")
def delewall():
     idu=request.cookies.get("user_id")
     wall="https://garden.spoonflower.com/c/13653066/p/f/l/2ew2IlKxO3d7zoMLO3NiUxf6MkJT7aeURreXyo89kPIiZJSXwkA5mAE/Solid%20nero%20grey.jpg"
     data.child(idu).child("wallpaper").push(wall)

     return redirect(url_for("wallpaper"))
                  

    

@app.route("/Settings-username",methods=["POST","GET"])
def username():
    idu=request.cookies.get("user_id")
    datasus=data.child(idu).get().val()

    ver=datasus.get("verified",True)
    

    
     
     
    if ver:
       
        success=None
        
        if request.method=="POST":
            name=request.form["user"]
            try:
                  data.child(idu).child("Handle").set(name)
                  

                 
                  success="username successfully updated"
            except Exception as e:
                 pass
        return render_template("username.html",success=success)
             
        
    

    else:
        return render_template("verified.html")

@app.route("/Chat",methods=["POST","GET"])
def chat():
     images=None
    
     me=request.cookies.get("user_id")

     datasus=data.child(me).get().val()

     now = datetime.now()
     dt = now.strftime("%a %b %d, %Y")
     dtt = now.strftime("%I:%M %p")
     time=f"Last seen on {dt} at {dtt}"

     data.child(me).child("active").push(time)

     sus=datasus.get("suspended",False)
     wallpaper=data.child(me).child("wallpaper").get().val()
     if wallpaper is not None:
         b=data.child(me).child("wallpaper").get()
         for imgc in b.each():
                     wall=imgc.val()
     else:
                         wall= "https://garden.spoonflower.com/c/13653066/p/f/l/2ew2IlKxO3d7zoMLO3NiUxf6MkJT7aeURreXyo89kPIiZJSXwkA5mAE/Solid%20nero%20grey.jpg"
            
          
     
     
     if sus:
         return render_template("chatsus.html")
         
        
     else:
         if request.method=="POST":
             
             chat=request.form["chat"]
             userdata = data.child(me).child('Handle').get().val()

             nimg=data.child(me).child("Images").get().val()
             if nimg is not None:
                     v=data.child(me).child("Images").get()
                     for img in v.each():
                         imgc=img.val()
                         userdp=imgc
             else:
                     userdp="https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"

                
             suspen=data.child(me).get().val()
             verified=suspen.get("verified",True)
             if verified:
                     url="https://media2.giphy.com/media/xmOMPI63SsyZyKz2Tx/giphy.gif"

             else:
                     url="https://i.redd.it/ynd3as3qqxt01.jpg"
             now = datetime.now()
             dt = now.strftime("%d / %m / %y")
             dtt = now.strftime("%I:%M %p")
             captiondata = f"{chat}"
             time=f"Shared on: {dt} at {dtt}"
             chatsofu= {"verified":url,"userid":me,"userdp":userdp,"username":userdata,"caption": captiondata,"time":time}
             data.child(me).child("chats").push(chatsofu)

         


     response = data.get("chats")
     post =response.val()
     images = []
     if post is not None:
         timestamps = []
         for postid, postcontent in post.items():
                  if isinstance(postcontent, dict):
                      postsdata = postcontent.get("chats")
                      if postsdata is not None:
                          for postin in postsdata.values():
                              timestamps.append(postin["time"])
         sorted_timestamps = sorted(timestamps, reverse=True)
         images = [] 
         for timestamp in sorted_timestamps:
                   for postid, postcontent in post.items():
                       if isinstance(postcontent, dict):
                           postsdata = postcontent.get("chats")
                           if postsdata is not None:
                               for postin in postsdata.values():
                                   if postin["time"] == timestamp:
                                       images.append({"verified":postin["verified"],"userid":postin["userid"],"userdp": postin["userdp"], "username": postin["username"], "time": postin["time"], "caption": postin["caption"] })
        

    
     return render_template("chatwith.html",images=images,wall=wall)


@app.route("/logout")
def logout():
    username=request.cookies.get("user_id")
    log=make_response(redirect(url_for("landing")))
    log.set_cookie("user_id",username,expires=0)
    return log

@app.errorhandler(500)
def error(error):
    return render_template("500.html")

@app.errorhandler(404)
def notfound(error):
             return render_template("404.html")
@app.route("/verification")
def verification():
    idu=request.cookies.get("user_id")
    suspen=data.child(idu).get().val()
    verified=suspen.get("verified",True)
    if verified:
                     return render_template("userver.html")

    else:
                    return render_template("usernv.html")
@app.route("/request-verification")
def requestv():
    idu=request.cookies.get("user_id")
    now = datetime.now()
    dt = now.strftime("%a %b %d, %Y")
    dtt = now.strftime("%I:%M %p")
    time=f"requested for verification on  {dt} at {dtt}"

    data.child(idu).child("verificationrequest").push(time)

    return render_template("successrequest.html")

@app.route("/Delete/<postid>")
def deletepost(postid):
    idu=request.cookies.get("user_id")
    delda=data.child(idu).child("posts").child(postid).remove()
   
    return redirect(url_for("id"))
    
@app.route("/Chats")
def chats():
    idu=request.cookies.get("user_id")
    now = datetime.now()
    dt = now.strftime("%a %b %d, %Y")
    dtt = now.strftime("%I:%M %p")
           
    time=f"Last seen on {dt} at {dtt}"

         

    data.child(idu).child("active").push(time)

   
   
    
    wallpaper=data.child(idu).child("wallpaper").get().val()
    if wallpaper is not None:
         b=data.child(idu).child("wallpaper").get()
         for imgc in b.each():
                     wall=imgc.val()
    else:
                         wall= "https://garden.spoonflower.com/c/13653066/p/f/l/2ew2IlKxO3d7zoMLO3NiUxf6MkJT7aeURreXyo89kPIiZJSXwkA5mAE/Solid%20nero%20grey.jpg"
            
          
    
    allu=data.get()
    resa=[]
    userdp=None
    for ush in allu.each():
        user_data=ush.val()
        if isinstance(user_data,dict):
            idu=request.cookies.get("user_id")
            k=ush.val().get("Handle")
            abc=ush.val().get("ID")
            verified=ush.val().get("verified",True)
            if verified:
                     url="https://media2.giphy.com/media/xmOMPI63SsyZyKz2Tx/giphy.gif"
            else:
                     url="https://upload.wikimedia.org/wikipedia/commons/4/48/BLANK_ICON.png"
            ni=ush.val().get("Images")
            if ni:
                 for key, value in ni.items():
                     userdp = value 
                      
            else:
                      userdp="https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"

            suspen=data.child(idu).get().val()
            verified=suspen.get("verified",True)
            if verified:
                actived=ush.val().get("active")
                if actived:
                    for key,value in actived.items():
                        da=value
                else:
                    pass
                        
            else:
                     #iu=ush.val().get("Handle")
                     da=""


        
           
           
           
            if k:
                resa.append({"handle":[k],"id":[abc],"url":[url],"dp":[userdp],"active":[da]})
    
    return render_template("chats.html",resa=resa,wall=wall)   
    
@app.route("/chatswith/<profile>",methods=["POST","GET"])
def chatswith(profile):
    nop=None
    idu=profile
    wall=None
    url=None
    
    myid=request.cookies.get("user_id")

    now = datetime.now()
    dt = now.strftime("%a %b %d, %Y")
    dtt = now.strftime("%I:%M %p")
           
    time=f"Last seen on {dt} at {dtt}"

         

    data.child(myid).child("active").push(time)

    
    
    
    idofu=data.child(idu).child("Handle").get().val()

    datasus=data.child(idu).get().val()

    sus=datasus.get("suspended",False)


    if sus:
        return render_template("useridsus.html",idofu=idofu)
    else:
        if request.method=="POST":
             
             chat=request.form["chat"]
             userdata = data.child(myid).child('Handle').get().val()

             nimg=data.child(myid).child("Images").get().val()
             if nimg is not None:
                     v=data.child(myid).child("Images").get()
                     for img in v.each():
                         imgc=img.val()
                         userdp=imgc
             else:
                     userdp="https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"

                
             suspen=data.child(myid).get().val()
             verified=suspen.get("verified",True)
             if verified:
                     url="https://media2.giphy.com/media/xmOMPI63SsyZyKz2Tx/giphy.gif"

             else:
                     url="https://i.redd.it/ynd3as3qqxt01.jpg"
             now = datetime.now()
             dt = now.strftime("%d / %m / %y")
             dtt = now.strftime("%I:%M %p")
             captiondata = f"{chat}"
             time=f"Shared on: {dt} at {dtt}"
             theirid=data.child(idu).child("ID").get().val()
             chatsofu= {"verified":url,"userid":myid,"userdp":userdp,"username":userdata,"caption": captiondata,"time":time}
             data.child(myid).child("chats").child(idu).push(chatsofu)
             data.child(idu).child("chats").child(myid).push(chatsofu)

             
             
             mail=data.child(idu).child("email").get().val()
             if mail is not None:
                 mail=data.child(idu).child("email").get()
                 for mail in mail.each():
                     mail=mail.val()
             myid=data.child(myid).child("Handle").get().val()
             
             s = smtplib.SMTP('smtp.gmail.com', 587)
             s.starttls()
             s.login("picsta218@gmail.com", "baud wuit yaif ilzo")
             message = f"""Subject:You have got new chat's

             {myid} send you a chat on picsta check it here,https://picsta.up.railway.app/chatswith/{theirid}"""
             s.sendmail("noreply@picstanew.firebaseapp.com", f"{mail}", message)
             s.quit()
            
             
                 
             return redirect(url_for("chatswith",profile=idu))

             

         
        wallpaper=data.child(idu).child("wallpaper").get().val()
        if wallpaper is not None:
          b=data.child(idu).child("wallpaper").get()
          for imgc in b.each():
                     wall=imgc.val()
        else:
                         wall= "https://garden.spoonflower.com/c/13653066/p/f/l/2ew2IlKxO3d7zoMLO3NiUxf6MkJT7aeURreXyo89kPIiZJSXwkA5mAE/Solid%20nero%20grey.jpg"

        bio=data.child(idu).child("bio").get().val()
        if bio is not None:
            bio=data.child(idu).child("bio").get()
            for bio in bio.each():
                bio=bio.val()

        bday=data.child(idu).child("birthday").get()
        for bday in bday.each():
            bday=bday.val()

        date=data.child(idu).child("date").get()
        for date in date.each():
            date=date.val()


        nimg=data.child(idu).child("Images").get().val()
        if nimg is not None:
            v=data.child(idu).child("Images").get()
            for img in v.each():
                userdp=img.val()
        else:
            userdp = "https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"

    
        response = data.child(myid).child("chats").child(idu).get()
        posta = response.val()
        images = []
        datasus=data.child(idu).get().val()
        ver=datasus.get("verified",True)

        if ver:
         url="https://media2.giphy.com/media/xmOMPI63SsyZyKz2Tx/giphy.gif"
         actived=data.child(idu).child("active").get()
         for actived in actived.each():
            da=actived.val()
         
        else:
                     url="https://upload.wikimedia.org/wikipedia/commons/4/48/BLANK_ICON.png"
                     da="To see last seen of {{idofu}} you need to be verified first"
        datasus=data.child(myid).get().val()
        vere=datasus.get("verified",True)

        if vere:
        
         actived=data.child(idu).child("active").get()
         for actived in actived.each():
            da=actived.val()
         
        else:
                     iu=data.child(idu).child("Handle").get().val()
                     da=f"To see '{iu}'s' last seen, verify first."
        if posta:
            for post_id, post_content in reversed(posta.items()):
                images.append({"os":post_content.get("os",""),"verified":post_content.get("verified",""),"userid":post_content.get("userid",""),"userdp": post_content.get("userdp", ""),"username": post_content.get("username", ""), "time": post_content.get("time", ""),"caption": post_content.get("caption", ""),"image_url": post_content.get("image_url", "")})
        else:
            nop=f"No chats with {idofu}"
   
        return render_template("chatswith.html",ido=idofu,userdp=userdp,images=images,bd=bday,d=date,nop=nop,bio=bio,wall=wall,url=url,da=da,idu=idu)
       

                 


#openai.api_key = "sk-proj-C9eQKjYDFIShWRq7CBrQT3BlbkFJv3PAbGmexR2H5PNF5Mlb"

#token = "AKEyXzVdW-88KNp4D6Ct3_6L_mks89wfkqhrJtAKC2s7CG8xorNtJDVOBBuaPbDFR_Mn9JM5IMuc"
@app.route('/chatwithjeremy', methods=['POST',"GET"])
def chatwith():
    userdata=None
    myid = request.cookies.get("user_id")
    verget = data.child(myid).get().val() 
    ver = verget.get("verified", True)
    userdata=data.child(myid).child("Handle").get().val()

    now = datetime.now()
    dt = now.strftime("%a %b %d, %Y")
    dtt = now.strftime("%I:%M %p")
           
    time=f"Last seen on {dt} at {dtt}"

         

    data.child(myid).child("active").push(time)
  
    usern=None
    
    response = data.child(myid).child("jeremy").get()

                
   

    nop=None
    if ver:
        if request.method=="POST":
           
            myid = request.cookies.get("user_id")
            msg = request.form["chat"]
            userdata=data.child(myid).child("Handle").get().val()
            now = datetime.now()
            dt = now.strftime("%d / %m / %y")
            dtt = now.strftime("%I:%M %p")
            time = f"Shared on: {dt} at {dtt}"
            userdp = "https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"

            if msg == "clear <jeremy_data>":
                data.child(myid).child("jeremy").cremove()
               
            
            else:
                 co = cohere.Client('i6yM29f29bg6eY2l9599pwjMLFEUyrWrwJyRxOMr')
                 response = co.generate(model='command-nightly',prompt=msg,max_tokens=300,temperature=0.9,k=0,p=0.75,stop_sequences=[],return_likelihoods='NONE')
                 resp= response.generations[0].text
                 userdat = "✨ Jeremy"
                 chatsofj = {"userid": myid,"userdp": userdp,"username": userdata,"caption": msg,"time": time}
                 j = {"userid": myid,"username": userdat,"caption": resp,"time": time}

                 data.child(myid).child("jeremy").push(chatsofj)
                 data.child(myid).child("jeremy").push(j)

        response = data.child(myid).child("jeremy").get()
        posta = response.val()
        chatj = []  
        if posta:
            for post_id, post_content in reversed(posta.items()):
                        chatj.append({"verified":post_content.get("verified",""),"userid":post_content.get("userid",""),"userdp": post_content.get("userdp", ""),"username": post_content.get("username", ""), "time": post_content.get("time", ""),"caption": post_content.get("caption", ""),"image_url": post_content.get("image_url", "")})
        else:
                    nop=f" "
        return render_template("jeremychat.html",chatj=chatj,nop=nop,userdata=userdata)
    else:
        usern=data.child(myid).child("Handle").get().val()
        
        
        return render_template("jeremyunvr.html",usern=usern)
#------write in id.html after {%if bio%} .... {%endif%} ------
#<div class="addpic">
#<a href="{{url_for("addpic")}}" style="color:white" ><h4 style="color:white;background:black;text-align:center;border-radius:10px;padding:10px;border:2px solid white">+ Add a snapic </a> </h4>
#</div>

@app.route("/addsnapic",methods=["POST","GET"])
def addpic():
    abc=request.cookies.get("user_id")

    sus=data.child(abc).get().val()
    susget=sus.get("suspended",True)
    suspen=None

    if susget:
        return render_template("addpicsus.html")
    else:
        if request.method=="POST":
           
             image=request.files["filename"]
             if image:
                      image_path = f"images/{image.filename}"
                      storage.child(image_path).put(image)
             else:
                      wall = "https://img.icons8.com/material-outlined/1/full-stop.png"
                      response = urllib.request.urlopen(wall)
                      image_path = f"images/image.jpg"
                      storage.child(image_path).put(response.read())
                  
            
                  

            
             userdata = data.child(abc).child('Handle').get().val()

             nimg=data.child(abc).child("Images").get().val()
             if nimg is not None:
                      v=data.child(abc).child("Images").get()
                      for img in v.each():
                         imgc=img.val()
                         userdp=imgc
             else:
                      userdp="https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"
             now = datetime.now()
             dt = now.strftime("%d / %m / %y")
             dtt = now.strftime("%I:%M %p")
            # captiondata = f"{caption}"
             time=f"Shared on: {dt} at {dtt}"
             suspen=data.child(abc).get().val()
             verified=suspen.get("verified",True)
             if verified:
                     url="https://media2.giphy.com/media/xmOMPI63SsyZyKz2Tx/giphy.gif"
             else:
                     url="https://upload.wikimedia.org/wikipedia/commons/4/48/BLANK_ICON.png"

             post_data = {"verified":url,"userid":abc,"userdp":userdp,"username":userdata, "image_url": storage.child(image_path).get_url(None),"time":time}
             data.child(abc).child("stories").push(post_data)

             return redirect(url_for("index"))

        resa=[]
        userdata = data.child(abc).child('Handle').get().val()

        nimg=data.child(abc).child("Images").get().val()
        if nimg is not None:
                      v=data.child(abc).child("Images").get()
                      for img in v.each():
                         imgc=img.val()
                         userdp=imgc
        else:
                      userdp="https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"
        wallpaper=data.child(abc).child("wallpaper").get().val()
        if wallpaper is not None:
          b=data.child(abc).child("wallpaper").get()
          for imgc in b.each():
                     wall=imgc.val()
        else:
                         wall= "https://garden.spoonflower.com/c/13653066/p/f/l/2ew2IlKxO3d7zoMLO3NiUxf6MkJT7aeURreXyo89kPIiZJSXwkA5mAE/Solid%20nero%20grey.jpg"
        suspen=data.child(abc).get().val()
        verified=suspen.get("verified",True)
        if verified:
                     url="https://media2.giphy.com/media/xmOMPI63SsyZyKz2Tx/giphy.gif"
        else:
                     url="https://upload.wikimedia.org/wikipedia/commons/4/48/BLANK_ICON.png"

        resa.append({"dp":[userdp],"handle":[userdata],"url":[url]})

        return render_template("addpic.html",wall=wall,resa=resa)

@app.route("/recoveraccountpage")
def recoverpage():
    return render_template("recover.html")

@app.route("/recoveraccount")
def recover():
    cookie=request.cookies.get("user_id")
    mail=data.child(cookie).child("email").get().val()
    if mail is not None:
                 mail=data.child(cookie).child("email").get()
                 for mail in mail.each():
                     mail=mail.val()
    auth.send_password_reset_email(mail)
    data.child(cookie).child("cookies").set(False)
    return redirect(url_for("login"))

    

#if __name__=="__main__":
    #app.run(debug=True,host="0.0.0.0",port=8000)#may change ;) using cohere for jeremy 
