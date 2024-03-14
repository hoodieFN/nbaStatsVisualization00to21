import pandas as pd
import matplotlib.pyplot as plt


class BlednySezon(Exception):
    komunikat = "Sezon który wybrałeś nie znajduje się w bazie - wybierz inny"
    def __init__(self, kom):
        self.komunikat = kom


def wybor_sezonow():
    jakiesezony = []
    while True:
        try:
            sezon = input("Podaj sezon w formacie RRRR-RR, np. 2000-01: ")
            rok, polrocze = sezon.split("-")
            rok, polrocze = int(rok), int(polrocze)

            if not (2000 <= rok <= 2020 and 1 <= polrocze <= 21):
                raise BlednySezon("Sezon który wybrałeś nie znajduje się w bazie - wybierz inny")

            if sezon in jakiesezony:
                print("Ten sezon został już przez Ciebie dodany")
                continue

            jakiesezony.append(sezon)

            while True:
                temp = input("Czy dodać kolejny sezon? (tak / nie) ")
                if temp in ('tak', 'nie'):
                    break
                else:
                    print("Napisz tak lub nie!")
                    continue

            if temp == 'tak':
                continue
            else:
                return jakiesezony

        except BlednySezon as exc:
            print(exc.komunikat)

        except ValueError:
            print("Błędny format!")


def wybor_danych():
    options = {'FGM': 'trafione rzuty z gry',
               'FGA': 'oddane rzuty z gry',
               'W': 'wygrane',
               'L': 'przegrane',
               'GP': 'zagrane gry',
               'PF': 'liczba fauli personalnych'}
    while True:
        print("Dostępne dane do obliczeń - wybierz jedną opcję.")
        for key, value in options.items():
            print(f'{key} - {value}')

        wybor = input().upper()
        if wybor in options:
            return wybor
        else:
            print(f'Dana {wybor} nie istnieje - dostępne opcje wyboru to FGM, FGA, W, L, GP lub PF!')

def wybierz_operacje():
    while True:
        operacje = {'sum': 'suma', 'avg': 'średnia', 'med': 'mediana'}
        print("Dostępne operacje - wybierz jedną opcję: ")
        for key, value in operacje.items():
            print(f"{key} - {value}")

        decyzja = input().lower()
        if decyzja in operacje.keys():
            return decyzja
        else:
            print("Wybrałeś niepoprawną operację! Wybierz sum, avg lub med!")

def projekt():
    plik = input("Podaj nazwe pliku z ktorego chcesz wczytac dane (Skopiuj - nba_team_stats_00_to_21.csv): ")
    if plik == 'nba_team_stats_00_to_21.csv':
        print("Pomyślny plik")


        sezony = wybor_sezonow()
        dane = wybor_danych()

        if len(sezony) == 1:
            plt.title(f'Sezon {sezony}')
            operacja = 'sum'
        else:
            plt.title(f'Sezony {sezony}')
            sezony.sort()
            operacja = wybierz_operacje()




        df = pd.read_csv('nba_team_stats_00_to_21.csv')
        df = df[['SEASON', 'TEAM', dane]]
        df = df[df['SEASON'].isin(sezony)]


        if operacja == 'avg':
            df = df.groupby('TEAM')[dane].mean()
            plt.ylabel('Średnia', fontsize=16)
        elif operacja == 'med':
            df = df.groupby('TEAM')[dane].median()
            plt.ylabel('Mediana', fontsize=16)
        else:
            df = df.groupby('TEAM')[dane].sum()
            plt.ylabel('Suma', fontsize=16)

        try:
            nazwapliku = input("Podaj nazwę pliku do którego chcesz zapisac: ")
            df.to_csv(f"{nazwapliku}.csv")
            print('Pomyślnie zapisano dane do pliku')
        except:
            print('Wystąpił błąd podczas zapisywania danych')

        #WYKRES
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')
        ax = df.plot(kind='bar', color='gray')
        ax.grid(True, axis='y', linestyle='--', color='gray', alpha=0.5)
        plt.subplots_adjust(left=0.06, bottom=0.2, right=0.95, top=0.9)
        current_figure = plt.gcf()
        current_figure.autofmt_xdate()
        plt.xlabel('Drużyny', fontsize = 16)

        plt.show()

        # print("Wynik:")
        # print(df)

    else:
        print("Błędna nazwa pliku")

if __name__ == '__main__':
    print("Projekt - statystyki NBA od 2000-01 do 2020-21")
    print()
    print("Dla jednego sezonu dostępna jest tylko operacja sumowania")
    projekt()