from user import user_blue # user 模塊


# user模塊
@user_blue.route('/register')
def register():
    return 'register'

@user_blue.route('/login')
def login():
    return 'login'

@user_blue.route('/modify_password')
def modify_password():
    return 'modify_password'