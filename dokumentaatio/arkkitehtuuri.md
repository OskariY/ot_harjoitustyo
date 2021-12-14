# Arkkitehtuurikuvaus
## Rakenne
### Pakkausrakenne
* src/
    * entities/
    * menus/
    * world.py
    * inventory.py
    * functions.py
    * save_functions.py
    * resources.py
    * settings.py
* resources/
    * images/
    * music/

## main
Peliohjelmoinnille tyypillisellä tavalla main loop pyörii pelin aloitettua jatkuvasti,
käsitellen pelaajan inputit sekä päivittäen ja piirtäen pelin eri objektit.

## World
World luokka vastaa maailman säilytyksestä, generoinnista ja muokkaamisesta. Esimerkiksi:
- `generate_chunk()`
- `remove_tile()`
- `place_tile()`

Esimerkki place_tile()-metodin logiikasta:

![place a tile](https://www.websequencediagrams.com/cgi-bin/cdraw?lz=dGl0bGUgcGxhY2UgYSB0aWxlCm1haW4oKS0-ZXZlbnQgbG9vcDogcmlnaHQgY2xpY2sKAA4KLT5JbnZlbnRvcnk6IGdldF9uZXh0X3RpbGVzKCkKABMJAD0OVHJ1ZQAsGACBAwUAPAUAMg5Xb3JsZDogaXMAgR0FAIEpBm1lbnQgdmFsaWQ_CgAbBQCBAQ1ZZXMALhN1cGRhdGUgZ2FtZV9tYXA&s=default)

## Inventory
Inventory luokka vastaa pelin sisäisten tavaroiden säilytyksestä ja niihin liittyvistä
toiminnoista. Esimerkiksi:
- `add_to_inventory()`
- `remove_item()`
- `inventory_drag()`
- `equip_item()`

## Entities
Kaikki pelin liikkuvat osat kuten pelaaja, viholliset ja maassa olevat esineet (dropit)
löytyvät entities/ kansion alta. Näillä luokilla on yleensä `draw()`-metodi, joka vastaa
piirtämisestä ja `update()`-metodi, joka vastaa joka main loopin iteraation aikana
päivitettävistä asioista. Näitä ovat poikkeuksetta esimerkiksi liikkuminen, ja
esimerkiksi pelaajan ja vihollisten tapauksessa myös esimerkiksi elämäpisteiden tarkkailu.

## Functions
Functions.py tiedosto sisältää kaikki yleiset funktiot, jotka eivät sovi yksittäisten luokkien
sisälle. Näistä tärkeimmät ovat `print_text()`, joka vastaa tekstin piirtämisestä,
`move()`, joka vastaa entiteettien liikuttamisesta ja kollisioiden käsittelystä.

## Save functions
Maailma tallennetaan dictionary-muodossa pickle tiedostoon.

## Asetukset / konfiguraatio
Muutettavaksi tarkoitetut asetukset luetaan projektin juurihakemistossa sijaitsevasta
`config.json`-tiedostosta. Muut asetukset on koodattu `settings.py`-tiedostoon. Tämä mahdollistaa
graafisen käyttöliittymän luomisen asetuksia varten tulevaisuudessa.

## Resurssit
Pelin käyttämät kuvat ja äänitiedostot sijaitsevat projektin juurihakemiston alta löytyvästä
resources hakemistosta. Ne ladataan koodissa `resources.py`-tiedostossa.

## Käyttöliittymä
Ylipäätänsä käyttöliittymä on eroteltu sovelluslogiikasta ennen kaikkea funktiotasolla.
Kaikki sovelluslogiikan kannalta olennaiset luokat ja funktiot on mahdollista yksikkötestata.

### Luokkien suhdetta kuvaava luokkakaavio:

![luokkakaavio](https://yuml.me/2b87d31b.png)
