# bacup photos from album on vk.com to Cloud (yandexDisk)

Это приложерие позволяет сделать резервную корию фотографий из альбомов на сайте vk.vom в облачное хранилище Яндекс Диска

# Требования

1. Необходимо получить ключ авторизации (token) для доступа к профилю пользователя на сайте vk.com (если у Вас нет такого ключа, при первом запуске приложение выведет в терминале ссылку на страницу для получения этого токена, более подробная информация находится в разделе API на сайте vk.com)
Для Янлекс диска тоже нужен токен, его можно получить в разделе Яндекс Полигон
Почле этого в папке с программой нужно создать файл tokens.py и добавить туда две строчки:  
yaToken = ""  
vkToken = ""  
ВАЖНО! Токен для ВК действует около суток и только для IP адреса, с которого был получен
Токен же для Яндекса действует неограниченное время, для любого IP и позволяет получить ПОЛНЫЙ доступ к Яндексу. Поэтому **_НЕ ПУБЛИКУЙТЕ_** токен от Яндекса 
2. Необходимо заполнить файл vars.py:
- указать количество фото для копирования (photoCount).Допустимы целые числа или значение "all", если необходимо скачать все фотографии из запрошенных альбомов
- указать названия альбомов в переменной albumsName, названия альбома в кавычках, через запятую. Если название окажется неверным это будет отображено в выходных файлах (output.json и upload.json)
- указать vkUserID - id пользователя Вконтакте, для которого необходимо сделать резервное копирование
3. Приложение будет отображать в терминале ход своего выполнения и выводить информацию об ошибках, если они будут возникать
4. Вся информация о проделанной работе приложения будет записана в файлы output.json и upload.json