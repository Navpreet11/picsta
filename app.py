from flask import*
import pyrebase
from datetime import datetime
from datetime import datetime,timedelta

firebaseConfig = {
  "apiKey": "AIzaSyB-JHJrL3p6V-MlsitkgoWnN4HZ4eQuCHs",
  "authDomain": "picsta-9b3d0.firebaseapp.com",
  "databaseURL":"https://picsta-9b3d0-default-rtdb.firebaseio.com/",
  "projectId": "picsta-9b3d0",
  "storageBucket": "picsta-9b3d0.appspot.com",
  "messagingSenderId": "908730701999",
  "appId": "1:908730701999:web:aeb59ed18e7dd68e8a1c5a",
  "measurementId": "G-TVQM8LZC49"
}

firebase= pyrebase.initialize_app(firebaseConfig)

auth=firebase.auth()

data=firebase.database()
storage=firebase.storage()

app=Flask(__name__)


app.secret_key = "123abc"

@app.route('/')
def landing():
    user_token = request.cookies.get("user_id")
    if user_token:
        return redirect(url_for("index"))
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
                return response
               
                #return redirect(url_for("index"))
                

            except:
                error="Invalid email or password"
                

                
                
     
            
    
    return render_template("login.html",error=error)
@app.route("/Home",methods=["POST","GET"])
def index():
          idu=request.cookies.get("user_id")
          datasus=data.child(idu).get().val()
          sus=datasus.get("suspended",False)
          wallpaper=data.child(idu).child("wallpaper").get().val()
          if wallpaper is not None:
              b=data.child(idu).child("wallpaper").get()
              for imgc in b.each():
                     wall=imgc.val()
          else:
                         wall= "https://garden.spoonflower.com/c/13653066/p/f/l/2ew2IlKxO3d7zoMLO3NiUxf6MkJT7aeURreXyo89kPIiZJSXwkA5mAE/Solid%20nero%20grey.jpg"
            
          
    

          if sus:
              return render_template("uploadsus.html")
          else:
              user_id=request.cookies.get("user_id")
              error=None
              success=None
              userdp=None

              if request.method=="POST":
                  caption=request.form["caption"]
                  image=request.files["filename"]
            
                  image_path = f"images/{image.filename}"
                  storage.child(image_path).put(image)

            
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
                     url="https://i.redd.it/ynd3as3qqxt01.jpg"
                  post_data = {"verified":url,"userid":user_id,"userdp":userdp,"username":userdata,"caption": captiondata, "image_url": storage.child(image_path).get_url(None),"time":time}
                  data.child(user_id).child("posts").push(post_data)
                  success="Pic shared successfully!"
                  
              

                 
           
         


       
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
                                       images.append({"verified":postin["verified"],"userid":postin["userid"],"userdp": postin["userdp"], "username": postin["username"], "time": postin["time"], "caption": postin["caption"],"image_url": postin["image_url"] })
        

        
       
          return  render_template("index.html",images=images,success=success,wall=wall)
@app.route("/Search")
def search():
    idu=request.cookies.get("user_id")
   
    
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
            k=ush.val().get("Handle")
            abc=ush.val().get("ID")
            verified=ush.val().get("verified",True)
            if verified:
                     url="https://media2.giphy.com/media/xmOMPI63SsyZyKz2Tx/giphy.gif"
            else:
                     url="https://img.icons8.com/wired/00/000000/sphere.png"
            ni=ush.val().get("Images")
            if ni:
                 for key, value in ni.items():
                     userdp = value 
                      
            else:
                      userdp="https://img.icons8.com/material-sharp/500/228BE6/user-male-circle.png"

        
           
           
           
            if k:
                resa.append({"handle":[k],"id":[abc],"url":[url],"dp":[userdp]})
    
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
         error=None
         success=None
         userdp=None
         if request.method=="POST":
             caption=request.form["caption"]
             image=request.files["filename"]
             try:
                 image_path = f"images/{image.filename}"
                 storage.child(image_path).put(image)

            
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
                     url="https://i.redd.it/ynd3as3qqxt01.jpg"
                 
                 post_data = {"verified":url,"userid":user_id,"userdp":userdp,"username":userdata,"caption": captiondata, "image_url": storage.child(image_path).get_url(None),"time":time}
                 data.child(user_id).child("posts").push(post_data)
                 success="Pic shared successfully!"

                 
             except Exception as e :
                  error=e
         
         return render_template("upload.html",error=error,success=success)


@app.route("/Id")
def id():

    nop=None
    wall=None
    url=None
    idu=request.cookies.get("user_id")
    
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
                     url="https://img.icons8.com/wired/00/000000/sphere.png"

    if posta:
        for post_id, post_content in reversed(posta.items()):
            images.append({"verified":post_content.get("verified",""),"userid":post_content.get("userid",""),"userdp": post_content.get("userdp", ""),"username": post_content.get("username", ""), "time": post_content.get("time", ""),"caption": post_content.get("caption", ""),"image_url": post_content.get("image_url", "")})

    else:
        nop="No pic's yet"

   

    
         
        
    return render_template("id.html",ido=idofu,userdp=userdp,images=images,bd=bday,d=date,nop=nop,bio=bio,wall=wall,url=url)
    
   
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
        else:
                     url="https://img.icons8.com/wired/00/000000/sphere.png"
        if posta:
            for post_id, post_content in reversed(posta.items()):
                images.append({"verified":post_content.get("verified",""),"userid":post_content.get("userid",""),"userdp": post_content.get("userdp", ""),"username": post_content.get("username", ""), "time": post_content.get("time", ""),"caption": post_content.get("caption", ""),"image_url": post_content.get("image_url", "")})
        else:
            nop="No pic's yet"
   
        return render_template("userid.html",ido=idofu,userdp=userdp,images=images,bd=bday,d=date,nop=nop,bio=bio,wall=wall,url=url)
    
@app.route("/Settings",methods=["POST","GET"])
def settings():
     
      userdp=None
      success=None
      wall=None
      user_id=request.cookies.get("user_id")
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
if __name__=="__main__":
    app.run(debug=True,port=8000,host="0.0.0.0")
