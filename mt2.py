import pygame
from time import *
from datetime import datetime, time, timedelta
from RPLCD.i2c import CharLCD
from gpiozero import LED

relais1 = LED(17,active_high=False)
relais2 = LED(18,active_high=False)
relais3 = LED(27,active_high=False)
relais4 = LED(22,active_high=False)
relais5 = LED(23,active_high=False)
relais6 = LED(24,active_high=False)
relais7 = LED(10,active_high=False)
relais8 = LED(9,active_high=False)
relais9 = LED(11,active_high=False)


lcd = CharLCD(i2c_expander='PCF8574', address=0x20, port=1,
              cols=20, rows=4, dotsize=8, charmap='A02',
              auto_linebreaks=True, backlight_enabled=True)

# Display löschen und Starttext ausgeben
lcd.clear()
lcd.cursor_pos = (1, 1)
lcd.write_string("Initialisierung ...")

#Relais auf 0 schalten
relais1.off()
relais2.off()
relais3.off()
relais4.off()
relais5.off()
relais6.off()
relais7.off()
relais8.off()
relais9.off()

# Pygame starten für USB-KeyPad
pygame.init()
pygame.display.set_mode()

# Timer: Defaultwerte setzen, Timer löschen
tds =False; tdh =10; tdm =0   # Defaultwert für Stern-Taste, 10:00
tss =False; tsh =10; tsm =0    # Startwert für selektierte Timer 0:00
tts =False; tth =0; ttm =0    # Inc-Dec-Wert für selektierte Timer 
                            # tts-Flag true bedeutet die Editierphase ist
                            # aktiv, bis Enter oder Timeout kommen
t1s =False; t1h =0; t1m =0; t1inf =False
t2s =False; t2h =0; t2m =0; t2inf =False
t3s =False; t3h =0; t3m =0; t3inf =False
t4s =False; t4h =0; t4m =0; t4inf =False
t5s =False; t5h =0; t5m =0; t5inf =False
t6s =False; t6h =0; t6m =0; t6inf =False
t7s =False; t7h =0; t7m =0; t7inf =False
t8s =False; t8h =0; t8m =0; t8inf =False
t9s =False; t9h =0; t9m =0; t9inf =False

timeoutd =2; timeoutc =0  # TimeOut DefaultDefault und -Counter

minn = 0; mino = 0;     # Minute now und Minute old für Minutenevent 
now = datetime.now()
minn = now.minute       # hole aktuelle Minute 
mino = minn             # beide gleich -> Reset Minutenevent

# MAIN-LOOP
lcd.clear()
while True:

# Tastatur einlesen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_KP_DIVIDE:
            #    lcd.close(clear=True) 
            #    pygame.quit(); #sys.exit() if sys is imported
            if event.key == pygame.K_KP_MULTIPLY:
            #    # Timer auf unendlich setzen, Togglefunktion mit der *-Taste
                if t1s == True: t1inf = not t1inf; t1h =0; t1m =0
                if t2s == True: t2inf = not t2inf; t2h =0; t2m =0
                if t3s == True: t3inf = not t3inf; t3h =0; t3m =0
                if t4s == True: t4inf = not t4inf; t4h =0; t4m =0
                if t5s == True: t5inf = not t5inf; t5h =0; t5m =0
                if t6s == True: t6inf = not t6inf; t6h =0; t6m =0
                if t7s == True: t7inf = not t7inf; t7h =0; t7m =0
                if t8s == True: t8inf = not t8inf; t8h =0; t8m =0
                if t9s == True: t9inf = not t9inf; t9h =0; t9m =0

            if event.key == pygame.K_KP1:
                t1s = not t1s
                timeoutc = timeoutd
            if event.key == pygame.K_KP2:
                t2s = not t2s
                timeoutc = timeoutd
            if event.key == pygame.K_KP3:
                t3s = not t3s
                timeoutc = timeoutd
            if event.key == pygame.K_KP4:
                t4s = not t4s
                timeoutc = timeoutd
            if event.key == pygame.K_KP5:
                t5s = not t5s
                timeoutc = timeoutd
            if event.key == pygame.K_KP6:
                t6s = not t6s
                timeoutc = timeoutd
            if event.key == pygame.K_KP7:
                t7s = not t7s
                timeoutc = timeoutd
            if event.key == pygame.K_KP8:
                t8s = not t8s
                timeoutc = timeoutd
            if event.key == pygame.K_KP9:
                t9s = not t9s
                timeoutc = timeoutd
            if event.key == pygame.K_KP_PLUS:
                timeoutc = timeoutd
                if tth == 0:
                    tth = 1; ttm = 0
                else:
                    tth = tth +1
                if tth == 24:
                    tth = 23
                if t1s == True: t1h = tth; t1m = ttm
                if t2s == True: t2h = tth; t2m = ttm
                if t3s == True: t3h = tth; t3m = ttm
                if t4s == True: t4h = tth; t4m = ttm
                if t5s == True: t5h = tth; t5m = ttm
                if t6s == True: t6h = tth; t6m = ttm
                if t7s == True: t7h = tth; t7m = ttm
                if t8s == True: t8h = tth; t8m = ttm
                if t9s == True: t9h = tth; t9m = ttm
            if event.key == pygame.K_KP_MINUS:
                timeoutc = timeoutd
                if tth == 0:
                    tth = 0; ttm = 0
                else:
                    tth = tth -1
                if tth == -1:
                    tth = 0
                if t1s == True: t1h = tth; t1m = ttm
                if t2s == True: t2h = tth; t2m = ttm
                if t3s == True: t3h = tth; t3m = ttm
                if t4s == True: t4h = tth; t4m = ttm
                if t5s == True: t5h = tth; t5m = ttm
                if t6s == True: t6h = tth; t6m = ttm
                if t7s == True: t7h = tth; t7m = ttm
                if t8s == True: t8h = tth; t8m = ttm
                if t9s == True: t9h = tth; t9m = ttm
            if event.key == pygame.K_KP_ENTER:  # unselect all
                t1s=False; t2s=False; t3s=False; t4s=False; t5s=False
                t6s=False; t7s=False; t8s=False; t9s=False; tts=False 
                tth = 0; ttm = 0
                timeoutc = 0


# sollte ein Timer worden selektiert sein, dann das Editierflag tts setzen
    if t1s or t2s or t3s or t4s or t5s or t6s or t7s or t8s or t9s:
        tts=True


# oberste Zeile ausgeben mit Uhrzeit
    now = datetime.now()
    lcd.cursor_pos = (0, 0)
    if tts ==True:
        lcd.write_string("-Editieren- {:%H:%M:%S}".format(now))
    else:
        lcd.write_string("Multi-Timer {:%H:%M:%S}".format(now))

# zeige Timer 1 an
    lcd.cursor_pos = (3, 0)
    if t1s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (3, 1)
    if t1inf == True:
        lcd.write_string("infnt")
    else:
        lcd.write_string("{:%H:%M}".format(time(t1h, t1m)))

# zeige Timer 2 an
    lcd.cursor_pos = (3, 7)
    if t2s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (3, 8)
    if t2inf == True:
        lcd.write_string("infnt")
    else:
        lcd.write_string("{:%H:%M}".format(time(t2h, t2m)))

# zeige Timer 3 an
    lcd.cursor_pos = (3, 14)
    if t3s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (3, 15)
    if t3inf == True:
        lcd.write_string("infnt")
    else:
        lcd.write_string("{:%H:%M}".format(time(t3h, t3m)))

# zeige Timer 4 an
    lcd.cursor_pos = (2, 0)
    if t4s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (2, 1)
    if t4inf == True:
        lcd.write_string("infnt")
    else:
        lcd.write_string("{:%H:%M}".format(time(t4h, t4m)))

# zeige Timer 5 an
    lcd.cursor_pos = (2, 7)
    if t5s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (2, 8)
    if t5inf == True:
        lcd.write_string("infnt")
    else:
        lcd.write_string("{:%H:%M}".format(time(t5h, t5m)))

# zeige Timer 6 an
    lcd.cursor_pos = (2, 14)
    if t6s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (2, 15)
    if t6inf == True:
        lcd.write_string("infnt")
    else:
        lcd.write_string("{:%H:%M}".format(time(t6h, t6m)))

# zeige Timer 7 an
    lcd.cursor_pos = (1, 0)
    if t7s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (1, 1)
    if t7inf == True:
        lcd.write_string("infnt")
    else:
        lcd.write_string("{:%H:%M}".format(time(t7h, t7m)))

# zeige Timer 8 an
    lcd.cursor_pos = (1, 7)
    if t8s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (1, 8)
    if t8inf == True:
        lcd.write_string("infnt")
    else:
        lcd.write_string("{:%H:%M}".format(time(t8h, t8m)))

# zeige Timer 9 an
    lcd.cursor_pos = (1, 14)
    if t9s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (1, 15)
    if t9inf == True:
        lcd.write_string("infnt")
    else:
        lcd.write_string("{:%H:%M}".format(time(t9h, t9m)))

# Timer 1
    if t1inf == True:
         relais1.on()
    else:
        if (t1m == 0 and t1h == 0):
             relais1.off()
        else:
             relais1.on()

# Timer 2
    if t2inf == True:
         relais2.on()
    else:
        if (t2m == 0 and t2h == 0):
             relais2.off()
        else:
             relais2.on()

# Timer 3
    if t3inf == True:
         relais3.on()
    else:
        if (t3m == 0 and t3h == 0):
             relais3.off()
        else:
             relais3.on()

# Timer 4
    if t4inf == True:
         relais4.on()
    else:
        if (t4m == 0 and t4h == 0):
             relais4.off()
        else:
             relais4.on()

# Timer 5
    if t5inf == True:
         relais5.on()
    else:
        if (t5m == 0 and t5h == 0):
             relais5.off()
        else:
             relais5.on()

# Timer 6
    if t6inf == True:
         relais6.on()
    else:
        if (t6m == 0 and t6h == 0):
             relais6.off()
        else:
             relais6.on()

# Timer 7
    if t7inf == True:
         relais7.on()
    else:
        if (t7m == 0 and t7h == 0):
             relais7.off()
        else:
             relais7.on()

# Timer 8
    if t8inf == True:
         relais8.on()
    else:
        if (t8m == 0 and t8h == 0):
             relais8.off()
        else:
             relais8.on()

# Timer 9
    if t9inf == True:
         relais9.on()
    else:
        if (t9m == 0 and t9h == 0):
             relais9.off()
        else:
             relais9.on()

# generiere Minutenevent
    minn = now.minute 
    if (minn != mino):     # falls unterschiedlich -> Minutenevent

	# Timer 1
        t1m = t1m - 1
        if (t1m < 0):
            t1m = 59; t1h = t1h - 1      # ggfls. Stundenübertrag
            if (t1h < 0):
                t1h = 0; t1m = 0          # pinning bei 00:00
        # Timer 2
        t2m = t2m - 1
        if (t2m < 0):
            t2m = 59; t2h = t2h - 1      # ggfls. Stundenübertrag
            if (t2h < 0):
                t2h = 0; t2m = 0          # pinning bei 00:00
        
        # Timer 3
        t3m = t3m - 1
        if (t3m < 0):
            t3m = 59; t3h = t3h - 1      # ggfls. Stundenübertrag
            if (t3h < 0):
                t3h = 0; t3m = 0          # pinning bei 00:00
        
        # Timer 4
        t4m = t4m - 1
        if (t4m < 0):
            t4m = 59; t4h = t4h - 1      # ggfls. Stundenübertrag
            if (t4h < 0):
                t4h = 0; t4m = 0          # pinning bei 00:00
        
        # Timer 5
        t5m = t5m - 1
        if (t5m < 0):
            t5m = 59; t5h = t5h - 1      # ggfls. Stundenübertrag
            if (t5h < 0):
                t5h = 0; t5m = 0          # pinning bei 00:00
        
        # Timer 6
        t6m = t6m - 1
        if (t6m < 0):
            t6m = 59; t6h = t6h - 1      # ggfls. Stundenübertrag
            if (t6h < 0):
                t6h = 0; t6m = 0          # pinning bei 00:00
        
        # Timer 7
        t7m = t7m - 1
        if (t7m < 0):
            t7m = 59; t7h = t7h - 1      # ggfls. Stundenübertrag
            if (t7h < 0):
                t7h = 0; t7m = 0          # pinning bei 00:00
        
        # Timer 8
        t8m = t8m - 1
        if (t8m < 0):
            t8m = 59; t8h = t8h - 1      # ggfls. Stundenübertrag
            if (t8h < 0):
                t8h = 0; t8m = 0          # pinning bei 00:00
        
        # Timer 9
        t9m = t9m - 1
        if (t9m < 0):
            t9m = 59; t9h = t9h - 1      # ggfls. Stundenübertrag
            if (t9h < 0):
                t9h = 0; t9m = 0          # pinning bei 00:00

        timeoutc = timeoutc - 1   # dec TimeOut-Counter
        if (timeoutc < 0):  # Time out -> unselect all
                t1s=False; t2s=False; t3s=False; t4s=False; t5s=False
                t6s=False; t7s=False; t8s=False; t9s=False; tts=False 
                tth = 0; ttm = 0
                timeoutc = 0
        
        minn = now.minute     # Reset Minutenevent
        mino = minn

