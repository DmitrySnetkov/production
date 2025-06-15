from yml_data import old_yml, new_yml
import os
import datetime as dt

os.system('cls')
print(f"Сравнение в {dt.datetime.now().time()}")
old_yml = set(i.split('/')[-1] for i in old_yml.strip().split('\n') if '$$$' in i)
new_yml = set(i.split('/')[-1] for i in new_yml.strip().split('\n') if '$$$' in i)


print('yml файлы идентичны -', old_yml == new_yml)

if old_yml != new_yml:
    print("Разница в:")
    # print('old <- new')
    for i in old_yml.difference(new_yml)|new_yml.difference(old_yml):
        print('   ', i)




# TODO(Снетков) надо добавить проверку схемы, она может отличаться
# TODO (Снетков) если блоков несколько, то надо проверять блоки отдельно
# TODO(Снетков) можно сделать проверку правильности построения yml при помощи дерева
#       или расстановке приоритетов для каждой функции на основе того кто и где вызывается(подсчёт вызовов даст ранг функции)
# сделать автоматическое построение скрипта отката