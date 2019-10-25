from flask import Blueprint,render_template,request,redirect
from App.models import Student,db,Grade

student = Blueprint('student',__name__,template_folder="../templates")

from flask import session

from utils.confirm import decorator
#学生列表
@student.route('/student/',methods=['GET','POST'])
@decorator
def student_list():
    page = int(request.args.get('page', 1))
    per_page = 5
    paginate = Student.query.paginate(page, per_page, error_out=False)
    stus = Student.query.all()
    return render_template('student.html', paginate=paginate, stus=stus)

#添加学生
@student.route('/addstu/',methods=['GET','POST'])
@decorator
def addstu():
    if request.method == 'GET':
        grades = Grade.query.all()
        return render_template('addstu.html',grades=grades)
    if request.method == 'POST':
        s_name = request.form['s_name']
        s_sex = request.form['s_sex']
        grade_id = request.form['g_name']
        stu = Student.query.filter(Student.s_name == s_name).first()
        if stu:
            msg = "该学生已存在"
            return render_template('addstu.html', msg=msg)
        elif s_name == "":
            msg = "学生姓名不能为空"
            return render_template('addstu.html', msg=msg)
        else:
            new_stu = Student(s_name=s_name,s_sex=s_sex,grade_id=grade_id)
            db.session.add_all([new_stu])
            db.session.commit()
            return redirect('/student/student')


#删除学生
@student.route('/del_stu/<id>',methods=['GET','POST'])
@decorator
def del_stu(id):
    grades = Student.query.filter(Student.s_id == id).delete()
    db.session.commit()
    return redirect('/student/student/')