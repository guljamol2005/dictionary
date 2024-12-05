import googletrans
from googletrans import Translator

class dictionary:
    def __init__(self):
        self.sozlar = []
        self.sozlarni_yuklash()

    def sozlarni_yuklash(self):
        try:
            with open("dictionary.txt", "r", encoding="utf-8") as fayl:
                for qator in fayl:
                    qismlar = qator.strip().split(" | ")
                    if len(qismlar) == 3:
                        soz_id, uzb, ing = qismlar
                        self.sozlar.append({
                            "ID": int(soz_id),
                            "uzb": uzb,
                            "ing": ing
                        })
        except FileNotFoundError:
            print("Fayl topilmadi, yangi dictionary yaratildi.")
            self.sozlar = []  
        except Exception as e:
            print(f"Faylni yuklashda xato yuz berdi: {e}")

    def sozlarni_saqlash(self):
        with open("dictionary.txt", "w", encoding="utf-8") as fayl:
            for soz in self.sozlar:
                fayl.write(f"{soz['ID']} | {soz['uzb']} | {soz['ing']}\n")

    def keyingi_id(self):
        if not self.sozlar:
            return 1
        max_id = max(soz["ID"] for soz in self.sozlar)
        return max_id + 1

    def add(self, uzb: str, ing: str):
        soz_id = self.keyingi_id()  
        yangi_soz = {
            "ID": soz_id,
            "uzb": uzb,
            "ing": ing
        }
        self.sozlar.append(yangi_soz)
        self.sozlarni_saqlash()

    def sozlarni_korish(self):
        if not self.sozlar:
            print("Hech qanday so'z qo'shilmagan.")
            return
        for soz in self.sozlar:
            print(f"ID: {soz['ID']}, O'zbekcha: {soz['uzb']}, Inglizcha: {soz['ing']}")

    def yodlash(self, son: int):
        if len(self.sozlar) < son:
            print("So'zlar soni yetarli emas.")
            return

        javoblar = 0
        xato = []

        for i in range(son):
            soz = self.sozlar[i]
            foydalanuvchi = input(f"Inglizcha so'z: {soz['ing']} - O'zbekchasini kiriting: ")
            if not foydalanuvchi.strip():
                print("Iltimos, biror javob kiriting.")
                continue

            if foydalanuvchi.lower() == soz['uzb'].lower():
                javoblar += 1
            else:
                xato.append((soz['ing'], soz['uzb']))

        umumiy = len(self.sozlar)
        foiz = (javoblar / son) * 100
        print(f"\nTo'g'ri javoblar: {javoblar}/{son} ({foiz:.2f}%)")
        if xato:
            print("Xato javoblar:")
            for ing, uzb in xato:
                print(f"Inglizcha: {ing} - To'g'ri O'zbekcha: {uzb}")

    def soz_topish(self, uzb: str):
        for soz in self.sozlar:
            if soz['uzb'].lower() == uzb.lower():
                return soz['ing']
        return None

    def tarjima_qilish(self, uzb: str):
        translator = Translator()
        tarjima = translator.translate(uzb, src='uz', dest='en')
        return tarjima.text

    def menyu(self):
        while True:
            print("dictionary dasturi")
            print("1. So'zlarni ko'rish")
            print("2. Yangi so'z qo'shish")
            print("3. So'zlarni yodlash")
            print("4. O'zbekcha so'zdan Inglizcha tarjimasini topish")
            print("5. Chiqish")
            tanlov = input("Tanlovni kiriting: ")

            if tanlov == "1":
                self.sozlarni_korish()
            elif tanlov == "2":
                uzb = input("O'zbekcha so'zni kiriting: ")
                ing = input("Inglizcha so'zni kiriting (agar bilmasangiz, Enterni bosing): ")
                if not ing.strip(): 
                    ing = self.tarjima_qilish(uzb)  

                    print(f"Tarjima qilindi: {uzb} - {ing}")
                self.add(uzb, ing)
            elif tanlov == "3":
                son = int(input("Nechta so'zni yodlashni xohlaysiz? "))
                self.yodlash(son)
            elif tanlov == "4":
                uzb = input("O'zbekcha so'zni kiriting: ")
                ing = self.soz_topish(uzb)
                if ing:
                    print(f"O'zbekcha: {uzb} - Inglizcha: {ing}")
                else:
                    print(f"{uzb} so'zi topilmadi.")
            elif tanlov == "5":
                print("Chiqish")
                break
            else:
                print("Noto'g'ri tanlov")
                
if __name__ == "__main__":
    dictionary = dictionary()
    dictionary.menyu()
