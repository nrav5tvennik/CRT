from flask import Flask, render_template, Response, request # Импортируем библиотеку для работы с веб-страницей
from camera import VideoCamera 
import RPi.GPIO as GPIO # Импортируем библиотеку по работе с GPIO
import time 


app = Flask(__name__)

GPIO.setwarnings(False) # Убираем предупреждения из консоли, дабы её не засорять
#Пины, отвечающие за изменение направления вращения двигателей
pin=5
pinn=6
pinnn=9
pinnnn=10 
pinPWM, pinnPWM = 17, 18 # ШИМ пины, необходимые для контролирования скорости вращения двигателей

GPIO.setmode(GPIO.BCM) # Устанавливаем режим нумерации пинов
GPIO.setup(pin, GPIO.OUT)
GPIO.setup(pinn, GPIO.OUT)
GPIO.setup(pinnn, GPIO.OUT)
GPIO.setup(pinnnn, GPIO.OUT)
GPIO.setup(pinPWM, GPIO.OUT)
GPIO.setup(pinnPWM, GPIO.OUT)

pwm, pwmm = GPIO.PWM(pinPWM, 100), GPIO.PWM(pinnPWM, 100)
# Запускаем ШИМ на пине со скважностью 0%
pwm.start(0)
pwmm.start(0)
pwm.ChangeFrequency(100)
@app.route('/', methods=['GET', 'POST']) # Запускаем веб-страницу при помощи Flask
def index():
    # Сценарии, которые будут происходить при нажатии кнопок на веб-странице
    if 'forward' in request.form: # Подаем логические переменные на порт
        GPIO.output(pin, GPIO.HIGH)
        GPIO.output(pinn, GPIO.LOW)
        GPIO.output(pinnn, GPIO.HIGH)
        GPIO.output(pinnnn, GPIO.LOW)
        for i in range(0,50): # Изменяем коэффициент запонения (скважность) от 0 до 50%
            pwm.ChangeDutyCycle(i) # Меняет скорость робота
            pwmm.ChangeDutyCycle(i)
            time.sleep(0.01) # Чем больше значение, тем медленнее робот будет разгоняться
    if 'stop' in request.form:
        for i in range(50,-1,-1):
            pwm.ChangeDutyCycle(i)
            pwmm.ChangeDutyCycle(i)
            time.sleep(0.001)
    if 'back' in request.form:
        GPIO.output(pin, GPIO.LOW)
        GPIO.output(pinn, GPIO.HIGH)
        GPIO.output(pinnn, GPIO.LOW)
        GPIO.output(pinnnn, GPIO.HIGH)
        for i in range(0,50):
            pwm.ChangeDutyCycle(i)
            pwmm.ChangeDutyCycle(i)
            time.sleep(0.01)
    if 'right' in request.form:
        GPIO.output(pin, GPIO.LOW)
        GPIO.output(pinn, GPIO.HIGH)
        GPIO.output(pinnn, GPIO.HIGH)
        GPIO.output(pinnnn, GPIO.LOW)
        for i in range(0,50):
            pwm.ChangeDutyCycle(i)
            pwmm.ChangeDutyCycle(i)
            time.sleep(0.01)
    if 'left' in request.form:
        GPIO.output(pin, GPIO.HIGH)
        GPIO.output(pinn, GPIO.LOW)
        GPIO.output(pinnn, GPIO.LOW)
        GPIO.output(pinnnn, GPIO.HIGH)
        for i in range(0,50):
            pwm.ChangeDutyCycle(i)
            pwmm.ChangeDutyCycle(i)
            time.sleep(0.01)
            
    return render_template('index.html') # Возвращает на страницу index.html



def gen(camera): # Передает на страницу видео
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed') # Создание страницы /video_feed с видеопотоком
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__': # Запускает сервер по определенному адресу
    app.debug = False
    app.run(host="0.0.0.0", port=5000)# В консоли напишет что сервер запущен по адресу 0.0.0.0:5000, но на самом деле он запустится на localhost:5000
