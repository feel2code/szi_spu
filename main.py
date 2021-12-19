import random
from mimesis import Person
from mimesis.enums import Gender
from mimesis.locales import Locale
from uuid import uuid4


person = Person(Locale.RU)


# GUID LOWER
def guid_lower(): return str(uuid4()).lower()

guid_new = guid_lower()



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


name = person.full_name(gender = Gender.FEMALE)
pat_name = person.full_name().split()
fio_new = name + ' ' + pat_name[1] + 'вна'
fio_new = fio_new.upper().split()
snils_new = snils()

with open('toserver.xml') as file_in:
    text = file_in.read()

text = text.replace("ФАМИЛИЯ", fio_new[1])
text = text.replace("ИМЯ",  fio_new[0])
text = text.replace("ОТЧЕСТВО",  fio_new[2])
text = text.replace('oldsnils', snils_new)

newfile = "[" + snils_new + "].xml"
with open(newfile, "w") as file_out:
    file_out.write(text)


with open('tovio.xml') as file_in2:
    textvio = file_in2.read()

textvio = textvio.replace('номерочек', str(random.randint(11111111111,99999999999)))
textvio = textvio.replace('снилсмать', snils_new)
textvio = textvio.replace('фамилияребенок', fio_new[1])
textvio = textvio.replace('имямать', fio_new[0])
textvio = textvio.replace('отчествомать', fio_new[2])



name_rebenok = str(person.full_name(gender = Gender.MALE)).upper()
fio_rebenok = name_rebenok.split()
snils_rebenok = snils()
textvio = textvio.replace('снилсребенок', snils_rebenok)
textvio = textvio.replace('имяребенок', fio_rebenok[0])
textvio = textvio.replace('имяребенок', fio_rebenok[0])

snils_otec = snils()
textvio = textvio.replace('снилсотец', snils_otec)

textvio = textvio.replace('гуид', guid_new)


newfile2 = "СЗИ_СПУ_" + snils_new + ".xml"
with open(newfile2, "w") as file_out2:
    file_out2.write(textvio)
