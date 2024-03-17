from emp_app import emp_app,db

if __name__=='__main__':
    with emp_app.app_context():
        db.create_all()
    emp_app.run(debug=True) 