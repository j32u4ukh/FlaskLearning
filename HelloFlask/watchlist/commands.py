import click

from watchlist import app, db
from watchlist.models import User, Movie

# 利用下方指令，生成資料庫以及相關表格(附帶 --drop，則先刪除原本的，再建立新的。)
# $ flask initdb
@app.cli.command()  # 注冊為命令，可以傳入 name 參數來自定義命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 設置選項
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判斷是否輸入了選項
        click.echo("Drop database.")
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 輸出提示信息

# 利用下方指令，建立用戶(第一位會是管理員)
# $ flask admin
# Username: Henry Lee
# Password: (因設置 hide_input=True，因此看不到輸入的內容)
# Repeat for confirmation: (因設置 hide_input=True，因此看不到輸入的內容)
# 使用 click.option() 裝飾器設置的兩個選項分別用來接受輸入用戶名和密碼。
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 設置密碼
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)  # 設置密碼
        db.session.add(user)

    db.session.commit()  # 提交數據庫會話
    click.echo('Done.')

# 利用下方指令，初始化資料庫數據
# $ flask forge
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的兩個變量移動到這個函數內
    # name = 'Henry Li'
    # user = User(name=name)
    # db.session.add(user)

    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')
