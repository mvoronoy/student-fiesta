# Придбати навички командної роботи
## 0 - налаштувати IDE
З меню VCS / Git вибрати "Clone" та додати URL https://github.com/mvoronoy/student-fiesta.git 

## 1. Оновити проєкт.

  Наступна команда витягує останній стан проєкту з віддаленого репозіторія

```
git pull origin main
```

## 2. Локальні зміни.

- Створити на вашому локальному диску вашу персональну теку (наприклад: `LB-1\MaxVoronoy`)
- В цій теці створить текстовий файл з привітанням. Наприклад `LB-1\MaxVoronoy\hello.txt`


## 3. Локальні зміни в суспільному файлі:

Додати наприкінці цього файлу посилання на ваш створений файл (просто відредагуйти цей README.md). Додавати
слід у вигляді "прізвище у квадратних дужках"+"ваш файл у круглих дужках": 
```
   [Прізвище](тека/ваш-файл-з-привітанням)
```
Наприклад в моєму випадку ```[MaxVoronoy](MaxVoronoy/helllo.txt)```

## 4. Зробити зміни доступними для загалу

На цей момент ви маєте 2 зміни: 1 новий файл (`LB-1\MaxVoronoy\hello.txt`) та 1 змінений ('`LB-1\README.md`').

### 4.1 Підсвітити зміни `add`
За допомогою середовища додайте зміни на локальному репозитарії 
```bash
git add LB-1\MaxVoronoy\hello.txt LB-1\MaxVoronoy\hello.txt
```

### 4.2 Зробіть `commit`

Обов'язково опішить коментар, що зроблено.

```bash
git commit -m "Додав свою частину...."
```

### 4.3 Перевірити актуальність вашого локального репозитарію  

Треба впевнитись, що ваші зміни не конфліктують з віддаленими, для цього ще раз виконуємо команду `pull` (дивись вище).

### 4.4 Перемістити локальні зміни на віддалений репозитарій

Спробувати виконати команду `push` (але це може спричинити конфлікт)

```bash
git push origin main
```

Якщо конфлікт виник, то треба скорегувати суспільний файл та повторити кроки 4.1 - 4.4


[KseniiaMoskalenko](KseniiaMoskalenko/hello.txt)

[ArturTodoruk](ArturTodoruk/hello_world.txt)
[VerizhenkoOleksandr](VerizhenkoOleksandr/hello.)

[KaterynaKulak](KaterynaKulak/hello.txt)

[MakarenkoIllia](MakarenkoIllia/hello.txt)
[OleksandraKhlypun](OleksandraKhlypun/hello.txt)

[ArturTodoruk](ArturTodoruk/hello_world.txt)

[DanKopylov](DanKopylov/hello.txt)


[SerhiiBukhtiiarov](SerhiiBukhtiiarov/hello.txt)

[DenysKryvenko](DenKryvenko/hello.txt)

[KuruloVoronkin](KuruloVoronkin/hello.txt)

[IhorLevchenko](IhorLevchenko/hello.txt)

[GuivanLiza](GuivanLiza/hello.txt)
