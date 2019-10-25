from flask import Blueprint,render_template,request,redirect
from App.models import db,Grade,Student

grade = Blueprint('grade',__name__,template_folder="../templates")
from utils.confirm import decorator

#添加班级
@grade.route('/addgrade/',methods=['GET','POST'])
@decorator
def addgrade():
    if request.method == 'GET':
        return render_template('addgrade.html')
    if request.method == 'POST':
        g_name = request.form['g_name']
        grade_obj = Student.query.filter(Grade.g_name == g_name).first()
        if grade_obj:
            msg = "该班级已存在"
            return render_template('addgrade.html', msg=msg)
        elif g_name == "":
            msg = "班级名称不能为空"
            return render_template('addgrade.html', msg=msg)
        else:
            new_grade = Grade(g_name=g_name)
            db.session.add_all([new_grade])
            db.session.commit()
            return redirect('/user/grade/')

#编辑班级
@grade.route('/edit_grade/<id>',methods=['GET','POST'])
@decorator
def edit_grade(id):
    grades = Grade.query.filter(Grade.g_id == id).first()
    if request.method == "GET":
        return render_template('edit_grade.html',grades = grades)
    if request.method == "POST":
        # g_id = request.form['g_id']
        g_name = request.form['g_name']
        g_create_time = request.form['g_create_time']
        # grades.g_id = g_id
        grades.g_name = g_name
        grades.g_create_time = g_create_time
        db.session.commit()
        return redirect('/user/grade/')

#删除班级
@grade.route('/del_grade/<id>',methods=['GET','POST'])
@decorator
def del_grade(id):
    stu = Student.query.filter(Student.grade_id==id).delete()
    db.session.commit()
    grades = Grade.query.filter(Grade.g_id == id).delete()
    db.session.commit()
    return redirect('/user/grade/')

#查看学生
@grade.route('/look_stu/<id>',methods=['GET','POST'])
@decorator
def look_stu(id):
    grades = Grade.query.filter(Grade.g_id == id).first()
    print(grades.g_name)
    look_studuent = Student.query.filter(Student.grade_id==id).all()
    return render_template('look_stu.html',look_studuent=look_studuent,grades=grades)
