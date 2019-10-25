from flask import Blueprint,render_template,request,redirect
from App.models import Grade,Student,Permission,User,Role
from App.models import db
from flask import session
from utils.confirm import decorator

user = Blueprint('user',__name__,template_folder="../templates")

#登录页面
@user.route('/login',methods=['GET','POST'])
def Login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_obj = User.query.filter(User.username==username,User.password==password).first()
        if user_obj:
            session['user'] = username
            return redirect('/user/index')
        else:
            return render_template('login.html')

#注销
@user.route('/logout/',methods=['GET','POST'])
@decorator
def test():
    user = session.get('user')
    if user:
        session.pop('user')
        return redirect('/user/login')
    else:
        return '错误'

#注册
@user.route('/register',methods=['GET','POST'])
def Register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        pwd1 = request.form['pwd1']
        pwd2 = request.form['pwd2']
        user_obj = User.query.filter(User.username == username).first()
        if user_obj:
            return render_template('register.html')
        elif pwd1 == pwd2:
            new_user = User(username=username,password=pwd1)
            db.session.add_all([new_user])
            db.session.commit()
            return redirect('/user/login')
        else:
            return render_template('register.html')

#主页
@user.route('/index')
@decorator
def Index():
    return render_template('index.html')

#页头
@user.route('/head/',methods=['GET','POST'])
@decorator
def Head():
    if request.method == 'GET':
        user = session.get('user')
        return render_template('head.html',user=user)

#页左
@user.route('/left/',methods=['GET','POST'])
@decorator
def Left():
    if request.method == 'GET':
        user = session.get('user')
        permissions = User.query.filter(User.username == user).first().role.permission
        return render_template('left.html',permissions=permissions)

#页身
@user.route('/grade/',methods=['GET','POST'])
@decorator
def Grades():
    page = int(request.args.get('page',1))
    per_page = 5
    paginate = Grade.query.paginate(page,per_page,error_out=False)
    grades = Grade.query.all()
    return render_template('grade.html',paginate=paginate,grades=grades)

#用户列表
@user.route('/userlist/',methods=['GET','POST'])
@decorator
def Userlist():
    page = int(request.args.get('page', 1))
    per_page = 5
    paginate = User.query.paginate(page, per_page, error_out=False)
    users = User.query.all()
    return render_template('users.html',paginate=paginate,users=users)

#添加用户
@user.route('/adduser/',methods=['GET','POST'])
@decorator
def adduser():
    if request.method == 'GET':
        return render_template('adduser.html')
    if request.method == 'POST':
        user_name = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        old_user = User.query.filter(User.username==user_name).first()
        if old_user:
            msg = "该用户已存在"
            return render_template('adduser.html',msg=msg)
        elif user_name == "":
            msg = "用户名不能为空"
            return render_template('adduser.html', msg=msg)
        elif password1 == password2 and (password1 != "" or password2 != ""):
            new_user = User(username=user_name, password=password1)
            db.session.add_all([new_user])
            db.session.commit()
            msg = "用户创建成功"
            return render_template('adduser.html', msg=msg)
        elif password1 == "" or password2 == "":
            msg = "密码不能为空"
            return render_template('adduser.html', msg=msg)
        else:
            msg = "两次密码输入不一致"
            return render_template('adduser.html', msg=msg)



#修改密码
@user.route('/changepwd/',methods=['GET','POST'])
@decorator
def changepwd():
    username = session.get('user')
    user = User.query.filter(User.username == username).first()
    if request.method =="GET":
        return render_template('changepwd.html',user=user)
    if request.method =="POST":
        old_pwd = request.form['pwd1']
        pwd2 = request.form['pwd2']
        pwd3 = request.form['pwd3']
        print(old_pwd)
        print(user.password)
        if old_pwd == user.password and old_pwd != pwd2:
            if pwd2 == "" or pwd3 =="":
                msg = "密码不能为空"
                return render_template('changepwd.html',msg=msg,user=user)
            elif pwd2 == pwd3:
                user.password = pwd2
                db.session.commit()
                msg = "密码修改成功"
                return render_template('changepwd.html',msg=msg,user=user)
            else:
                msg = "两次密码不一致"
                return render_template('changepwd.html',msg=msg,user=user)
        elif old_pwd == pwd2:
            msg = "密码不能与原先一致"
            return render_template('changepwd.html', msg=msg, user=user)
        else:
            msg = "旧密码不正确"
            return render_template('changepwd.html',msg=msg,user=user)

#分配用户角色
@user.route('/assign/<id>',methods=['GET','POST'])
@decorator
def assign(id):
    user = User.query.filter(User.u_id == id).first()
    if request.method == 'GET':
        roles = Role.query.all()
        return render_template('assign_user_role.html',roles=roles)
    if request.method == 'POST':
        r_id = request.form['r_id']
        user.role_id = r_id
        db.session.commit()
        return redirect('/user/userlist/')

#删除用户
@user.route('/deluser/<id>',methods=['GET','POST'])
@decorator
def deluser(id):
        User.query.filter(User.u_id==id).delete()
        db.session.commit()
        return redirect('/user/userlist/')