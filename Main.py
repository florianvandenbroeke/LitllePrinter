from Google import get_list
from PIL import Image
import Snippets

def stitch_images(imagelist):

    totalheight = sum([image.height for image in imagelist])
    height = 0

    image = Image.new("RGB", (384, totalheight), "white")

    for im in imagelist:
        image.paste(im, box=(0, height))
        height += im.height

    image.show()

quote = "Ik haat honden, behalve als ze tussen een broodje liggen."
author = "Matthijs"
joke = "Don't you hate jokes about German sausage? They're the wurst!"
fact = "Urine from men's public urinals was sold as a commodity in Ancient Rome. It was used as a dye and for making clothes hard"

dayword, day, month, h, m = "Tuesday", "25", "June", "15", "47"
birthdays = ["Max", "Florian"]
# dog = "https://images.dog.ceo/breeds/gaddi-indian/Gaddi.jpg"
from dogtest import get_dog
dog = get_dog()
from wikipediatest import get_picture
# pic, desc = get_picture()
# picture = ('https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/20100723_Miyajima_4904.jpg/640px-20100723_Miyajima_4904.jpg', 'The floating torii gate of the Itsukushima Shrine in Japan, during low tide')
picture = ('https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Vasco_da_Gama_Bridge_B%26W_%28crop2%29.jpg/640px-Vasco_da_Gama_Bridge_B%26W_%28crop2%29.jpg', 'Vasco da Gama Bridge (Ponte Vasco da Gama), Lisbon, Portugal')
history = ('Julia Gardiner (pictured) married President John Tyler at the Church of the Ascension in New York, becoming the first lady of the United States.', 1844)
appointments = [('Uitstap', None, None), ('Belangrijke vergadering', '2024-06-30T22:00:00+02:00', '2024-06-30T23:00:00+02:00'), ('Belangrijke vergadering', '2024-06-30T22:00:00+02:00', '2024-06-30T23:00:00+02:00')]
list = get_list("UHhMeHVYX2dhaGZWdGJ2ag")

titles = ['Tesla-aandeelhouders keuren miljardenbonus voor Musk goed',
          'Derde dodelijk slachtoffer vanonder het puin gehaald na explosie in Hoboken, hulpdiensten zoeken nog 2 vermisten',
          'Linkse partijen in Frankrijk sluiten akkoord over frontvorming voor parlementsverkiezingen',
          'Groen en Vooruit Mortsel in kartel naar de verkiezingen: “Samen zijn we sterker"',
          'ANC sluit coalitieakkoord met verschillende partijen in Zuid-Afrika',
          'Voordeur beschadigd bij ontploffing in Borgerhout: verdachte opgepakt',
          'Drie ooievaarsjongen in Stokkem overleden: "Waarschijnlijk door koude weer en hevige regen"',
          'Geert Wilders kiest dan toch voor andere minister van Migratie na veiligheidsonderzoek',
          'Akkoord binnen G7 over lening van 50 miljard dollar aan Oekraïne, Biden en Zelenski tekenen veiligheidsakkoord',
          'Pro-Palestijnse actievoerders krijgen van deurwaarder tot 8.30 uur tijd om UGent-gebouw vrijwillig te verlaten: "We gaan in overleg over wat we nu gaan doen"',
          'Zware brand bij bedrijf in Ieper: rookpluim van ver te zien, evacuatie van bedrijven in de buurt',
          'Opnieuw probleem voor Boeing: defect gesignaleerd bij productie Dreamliner-toestellen',
          'Grote brand en ontploffing in loods op terrein Brucargo in Machelen na dakwerken',
          'Waait Franse MeToo-beweging over naar Belgische filmindustrie? Regisseur Joachim Lafosse beschuldigd van grensoverschrijdend gedrag',
          'Cabaretier Willy Lustenhouwer krijgt tegel aan Stadsschouwburg in Brugge',
          'Belgische brouwers moeten afrekenen met historische daling bierexport',
          'Hongarije moet 1 miljoen euro per dag betalen zolang het de Europese migratieregels niet naleeft',
          'Kloof tussen Vooruit en centrumrechtse partijen is Vlaams groter dan federaal, blijkt uit De Stemtest (al zegt dat niet alles)',
          'Kledingketen Scotch & Soda jaar na doorstart weer failliet',
          'Molen van Doel komt opnieuw boven op de Scheldedijk: "We geven hem weer de uitstraling van vroeger"\xa0',
          'Ontploffing in Hoboken brengt nare herinneringen naar boven rond Paardenmarkt en in Wilrijk: "De nachtmerrie komt terug"',
          'Vier dagen na verkiezingen heeft Duitstalige Gemeenschap nieuwe regering: Paasch blijft aan het roer',
          '8 EU-landen willen bewegingsvrijheid van Russische diplomaten in Schengenzone beperken',
          'Brouwerij in Pelt en bakkerij in Bocholt maken bier van oud stokbrood: "Licht blond bier met moutige smaak"',
          'Amerikaans Hooggerechtshof verwerpt poging om toegang tot veelgebruikte abortuspil te beperken',
          'Juf Sofie van basisschool in Neder-Over-Heembeek doet kinderen weer boeken lezen: "Lezen is gewoon plezant"',
          'Oh yes, bien sûr!\xa0Meertaligheid begint al in de buik, blijkt uit onderzoek',
          'Computerchipbedrijf Onsemi wil afdeling Oudenaarde sluiten, ook gevolgen voor afdeling Mechelen\xa0\xa0',
          'Oud-minister Luc Martens opgepakt op verdenking van oplichting en witwassen: "Ik heb nog nooit iemand bestolen, waarom zou ik dat op mijn 78 wél doen?"',
          '13.000 Limburgers klopten vorig jaar aan bij CAW: "Veel financiële stress, dakloosheid en drugsproblematiek"',
          '"Slapen is nog altijd moeilijk": Niels Destadsbader blikt terug op brand die zijn loft verwoestte',
          'Atheneum in Landen verbiedt vanaf volgend schooljaar gsm-gebruik: "Leerlingen vinden het een goed idee"',
          'Politieke partijen hebben tijdens campagne ruim 7,3 miljoen euro uitgegeven aan online-advertenties',
          'Al meer dan 100.000 spelers wagen zich aan de Sporza EK-pronostiek: doe zelf ook mee!',
          'Theater aan Zee in Oostende wil bruggen bouwen tussen generaties ',
          'Caravan langs Lovaart in Lo-Reninge is niet van kampeerder, maar van sluikstorters',
          'Van grootste producent van luiers en maandverband in Europa tot herstructureringen en banenverlies: hoe het fout liep met Ontex',
          'Lembeek organiseert Belgisch kampioenschap stringschieten: "Wij proberen altijd met iets origineels uit te pakken"',
          "Van chatbot tot vriendje: steeds meer Chinese vrouwen worden 'verliefd' op AI-bot DAN",
          'Voorzitter Franse Les Républicains weigert te vertrekken en vecht ontslag aan voor de rechtbank',
          'Vrije basisschool Sint-Paulus in Kortrijk maakt kans op belangrijke internationale milieuprijs',
          'Spookbedrijven en valse facturen voor meer dan 4 miljoen: opnieuw huiszoekingen in onderzoek naar boekhoudkantoor dat criminele bendes zou bijstaan',
          'Ook Limburgse reddingshonden ingezet in zoekactie naar slachtoffers bij explosie in Hoboken',
          'Liveblog verkiezingen: Filip Dewinter ziet rooskleurige toekomst voor Jos D\'Haese: "U wordt een van de volgende burgemeesters van Antwerpen"',
          'Patiënt krijgt gemiddeld 15 minuten bij de huisarts: "Dat is te kort voor kwaliteitsvolle consultatie"',
          'Fietser sterft bij aanrijding in Kortemark: onduidelijk wie man aanreed',
          'Straattekening Rode Duivel Jérémy Doku duikt op in Borgerhout',
          'Lisbeth Imbo stopt als co-presentator van De Zevende Dag',
          'Maximumstraf van 15 jaar cel voor Roemeen die studente in Gent verkrachtte',
          'Minder praten over klimaat, meer over industrie: dit blijft over van de Europese Green Deal na de verkiezingen']

quote_image = Snippets.create_quote(quote, author)
date_image = Snippets.create_date(dayword, day, month, h, m)
news_image = Snippets.create_news(titles)
birthdays_image = Snippets.create_birthdays(birthdays)
dog_image = Snippets.create_dog(dog)
joke_image = Snippets.create_joke(joke)
fact_image = Snippets.create_fact(fact)
# picture_image = Snippets.create_picture(pic, desc)
history_image = Snippets.create_history(history[0], history[1])
appointments_image = Snippets.create_appointments(appointments)
list_image = Snippets.create_list(list, "Boodschappenlijst")
error_image = Snippets.create_error("Could not load dog")


# stitch_images([date_image, birthdays_image, news_image, quote_image, dog_image, joke_image, fact_image, picture_image, history_image])
stitch_images([quote_image])