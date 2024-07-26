import flet as ft
import sqlite3
import requests
import asyncio

class Message:
    def __init__(self, user: str, text: str, message_type: str):
        self.user = user
        self.text = text
        self.message_type = message_type

def main(page: ft.Page):
    page.title = "UsersFace"
    page.theme_mode = "Dark" # Light
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    uers_lists = ft.ListView(spacing=10, padding=20)
    user_data = ft.TextField(label='You\'r city', width=400)
    weatherr_data = ft.Text('')
    page.scroll = 'adaptive'
    score = ft.Text(value='0', size=100, data = 0, weight=ft.FontWeight.W_900)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    chat = ft.Column()
    new_message = ft.TextField()
# function
    def on_message(message: Message):
        if message.message_type == "chat_message":
            chat.controls.append(ft.Text(f"{message.user}: {message.text}"))
        elif message.message_type == "login_message":
            chat.controls.append(
                ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
            )
        page.update()

    page.pubsub.subscribe(on_message)

    def send_click(e):
        page.pubsub.send_all(
            Message(
                user=page.session.get("user_name"),
                text=new_message.value,
                message_type="chat_message",
            )
        )
        new_message.value = ""
        page.update()

    user_name = ft.TextField(label="Enter your name")

    def join_click(e):
        if not user_name.value:
            user_name.error_text = "Name cannot be blank!"
            user_name.update()
        else:
            page.session.set("user_name", user_name.value)
            page.dialog.open = False
            page.pubsub.send_all(
                Message(
                    user=user_name.value,
                    text=f"{user_name.value} has joined the chat.",
                    message_type="login_message",
                )
            )
            page.update()

    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([user_name], tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=join_click)],
        actions_alignment="end",
    )
    score_counter = ft.Text(
        size=50, animate_opacity=ft.Animation(duration=600, curve=ft.AnimationCurve.BOUNCE_IN)
        )
    image = ft.Image(
        src='https://cdn-icons-png.flaticon.com/512/590/590685.png',
        fit=ft.ImageFit.CONTAIN,
        animate_scale=ft.Animation(duration=600, curve=ft.AnimationCurve.EASE)
    )
    progress_bar = ft.ProgressBar(
        value=0,
        width=page.width - 100,
        bar_height=20,
        color='#ff002b',
        bgcolor='#ff4262')
    async def score_up(event: ft.ContainerTapEvent) -> None:
        score.data += 1
        score.value = str(score.data)
        
        image.scale = 0.80
        
        score_counter.opacity = 1
        score_counter.value = "💡"
        score_counter.color = '#ffb647'
        
        progress_bar.value += (1 / 100)
        
        if score.data % 100 == 0:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                value="Good.... +100 🍓 - Strawberrys 🏆",
                size=20,
                color='#fafafa',
                text_align=ft.TextAlign.CENTER
            ),
            bgcolor='#25223a'
            )
            page.snack_bar.open = True
            progress_bar.value = 0
        
        page.update()
        
        await asyncio.sleep(0.1)
        image.scale = 1
        score_counter.opacity = 0
        page.update()
    score = ft.Text(value='0', size=100, data = 0, weight=ft.FontWeight.W_900)
    score_counter = ft.Text(
        size=50, animate_opacity=ft.Animation(duration=600, curve=ft.AnimationCurve.BOUNCE_IN)
        )
    image = ft.Image(
        src='https://cdn-icons-png.flaticon.com/512/590/590685.png',
        fit=ft.ImageFit.CONTAIN,
        animate_scale=ft.Animation(duration=600, curve=ft.AnimationCurve.EASE)
    )
    progress_bar = ft.ProgressBar(
        value=0,
        width=page.width - 100,
        bar_height=20,
        color='#ff002b',
        bgcolor='#ff4262'
    )
    def register(e):
        db = sqlite3.connect('it.saves1')
        
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            surname TEXT,
            comment TEXT,
            class TEXT,
            years TEXT,
            school TEXT,
            skills TEXT
            
        )""")
        cur.execute(f"INSERT INTO users VALUES(NULL, '{user_login.value}', '{user_password.value}', '{user_comment.value}', '{user_class.value}', '{user_years.value}', '{user_school.value}', '{user_skills.value}')")
        user_button.text = 'You Joind'
        user_button2.text = 'Authorize\'d'
        db.commit()
        db.close()
        page.update()
        page.update()

    def vlitdate(e):
        if all([user_login, user_password]):
            user_button.disabled = False
            user_button2.disabled = False
        else:
            user_button.disabled = True
            user_button2.disabled = True
            
        page.update()
    def get_info(e):
        
        if len(user_data.value) < 2:
            return
        API = '7b976759cbc422ea6bf11ccbb84927b0'
        URL = f'https://api.openweathermap.org/data/2.5/weather?q={user_data.value}&appid={API}&units=metric'
        res = requests.get(URL).json()
        temp = res['main']['temp']
        weatherr_data.value = 'Weather in ' + str(user_data.value) + ' is : ' + str(temp) + '\'c'
        page.update()       
    def change_theme(e):
        page.theme_mode = 'Dark' if page.theme_mode == 'Light' else 'Light'
        page.update()

    def auth_user(e):
        db = sqlite3.connect('it.saves1')
        
        cur = db.cursor()
        # Baza danix
        cur.execute(f"SELECT * FROM users WHERE name = '{user_login.value}'AND surname = '{user_password.value}'")
        if cur.fetchone() != None:
            user_login.value = ''
            user_password.value = ''
            user_comment.value = ''
            user_class.value = ''
            user_skills.value = ''
            user_years.value = ''
            user_school.value = ''
            user_button.text = 'Join'
            user_button2.text = 'Added'
        
            db.commit()
            db.close()
            page.update()
            if len(page.navigation_bar.destinations) == 6:
                page.navigation_bar.destinations.append(ft.NavigationDestination(
                    icon = ft.icons.APP_REGISTRATION,
                    label="Users",
                    selected_icon=ft.icons.PEOPLE_ALT_SHARP),)
                if len(page.navigation_bar.destinations) == 7:
                    page.snack_bar = ft.SnackBar(ft.Text("Good.... You register ser  :)", color='black'), bgcolor='#63ff38')
                    page.snack_bar.open = True
                    page.update()
                        
            
            
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Incorrectly entered data !",color='white'), bgcolor='#ff2b2b')
            page.snack_bar.open = True
            page.update()
            
            db.commit()
            db.close()
            user_login.value = ''
            user_password.value = ''
            user_comment.value = ''
            user_skills.value = ''
            user_class.value = ''
            user_years.value = ''
            user_school.value = ''
            user_button.text = 'Join'
            user_button2.text = 'Added'
            page.update()
    # variables
    user_login = ft.TextField(label='Name', width=210, on_change=vlitdate, icon=ft.icons.SUPERVISED_USER_CIRCLE_SHARP)
    user_password = ft.TextField(label='Surname', width=210, on_change=vlitdate, icon=ft.icons.SUPERVISED_USER_CIRCLE_SHARP)
    user_comment = ft.TextField(label='You\'r post\'s', width=300, on_change=vlitdate, multiline=True, icon=ft.icons.SEND_AND_ARCHIVE)
    user_skills = ft.TextField(label='Skills', width=300, on_change=vlitdate, icon=ft.icons.POWER)
    user_years = ft.TextField(label='Years', width=210, on_change=vlitdate, icon=ft.icons.VIEW_DAY)
    user_button = ft.ElevatedButton(text="Join", width=210, on_click=register, icon=ft.icons.SAVE_ALT, icon_color='#ad73ff',)
    user_button2 = ft.ElevatedButton(text="Avtorist", width=210, on_click=auth_user, icon=ft.icons.BUILD_CIRCLE, icon_color='#73c9ff')
    user_send = ft.ElevatedButton(text="Send post", width=210, on_click=auth_user, icon=ft.icons.SEND_ROUNDED, icon_color='#1aff00')
    user_class = ft.TextField(label='Class and letter', width=210, on_change=vlitdate, icon=ft.icons.CLASS_OUTLINED)
    user_school = ft.TextField(label='School', width=210, on_change=vlitdate,  icon=ft.icons.SCHOOL_SHARP)
    pannel_new2 = ft.Row([ chat, ft.Row([new_message, ft.ElevatedButton("Send", on_click=send_click)])])
            
    
    pannel_send = ft.Column(
            [
                ft.Text('Every  blog\'s', color='#00ffd5', weight=ft.FontWeight.W_900, size=30),
                uers_lists
            ], alignment=ft.MainAxisAlignment.CENTER
    )
    pannel_aught = ft.Row(
            [
                ft.Column(
                [
                    ft.Text("Register yourself"),
                    ft.Image(src='https://cdn-icons-png.flaticon.com/128/9187/9187466.png', width=80),
                    user_login,
                    user_password,
                    user_school,
                    user_class,
                    user_years,
                    user_skills,
                    user_comment,
                    user_button,
                    user_button2,
                    user_send,
                    ft.IconButton(ft.icons.SUNNY, on_click=change_theme, icon_color='yellow'),
                    ft.Text('Push to cange theme'),
    ]
                )
            ] ,
            alignment=ft.MainAxisAlignment.CENTER
        )
    pannel_cabinet =ft.Column(
                [
                    ft.Text("Every avtorisation"),
                    uers_lists,
                ], alignment=ft.MainAxisAlignment.CENTER
                )
    pannel_clicker =ft.Column(
        [
            score,
        ft.Container(
            content=ft.Stack(controls=[image, score_counter]),
            on_click=score_up,
            margin=ft.Margin(0, 0, 0, 30)     
            ),
    ft.Container(
        content=progress_bar,
        border_radius=ft.BorderRadius(10, 10, 10, 10)
    )
        ])
    pannel_me = ft.Column(
        [
            ft.Container(
                    content=ft.Text(""""About me \nI m Faridun.I m 14 years old.I m study in lip(liceum presidantal).This school for only smart's people.But i can stop thinking how i m study in this school.
                                    Okey.I m programmer - How i beecome a programmer ?
                                    I m watch film about facebook and after watching i think about programming.And than i download python and strt to study.I m like 5 month to study it.I m self-taught 
                                    I don't now why but i don't like to study programming in a school or something like there.I make this programm like in 4 or 5 day's.\nDay 1 - I got the idea\nDay 2 - I start to make my project.(And the problams started to.)\nday 3 - I make the second tab.Tab About people who register in my programm
                                    \nday 4 - i think about 3 new tab\nday 5 - i make new tab\nAnd in day 6 i write this info 😎💻👍
                                    \nAnd if you don't now i have 2 monitor becose programmers need 2 monitor's 🖥🖥""", color='white', weight=ft.FontWeight.W_500),
                    image_src = 'https://www.mooc.org/hubfs/applications-of-computer-programming.jpg',
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor='#009eba',
                    ink_color='#9000ff',
                    width=450,
                    height=500,
                    border_radius=10,
                    ink=True,
                    url='https://itproger011.tilda.ws/aboutme',
                    on_click=lambda e: print("About you 😎"),

            ),ft.Row([ft.Image(src='https://images.ctfassets.net/pdf29us7flmy/2ZtlOujWNf4ztl5wbRnTpC/4a394c414c6a2e3f68749802e5e4d042/GettyImages-689291632_optimized.jpg?w=720&q=100&fm=jpg', border_radius=20),
                    ft.Text("""I like working in hight.\nWhy ?\nBecouse in night nobody in the street\'s or something like there.Nobody ask me questions\nAnd nobody talk with me\nI m alone write code 🌠\nCode make my life better.I don't now but i like coding\nWhen i can't write code i think 1 game programmer can make in 2 or 3 month an dnot only me.Everybody think's that to make good game need 1 or 2 year but.\nProgrammers now that  simply game makes in 1 or 2 day's.\nFor example facebook make in 2 week.And instagram to makes in 2 month in python.The programm who i now write this code\nIf you see this programm's you think he made's in 1 or 2 years.\nI can make instagramm but without avtorist and sql command's\nI like python💕💻😎""", color='#00ff1e', weight=ft.FontWeight.W_500),
            
            ]), ft.Row(
                    [
                ft.Text("Builder web-sites"),
                ft.IconButton(ft.icons.FACEBOOK, width=70, url='http://html.sites.tilda.ws/facemashcom', icon_color='#ff0000', icon_size=50),
                ft.TextButton("New Facemash", url='http://html.sites.tilda.ws/facemashcom', icon_color='#ff0000', on_click='print("Users use home and open programms.")'),
                ft.IconButton(ft.icons.FACEBOOK, width=70, url='https://theptojectblack.tilda.ws/facemash1', icon_color='#ff0000', icon_size=50),
                ft.TextButton("Facemash", url='https://theptojectblack.tilda.ws/facemash1', icon_color='#ff0000'),
                ft.IconButton(ft.icons.DARK_MODE, width=70, url='https://theptojectblack.tilda.ws/darknet', icon_size=50),
                ft.TextButton("Dark.net", url='https://theptojectblack.tilda.ws/darknet'),
                ft.IconButton(ft.icons.SOUTH_AMERICA_SHARP, width=70, url='http://theptojectblack.tilda.ws/americanspace01', icon_color='#ff00f7', icon_size=50),
                ft.TextButton("American space", url='http://theptojectblack.tilda.ws/americanspace01', icon_color='#ff00f7'),
                ft.IconButton(ft.icons.FOOD_BANK, width=70, url='http://theptojectblack.tilda.ws/maxbiffburger', icon_color='#002fff', icon_size=50),
                ft.TextButton("Burger biff max", url='http://theptojectblack.tilda.ws/maxbiffburger', icon_color='#002fff'),    
                    
                    
                    ])
        ])

    pannel_new = ft.Column(
            [
                ft.Row(
            [
                ft.TextButton('Soceal network', url='http://itproger011.tilda.ws/socelnetwork', scale=2),
            ], alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                
                ft.IconButton(ft.icons.SUNNY, on_click=change_theme),
                ft.Text('Push to cange theme'),
                
            ], alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                ft.Text("Programs"),
            ], alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                ft.IconButton(ft.icons.PLAY_ARROW, width=70, url='https://www.youtube.com/?feature=ytca', icon_color='#ff0000', icon_size=50),
                ft.TextButton("Youtube", url='https://www.youtube.com/?feature=ytca', icon_color='#ff0000', on_click='print("Users use home and open programms.")'),
                ft.IconButton(ft.icons.SNAPCHAT, width=70, url='https://www.snapchat.com/spotlight', icon_color='#ff6f00', icon_size=50),
                ft.TextButton("Snapchat", url='https://www.snapchat.com/spotlight', icon_color='#ff6f00'),
                ft.IconButton(ft.icons.LABEL, width=70, url='https://www.linkedin.com/login/ru', icon_color='#08a3fc', icon_size=50),
                ft.TextButton("Linkdin", url='https://www.linkedin.com/login/ru', icon_color='#08a3fc'),
                ft.IconButton(ft.icons.TIKTOK, width=70, url='https://www.tiktok.com/', icon_size=50),
                ft.TextButton("TikTok", url='https://www.tiktok.com/'),
                ft.IconButton(ft.icons.CAMERA_ALT_OUTLINED, width=70, url='https://www.instagram.com/', icon_color='#ff00f7', icon_size=50),
                ft.TextButton("Instagram", url='https://www.instagram.com/', icon_color='#ff00f7'),
                ft.IconButton(ft.icons.FACEBOOK, width=70, url='https://www.facebook.com/?locale=ru_RU', icon_color='#002fff', icon_size=50),
                ft.TextButton("Facebook", url='https://www.facebook.com/?locale=ru_RU', icon_color='#002fff'),
                ft.IconButton(ft.icons.REDDIT_OUTLINED, width=70, url='https://www.reddit.com/', icon_color='#ffa600', icon_size=50),
                ft.TextButton("Reddit", url='https://www.reddit.com/', icon_color='#ffa600'),
                ft.IconButton(ft.icons.WECHAT, width=70, url='https://www.wechat.com/ru/', icon_color='#b3ff00', icon_size=50),
                ft.TextButton("WeChat", url='https://www.wechat.com/ru/', icon_color='#b3ff00'),
                ft.IconButton(ft.icons.G_MOBILEDATA, width=70, url='https://www.google.com/?hl=ru', icon_color='#ff0000', icon_size=50),
                ft.TextButton("Google", url='https://www.google.com/?hl=ru', icon_color='#ff0000'),
                ft.IconButton(ft.icons.WIFI, width=70, url='https://open.spotify.com/', icon_color='#00ff26', icon_size=50),
                ft.TextButton("Spotify" , url='https://open.spotify.com/'),
                ft.IconButton(ft.icons.KEY, width=70, url='https://m.vk.com/', icon_color='#009dff', icon_size=50),
                ft.TextButton("Vk", url='https://m.vk.com/'),
                
                
            ],alignment=ft.MainAxisAlignment.CENTER
            
            
        ),
        ft.Row( 
                [
                    ft.IconButton(ft.icons.FOOD_BANK, width=70, url='https://www.kfc.tj/', icon_color='#d43f35', icon_size=50),
                    ft.TextButton('Kfc', url='https://www.kfc.tj/' ),
                    ft.IconButton(ft.icons.LOCAL_PIZZA, width=70, url='https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwjNpp6HjY-HAxUUVpEFHeNzCEUYABAAGgJscg&co=1&ase=2&gclid=CjwKCAjwkJm0BhBxEiwAwT1AXOtrZ_nnDWexDefX4Vy31bdglVLEEuFcCCO6mmoUU5N_zp8JsZbHHBoCk8wQAvD_BwE&ohost=www.google.com&cid=CAESVuD22QPf7iHr8TRzNbO1qKgC2drDOfAfpkT_ofMZv5zlLrZlEmbUD7unDkaw7KQQqSEFty4vpHYMblG6Kvy42ADJuj53pxQa6LHHj6HPoGrVV5iLWAkE&sig=AOD64_0xeoKCw_eU478uGvr56E7j6uaTfA&q&nis=4&adurl&ved=2ahUKEwjt2ZeHjY-HAxXPPxAIHUW1DP0Q0Qx6BAgIEAE', icon_color='#f07218', icon_size=50),
                    ft.TextButton('Dodo pizza.tj', url='https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwjNpp6HjY-HAxUUVpEFHeNzCEUYABAAGgJscg&co=1&ase=2&gclid=CjwKCAjwkJm0BhBxEiwAwT1AXOtrZ_nnDWexDefX4Vy31bdglVLEEuFcCCO6mmoUU5N_zp8JsZbHHBoCk8wQAvD_BwE&ohost=www.google.com&cid=CAESVuD22QPf7iHr8TRzNbO1qKgC2drDOfAfpkT_ofMZv5zlLrZlEmbUD7unDkaw7KQQqSEFty4vpHYMblG6Kvy42ADJuj53pxQa6LHHj6HPoGrVV5iLWAkE&sig=AOD64_0xeoKCw_eU478uGvr56E7j6uaTfA&q&nis=4&adurl&ved=2ahUKEwjt2ZeHjY-HAxXPPxAIHUW1DP0Q0Qx6BAgIEAE'),
                    ft.IconButton(ft.icons.FOOD_BANK_SHARP, width=70, url='https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwjNpp6HjY-HAxUUVpEFHeNzCEUYABAAGgJscg&co=1&ase=2&gclid=CjwKCAjwkJm0BhBxEiwAwT1AXOtrZ_nnDWexDefX4Vy31bdglVLEEuFcCCO6mmoUU5N_zp8JsZbHHBoCk8wQAvD_BwE&ohost=www.google.com&cid=CAESVuD22QPf7iHr8TRzNbO1qKgC2drDOfAfpkT_ofMZv5zlLrZlEmbUD7unDkaw7KQQqSEFty4vpHYMblG6Kvy42ADJuj53pxQa6LHHj6HPoGrVV5iLWAkE&sig=AOD64_0xeoKCw_eU478uGvr56E7j6uaTfA&q&nis=4&adurl&ved=2ahUKEwjt2ZeHjY-HAxXPPxAIHUW1DP0Q0Qx6BAgIEAE', icon_color='#f07218', icon_size=50),
                    ft.TextButton('Max biff burger', url='https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwjNpp6HjY-HAxUUVpEFHeNzCEUYABAAGgJscg&co=1&ase=2&gclid=CjwKCAjwkJm0BhBxEiwAwT1AXOtrZ_nnDWexDefX4Vy31bdglVLEEuFcCCO6mmoUU5N_zp8JsZbHHBoCk8wQAvD_BwE&ohost=www.google.com&cid=CAESVuD22QPf7iHr8TRzNbO1qKgC2drDOfAfpkT_ofMZv5zlLrZlEmbUD7unDkaw7KQQqSEFty4vpHYMblG6Kvy42ADJuj53pxQa6LHHj6HPoGrVV5iLWAkE&sig=AOD64_0xeoKCw_eU478uGvr56E7j6uaTfA&q&nis=4&adurl&ved=2ahUKEwjt2ZeHjY-HAxXPPxAIHUW1DP0Q0Qx6BAgIEAE'), 
                    ft.IconButton(ft.icons.LOCATION_CITY_ROUNDED, width=70, url='https://yandex.tj/maps/?azimuth=5.3945852453613625&ll=68.720667%2C37.993054&tilt=0.8726646259971648&z=7.8', icon_color='#f00000', icon_size=50),
                    ft.TextButton('Carta of Tajikistan', url='https://yandex.tj/maps/?azimuth=5.3945852453613625&ll=68.720667%2C37.993054&tilt=0.8726646259971648&z=7.8'),
                    ft.IconButton(ft.icons.WORDPRESS_OUTLINED, width=70, url='https://ru.wordpress.org/', icon_color='#009dff', icon_size=50),
                    ft.TextButton("Wordpress", url='https://ru.wordpress.org/'),
                    ft.IconButton(ft.icons.COMPUTER_OUTLINED, width=70, url='https://www.microsoft.com/ru-ru', icon_color='#5eff00', icon_size=50),
                    ft.TextButton("Microsoft", url='https://www.microsoft.com/ru-ru'),
                    ft.IconButton(ft.icons.COMPUTER_OUTLINED, width=70, url='https://www.linux.org/', icon_color='#ffa02b', icon_size=50),
                    ft.TextButton("Linux", url='https://www.linux.org/'),
                    ft.IconButton(ft.icons.SOUTH_AMERICA_SHARP, width=70, url='https://www.usa.gov/', icon_color='#ff4a4a', icon_size=50),
                    ft.TextButton("America.gov", url='https://www.usa.gov/'),
                ]
                ),
        ft.Row(
            [   ft.IconButton(ft.icons.HUB_OUTLINED, width=70, url='https://www.flaticon.com/ru/', icon_color='#85cbd4', icon_size=50),
                ft.TextButton('Github', url='https://www.flaticon.com/ru/'),
                ft.IconButton(ft.icons.HOME_MAX_SHARP, url='https://kinogo.biz/', width=70, icon_color='#525252, icon_size=50'),
                ft.TextButton('Kinogo', url='https://kinogo.biz/'),
                ft.IconButton(ft.icons.POINT_OF_SALE, url='https://www.rightmove.co.uk/property-for-sale.html', width=70, icon_color='#ffb300', icon_size=50),
                ft.TextButton('For sale', url='https://www.rightmove.co.uk/property-for-sale.html'),
                ft.IconButton(ft.icons.MONEY, url='https://m.somon.tj/', width=70, icon_color='#48ff00', icon_size=50),
                ft.TextButton('Somon TJ', url='https://m.somon.tj/'),
                ft.IconButton(ft.icons.INFO_OUTLINE, url='https://www.wikipedia.org/', width=70, icon_color='#7194ad', icon_size=50),
                ft.TextButton('Wikipedia', url='https://www.wikipedia.org/'),
                ft.IconButton(ft.icons.MUSIC_NOTE, url='https://www.jamendo.com/start?language=ru', width=70, icon_color='#c046db', icon_size=50),
                ft.TextButton('Musics download', url='https://www.jamendo.com/start?language=ru'),
                ft.IconButton(ft.icons.CHAT, url='http://itproger011.tilda.ws/programerteam', width=70, icon_color='#badbaf', icon_size=50),
                ft.TextButton('Chat for programmer', url='http://itproger011.tilda.ws/programerteam'),
                ft.IconButton(ft.icons.CHAT_BUBBLE_OUTLINE, url='http://10.0.0.20:8080/', width=70, icon_color='#00f7ff', icon_size=50),
                ft.TextButton('Online Chat', url='http://10.0.0.20:8080/'),
                ft.IconButton(ft.icons.FACEBOOK_OUTLINED, url='http://itproger011.tilda.ws/facemash', width=70, icon_color='#ad0c00', icon_size=50),
                ft.TextButton('New Facemasah', url='http://itproger011.tilda.ws/facemash'),
                
                
            ], alignment=ft.MainAxisAlignment
        ),
        ft.Row(
            [
                ft.Text('Shorts from - ?'),
                ft.Icon(ft.icons.PLAY_ARROW),
                
            ], alignment=ft.MainAxisAlignment.CENTER,
            
        ),
        ft.Row (
            [
         ft.Container(
             
                    content=ft.Text("Click to watch shorts from Youtube"),
                    url='https://www.youtube.com/shorts/',
                    margin=10,
                    padding=10,
                    bgcolor=ft.colors.RED,
                    width=150,
                    height=300,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print("Short"),
                ),
        ft.Container(
             
                    content=ft.Text("Click to watch reels from Facebook"),
                    url='https://www.facebook.com/reel/',
                    margin=10,
                    padding=10,
                    bgcolor=ft.colors.BLUE,
                    width=150,
                    height=300,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print("Short"),
                ),
        ft.Container(
             
                    content=ft.Text("Click to watch reels from Instagrm"),
                    url='https://www.instagram.com/reels/',
                    margin=10,
                    padding=10,
                    bgcolor=ft.colors.PINK_500,
                    width=150,
                    height=300,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print("Short"),
                ),
        ft.Container(
             
                    content=ft.Text("Click to watch shorts from TikTok", color='#fafafa'),
                    url='https://www.tiktok.com/video/',
                    margin=10,
                    padding=10,
                    bgcolor=ft.colors.BLACK,
                    width=150,
                    height=300,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print("Short"),
                ),
        ft.Container(
             
                    content=ft.Text("Click to watch shorts from Snpchat"),
                    url='https://www.snapchat.com/spotlight/',
                    margin=10,
                    padding=10,
                    bgcolor=ft.colors.ORANGE_900,
                    width=150,
                    height=300,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print("Short"),
        ),
        ft.Container(
             
                    content=ft.Text("Carta Tajikistan", color='#000000'),
                    url='https://yandex.tj/maps/?azimuth=5.3945852453613625&ll=68.720667%2C37.993054&tilt=0.8726646259971648&z=7.8',
                    margin=10,
                    padding=10,
                    bgcolor=ft.colors.WHITE,
                    width=300,
                    height=300,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print("Carta"),
                    image_src='https://www.mapsofindia.com/world-map/tajikistan/tajikistan-states-and-capital-map.jpg'
        ),
        ft.Container(
             
                    content=ft.Text("Wikipedia", color='#000000'),
                    url='https://www.wikipedia.org/',
                    margin=10,
                    padding=10,
                    bgcolor=ft.colors.WHITE,
                    width=300,
                    height=300,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print("wiki"),
                    image_src='https://cdn-icons-png.freepik.com/512/49/49360.png'
        ),
        ft.Container(
             
                    content=ft.Text("Facemash", color='#a30000'),
                    url='https://theptojectblack.tilda.ws/facemash1',
                    margin=10,
                    padding=10,
                    bgcolor=ft.colors.WHITE,
                    width=300,
                    height=300,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print("wiki"),
                    image_src='https://storage.yandexcloud.net/incrussia-prod/wp-content/uploads/2020/02/Di_mg1zUYAAzj-g.jpg'
        ),        
                    
            ],
             
              
        ),
        ft.Row(
            [
                ft.Text('Weather program')
            ], alignment=ft.MainAxisAlignment.CENTER
        ),  ft.Row(
                [
                   ft.IconButton(ft.icons.WB_SUNNY_ROUNDED, icon_color='#ffa600') 
                ], alignment=ft.MainAxisAlignment.CENTER
            ),
        
            ft.Row([user_data], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([weatherr_data], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.ElevatedButton(text='Give', on_click=get_info)], alignment=ft.MainAxisAlignment.CENTER),
                
            ],alignment=ft.MainAxisAlignment.CENTER  
        )
    
    # print everything
    def navigate(e):
        index = page.navigation_bar.selected_index
        page.clean()
        
        if index == 0: page.add(pannel_aught)
        elif index == 6: 
            uers_lists.controls.clear()
            
            db = sqlite3.connect('it.saves1')

            cur = db.cursor()
            # Baza danix
            cur.execute("SELECT * FROM users")
            res = cur.fetchall()
            if res != None:
                for user in res:
                    if user[1 and 6 and 4 and 5 and 2] == '':
                        page.update()
                    else:
                        uers_lists.controls.append(ft.Row([
                            ft.Tooltip(ft.Image(src="https://cdn-icons-png.flaticon.com/128/3177/3177440.png", width=70), message=f'     User\nName - {user[1]}\nSurname - {user[2]}\nPost - {user[3]}\nClass - {user[4]}\nYears - {user[5]}\nSchool - {user[6]}'),
                            ft.Text(f"Name - ", color="#80f9ff", size=20),
                            ft.Text(f"{user[1]} :", size=20, ),
                            ft.Text(f"  Surname -", color="#8cff80", size=20),
                            ft.Text(f"{user[2]} :", size=20),
                            ft.Text(f" Class -", color="#00e5ff", size=20),
                            ft.Text(f"{user[4]} :", size=20),
                            ft.Text(f" Years -", color="#ffd500", size=20),
                            ft.Text(f"{user[5]} :", color="#ff00d0", size=20),
                            ft.Text(f" School -", color="#fc7303", size=20),
                            ft.Text(f"{user[6]}", bgcolor="#fc7303", size=20),
                            ft.Text(f" Skills ", bgcolor='#15ff00', color='#000000', size=20),
                            ft.Text(f"- ", size=20),
                            ft.Text(f"{user[7]}", bgcolor='#000000', color='#15ff00', size=20),
                            
        ],  scroll=ft.ScrollMode.ADAPTIVE, spacing=20))
                print(f'+ 1 user. Name - {user[1]} in you\'r programm. He\'s post is - {user[3]}')
                db.commit()
                db.close()        
                page.add(pannel_cabinet)
        elif index == 1: page.add(pannel_new)
        elif index == 2: page.add(pannel_me)
        elif index == 3: page.add(pannel_clicker)
        elif index == 4: page.add(pannel_new2)
        elif index == 5: 
            uers_lists.controls.clear()
            
            db = sqlite3.connect('it.saves1')

            cur = db.cursor()
            # Baza danix
            cur.execute("SELECT * FROM users")
            res = cur.fetchall()
            if res != None:
                for user in res:
                    if user[1 and 6 and 4 and 5 and 2] == '':
                        page.update()
                    else:
                        uers_lists.controls.append(ft.Row([
                            ft.Tooltip(ft.Image(src="https://cdn-icons-png.flaticon.com/128/3177/3177440.png", width=70), message=f'     User\nName - {user[1]}\nSurname - {user[2]}\nHis post - {user[3]}\n     Info about me\nClass - {user[4]}\nYears - {user[5]}\nSchool - {user[6]}'),
                            ft.Icon(ft.icons.ACCOUNT_BOX),ft.Text(f"User - ", color="#80f9ff", size=20),
                            ft.Text(f"{user[1]} ", size=20 , bgcolor='#dd00ff'),
                            ft.Text(f"{user[2]} ", size=20,  bgcolor='#dd00ff'),
                            ft.Text(f"  Post -", color="#ff7a7a", size=20),ft.Icon(ft.icons.SEND_ROUNDED),
                            ft.Text(f"{user[3]}", size=20, bgcolor='#000000', color='#1eff00'),
                        
        ],  scroll=ft.ScrollMode.ADAPTIVE, spacing=20))
                print(f'+ 1 user. Name - {user[1]} in you\'r programm. He\'s post is - {user[3]}')
                db.commit()
                db.close()        
                page.add(pannel_send)
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER, label='Avtorisation',selected_icon=ft.icons.VERIFIED),
            ft.NavigationDestination(icon=ft.icons.HOME_WORK, label='Home',selected_icon=ft.icons.HOME),
            ft.NavigationDestination(icon=ft.icons.IMAGE, label='About me',selected_icon=ft.icons.INFO_SHARP),
            ft.NavigationDestination(icon=ft.icons.ADS_CLICK, label='Clicker',selected_icon=ft.icons.PLAY_ARROW),
            ft.NavigationDestination(icon=ft.icons.CHAT_BUBBLE, label='Chat',selected_icon=ft.icons.CHAT_ROUNDED),
            ft.NavigationDestination(icon=ft.icons.SEND_ROUNDED, label='Blog\'s',selected_icon=ft.icons.SEND_AND_ARCHIVE),
        ], on_change=navigate
    )
    
    page.add(pannel_aught)
ft.app(target=main, view=ft.WEB_BROWSER)