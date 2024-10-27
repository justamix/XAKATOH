import random

from django.core.management.base import BaseCommand
from minio import Minio

from ...models import *

def add_users():
    sex_list = ['female', 'male']

    for i in range(1, 10):
        CustomUser.objects.create_user(f"user{i}", f"user{i}@user.com", "1234", random.randint(15, 40), sex_list[i % 2])
        # CustomUser.objects.create_superuser(f"user{i}", f"user{i}@user.com", "1234", random.randint(15, 40), random.choice(sex_list))
    CustomUser.objects.create_superuser(f"admin", f"admin@user.com", "admin", random.randint(15, 40), sex_list[0])
    print("Пользователи созданы")

def add_category():
    name = ['Спорт', 'Настольные игры', 'Искусство', 'Природа', 'Питание']
    for var in name:
        Category.objects.create(name=var) 
    print("Категории созданы")

def add_event():
    # for i in range(1):
    event.objects.create(
        name="Футбольный матч",
        description = "Увлекательный футбол матч между командами",
        date = '2023-11-01 15:00:00',
        playground = "Стадион 1",
        address = 'Москва, ул. Ленина, 1',
        is_open = True,
        duration_in_minutes = 90,
        capacity = 25,
        category = Category.objects.filter(name='Спорт').first(),
        creater = CustomUser.objects.filter(pk=random.randint(1, 10)).first(),
        url = 'http://127.0.0.1:9000/hack/img1.jpg',
    )

    event.objects.create(
        name="Хоккейный матч",
        description = "Увлекательный хоккейный матч между командами",
        date = '2023-11-02 15:00:00',
        playground = "Стадион 2",
        address = 'Москва, ул. Ленина, 1',
        is_open = True,
        duration_in_minutes = 90,
        capacity = 15,
        category = Category.objects.filter(name='Спорт').first(),
        creater = CustomUser.objects.filter(pk=random.randint(1, 10)).first(),
        url = 'http://127.0.0.1:9000/hack/img1.jpg',
    )

    event.objects.create(
        name="Выставка Айвазовского",
        description = "Бесплатная выставка",
        date = '2023-10-06 15:00:00',
        playground = "Художественный музей",
        address = 'Москва, ул. Ленина, 2',
        is_open = True,
        duration_in_minutes = 120,
        capacity = 28,
        category = Category.objects.filter(name='Искусство').first(),
        creater = CustomUser.objects.filter(pk=random.randint(1, 10)).first(),
        url = 'http://127.0.0.1:9000/hack/img2.jpg',
    )

    event.objects.create(
        name="Игра в монополию",
        description = "Увлекательная игра в монополию",
        date = '2023-09-01 15:00:00',
        playground = "Мой дом",
        address = 'Москва, ул. Почтовая, 1',
        is_open = True,
        duration_in_minutes = 90,
        capacity = 25,
        category = Category.objects.filter(name='Настольные игры').first(),
        creater = CustomUser.objects.filter(pk=random.randint(1, 10)).first(),
        url = 'http://127.0.0.1:9000/hack/img1.jpg',
    )

    event.objects.create(
        name="Выставка Айвазовского",
        description = "Бесплатная выставка",
        date = '2023-10-06 15:00:00',
        playground = "Художественный музей",
        address = 'Москва, ул. Ленина, 2',
        is_open = True,
        duration_in_minutes = 120,
        capacity = 28,
        category = Category.objects.filter(name='Искусство').first(),
        creater = CustomUser.objects.filter(pk=random.randint(1, 10)).first(),
        url = 'http://127.0.0.1:9000/hack/img2.jpg',
    )

    event.objects.create(
        name="Дегустация вина",
        description = "Дегустация новой партии вина",
        date = '2023-10-09 12:00:00',
        playground = "Ресторан Vines",
        address = 'Москва, ул. Ленина, 3',
        is_open = True,
        duration_in_minutes = 60,
        capacity = 24,
        category = Category.objects.filter(name='Питание').first(),
        creater = CustomUser.objects.filter(pk=random.randint(1, 10)).first(),
        url = 'http://127.0.0.1:9000/hack/img3.jpg',
    )

    event.objects.create(
        name="Дегустация пельменей",
        description = "Дегустация новой партии пельменей",
        date = '2023-10-03 12:00:00',
        playground = "Ресторан Пельмень Макса",
        address = 'Москва, ул. Ленина, 3',
        is_open = True,
        duration_in_minutes = 60,
        capacity = 24,
        category = Category.objects.filter(name='Питание').first(),
        creater = CustomUser.objects.filter(pk=random.randint(1, 10)).first(),
        url = 'http://127.0.0.1:9000/hack/img3.jpg',
    )

    event.objects.create(
        name="велопрогулка",
        description = "велопрогулка в парке",
        date = '2023-10-09 12:00:00',
        playground = "Ресторан Vines",
        address = 'Москва, ул. Ленина, 3',
        is_open = True,
        duration_in_minutes = 60,
        capacity = 10,
        category = Category.objects.filter(name='Природа').first(),
        creater = CustomUser.objects.filter(pk=random.randint(1, 10)).first(),
        url = 'http://127.0.0.1:9000/hack/img3.jpg',
    )

    event.objects.create(
        name="Выставка картин",
        description = "Выставка картин у Феди",
        date = '2023-7-09 12:00:00',
        playground = "Футостудия Феди",
        address = 'Москва, ул. Гончарова, 10',
        is_open = True,
        duration_in_minutes = 60,
        capacity = 12,
        category = Category.objects.filter(name='Искусство').first(),
        creater = CustomUser.objects.filter(pk=random.randint(1, 10)).first(),
        url = 'http://127.0.0.1:9000/hack/img3.jpg',
    )

    event.objects.create(
        name="Играем в покер",
        description = "Собираемя хорошей компанией и играем в любимую игру",
        date = '2023-12-10 15:00:00',
        playground = "Хата у Влада",
        address = 'Залупинск, ул. Панина, 3',
        is_open = True,
        duration_in_minutes = 69,
        capacity = 7,
        category = Category.objects.filter(name='Настольные игры').first(),
        creater = CustomUser.objects.filter(pk=random.randint(1, 10)).first(),
        url = 'http://127.0.0.1:9000/hack/img3.jpg',
    )

    event.objects.create(
        name="Бесплатный концерт Тревисса Скоттта",
        description = "величественная музыка, которая нравится и детям, и взрослым",
        date = '2024-10-09 12:00:00',
        playground = "ВТБ Арена",
        address = 'Москва, ул. Лужники, 3',
        is_open = True,
        duration_in_minutes = 60,
        capacity = 100,
        category = Category.objects.filter(name='Искусство').first(),
        creater = CustomUser.objects.filter(pk=random.randint(1, 10)).first(),
        url = 'http://127.0.0.1:9000/hack/img3.jpg',
    )

    print('Мероприятия созданы')




class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users(),
        add_category(),
        add_event()


# insers_category = [
#     "INSERT INTO category (name) VALUES ('Спорт')",
#     "INSERT INTO category (name) VALUES ('Настольные игры')",
#     "INSERT INTO category (name) VALUES ('Искусство')",
#     "INSERT INTO category (name) VALUES ('Природа')",
#     "INSERT INTO category (name) VALUES ('Питание')"
# ]

# user_start = "INSERT INTO custom_user (username, email, password, age, sex) VALUES"


# event_start = "INSERT INTO event (name, description, date, playground, latitude, longitude, address, is_open, duration_in_minutes, capacity, category, creater) VALUES"
# insers_event = [
#     "('Футбольный матч', 'Увлекательный футбол между командами.', '2023-11-01 15:00:00', 'Стадион 1', 55.7558, 37.6173, 'Москва, ул. Ленина, 1', true, 90, 25, 1)",
#     "('Хоккейный матч', 'Увлекательный хоккей между командами.', '2023-11-02 15:00:00', 'Стадион 1', 55.7558, 37.6173, 'Москва, ул. Ленина, 1', true, 90, 25, 1)",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
# ]