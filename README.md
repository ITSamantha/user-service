# ✨Задание 1
Цель: Написать сервис хранения сотрудников компании(user-service)

Сервис нужно написать на FastAPI с БД postgres + тесты для него.

## Требования к БД
   - можно сохранить ФИО, логин, пароль, email сотрудника
   - сотрудники разделены по подразделениям
   - у подразделения ставится руководитель
   - у каждого сотрудника есть график командировок и отпусков которые не должны пересекаться

## Требования к API
   - Возможность получения и изменения информации для каждой сущности сервиса
   - Возможность поиска сотрудника
   - Возможность получения карточки сотрудника с его графиком отпусков и/или 
   графиком командировок

## Требования к тестам
   - Покрытие должно быть более 50%

## Требования к коду
   - Соблюдение PEP8
   - python 3.10

Рекомендованные внешние библиотеки(желательно, но не обязательно)
```
1. FastApi
https://fastapi.tiangolo.com/tutorial/first-steps/
2. Tortoise ORM + Aerich - БД
https://tortoise.github.io/migration.html
3. pytest - тесты
https://docs.pytest.org/en/7.1.x/getting-started.html
4. pydentic - типизация(опционально)
https://docs.pydantic.dev/latest/
```


<br>
<br>
# ✨Задание 2
Цель: Для user-service написать Dockerfile и docker-compose.yaml файлы.

## Требования к запуску сервиса
   - Сервис с БД запускается в контейнере одной командой ```docker compose up```


<br>
<br>
# ✨Задание 3
Цель:  Проект опубликовать в GitLab. Настроить CI. Публикация в хранилище докера.

## Требования к CI
   - Создать .gitlab-ci.yml
   - Настроить автосборку проекта при коммите в удалённый репозиторий
   - Настроить автозапуск тестов при коммитах
   - Создание докер-образа, сборка и публикация его в репозитории.


<br>
<br>
# ✨Задание 4
Цель: Написание второго микро сервисного приложения на FastApi, который хранит задачи(task-service)

Сервис нужно написать на FastAPI с БД postgres + тесты для него.

Описание: Сервис для постановки задач работникам, это список проектов, в проектах есть задачи, которые ставятся руководителем на работников в своих отделах.

## Требования к БД
   - Можно хранить задачи
   - Задача принадлежит проекту

## Требования к API
   - Возможность получения и изменения информации для каждой сущности сервиса
   - Возможность поиска задач

## Требования к тестам
   - Покрытие должно быть более 50%

## Требования к коду
   - Соблюдение PEP8
   - Проверка pylint

## Требования к CI/CD
   - Dockerfile
   - docker-compose.yml
   - gitlab-ci.yml


<br>
<br>
# ✨Задание 5

Цель: Написать третий сервис(interface-service) на FastApi, который общается с первыми двумя и предоставляет API на языке GraphQL

Описание: 
Нижний уровень - два сервиса user-service и task-service
Передача данных между сервисами по REST

Средний уровень - interface-service
обменивается данными с сервисами первого уровня через REST
Обменивается данными с сервисами верхнего уровня на языке GraphQL

## Требования к сервису:
   1. ✅ Регистрация и аутентификация пользователей: Пользователи могут создавать аккаунты и входить в систему.
   2. ✅ Создание, просмотр, редактирование и удаление задач: Задачи содержат название, описание, срок выполнения(предполагаемый и фактический), счётчик часов потраченных на выполнение и статус (выполнена/не выполнена).
Нельзя поставить задачу на человека, если он находится в отпуске.
   3. ✅ Фильтрация и сортировка задач: Пользователи могут фильтровать задачи по различным критериям (например, по статусу выполнения или сроку выполнения).
   4.✅ Уведомления о задачах: Оповещения о приближающемся сроке выполнения задачи.
 Например на почту или в телеграм.
   5. ✅ Аутентификация через API токен: Позволяет пользователям использовать API для взаимодействия с приложением.
   6. ✅ Тесты: Напишите автоматические тесты для проверки функционала приложения. Тесты должны проверять не работу отдельных модулей, а системы в целом.
      Пример теста может быть таким.
         - создаём пользователя, руководителя; задачу; назначаем задачу на пользователя; пользователь получает список задач, назначенных на него; пользователю на почту приходит уведомление о необходимости выполнить задачу.

## Требования к тестам
   - Покрытие должно быть более 50%

## Требования к коду
   - Соблюдение PEP8

## Требования к CI/CD
   - Dockerfile
   - docker-compose.yml
   - gitlab-ci.yml
