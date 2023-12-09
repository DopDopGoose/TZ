import sqlite3


#
# Техническое задание для оценки качество кода.
# Цель: Разработать консольное приложение, представляющее собой систему управления базой данных игр.
#
# Описание приложения:
# Приложение будет представлять собой систему управления базой данных игр. Для хранения данных используйте SQLite.
# Основные функции:
#
# Добавление игры: Пользователь вводит информацию о игре: название, издатель, год издания. Данные сохраняются в базу.
# Поиск игры: По заданным параметрам (название, издатель, год издания) производится поиск соответствующих игр в базе.
# Удаление игры: Пользователь может удалить игру из базы по заданным параметрам.
# Редактирование данных о игре: Пользователь может изменить данные о игре в базе.
# Вывод списка всех игр: Выводит список всех игр в базе.
#
# Дополнительные указания:
#
# Уделите внимание обработке возможных ошибок (например, попытка добавить игру без указания автора или названия).
# При разработке используйте принципы ООП для структурирования кода.
# Напишите инструкцию по запуску приложения и короткое руководство пользователя.
#
# После завершения работы над проектом, предоставьте исходный код для проверки мне в телеграм.

class GameBase:
    def __init__(self):
        self.db_path = "db.sqlite"

    @staticmethod
    def GetCleanStringForDb(str):
        return str.replace("\n", "").replace("\r", "").replace('"', "").replace("'", "")

    def GetGames(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        result = cursor.execute("SELECT * FROM games").fetchall()
        conn.close()
        if result == None:
            return "[!]No games in base"

        output = "\nGames list:\n"
        for game in result:
            output += f"{game[0]} | {game[1]} | {game[2]}\n"

        return output

    def AddGame(self):
        game_name = input("Enter game name: ")
        game_owner = input("Enter game owner: ")
        game_year = input("Enter game year: ")

        if (len(game_name) == 0 or len(game_owner) == 0 or len(game_year) == 0):
            return "[!]Incorrect game info\n"

        try:
            year = int(game_year)
            if year > 2023:
                raise "[!]Incorrect date\n"
        except:
            return "[!]Game year must be integer value and < 2023\n"

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            result = cursor.execute(
                f"INSERT INTO games VALUES('{GameBase.GetCleanStringForDb(game_name)}','{GameBase.GetCleanStringForDb(game_owner)}','{GameBase.GetCleanStringForDb(game_year)}')")
            conn.commit()
            conn.close()
            return "[$]Game added\n"
        except:
            conn.close()
            return "[!]Game already in base\n"

    def DeleteGame(self):
        game_name = input("Enter game name to delete: ")
        game_name = GameBase.GetCleanStringForDb(game_name)
        if len(game_name) == 0: return "[!]Incorrect game name\n"

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        result = cursor.execute(f"SELECT * FROM games WHERE `name` = '{game_name}'")
        if result == None:
            conn.close()
            return "[!]Game not found\n"

        cursor.execute(f"DELETE FROM games WHERE `name` = '{game_name}'")
        conn.commit()

        return "[$]Game Deleted\n"


    def SearchGameByParams(self):
        game_name = GameBase.GetCleanStringForDb(input("Search by substring in name (leave blank if not needed): "))
        game_owner = GameBase.GetCleanStringForDb(input("Search by owner (leave blank if not needed): "))
        game_year = GameBase.GetCleanStringForDb(input("Search by year (leave blank if not needed): "))

        if len(game_year) != 0:
            try:
                game_year_ = int(game_year)
                if game_year_ > 2023:
                    raise "[!]Incorrect date\n"
            except:
                return "[!]Game year must be integer value and < 2023\n"

        sqlite_command = "SELECT * FROM games WHERE "

        need_and = False
        if len(game_name) > 0:
            sqlite_command += f"`name` LIKE '%{game_name}%'"
            need_and = True
        if len(game_owner) > 0:
            if need_and:
                sqlite_command += " AND "
            sqlite_command += f"`owner` = '{game_owner}'"
        if len(game_year) > 0:
            if need_and:
                sqlite_command += " AND "
            sqlite_command += f"`year` = '{game_year}'"

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        result = cursor.execute(sqlite_command).fetchall()
        conn.close()
        if result == None:
            return "[!]No games found with given params"

        output = "\nFound games by given params\n"
        for game in result:
            output += f"{game[0]} | {game[1]} | {game[2]}\n"

        return output + "\n"



    def GetCommand(self):
        command = input("""1 - View all games
2 - Add new game to base
3 - Delete game from base
4 - Search game by name/owner/year

Enter command: """)

        if command == "1":
            print(self.GetGames())
        elif command == "2":
            print(self.AddGame())
        elif command == "3":
            print(self.DeleteGame())
        elif command == "4":
            print(self.SearchGameByParams())
        else:
            print("Incorrect command\n")

        return


if __name__ == "__main__":
    game_base = GameBase()

    while (True):
        game_base.GetCommand()
