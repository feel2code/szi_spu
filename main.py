import random
from mimesis import Person
from mimesis.enums import Gender
from mimesis.locales import Locale
from uuid import uuid4

# выбираю локализацию для генерирования персональных данных
person = Person(Locale.RU)


# генерирую GUID в нижнем регистре
def guid_lower(): return str(uuid4()).lower()


# генератор СНИЛС
def snils():
    nums = [
        random.randint(1, 1) if x == 0
        else '-' if x == 3
        else '-' if x == 7
        else ' ' if x == 11
        else random.randint(0, 9)
        for x in range(0, 12)
    ]

    cont = (nums[10] * 1) + (nums[9] * 2) + (nums[8] * 3) + \
           (nums[6] * 4) + (nums[5] * 5) + (nums[4] * 6) + \
           (nums[2] * 7) + (nums[1] * 8) + (nums[0] * 9)

    if cont in (100, 101):
        cont = '00'

    elif cont > 101:
        cont = (cont % 101)
        if cont in (100, 101): cont = '00'
        elif cont < 10: cont = '0' + str(cont)

    elif cont < 10: cont = '0' + str(cont)

    nums.append(cont)
    return ''.join([str(x) for x in nums])


# генерирую данные для матери
name = person.full_name(gender = Gender.FEMALE)
pat_name = person.full_name().split()
fio_new = name + ' ' + pat_name[1] + 'вна'
fio_new = fio_new.upper().split()
snils_new = snils()

# открываем файл для сервера и меняем там данные матери
with open('toserver.xml') as file_in:
    text = file_in.read()
text = text.replace("ФАМИЛИЯ", fio_new[1])
text = text.replace("ИМЯ",  fio_new[0])
text = text.replace("ОТЧЕСТВО",  fio_new[2])
text = text.replace('oldsnils', snils_new)
newfile = "[" + snils_new + "].xml"
with open(newfile, "w") as file_out:
    file_out.write(text)

# открываем файл для ВИО и меняем там данные матери, ребенка и отца
with open('tovio.xml') as file_in2:
    textvio = file_in2.read()
# мать
textvio = textvio.replace('номерочек', str(random.randint(11111111111,99999999999)))
textvio = textvio.replace('снилсмать', snils_new)
textvio = textvio.replace('фамилияребенок', fio_new[1])
textvio = textvio.replace('имямать', fio_new[0])
textvio = textvio.replace('отчествомать', fio_new[2])
# ребенок
name_rebenok = str(person.full_name(gender = Gender.FEMALE)).upper()
fio_rebenok = name_rebenok.split()
snils_rebenok = snils()
textvio = textvio.replace('снилсребенок', snils_rebenok)
textvio = textvio.replace('имяребенок', fio_rebenok[0])
# отец
snils_otec = snils()
fio_otec = str(fio_new[1])
textvio = textvio.replace('фамилияотец', fio_otec[0:-1])
textvio = textvio.replace('снилсотец', snils_otec)
# гуид
guid_new = guid_lower()
textvio = textvio.replace('гуид', guid_new)
# сохраняем файл для вио
newfile2 = "СЗИ_СПУ_" + str(snils_new.replace(' ', '_')) + ".xml"
with open(newfile2, "w") as file_out2:
    file_out2.write(textvio)


# создаем файл скрипта для отправки
with open('send.sh') as send_script:
    sendtext = send_script.read()
sendtext = sendtext.replace('123', snils_new)
with open('send' + str(snils_new.replace(' ', '_')) + '.sh', "w") as file_out3:
    file_out3.write(sendtext)
