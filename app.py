from flask import Flask, render_template, Response, request
from camera import VideoCamera
import RPi.GPIO as GPIO # Импортируем библиотеку по работе с GPIO
import time # Импортируем класс для работы со временем


app = Flask(__name__)

GPIO.setwarnings(False)
pin=5
pinn=6
pinnn=9
pinnnn=10
pinPWM, pinnPWM = 17, 18

GPIO.setmode(GPIO.BCM) # Устанавливаем режим нумерации пинов
GPIO.setup(pin, GPIO.OUT)
GPIO.setup(pinn, GPIO.OUT)
GPIO.setup(pinnn, GPIO.OUT)
GPIO.setup(pinnnn, GPIO.OUT)
GPIO.setup(pinPWM, GPIO.OUT)
GPIO.setup(pinnPWM, GPIO.OUT) # Устанавливаем режим пина в OUTPUT
GPIO.output(pin, GPIO.HIGH)
GPIO.output(pinn, GPIO.LOW)
GPIO.output(pinnn, GPIO.HIGH)
GPIO.output(pinnnn, GPIO.LOW) # Подаем на выход пина логическую единицу

pwm, pwmm = GPIO.PWM(pinPWM, 100), GPIO.PWM(pinnPWM, 100)
pwm.start(0)
pwmm.start(0) # Запускаем ШИМ на пине со скважностью 10% (0-100%)
# Можно использовать данные типа float - 49.5, 2.45
pwm.ChangeFrequency(100)
current = 1
current1 =30
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'forward' in request.form:
        GPIO.output(pin, GPIO.HIGH)
        GPIO.output(pinn, GPIO.LOW)
        GPIO.output(pinnn, GPIO.HIGH)
        GPIO.output(pinnnn, GPIO.LOW)
        for i in range(0,50):
            pwm.ChangeDutyCycle(i)
            pwmm.ChangeDutyCycle(i)
            # Изменяем коэффициент запонения (скважность) от 0 до 100%
            time.sleep(0.01)
    if 'stop' in request.form:
        for i in range(50,-1,-1):
            pwm.ChangeDutyCycle(i)
            pwmm.ChangeDutyCycle(i)
            # Изменяем коэффициент запонения (скважность) от 100 до 0%
            time.sleep(0.001)
    if 'back' in request.form:
        GPIO.output(pin, GPIO.LOW)
        GPIO.output(pinn, GPIO.HIGH)
        GPIO.output(pinnn, GPIO.LOW)
        GPIO.output(pinnnn, GPIO.HIGH)
        for i in range(0,50):
            pwm.ChangeDutyCycle(i)
            pwmm.ChangeDutyCycle(i)
            # Изменяем коэффициент запонения (скважность) от 100 до 0%
            time.sleep(0.01)
    if 'right' in request.form:
        GPIO.output(pin, GPIO.LOW)
        GPIO.output(pinn, GPIO.HIGH)
        GPIO.output(pinnn, GPIO.HIGH)
        GPIO.output(pinnnn, GPIO.LOW)
        for i in range(0,50):
            pwm.ChangeDutyCycle(i)
            pwmm.ChangeDutyCycle(i)
            # Изменяем коэффициент запонения (скважность) от 100 до 0%
            time.sleep(0.01)
    if 'left' in request.form:
        GPIO.output(pin, GPIO.HIGH)
        GPIO.output(pinn, GPIO.LOW)
        GPIO.output(pinnn, GPIO.LOW)
        GPIO.output(pinnnn, GPIO.HIGH)
        for i in range(0,50):
            pwm.ChangeDutyCycle(i)
            pwmm.ChangeDutyCycle(i)
            # Изменяем коэффициент запонения (скважность) от 100 до 0%
            time.sleep(0.01)
            
    return render_template('index.html')



def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.debug = False
    app.run(host="192.168.1.243", port=5000)
