# CodeTheorie
Bij het kraken van ADFGVX hebben we een aantal methodes doorlopen voordat
we bij de juiste uitkwamen. We beginnen natuurlijk altijd met het omzetten van
de morse code naar zijn overeenkomstige ADFGVX code. Hierna moeten we de
kolomtranspositie kraken om een tekst te verkrijgen die enkel nog vercijferd is via
het polybiusvierkant. Het eerste dat we probeerden was een brute force methode
die voor een gegeven key lengte alle permutaties voor de kolomtranspositie afgaat.
Voor elke permutatie berekenden we de frequentie van de bigrammen (AD, AG,
. . . ) en koppelden we deze in het polybiusvierkant aan een alfanumeriek teken
dat ongeveer met dezelfde frequentie in de doeltaal voorkomt. Met het bekomen
vierkant konden we dan de tekst decrypteren en berekenen hoe dicht deze bij de
doeltaal zit via dezelfde score functie die we in playfair gebruiken. Deze methode
had in theorie de oplossing kunnen vinden maar was in de praktijk te traag.
Na lang zoeken naar een manier om deze berekening per permutatie kleiner
te maken zijn we uiteindelijk uitgekomen op de index of coincidence. Stel we
hebben een tekst verkregen na een kolomtranspositie en vertaling door een
polybiusvierkant die ingevuld is via de frequentieanalyse zoals hiervoor. Dan
laat deze index ons de kans berekenen dat de resulterende tekst slechts een
monoalfabetische substitutie verwijdert is van een bestaande taal. Dit is dus
5
de kans dat de kolomtranspositie correct is en enkel het berekende polybius
vierkant verschilt met die van de oplossing. Talen zoals het Frans, Spaans, Duits
en Nederlands hebben een index of coincidence rond de 0.7 en 0.8, bij het Engels
is dit iets lager maar deze taal waren we al uitgekomen bij Playfair.
We moesten dus nog enkel de monoalfabetische substitutie oplossen. Omdat het
polybiusvierkant is opgesteld met behulp van een frequentie analyse weten we
dat het maar met enkele elementen zal verschillen met die van de oplossing. We
kunnen dus willekeurig twee elementen in het vierkant verwisselen en dan de
score functie gebruiken. Als die ons laat weten dat we dichter bij de doeltaal
zitten kunnen we de verandering behouden. Dit kunnen we blijven doen totdat
er voor een aantal iteraties geen verbeterde versie meer is voorgekomen.
