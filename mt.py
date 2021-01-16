import pygame
from time import *
from datetime import datetime, time, timedelta
from RPLCD.i2c import CharLCD

lcd = CharLCD(i2c_expander='PCF8574', address=0x20, port=1,
              cols=20, rows=4, dotsize=8, charmap='A02',
              auto_linebreaks=True, backlight_enabled=True)

# Display löschen und Starttext ausgeben
lcd.clear()
lcd.cursor_pos = (1, 1)
lcd.write_string("Initialisierung ...")

# Pygame starten für USB-KeyPad
pygame.init()
pygame.display.set_mode()

# Timer: Defaultwerte setzen, Timer löschen
tds =False; tdh =10; tdm =0   # Defaultwert für Stern-Taste, 10:00
tss =False; tsh =0; tsm =0    # Startwert für selektierte Timer 0:00
tts =False; tth =0; ttm =0    # Inc-Dec-Wert für selektierte Timer 
                            # tts-Flag true bedeutet die Editierphase ist
                            # aktiv, die Ausgangslogik bleibt eingefroren
                            # bis Enter oder Timeout kommen
t1s =False; t1h =0; t1m =23
t2s =False; t2h =1; t2m =30
t3s =False; t3h =0; t3m =0
t4s =False; t4h =0; t4m =0
t5s =False; t5h =0; t5m =0
t6s =False; t6h =0; t6m =0
t7s =False; t7h =0; t7m =0
t8s =False; t8h =0; t8m =0
t9s =False; t9h =0; t9m =0

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
            if event.key == pygame.K_KP_DIVIDE:
                lcd.close(clear=True) 
                pygame.quit(); #sys.exit() if sys is imported
            if event.key == pygame.K_KP_MULTIPLY:
                # Editierphase aktiv, alle Timer selekt. und default
                t1s=True; t2s=True; t3s=True; t4s=True; t5s=True 
                t6s=True; t7s=True; t8s=True; t9s=True 
                t1h=tdh; t2h=tdh; t3h=tdh; t4h=tdh; t5h=tdh 
                t6h=tdh; t7h=tdh; t8h=tdh; t9h=tdh; tth=tdh 
                t1m=tdm; t2m=tdm; t3m=tdm; t4m=tdm; t5m=tdm 
                t6m=tdm; t7m=tdm; t8m=tdm; t9m=tdm; ttm=tdm 
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
            if event.key == pygame.K_KP_ENTER:  # unselect all, start output
                t1s=False; t2s=False; t3s=False; t4s=False; t5s=False
                t6s=False; t7s=False; t8s=False; t9s=False; tts=False 
                tth = 0; ttm = 0

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
    lcd.cursor_pos = (1, 0)
    if t1s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (1, 1)
    lcd.write_string("{:%H:%M}".format(time(t1h, t1m)))

# zeige Timer 2 an
    lcd.cursor_pos = (1, 7)
    if t2s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (1, 8)
    lcd.write_string("{:%H:%M}".format(time(t2h, t2m)))

# zeige Timer 3 an
    lcd.cursor_pos = (1, 14)
    if t3s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (1, 15)
    lcd.write_string("{:%H:%M}".format(time(t3h, t3m)))

# zeige Timer 4 an
    lcd.cursor_pos = (2, 0)
    if t4s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (2, 1)
    lcd.write_string("{:%H:%M}".format(time(t4h, t4m)))

# zeige Timer 5 an
    lcd.cursor_pos = (2, 7)
    if t5s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (2, 8)
    lcd.write_string("{:%H:%M}".format(time(t5h, t5m)))

# zeige Timer 6 an
    lcd.cursor_pos = (2, 14)
    if t6s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (2, 15)
    lcd.write_string("{:%H:%M}".format(time(t6h, t6m)))

# zeige Timer 7 an
    lcd.cursor_pos = (3, 0)
    if t7s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (3, 1)
    lcd.write_string("{:%H:%M}".format(time(t7h, t7m)))

# zeige Timer 8 an
    lcd.cursor_pos = (3, 7)
    if t8s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (3, 8)
    lcd.write_string("{:%H:%M}".format(time(t8h, t8m)))

# zeige Timer 9 an
    lcd.cursor_pos = (3, 14)
    if t9s == True:
        lcd.write_string("\xFF")
    else:
        lcd.write_string("\xA1")
    lcd.cursor_pos = (3, 15)
    lcd.write_string("{:%H:%M}".format(time(t9h, t9m)))

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
        
        minn = now.minute     # Reset Minutenevent
        mino = minn

