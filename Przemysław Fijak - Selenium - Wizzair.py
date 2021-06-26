#from selenium import webdriver

#tworzenie obiektu driver z klasy Chrome()
#driver = webdriver.Chrome() #odpala Chrome
#adam = Czlowiek()
#driver.get("http://www.wp.pl")
#driver.maximize_window()

"""
Scenariusz testowy:
Rejestracja na stronie wizzair.com

Przypadek testowy 001:
Rejestracja przy uzyciu blednego adresu e-mail

Warunki wstepne:
1. Uruchomiona przegladarka
2. https://wizzair.com/pl-pl#/
3. Uzytkownik niezalogowany

Kroki
1. Kliknij Zaloguj sie
2. Kliknij Rejestracja
3. Wpisz imie
4. Wpisz nazwisko
5. Wybierz plec
6. Wpisz kod kraju
7. Wpisz nr telefonu
8. Wpisz nieprawidlowy adres e-mail (bez @)
9. Wpisz haslo
10. Wybierz narodowosc

Oczekiwany rezultat:
1. Uzytkownik dostaje informacje "Nieprawidlowy adres email"

Warunki koncowe:
1. Konto nie zostaje zalozone
"""
import unittest
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

valid_firstname = "Marian"
valid_lastname = "Nowak"
valid_gender = "male"
valid_country_code = "+48"
valid_phone = "111222333"
valid_password = "Qwerty123@"
valid_country = "Polska"

invalid_email = "qweasd.pl"

#Scenariusz ScenariuszTestowy
#rejestracja na stronie wizzair
class WizzairRegistration(unittest.TestCase):
    #warunki wstepne
    def setUp(self):
        #1. Uruchomiona przegladarka
        self.driver = webdriver.Chrome()

        #maksymalizacja okna
        self.driver.maximize_window()

        #2. Na stronie wizzair.com
        self.driver.get("https://wizzair.com/pl-pl#/")

        #wlaczenie implicitly wait - mechanizmu czekania na elementy max 60 sekund
        self.driver.implicitly_wait(600)

    #przypadek testowy 001:
    #rejestacja przy uzyciu blednego adresu email
    def testInvalidEmail(self):
        driver = self.driver
        #Kroki
        #1. kliknij Zaloguj baw_sie
        #metoda odszuka element i zapisze go jako WebElement
        zaloguj_btn = driver.find_element_by_xpath('//button[@data-test="navigation-menu-signin"]')
        zaloguj_btn.click()
        #poczekaj 3 sekundy
        sleep(3)

        #2. kliknij Rejestracja
        rejestracja_btn = driver.find_element_by_css_selector('button[data-test="registration"]')
        rejestracja_btn.click()
        sleep(3)

        #3. wpisz Imie
        imie_input = driver.find_element_by_name('firstName')
        imie_input.click()
        imie_input.send_keys(valid_firstname)
        sleep(1)

        #4. wpisz Nazwisko
        nazwisko_input = driver.find_element_by_name('lastName')
        nazwisko_input.click()
        nazwisko_input.send_keys(valid_lastname)
        sleep(1)

        #5. wybierz Plec
        if valid_gender == "male":
            imie_input.click()
            driver.find_element_by_xpath('//label[@data-test="register-gendermale"]').click()
            sleep(1)
        else:
            nazwisko_input.click()
            driver.find_element_by_xpath('//label[@data-test="register-genderfemale"]').click()
            sleep(1)

        #6. wpisz kod kraju
        driver.find_element_by_xpath('//div[@data-test="booking-register-country-code"]').click()
        cc_input = driver.find_element_by_name('phone-number-country-code')
        cc_input.send_keys(valid_country_code, Keys.RETURN) #wpisze kod kraju i kliknie Enter
        sleep(1)

        #7. wpisz numer telefonu
        phone_input = driver.find_element_by_name('phoneNumberValidDigits')
        phone_input.send_keys(valid_phone)
        sleep(1)

        #8. wpisz nieprawidlowy email
        email_input = driver.find_element_by_xpath('//input[@data-test="booking-register-email"]')
        email_input.click()
        email_input.send_keys(invalid_email)
        sleep(1)

        #9. wpisz haslo
        psswd_input = driver.find_element_by_name('password')
        psswd_input.send_keys(valid_password)
        sleep(1)

        #10. wybierz narodowosc
        country_input = driver.find_element_by_xpath('//input[@data-test="booking-register-country"]')
        country_input.click()
        #lista webelementow
        countries = driver.find_elements_by_xpath('//div[@class="register-form__country-container__locations"]/label')
        #iterujemy po liscie webelementow
        for label in countries:
            #szukamy wewn. webelementu
            option = label.find_element_by_tag_name('strong')
            #debugowy print
            #print(option.get_attribute('innerText'))

            #jesli tekst elementu to kraj, ktory chcemy wybrac
            if option.get_attribute('innerText') == valid_country:
                #przewin do tego kraju
                option.location_once_scrolled_into_view
                #kliknij w niego
                option.click()
                #przerwij petle
                break
        sleep(2)

        #UWAGA, TUTAJ BEDZIE PRAWDZIWY TEST!!!
        #wyszukuje wszystkie bledy
        error_messages = driver.find_elements_by_xpath('//span[@class="input-error__message"]/span')

        #tworze liste widocznych bledow
        visible_error_notices = list() #pusta lista
        for error in error_messages:
            #jesli komunikat widoczny
            if error.is_displayed():
                #dodajemy ten komunikat do listy widocznych
                visible_error_notices.append(error)

        #sprawdzam czy ta lista widocznych komunikatow zawiera tylko jeden blad
        #CZYSTY Python
        assert len(visible_error_notices) == 1, "Liczba widocznych komunikatow nie zgadza sie!"
        #z wykorzystaniem unittesta
        self.assertEqual(len(visible_error_notices), 1, msg="Liczba widocznych komunikatow nie zgadza sie!")
        #sprawdzam tresc bledu
        self.assertEqual(visible_error_notices[0].text, "Nieprawidłowy adres e-mail")

    def tearDown(self):
        #zakonczenie testu
        self.driver.quit()

#jesli uruchamiamy z tego pliku
if __name__ == "__main__":
    #uzyjmy metody main(), ktora zajmie sie reszta
    unittest.main(verbosity=2)
