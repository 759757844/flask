from flask import Blueprint,render_template,request,redirect
from App.models import Role,db,Permission,r_p

role = Blueprint('role',__name__,template_folder="../templates")

from flask import session
from utils.confirm import decorator

#角色列表
@role.route('/role/',methods=['GET','POST'])
@decorator
def role_list():
    roles = Role.query.order_by(Role.r_id).all()
    return render_template('roles.html',roles=roles)

#添加角色
@role.route('/addroles/',methods=['GET','POST'])
@decorator
def addroles():
    if request.method == 'GET':
        return render_template('addroles.html')
    if request.method == 'POST':
        r_name = request.form['r_name']
        old_role = Role.query.filter(Role.r_name == r_name).first()
        if old_role:
            msg = "该角色已存在"
            return render_template('addroles.html', msg=msg)
        elif r_name == "":
            msg = "角色名称不能为空"
            return render_template('addroles.html', msg=msg)
        else:
            new_role = Role(r_name=r_name)
            db.session.add_all([new_role])
            db.session.commit()
            return redirect('/role/role/')

#用户添加权限
@role.route('/addper/<id>',methods=['GET','POST'])
@decorator
def addper(id):
    permissions = Permission.query.all()
    if request.method =='GET':
        return render_template('role_addper.html',permissions=permissions)
    if request.method == 'POST':
        role_obj = Role.query.filter(Role.r_id==id).first()
        p_id = request.form['p_id']
        per_obj = Permission.query.filter(Permission.p_id==p_id).first()
        per_obj.roles.append(role_obj)
        db.session.commit()
        return redirect('/role/role/')


#查看权限并删除
@role.route('/userperlist/<id>',methods=['GET','POST'])
@decorator
def userperlist(id):
    if request.method == 'GET':
        role_id = Role.query.filter(Role.r_id==id).first()
        pers = role_id.permission
        return render_template('user_per_list.html',pers=pers)
    if request.method == 'POST':
        p_id = request.form['p_id']
        role_obj = Role.query.filter(Role.r_id == id).first()
        per_obj = Permission.query.filter(Permission.p_id == p_id).first()
        per_obj.roles.remove(role_obj)
        db.session.commit()
        return redirect('#')