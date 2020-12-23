# RRF - Round Robot Following

## **Описание**

RRF - робот команды N, сделанный в детском технопарке _"Кванториум"_
под наставничеством Воронова Е. В.

Робот имеет округлую форму, камеру, вход для micro-usb зарядника, и кнопка включения

### **Сайт**

Робот управляется через веб-приложение, его интерфейс содержит кнопки управления, и видеотрансляцию с робота.

### **Управление**

Кнопок управления 5 - "Вперед", "Назад", "Влево", "Вправо" и "Стоп"

При нажатии конпки "Вперед", робот начнет движение прямо, при нажатии "Назад", двигаться назад. При нажатии кнопок "Вправо" или "Влево", робот будет поворачиваться направо или налево соотвественно. При нажатии "Стоп", робот прекратит движение/поворот.

### **Внутренности робота**
Робот имеет:
* 2 двигателя DF-FIT0493
* Драйвер двигателя L293D
* Одноплатный мини-компьютер Raspberry Pi 3

На одноплатный мини-компьютер Raspberry Pi 3 установлена ОС Raspbian, на компьютере содержится весь программный код, запуск осуществляется через файл [app.py](https://github.com/nrav5tvennik/CRT/blob/main/app.py) 

## **Программная часть**

Программный код состоит из 3 файлов:
* [app.py](https://github.com/nrav5tvennik/CRT/blob/main/app.py)  - через него проходит запуск программы
* [camera.py](https://github.com/nrav5tvennik/CRT/blob/main/camera.py)  - через него производится захват видео с камеры
* templates/[index.py](https://github.com/nrav5tvennik/CRT/blob/main/templates/index.html) - панель управления

