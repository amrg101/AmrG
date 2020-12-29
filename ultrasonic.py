import RPi.GPIO as GPIO
import Adafruit_DHT
import time  
GPIO.setmode(GPIO.BOARD)                     #حولنا استخدمانا لارقام ال bcm
GPIO.setwarnings(False)                    #هنا هنعمل استيراد للمكتبات ال هنستدخمها

TRIG = 13                                  # TRIG ب ال pin 23 هنربط ال
ECHO = 15                                  #ُ ECHO ب ال pin 24 هنربط ال
buzzer = 11                                # BUZZER ب ال pin 11 هنربط ال
button = 12                               #هنربط ال button 
buzzer_2 = 16   #GPIO23
button_2 = 18   #GPIO24
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
Led1_pin = 8
Led2_pin = 10

print "Distance measurement in progress"

GPIO.setup(TRIG,GPIO.OUT)                  #هنعامل التريج ك خرج
GPIO.setup(ECHO,GPIO.IN)                   #هنعامل ال اكو ك دخل 
GPIO.setup(buzzer,GPIO.OUT)                #هنعامل البين الخاص بالبازر كخرج 
GPIO.setup(button,GPIO.IN)                 #هنعامل البين بتاع الزرار كدخل عشان نعرف الاجراء ال هنتعامل معاه 
GPIO.setup(buzzer_2,GPIO.OUT)
GPIO.setup(button_2 , GPIO.IN)
GPIO.setup(Led1_pin,GPIO.OUT)		#red led
GPIO.setup(Led2_pin, GPIO.OUT)		#green led
while True:

  GPIO.output(TRIG, False)                 # هندى قيمة للتريج  LOW(0)
  print "Waitng For Sensor To Settle"        
  time.sleep(2)                            #نعمل تأخير 2 ثانية

  GPIO.output(TRIG, True)                  #هندى قيمة ل اكو HIGH(1) 
  time.sleep(0.00001)                      #نعمل تأخير 10 ميكرو ثانية
  GPIO.output(TRIG, False)                 #هنرجع قيمة التريج  LOW(0)

# عشان تبقا فاهم احنا بنعمل ايه 
# الصفر يبقا السنسور مش شغال صفر فولت عشان نشغله بنرسل ليه نبضة ف الايكو عشان يشتغل ويبقا واحد 
# ببساطه احنا هنخلى السنسور يحسب الزمن ما بين الصفر والواحد
# وهنستخدم معادلات الحركه عشان نحسب المسافة عادى فى الخطوة الجاية

  while GPIO.input(ECHO)==0:               #لو الدخل صفر 
    pulse_start = time.time()              #احفظ الوقت فى المتغير دا 

  while GPIO.input(ECHO)==1:               #لو الدخل واحد
    pulse_end = time.time()                #احفظ الوقت فى المتغير دا
  pulse_duration = pulse_end - pulse_start #هنحسب الزمن ال هنستخدمه بالفرق بين ومن الصفر والواحد

  distance = pulse_duration * 17150        #هنستخدم المعادلة دى لحساب المسافة

# مبدئيا كدا احنا هنشتغل بالسنتى عشان يبقا دقيق اكتر فى القياس
# الصوت = 343 متر فى الثانية يعنى 34300 سنتى متر فى الثانية
#الزمن الكلى ال حسبناه فوق هو فالاصل زمن فترين رايح جاى 
#فاحنا هانقسمه على اتنين ونستخدم معادلة المسافة = السرعه  على الزمن

  distance = round(distance, 2)            #هنقرب الناتج لرقمين عشرى
  if distance > 2 and distance <100 
  #هنشوف لو المسافة اقل من متر واكبر من 2 سنتى 
  #لان السنسور ميقدرش يقيس مسافة اقل من 2 سنتى
  #_نعمل نص سنتى هامش خطأ _اختيارى
    print "Distance:",distance - 0.5,"cm"  #هنطبع المسافة وهنطرح منها هامش الخطأ عشان دقة اكبر
    GPIO.output(buzzer,GPIO.HIGH)          #هنشغل الانذار
 #ممكن نضيف هنا الاجراء المطلوب تجاه الانذار
     if (GPIO.input(button)==True):
       GPIO.output(buzzer,GPIO.LOW)
  #لو تم الضغط على الزرار هيقفل الانذار
  else:
    print "Out Of Range"                   #لو المسافة مش اقل من متر يطبع الرساله دى
   #الكود الخاص بسنسور الحراره
    while True:
    temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if temperature is not None:
        print("Temp={0:0.1f}C".format(temperature))
    else:
        print("Sensor failure. Check wiring.")
       time.sleep(3)

     if temperature > 50:
             GPIO.output(buzzer_2,GPIO.HIGH)
	 if (GPIO.input(button_2) == True) :
                    GPIO.output(buzzer_2 , GPIO.LOW)
     elif  temperature <= 50 : 
             GPIO.output(buzzer_2,GPIO.LOW)
     else:
              print('Failed to get reading. Try again!')
if (GPIO.output(buzzer_1,GPIO.HIGH) AND GPIO.output(buzzer_2,GPIO.HIGH)):
	GPIO.output(Led1_pin , 1)
	GPIO.output(led2_pin,0)
	
elif(GPIO.output(buzzer_1,GPIO.LOW) AND GPIO.output(buzzer_2,GPIO.LOW)):
	GPIO.output(Led1_pin , 0)
	GPIO.output(led2_pin,1)
	
else:
	GPIO.output(Led1_pin , 0)
	GPIO.output(led2_pin,0)
	
	
