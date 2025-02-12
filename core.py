import requests
import os
#не реализовано:
def makemydir(whatever):#Нужно для подальшего создния папок для ранобе
  try:
    os.makedirs(whatever)
  except OSError:
    pass
  # let exception propagate if we just can't
  # cd into the specified directory
  os.chdir(whatever)
def description(link):
    n=""
#########
# link1="https://ranobehub.org/ranobe/508/1/2"
def get_title(link):
    #Для сайта https://ranobehub.org
    #Тайтл главы всегда находится в 1 и том же месте->  
    response = requests.get(link)
    html = response.text
    title=(html.find(link))
    title_end=title+len(link)+2
    str_title=""
    for latter in html[title_end:]:
        if latter=="<":#
            break
        else: str_title=str_title+latter 
    return str_title
def get_text(link):
    text = ""
    response = requests.get(link)
    if response.status_code == 200:
        html = response.text
        i = 0
        while i < len(html):
            # Ищем начало<p>
            if html[i:i+3] == "<p>":
            
                
                i += 3  # Перемещаемся за <p>
                start = i
                # Ищем конец </p>
                while i < len(html):
                    if html[i:i+4] == "</p>":
                        # Добавляем текст между <p> и </p>
                        text += html[start:i] + "\n"
                        i += 4  # Перемещаемся за </p>
                        break
                    i += 1
                
            else:
                i += 1
    else:
        print(f"Ошибка: Не удалось получить страницу. Код статуса: {response.status_code}")
    return text
def clear_text(text):
    #скорее всего можно как-то оптимизировать тут, но пока устраивает.
    # Заготовка если нужно будет еще добавить слова:
    # if ''.join(text[i:i+n]) == "string": Где n количество символов в string 
    #         del text[i:i+n]
    
    
    need_del=text.find("Горячие клавиши:")
    text=text[:need_del]
    text = list(text)
    i = 0
    while i < len(text):
        if ''.join(text[i:i+8]) == "<strong>":
            del text[i:i+8]  # Delete the "<strong>" part
        if ''.join(text[i:i+9]) == "</strong>":
            del text[i:i+9]  # Delete the "<strong>" part
        else:
            i += 1  # Move to the next character only if nothing is deleted
    
    return ''.join(text)
def save(title,text,link):
    name=link[29:]
    name_list=list(name)
    for i in range(len(name_list)):
        if name_list[i] =="/":
            name_list[i]="_"
    name="".join(name_list)+".txt"
    with open(name, "w", encoding="utf-8") as file:
    # Записываем текст в файл
        file.write(title+"\n")
        file.write(text)

# save(title=get_title(link1),text=clear_text(get_text(link1)),link=link1)


def link_update(link):
    #censer_code here🤓
    response = requests.get(link)
    if response.status_code == 200:
        html = response.text
        link_pos=html.find('class="ui right basic icon button  read_nav__buttons__manage')

        endpos=0
        i=link_pos
        while endpos !=2:
            if html[i]=='"' and endpos==0:
                end=i
                endpos=1
            elif html[i]=='"' and endpos==1:
                start=i+1
                endpos==2
                break
            i-=1
    
    return html[start:end]


def save_from1(link, visited=None):
    if visited is None:
        visited = set()  
    
    if link in visited:
        return  
    
    visited.add(link)

    response = requests.get(link)
    if response.status_code == 200:
        save(title=get_title(link), text=clear_text(get_text(link)), link=link)
        
        next_link = link_update(link)
        if isinstance(next_link, str) and next_link.startswith("http"):
            save_from1(next_link, visited)


#using whole thing
while True:
    user_input=str(input("Enter link or pres e to exit "))
    if user_input=="e":
        break
    else:
        print("Wait, work in progres....")
        try:save_from1(user_input)
        except:
            print("Wrong url")
        print("Done")
        