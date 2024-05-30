input_text = "r2Я Ь9К>>К2ЙЬБt ЬrДЫt12<Д>>tr82tМ<КЫ1ХО>12>t<rЬЧ82ЯК КБrtАДХО>12ЯЬ2ЙЬБЬrЬ<02Я Ь>О ДЫ>Оr02ЬЕК>ЯКatrД12r2Е0Б0cК<2Ф..КЙОtrЫЬК2ЯЬ2r К<КЫt2БКЙЬБt ЬrДЫtК2>ЛДОЬАЬ2ОКЙ>ОД2ЫЬ2r<К>ОК2>2tМ<КЫКЫtК<2 Д>ЯЬЧЬЛКЫt12ЬО КМЙЬr2>ЬЬОrКО>Оr0Хct32>t<rЬЧД<2r2ЙЬБЬrЬ<2Я Ь>О ДЫ>ОrК2tМ<КЫ1КО>12ОДЙЛК2t2Я КБ>ОДrЧКЫt12>ЛДО832>t<rЬЧЬr2ОЬ2К>О,2r2ЫДbt32ОК <tЫД32bt. ЬЕЬМЫДaКЫt1?2ЫДЯ t<К 2ЯК КБrtЫ0r2>t<rЬЧ2r2tМ2ЙЬЫ9Д2ЙЬБЬrЬАЬ2Я Ь>О ДЫ>ОrД2r2ЫДaДЧЬ2ЙЬБt 0ХcКК2МЫДaКЫtК2<ЬЛКО2r8АЧ1БКО,2ЫК2ЙДЙ2МДЯЧДЫt ЬrДЫЫЬК2tМЫДaДЧ,ЫЬ2Д2ЯЬБ 0АЬ<02>ЬЬОrКО>ОrКЫЫЬ2<КЫ1ХО>12t2ЕtО82ЙЬБt 0ХctК2ЫДbК2 КМ0Ч,Оt 0ХcКК2МЫДaКЫtК2rБЬЕДrЬЙ2ДБДЯОtrЫЬ<2ДЧАЬ tО<К2r>К2<КЫ1КО>12БtЫД<taК>Йt2ЯЬ>ЧК2tМ<КЫКЫt12ЙДЛБЬАЬ2>t<r ЬЧД"

def count_and_calculate_probability(text):
# Инициализация словаря для хранения количества каждого символа
    char_count = {}
    total_chars = 0

    # Подсчет количества символов
    for char in text:
        if char.isprintable(): # Игнорируем неотображаемые символы
            char_count[char] = char_count.get(char, 0) + 1
            total_chars += 1

            # Расчет вероятности встречи каждого символа
    probabilities = {char: count / total_chars for char, count in char_count.items()}

            # Сортировка символов по убыванию вероятности
    sorted_char_count = sorted(char_count.items(), key=lambda x: x[1], reverse=True)

            # Вывод результатов
    print("Символ\t\tКоличество\tВероятность")
    print("------------------------------------")
    for char, count in sorted_char_count:
        probability = probabilities[char]
        print(f"{repr(char)}\t\t{count}\t\t{probability:.4f}")

def replace_char(input_text, old_char, new_char):
# Преобразование строки в список символов
    text_list = list(input_text)

    # Замена символов
    for i in range(len(text_list)):
        if text_list[i] == old_char:
            text_list[i] = new_char

    # Преобразование списка символов обратно в строку
    result_text = ''.join(text_list)

    return result_text

old_character = "2"
new_character = " "

result = replace_char(input_text, old_character, new_character)
print("Результат замены:", result)

