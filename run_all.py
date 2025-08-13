from parsers.Зdlife_parser import main as run_3dlife
from parsers.acagroup_parser import main as run_acagroup
from parsers.alash_elec_parser import main as run_alash
from parsers.dbn_parser import main as run_dbn
from parsers.stemshop_parser import main as run_stemshop
from parsers.statis import main as run_statis

def main():
    print("Запускаем stemshop_parser...")
    run_stemshop()


    print("Запускаем 3dlife_parser...")
    run_3dlife()

    print("Запускаем acagroup_parser...")
    run_acagroup()

    print("Запускаем alash_elec_parser...")
    run_alash()

    print("Запускаем dbn_parser...")
    run_dbn()


    print("Запускаем statis_parser...")
    run_statis()

    print("✅ Все парсеры отработали")


if __name__ == "__main__":
    main()
