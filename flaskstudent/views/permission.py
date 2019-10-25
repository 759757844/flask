from flask import Blueprint,render_template,request,redirect
from App.models import Permission,db,Role

permission = Blueprint('permission',__name__,template_folder="../templates")

from flask import session
from utils.confirm import decorator

#权限
@permission.route('/permission/',methods=['GET','POST'])
@decorator
def permission_list():
    permissions = Permission.query.all()
    return render_template('permissions.html',permissions=permissions)

#添加权限
@permission.route('/addpermission/',methods=['GET','POST'])
@decorator
def userperlist():
    if request.method == 'GET':
        return render_template('addpermission.html')
    if request.method == 'POST':
        p_name = request.form['p_name']
        p_er = request.form['p_er']
        look_p_name = Permission.query.filter(Permission.p_name == p_name).first()
        look_p_er = Permission.query.filter(Permission.p_er == p_er).first()
        if not look_p_name:
            if not p_name == "":
                if not look_p_er:
                    if not p_er == "":
                        per_obj = Permission(p_name=p_name,p_er=p_er)
                        db.session.add_all([per_obj])
                        db.session.commit()
                        return redirect('/permission/permission/')
                    else:
                        msg1 = "权限简称名称不能为空"
                        return render_template('addpermission.html', msg1 = msg1)
                else:
                    msg1 = "该权限简称已存在"
                    return render_template('addpermission.html', msg1 = msg1)
            elif not look_p_er:
                if not p_er == "":
                    msg = "权限名称不能为空"
                    return render_template('addpermission.html', msg = msg)
                else:
                    msg = "权限名称不能为空"
                    msg1 = "权限简称名称不能为空"
                    return render_template('addpermission.html', msg = msg,msg1 = msg1)
            else:
                msg = "权限名称不能为空"
                msg1 = "该权限简称已存在"
                return render_template('addpermission.html', msg = msg, msg1 = msg1)
        elif not look_p_er:
            if not p_er  == "":
                msg = "该权限已存在"
                return render_template('addpermission.html', msg=msg)
            else:
                msg = "该权限已存在"
                msg1 = "权限简称名称不能为空"
                return render_template('addpermission.html', msg=msg,msg1=msg1)
        else:
            msg = "该权限已存在"
            msg1 = "该权限简称已存在"
            return render_template('addpermission.html', msg=msg, msg1=msg1)


#删除权限
@permission.route('/delpermission/<id>',methods=['GET','POST'])
@decorator
def delpermission(id):
    per_obj = Permission.query.filter(Permission.p_id==id).first()
    db.session.delete(per_obj)
    db.session.commit()
    return redirect('/permission/permission/')

#编辑权限
@permission.route('/editper/<id>',methods=['GET','POST'])
@decorator
def editper(id):
    permissions = Permission.query.filter(Permission.p_id==id).first()
    if request.method == 'GET':
        return render_template('edit_per.html',permissions=permissions)
    if request.method == 'POST':
        p_name = request.form['p_name']
        per_name = Permission.query.filter(Permission.p_name == p_name).first()
        if per_name:
            msg = "该权限名称已存在"
            return render_template('edit_per.html', permissions=permissions,msg=msg)
        elif p_name =="":
            msg = "该权限名称不能为空"
            return render_template('edit_per.html', permissions=permissions, msg=msg)
        else:
            permissions.p_name = p_name
            db.session.commit()
            msg = "该权限名称修改成功"
            return render_template('edit_per.html', permissions=permissions, msg=msg)
