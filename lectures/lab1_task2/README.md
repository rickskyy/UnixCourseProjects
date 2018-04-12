# Lab 1: Shell scripting

## Task2 Variant 34
У виклику сценарію задається два шляхи до каталогів. Отримати від користувача послідовність символів, яка задає
розширення імен файлів, і перемістити всі файли з цим розширенням з першого каталогу в другий. На екран вивести
сумарний розмір і кількість переміщених файлів. Якщо шляхи задають один і той самий каталог, переміщення не
відбувається.

## Run
Run `./script.sh` in Terminal. <br>
Required argument: 
- `$1`: path to the folder from which the files will be moved. <br>
- `$2`: path to the folder to which the files will be moved. <br>
Example: `./script.sh /home/user/from_folder /home/user/to_folder` 
