from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys
import math
from flask import jsonify

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()

@application.route("/") #첫화면
def hello():
     #return render_template("index.html")
    return redirect(url_for('view_home'))

@application.route("/home") #home으로
def view_home():
    page = request.args.get("page", 0, type=int)
    sort_by = request.args.get("sort", None)
    per_page=6
    per_row=3
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    
    data = DB.get_items()
    
    if sort_by == "price":
        data = {k: v for k, v in sorted(data.items(), key=lambda item: float(item[1]['price']))}
        
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)

    for i in range(row_count):
        if (i == row_count-1) and (tot_count%per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
            
    
    return render_template(
        "2_home.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts
    )


@application.route("/product_upload") #이거다
def product_upload():
    return render_template("1_product_upload.html")

@application.route("/home")
def home():
    return render_template("2_home.html")

@application.route("/product_detail/<name>/")
def view_item_detail(name):
    print("###name:",name)
    data = DB.get_item_byname(str(name))
    print("####data:",data)
    return render_template("3_product_detail.html", name=name, data=data)


@application.route("/product_detail", methods=['POST'])
def product_detail():
    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form
    DB.insert_item(data['name'], data, image_file.filename)

    return render_template("3_product_detail.html", data=data, img_path=
"static/images/{}".format(image_file.filename))
    # return render_template("3_product_detail.html")


@application.route("/seller_info")
def seller_info():
    return render_template("11_seller_information.html")

@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form
    DB.insert_item(data['name'], data, image_file.filename)

    view_item_detail(data['name'])
#     return render_template("submit_item_result.html", data=data, img_path=
# "static/images/{}".format(image_file.filename))

@application.route("/submit_item")
def reg_item_submit():
    name = request.args.get("name")
    title = request.args.get("title")
    price = request.args.get("price")
    productstatus = request.args.get("productstatus")
    deliverprice = request.args.get("deliverprice")
    category = request.args.get("category")
    placebox = request.args.get("placebox")
    place = request.args.get("place")
    info = request.args.get("info")
    sellerid = request.args.get("sellerid")


    
    
@application.route("/login")
def login():
    return render_template("7_1_log_in.html")

@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_, pw_hash):
        session['id']=id_
        return redirect(url_for('hello'))
    else:
        flash("아이디 또는 비밀번호가 잘못되었습니다.")
        return render_template("7_1_log_in.html")

@application.route("/sign_up")
def signup():
    return render_template("8_sign_up.html")


@application.route("/signup_post", methods=['POST'])
def register_user():
    data = request.form
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        flash("회원가입이 완료되었습니다.")
        return render_template("7_1_log_in.html")
    else:
        flash("아이디가 이미 존재합니다!")
        return render_template("8_sign_up.html")

    #print(name,addr,phone,category,status)
    #return render_template("reg_item.html")

    #print(name,addr,phone,category,status)
    #return render_template("reg_item.html")
    
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('hello'))

# @application.route("/view_detail/<name>/")
# def view_item_detail(name):
#     print("###name:",name)
#     data = DB.get_item_byname(str(name))
#     print("####data:",data)
#     return render_template("detail.html", name=name, data=data)
@application.route("/mypage")
def mypage():
    page = request.args.get("page", 0, type=int)
    per_page=4
    per_row=2
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    
    data = DB.get_items()
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)


    for i in range(row_count):
        if (i == row_count-1) and (tot_count%per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
            
    
    return render_template(
        "9_3_mypage.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts
    )
    #return render_template("9_3_mypage.html")

@application.route("/wishlist")
def wishlist():
    page = request.args.get("page", 0, type=int)
    per_page=6
    per_row=3
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    
    data = DB.get_items()
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)

    for i in range(row_count):
        if (i == row_count-1) and (tot_count%per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
            
    
    return render_template(
        "9_1_wishlist.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts
    )

@application.route("/shopping_cart")
def shoppingcart():
    page = request.args.get("page", 1, type=int)
    per_page=3
    per_row=1
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    
    data = DB.get_items()
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)

    for i in range(row_count):
        if (i == row_count-1) and (tot_count%per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
            
    
    return render_template(
        "9_2_shopping_cart.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts
    )
    #return render_template("9_2_shopping_cart.html")

# @application.route("/review")
# def view_review():
#     return render_template("review.html")

@application.route("/search")
def search():
    query = request.args.get("query")
    all_items = DB.get_items()
    
    # Filter items based on item name or seller's ID
    filtered_items = {name: details for name, details in all_items.items() 
                      if query.lower() in name.lower() or query.lower() in details.get('seller', '').lower()}
    
    return render_template("search_result.html", items=filtered_items)

@application.route("/review_upload")
def review_upload():
    return render_template("4_review_upload.html")

# @application.route("/review_all")
# def review_all():
#     return render_template("5_review_all.html")

@application.route("/review_detail")
def review_detail():
    return render_template("6_review_detail.html")

@application.route("/reg_review", methods=['POST'])
def reg_review():
    if 'id' not in session:
        return redirect(url_for('login'))
    data = request.form
    image_file = request.files["file"]
    img_path = "static/images/{}".format(image_file.filename)
    image_file.save(img_path)
    DB.reg_review(data, image_file.filename)
    return redirect(url_for('view_review'))

@application.route("/reg_review_init/<name>/<seller>")
def reg_review_init(name, seller):
    if 'id' not in session:
        return redirect(url_for('login'))
    return render_template("4_review_upload.html", name=name, seller=seller)

@application.route("/review")
def view_review():
    if 'id' not in session:
        return redirect(url_for('login'))
    
    page = request.args.get("page", 0, type = int)
    per_page = 3
    per_row = 1
    row_count = int(per_page/per_row)
    start_idx = per_page*page
    end_idx = per_page*(page+1)
    
    data = DB.get_reviews()
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    
    for i in range(row_count):
        if(i==row_count-1) and (tot_count%per_row!=0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else: 
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
    return render_template(
        "5_review_all.html",
        datas = data.items(),
        row1 = locals()['data_0'].items(),
        row2 = locals()['data_1'].items(),
        row3 = locals()['data_2'].items(),
        limit = per_page,
        page = page,
        page_count = int(item_counts/per_page+1),
        total = item_counts
    )

@application.route("/view_review_detail/<name>/")
def view_review_detail(name):
    if 'id' not in session:
        return redirect(url_for('login'))
    
    review_data = DB.get_review_byname(name)
    if review_data:
        return render_template("6_review_detail.html", data=review_data)
    else:
        return redirect(url_for('view_review'))
    
    
    
    
@application.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
    my_heart = DB.get_heart_byname(session['id'],name)
    return jsonify({'my_heart': my_heart})

@application.route('/like/<name>/', methods=['POST'])
def like(name):
    my_heart = DB.update_heart(session['id'],'Y',name)
    return jsonify({'msg': '좋아요 완료!'})

@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    my_heart = DB.update_heart(session['id'],'N',name)
    return jsonify({'msg': '안좋아요 완료!'})
    
    
if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)

    

''