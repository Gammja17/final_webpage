import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

            firebase = pyrebase.initialize_app(config)
            self.db = firebase.database()

    def insert_item(self, name, data, img_path):
        try:
            price = float(data['price'])
        except ValueError:
            print("Invalid price for item:", name)
            return False
        
        item_info = {
            "img_path": img_path,
            "name": data['name'],
            "title": data['title'],
            "price": price,
            "productstatus": data['productstatus'],
            "category": data['category'],
            "place": data['place'],
            "info": data['info'],
            "sellerid": data['sellerid'],
            "link": data['link']
            
        }
        self.db.child("item").child(name).set(item_info)
        print(data, img_path)
        return True

    def insert_user(self, data, pw):
        user_info = {
            "id": data['id'],
            "pw": pw,
            "name": data['name'],
            "email": data['email'],
            "tel": data['tel'],
            "addr": data['addr']
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False

    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()

        print("users###", users.val())
        if str(users.val()) == "None": # first registration
            return True
        else:
            for res in users.each():
                value = res.val()

                if value['id'] == id_string:
                    return False
            return True
        
    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        for res in users.each():
            value = res.val()
            
            if value['id'] == id_ and value['pw'] == pw_:
                return True
        return False 
    
    def get_items(self):
        items = self.db.child("item").get().val()
        return items
    
    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value=""
        print("###########",name)
        for res in items.each():
            key_value = res.key()
            if key_value == name:
                target_value=res.val()
        return target_value
    
    def reg_review(self, data, img_path):
        review_info ={
            "rate": data['reviewStar'],
            "reviewer": data['reviewer'],
            "title": data['title'],
            "review": data['reviewContents'],
            "name": data['name'],
            "seller": data['seller'],
            "img_path": img_path
        }
        self.db.child("review").child(data['name']).set(review_info)
        return True
    
    def get_review_byname(self,name):
        reviews = self.db.child("review").get().val()
        for key, value in reviews.items():
            if key == name:
                return value

    def get_reviews(self):
        reviews = self.db.child("review").get().val()
        return reviews
    
    def get_heart_byname(self,uid,name):
        hearts = self.db.child("heart").child(uid).get()
        target_value=""
        if hearts.val() == None:
            return target_value
        for res in hearts.each():
            key_value = res.key()
            
            if key_value == name:
                target_value=res.val()
        return target_value
    
    def update_heart(self,user_id,isHeart,item):
        heart_info={
            "interested":isHeart
        }
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        return True