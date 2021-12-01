# Ohjelmistotekniikan harjoitustyö
## Northlands unspaghettified
Koodi, tekstuurit ja äänet perustuvat omaan Northlands peliprojektiini. Opin kuitenkin monia asioita pelin kirjoittamisen aikana, joten lopputulos oli 2500 riviä huonosti kirjoitettua spagettikoodia yhdessä tiedostossa, jonka mielummin jätän julkaisematta.

Tämä projekti on yritys siistiä ja uudelleenkirjoittaa aikaisempi spagettikoodi selkeämpään muotoon välttämällä aikaisempia hyvin runsaita globaaleja muuttujia, jakamalla koodia eri tiedostoihin, kirjoittamalla kommentteja ja ylipäätänsä pyrkimällä noudattamaan yleisiä hyvän koodauksen tapoja. Olen päättänyt yksinkertaistaa alkuperäistä peliä myös jossain määrin, esimerkiksi poistamalla moninpelitoiminnot.

## Pelin idea
Northlands on 2D seikkailupeli, jossa pelaaja seikkailee satunnaisesti generoidussa maailmassa keräten resursseja, rakentaen ja yrittäen selvitä vihollisilta. Sain inspiraatiota peliin Minecraftin, Terrarian ja Valheimin tapaisista peleistä.

## Toteutus
Peli on kirjoitettu Pythonilla ja toteutettu käyttäen pygame-grafiikkakirjastoa sekä yksi- ja kaksiulotteista noise-algorytmia maailman generoimiseen.

## Lisenssi
[GNU General Public License](https://opensource.org/licenses/GPL-3.0)

## Linkit:

[Vaatimusmäärittely](https://github.com/yoskari/ot_harjoitustyo/blob/main/dokumentaatio/maarittely.md)

[Tuntikirjanpito](https://github.com/yoskari/ot_harjoitustyo/blob/main/dokumentaatio/tuntikirjanpito.md)

## Asennus
1. Asenna riippuvuudet komennolla:

```bash
poetry install
```

2. Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```

## Komentorivitoiminnot

### Ohjelman suorittaminen

Ohjelman pystyy suorittamaan komennolla:

```bash
poetry run invoke start
```

### Kontrollit
A: liiku vasemmalle

D: liiku oikealle

W: hyppää

TAB: avaa/sulje inventory

MOUSE1: riko palikoita, lyö

MOUSE2: aseta palikoita (pitää olla valittuna)


### Testaus

Testit suoritetaan komennolla:

```bash
poetry run invoke test
```

### Testikattavuus

Testikattavuusraportin voi generoida komennolla:

```bash
poetry run invoke coverage-report
```

Raportti generoituu _htmlcov_-hakemistoon.
