from PIL import Image, ImageDraw, ImageFont
import textwrap

wagner = "NT Wagner.otf"
franchise = "Franchise.ttf"
clab = "Clab.otf"
clab_bold = "Clab bold.otf"
product = "Product Sans Regular.ttf"
blackout = "Blackout Sunrise.ttf"
dillan = "Dillan.otf"
market_deco = "market deco.ttf"
harlem_deco = "harlem deco.ttf"
retrolight = "Retrolight.ttf"
london = "Old London.ttf"
linux = "Linux.ttf"
normal = "new normal.ttf"
times = "Times New Roman.ttf"
futura = "futura medium bt.ttf"
futura_light = "futura light bt.ttf"
magazine = "Magazine.ttf"
gravity = "Gravity.ttf"
mermaid = "Mermaid.ttf"


class Frame:

    def __init__(self, width=384):
        self.boxcoords = None
        self.width = width
        self.image = Image.new("RGB", (self.width, 1000), "white")
        self.d = ImageDraw.Draw(self.image)
        self.current_h = 0

    def draw_line(self, start_x, end_x, width):
        self.d.rectangle((start_x, self.current_h, end_x, self.current_h + width - 1), fill="black", outline=0, width=0)
        self.current_h += width

    def paste_im(self, path):
        to_paste = Image.open(path)
        self.image.paste(to_paste, box=(0, self.current_h))
        self.current_h += to_paste.height

    def add_whitespace(self, space):
        self.current_h += space

    def draw_center_text(self, text, font, size, cbox=False, add_offset=0, spacing=4):
        font = ImageFont.truetype(font, size)
        self.boxcoords = self.d.textbbox((self.width / 2, self.current_h), text, anchor="ma", font=font, align="center",
                                         spacing=spacing)
        offset = self.boxcoords[1] - self.current_h
        self.d.text((self.width / 2 + add_offset, self.current_h - offset), text, fill="black", font=font,
                    align="center", spacing=spacing, anchor="ma")
        # self.boxcoords = self.d.textbbox((self.width/2 + add_offset, self.current_h - offset), text, anchor="ma", font=font, align="center", spacing=4)
        # self.d.rectangle(self.boxcoords, outline="black")
        h_increment = self.boxcoords[3] - self.boxcoords[1]
        self.current_h += h_increment

    def draw_width(self, text, font, width, offset=0, alignment="c"):
        size = 1
        self.boxcoords = self.d.textbbox((0, 0), text, ImageFont.truetype(font, size))
        while self.boxcoords[2] - self.boxcoords[0] <= width:
            size += 1
            self.boxcoords = self.d.textbbox((0, 0), text, ImageFont.truetype(font, size))

        if alignment == "c":
            self.draw_center_text(text, font, size, add_offset=offset)
        elif alignment == "r":
            self.draw_right_text(text, font, size, add_offset=offset)
        elif alignment == "l":
            self.draw_left_text(text, font, size, add_offset=offset)

    def draw_left_text(self, text, font, size, cbox=False, add_offset=0, spacing=4):
        font = ImageFont.truetype(font, size)
        self.boxcoords = self.d.textbbox((self.width / 2, self.current_h), text, anchor="la", font=font, align="left",
                                         spacing=4)
        offset = self.boxcoords[1] - self.current_h
        self.d.text((add_offset, self.current_h - offset), text, fill="black", font=font, align="left", spacing=spacing,
                    anchor="la")
        # self.boxcoords = self.d.textbbox((add_offset, self.current_h - offset), text, font=font, align="left", spacing=spacing, anchor="la")
        # self.d.rectangle(self.boxcoords, outline="black")
        h_increment = self.boxcoords[3] - self.boxcoords[1]
        self.current_h += h_increment

    def draw_right_text(self, text, font, size, cbox=False, add_offset=0, spacing=4):
        font = ImageFont.truetype(font, size)
        self.boxcoords = self.d.textbbox((self.width / 2, self.current_h), text, anchor="ra", font=font, align="right",
                                         spacing=spacing)
        offset = self.boxcoords[1] - self.current_h
        self.d.text((self.width - add_offset, self.current_h - offset), text, fill="black", font=font, align="right",
                    spacing=spacing, anchor="ra")
        # self.boxcoords = self.d.textbbox((self.width - add_offset, self.current_h - offset), text, anchor="ra", font=font, align="right", spacing=4)
        # self.d.rectangle(self.boxcoords, outline="black")
        h_increment = self.boxcoords[3] - self.boxcoords[1]
        self.current_h += h_increment

    def text_wrap(self, text, font, size, max_width, alignment="c", offset=0, spacing=4):

        font_t = ImageFont.truetype(font, size)
        wordlist = text.split(" ")
        line = []
        textlist = []

        for word in wordlist:

            line.append(word)
            linewidth = self.d.textbbox((0, 0), " ".join(line), font=font_t)[2]

            if linewidth > max_width:
                textlist += [line[:-1]]
                line = [line[-1]]

        textlist += [line]

        if not textlist[0]:
            textlist.pop(0)

        text = "\n".join([" ".join(part) for part in textlist])

        if alignment == "c":
            self.draw_center_text(text, font, size, add_offset=offset, spacing=spacing)
        elif alignment == "r":
            self.draw_right_text(text, font, size, add_offset=offset, spacing=spacing)
        elif alignment == "l":
            self.draw_left_text(text, font, size, add_offset=offset, spacing=spacing)

    def draw_underline(self, offfset, w):
        x1, y1 = self.boxcoords[0], self.boxcoords[3] + offfset
        x2, y2 = self.boxcoords[2], self.boxcoords[3] + offfset
        self.d.line((x1, y1, x2, y2), "black", width=w)
        self.current_h += offfset + w

    def draw_sidebars(self, offset, w):
        x1, y1 = self.boxcoords[0] - offset, self.boxcoords[1]
        x2, y2 = self.boxcoords[2] + offset, self.boxcoords[3]
        self.d.line((x1, y1, x1, y2), fill="black", width=w)
        self.d.line((x1, (y1 + y2) // 2, 0, (y1 + y2) // 2), fill="black", width=w)
        self.d.line((x2, y1, x2, y2), fill="black", width=w)
        self.d.line((x2, (y1 + y2) // 2, self.width, (y1 + y2) // 2), fill="black", width=w)

    def show(self):
        self.image = self.image.crop((0, 0, self.width, self.current_h))
        self.image.show()


def create_date(dayword, day, month, h, m):
    frame = Frame()

    frame.add_whitespace(10)
    frame.draw_width(dayword, franchise, 320)
    frame.add_whitespace(15)
    frame.draw_width(f"{day} {month} | {h}:{m}", futura, 320)
    frame.add_whitespace(10)

    frame.show()


def create_quote(quote, author):
    frame = Frame()

    frame.add_whitespace(10)
    frame.paste_im("Images/dot_line.png")
    frame.add_whitespace(20)
    frame.paste_im("Images/quote_header.png")
    frame.add_whitespace(20)
    frame.text_wrap(quote, normal, 35, 300)
    frame.add_whitespace(10)
    frame.text_wrap(f"- {author}", product, 20, 100, alignment="r", offset=15)
    frame.add_whitespace(20)

    frame.show()


def create_news(items):
    frame = Frame()

    frame.add_whitespace(10)
    frame.paste_im("Images/dot_line.png")
    frame.add_whitespace(15)
    frame.draw_center_text("Today's news", london, 62)
    frame.add_whitespace(5)
    frame.draw_line(192 - 150, 192 + 150, 2)
    frame.add_whitespace(2)
    frame.draw_line(192 - 150, 192 + 150, 2)

    frame.add_whitespace(15)

    for i in range(4):
        frame.text_wrap(items[i], clab, 20, 350, "r" * (i % 2) + "l" * (not i % 2), 15, spacing=4)
        frame.add_whitespace(16)

    frame.show()


quote = "\"Ik haat honden, behalve als ze tussen een broodje liggen.\""
author = "Matthijs"
dayword, day, month, h, m = "Thursday", "13", "September", "23", "55"

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
summaries = [
    'De aandeelhouders van Tesla hebben op de algemene vergadering opnieuw hun goedkeuring uitgesproken voor een enorm aandelenpakket ter waarde van tientallen miljarden dollar voor bedrijfsbaas Elon Musk.',
    'In Hoboken is vanavond een derde dodelijk slachtoffer vanonder het puin gehaald na een zware explosie in de Sint-Bernardsesteenweg. De hulpdiensten zoeken nog zeker 2 vermisten in het gebouw. Vanochtend en vanmiddag werden al 2 lichamen geborgen. Bij de explosie raakten ook 5 mensen gewond. De hulpdiensten zijn nog steeds op zoek naar bewoners en evalueren uur per uur of ze verder werken.',
    "De linkse politieke partijen in Frankrijk hebben donderdagavond een akkoord bereikt over de vorming van een 'Nieuw Volksfront' voor de komende parlementsverkiezingen.",
    'Groen Vooruit, dat is de naam van het nieuwe kartel dat in Mortsel is gevormd voor de gemeenteraadsverkiezingen. Vooruit zat in het gemeentebestuur de afgelopen jaren, Groen in de oppositie. Maar de partijen waren het vaak met elkaar eens, zegt lijsttrekker Michiel Hubeau (Groen). “De 2 partijen willen een progressief beleid. Samen willen we de grootste partij van Mortsel worden.”',
    'De Zuid-Afrikaanse partij ANC is met verschillende partijen tot een akkoord gekomen over de vorming van een coalitieregering. Dat is donderdag op een persconferentie medegedeeld.',
    'In de Maréestraat in Borgerhout heeft een onbekende in de vooravond een projectiel naar een huis gegooid. Dat kwam tot ontploffing en heeft de voordeur beschadigd. Kort na de feiten heeft de politie een verdachte opgepakt.',
    'De 3 ooievaarsjongen die midden mei werden geboren in het natuurgebied Negenoord-Kerkeweerd in Dilsen-Stokkem zijn gestorven. Dat schrijft het Belang van Limburg en het nieuws is bevestigd aan onze redactie. Vermoedelijk zijn ze slachtoffer geworden van het koude weer en de hevige regen.',
    'Gidi Markuszower, een parlementslid van de radicaal-rechtse partij PVV van Geert Wilders, zal dan toch geen minister van Asiel en Migratie worden in de nieuwe Nederlandse regering. Na een veiligheidsonderzoek door de Nederlandse inlichtingendienst AIVD is zijn kandidatuur opnieuw ingetrokken. Dat meldt RTL Nieuws en de informatie is door Wilders ook bevestigd op de sociaalnetwerksite X.',
    'De leiders van de G7-landen zijn het eens geraakt over een lening van 50 miljard dollar aan Oekraïne. De 7 landen zullen de toekomstige opbrengst van Russisch geblokkeerd geld gebruiken als waarborg voor die lening. In de marge van de G7-top ondertekenden de Verenigde Staten en Oekraïne ook een bilateraal veiligheidsakkoord.',
    'De pro-Palestijnse actievoerders die al enkele weken een gebouw van de UGent bezetten, hebben officieel het bevel gekregen om het gebouw te verlaten. Rond 20.30 uur heeft de deurwaarder een officieel bevel tot ontruiming overgemaakt. Op dit moment is er nog een 40-tal actievoerders aanwezig in het gebouw. Ze krijgen 12 uur de tijd - ongeveer tot 8.30 dus - om vrijwillig te vertrekken. Het is nog niet duidelijk of ze gehoor zullen geven aan het bevel.',
    'In Ieper woedt op dit moment een zware industriebrand bij het bedrijf Orgamex. Bij de brand komt een gigantische rookpluim vrij die tot ver buiten Ieper te zien is. De brandweer is massaal ter plaatse en probeert het vuur te blussen.',
    'Er is opnieuw een probleem opgedoken bij vliegtuigbouwer Boeing. Het bedrijf heeft medegedeeld dat aan het licht is gekomen dat bevestigingsmiddelen niet goed waren vastgemaakt in de romp van nog niet geleverde Dreamliner-vliegtuigen.',
    'Er is een zware brand uitgebroken in een loods op de terreinen van Brucargo, de vrachtafdeling van Brussels Airport in Machelen. De brand is ontstaan door dakwerken, er was ook een ontploffing. Voorlopig is er geen sprake van slachtoffers. De omgeving is afgesloten.',
    'Een tiental oud-medewerkers van Joachim Lafosse beschuldigt de Brusselse regisseur van morele of seksuele intimidatie op de set. Heeft het MeToo-protest uit de Franse filmindustrie ook ons land bereikt? “Als het regent in Frankrijk, druppelt het ook in Franstalig België”, zegt filmjournalist Lieven Trio.',
    'Voor de Koninklijke Stadsschouwburg van Brugge is een tegel onthuld als eerbetoon aan cabaretier Willy Lustenhouwer. Hij is onder meer bekend van het nummer ‘Zie je van Brugge’. Lustenhouwer heeft bovendien veel betekend voor de stadsschouwburg.',
    'Zowel de binnenlandse bierconsumptie als de export daalde vorig jaar sterk. Dat meldt sectorkoepel Belgische Brouwers woensdag bij de publicatie van het jaarverslag. Voor de export is sprake van een historische daling. De brouwers verwijzen naar de inflatie, koopkrachtcrisis en een personeelstekort.',
    'Hongarije moet een boete van 200 miljoen euro betalen, omdat het land met opzet weigert om de Europese regels rond migratie na te leven. Dat heeft het Europees Hof van Justitie geoordeeld. Hongarije moet bovenop die boete ook 1 miljoen euro per dag betalen, zolang het de EU-regels niet naleeft.',
    'De kloof tussen Vooruit en de centrumrechtse partijen is groter op Vlaams niveau dan op federaal niveau. Dat blijkt uit De Stemtest. Nochtans aarzelt kopstuk Conner Rousseau meer over een federale regeringsdeelname dan een Vlaamse. "Maar er zijn belangrijke nuances", zegt professor politieke communicatie Jonas Lefevere.',
    'Het van oorsprong Nederlandse modemerk Scotch & Soda is ruim een jaar na een doorstart opnieuw failliet, meldt het bedrijf. Het merk ging al eens failliet, maar werd in maart vorig jaar overgenomen door Bluestar Alliance, een Amerikaanse onderneming die meerdere modemerken bezit. Dit keer is ook voor de vestigingen in ons land, maar ook Duitsland, Luxemburg en Oostenrijk het faillissement aangevraagd.',
    'In de loop van volgend jaar zal de molen van Doel bij Beveren op de dijk staan in plaats van ernaast. De Maatschappij Linker Schelde Oever (MLSO) is eigenaar van de molen, en gaat in op een vraag van de Dienst Onroerend Erfgoed. Die wil niet dat de nieuwe brasserie boven de molen uitkomt. "Door de molen naar de dijk te verhuizen, zal die zeker goed tot zijn recht komen", luidt het bij MLSO.',
    'Een ontploffing die een woning vernielt en waarbij doden vallen, het brengt nare herinneringen naar boven. Dat zeggen buurtbewoners van de Paardenmarkt in Antwerpen en het Ridderveld in Wilrijk waar in 2018 en in 2019 een explosie plaatsvond, na het drama in Hoboken. "De nachtmerrie komt terug."',
    'Vier dagen na de verkiezingen heeft de Duitstalige Gemeenschap al een nieuwe regering. De regionalistische ProDG van minister-president Oliver Paasch gaat in zee met de christendemocratische CSP en de liberale PFF. De socialistische SP verhuist voor het eerst sinds 1990 naar de oppositiebanken.',
    '8 EU-ministers van Buitenlandse Zaken willen de bewegingsvrijheid van Russische diplomaten in de Schengenzone beperken. Zo willen ze het moeilijker maken voor de diplomaten om "kwaadwillige acties" uit te voeren tegen de Europese Unie.',
    'Om voedselverspilling tegen te gaan hebben Bakkerij Knapen in Bocholt en de Microbrouwerij Mølder & Coöp in Pelt samengewerkt aan een nieuw bier met de naam "De Glazen Boterham". Dat bier is gemaakt van verloren brood, ofwel stokbrood dat na 1 dag wordt weggegooid. "Als we producten die we weggooien terug kunnen gebruiken, dan zijn we goed bezig", vindt bakker Jack Knapen.',
    'In de Verenigde Staten heeft het Hooggerechtshof geoordeeld dat het gebruik van mifepriston, een veelgebruikte abortuspil, niet mag worden beperkt. Volgens het hof hadden de aanklagers, een groep anti-abortusartsen en activisten, geen wettelijke grond om een zaak aan te spannen.',
    '3 juffen uit het basisonderwijs zijn verkozen tot boekenjuf in 2024. Deze prijs beloont leerkrachten die hun leerlingen stimuleren om te lezen. De winnaars zijn Sofie Glorieus uit Neder-Over-Heembeek, Els De Latter uit Gent en Marianne Flour uit Hoboken. Het is een initiatief van onder andere de stichting Iedereen Leest en de Vlaamse Uitgevers van Kinder- en Jeugdboeken.',
    'Al tijdens de zwangerschap krijgen de kinderen van meertalige moeders een gevoeligheid voor die verschillende talen mee. Dat hebben onderzoekers van de Universiteit van Barcelona op basis van hersenonderzoek ontdekt. "De hersentjes worden er dus zelfs dan al op ingericht om 1 of 2 talen te verwerken", zegt Sofja Volkova, doctor in taalkunde aan de Universiteit Utrecht.',
    'In Oudenaarde wil het technologisch bedrijf Onsemi sluiten. Er staan 90 banen op de tocht. Onsemi maakt computerchips en heeft ook een afdeling in Mechelen. Daar zijn 16 banen bedreigd. Naast de ontslagen, zouden 63 werknemers van Oudenaarde in Mechelen mogen gaan werken. Onsemi herstructureert om te besparen, efficiënter te werken en sterker te staan in de wereld van de computerchips.',
    'Oud-minister Luc Martens is even opgepakt op verdenking van oplichting, valsheid in geschrifte, misbruik van vertrouwen, gebruik van valse stukken en witwassen. Dat meldt het parket van West-Vlaanderen. Hij is intussen wel vrij onder voorwaarden. "Ik heb niets te verbergen", reageert Martens intussen zelf.',
    'In 2023 kwamen meer dan 13.000 mensen aankloppen bij het CAW (Centrum Algemeen Welzijnswerk) in Limburg. Dat blijkt uit een jaarverslag. Een groot deel van hen had financiële stress of kreeg te maken met dak- en thuisloosheid. Elk jaar stijgt het aantal mensen dat naar de welzijnsorganisatie trekt met een probleem.',
    '"Ik zat in bad toen de brand uitbrak en ben maar net op tijd kunnen ontsnappen. Ik heb mijn thuis zien afbranden." Zanger, acteur en presentator Niels Destadsbader vertelt in het VRT 1-programma \'Niks te zien\' voor het eerst op tv over de brand die zijn loft verwoestte. "Ik slaap er nog altijd heel moeilijk door."',
    "In steeds meer scholen moeten leerlingen vanaf volgend schooljaar hun gsm 's morgens afgeven en krijgen ze die pas op het einde van de dag terug. Ook op GO! campus D'Hek in Landen zijn smartphones vanaf september niet meer welkom. In mei probeerde de school al eens een gsm-vrije week uit. Dat was toen een groot succes, daarom besloot de directie de regel door te trekken naar volgend jaar.",
    "Tijdens de laatste 4 maanden voor de verkiezingen van 9 juni hebben alle politieke partijen samen ruim 7,3 miljoen euro uitgegeven aan advertenties op sociale media. Ruim driekwart daarvan is uitgegeven door Vlaamse partijen. Dat blijkt uit onderzoek van AdLens, een collectief dat politieke advertenties onderzoekt op sociale media. Tom Van Grieken en zijn partij Vlaams Belang blijken met voorsprong de 'big spenders' te zijn.",
    "Al meer dan 112.000 kanshebbers op het hoogste schavot. De Sporza EK-pronostiek wordt tijdens Euro 2024 talk of the town. Aarzel niet om je - net als 14 BV's - te wagen aan een voorspelling. Een voorzetje nodig? Dit zijn alvast de meest gekozen pronostieken van 5 belangrijke groepsmatchen.",
    'In Oostende is het programma voorgesteld voor Theater aan Zee komende zomer. De titel van het festival dit jaar is "neem me mee over golven en generaties". Heel wat voorstellingen en projecten gaan over de manier waarop jong en oud met elkaar omgaan, maar ook over de dingen die we meeslepen uit het verleden en graag zouden overbrengen naar de toekomst.',
    "Langs de Lovaart in Lo-Reninge staat al enkele weken een caravan. Die blijkt niet van een kampeerder of visser te zijn, maar van sluikstorters die hem daar gedumpt hebben. Op de caravan staat 'gratis cadeau', maar het stadsbestuur is allesbehalve blij met het 'cadeau'.",
    'Een combinatie van stijgende grondstofprijzen, een toenemende concurrentie én de coronacrisis: dat ligt aan de basis van de malaise bij Ontex, de luierfabrikant die 500 banen schrapt in Eeklo en Buggenhout. Nochtans leek het het bedrijf tien jaar geleden nog voor de wind te gaan en kon het jaar na jaar winstcijfers optekenen. Hoe kon het zo fout lopen?',
    'Deze zomer wordt op kermis Hondzocht in Lembeek het Belgisch kampioenschap stringschieten gehouden. De wedstrijd werd jarenlang georganiseerd in Teralfene, een deelgemeente van Affligem. "Nu worden ook dezelfde strings als in Teralfene gebruikt", klinkt het.',
    "In China worden steeds meer vrouwen 'verliefd' op DAN, een variant op ChatGPT die kan flirten en seksueel getinte opmerkingen geeft. Het succes komt grotendeels door Lisa, een studente computerwetenschappen van 30. Ze gebruikte DAN eerst als een taalmodel, maar al snel groeide een intieme band. Veel Chinese vrouwen volgen hun liefdesverhaal op sociale media en zoeken nu zelf hun toevlucht tot een AI-vriendje.",
    'Eric Ciotti, de voorzitter van de Franse partij Les Républicains, weigert te vertrekken nadat het partijbestuur hem gisteren uit de partij had gezet. Ciotti wil via de rechtbank bewijzen dat hij nog altijd de voorzitter is.',
    'De vrije basisschool Sint-Paulus in Kortrijk maakt kans op een belangrijke internationale milieuprijs. Sint-Paulus staat in de top 10 van scholen van over de hele wereld die zich inzetten om klimaatvriendelijker te zijn. De school bouwde bijvoorbeeld de hele speelplaats om tot een groene omgeving en startte ook verschillende milieuvriendelijke projecten. In november kennen we de winnaar.',
    'In ons land zijn er opnieuw vier huiszoekingen uitgevoerd in een onderzoek naar een boekhoudkantoor dat andere criminele organisaties financieel advies geeft. Dat laat het parket van Limburg weten. Met die hulp kunnen netwerken dan bijvoorbeeld fiscale fraude plegen of geld witwassen.',
    'In Hoboken wordt na de ontploffing van vanmorgen nog altijd gezocht naar 4 mensen onder het puin. Daarbij worden reddingshonden ingezet die worden getraind in het Rescue Center Vicky en Alexis in Genk. Dat centrum is vernoemd naar Vicky Storms (24) uit Heusden-Zolder en haar verloofde Alexis Robert (24), twee van de slachtoffers bij een gasontploffing in Luik in 2010. Het trainingscentrum werd opgericht door de ouders van de overleden jongeren.',
    'Vier dagen na de verkiezingen zijn al heel wat stappen gezet. Vlaams informateur Bart De Wever (N-VA) zit morgen samen met Melissa Depraetere (Vooruit) en Sammy Mahdi (CD&V) voor gesprekken over de vorming van een Vlaamse regering. De koning heeft De Wever ook federaal het veld ingestuurd als informateur. In Wallonië gaat het nog sneller: MR en Les Engagés zijn al volop bezig met het vormen van een regering. De Duitstalige Gemeenschap heeft intussen al een regering. Volg hier het verkiezingsnieuws op de voet.',
    'Een huisarts maakt gemiddeld 15 minuten tijd voor een consultatie met een patiënt. Het Vlaams Patiëntenplatform vindt dat te kort om persoonlijke en doelgerichte zorg te kunnen bieden. "Artsen moeten oog hebben voor de persoon in zijn geheel, voor meer dan één symptoom", zegt directeur Else Tambuyzer. "Een praktijkassistent aannemen kan dokters meer tijd daarvoor geven."',
    'Op de Staatsbaan in Kortemark is een fietser van 75 uit Hooglede om het leven gekomen. Het slachtoffer werd gevonden door een voorbijganger. De hulpdiensten kwamen ter plaatse, maar alle hulp kwam te laat. Volgens de eerste bevindingen van de verkeersdeskundige werd het slachtoffer aangereden door een voertuig. Of de bestuurder dat opmerkte en dus vluchtmisdrijf pleegde, is onduidelijk.',
    'Op het voetbalpleintje op het Luitenant Naeyaertplein in Borgerhout is het portret van Rode Duivel Jérémy Doku opgedoken. Alle Rode Duivels die geselecteerd zijn voor het EK krijgen een portret op een plek die voor hen belangrijk was in hun jeugd. Doku heeft vaak op het pleintje in Borgerhout gevoetbald.',
    'Journalist Lisbeth Imbo stopt als co-presentator van De Zevende Dag. 6 jaar lang presenteerde ze het VRT-duidingsprogramma, maar aan het einde van dit seizoen geeft ze de fakkel door. Imbo blijft aan de slag als uitgever en als zelfstandig journalist.',
    'De man die in november vorig jaar een studente van 20 verkrachtte, heeft de maximumstraf van 15 jaar cel gekregen. Hij trok haar in de buurt van de Dampoort van haar fiets, sloeg en verkrachtte haar. Omdat hij in zijn thuisland Roemenië al celstraffen had gekregen voor zware zedenfeiten, was de rechter in Gent streng. Na zijn celstraf blijft hij nog 15 jaar onder toezicht van de rechtbank. Hij verliest levenslang zijn burgerrechten. Het slachtoffer moet hij een schadevergoeding van 10.000 euro betalen.',
    'Ondanks de ruk naar rechts tijdens de Europese verkiezingen lijken de fundamenten van het Europees klimaatbeleid overeind te zullen blijven. De tijd van nieuwe, hoge doelstellingen is voorlopig wel voorbij. En het zal nog gaan spannen om enkele symbooldossiers zoals de natuurherstelwet en het verbod op benzinewagens.']
items = [('Tesla-aandeelhouders keuren miljardenbonus voor Musk goed',
          'De aandeelhouders van Tesla hebben op de algemene vergadering opnieuw hun goedkeuring uitgesproken voor een enorm aandelenpakket ter waarde van tientallen miljarden dollar voor bedrijfsbaas Elon Musk.'),
         (
         'Derde dodelijk slachtoffer vanonder het puin gehaald na explosie in Hoboken, hulpdiensten zoeken nog 2 vermisten',
         'In Hoboken is vanavond een derde dodelijk slachtoffer vanonder het puin gehaald na een zware explosie in de Sint-Bernardsesteenweg. De hulpdiensten zoeken nog zeker 2 vermisten in het gebouw. Vanochtend en vanmiddag werden al 2 lichamen geborgen. Bij de explosie raakten ook 5 mensen gewond. De hulpdiensten zijn nog steeds op zoek naar bewoners en evalueren uur per uur of ze verder werken.'),
         ('Linkse partijen in Frankrijk sluiten akkoord over frontvorming voor parlementsverkiezingen',
          "De linkse politieke partijen in Frankrijk hebben donderdagavond een akkoord bereikt over de vorming van een 'Nieuw Volksfront' voor de komende parlementsverkiezingen."),
         ('Groen en Vooruit Mortsel in kartel naar de verkiezingen: “Samen zijn we sterker"',
          'Groen Vooruit, dat is de naam van het nieuwe kartel dat in Mortsel is gevormd voor de gemeenteraadsverkiezingen. Vooruit zat in het gemeentebestuur de afgelopen jaren, Groen in de oppositie. Maar de partijen waren het vaak met elkaar eens, zegt lijsttrekker Michiel Hubeau (Groen). “De 2 partijen willen een progressief beleid. Samen willen we de grootste partij van Mortsel worden.”'),
         ('ANC sluit coalitieakkoord met verschillende partijen in Zuid-Afrika',
          'De Zuid-Afrikaanse partij ANC is met verschillende partijen tot een akkoord gekomen over de vorming van een coalitieregering. Dat is donderdag op een persconferentie medegedeeld.'),
         ('Voordeur beschadigd bij ontploffing in Borgerhout: verdachte opgepakt',
          'In de Maréestraat in Borgerhout heeft een onbekende in de vooravond een projectiel naar een huis gegooid. Dat kwam tot ontploffing en heeft de voordeur beschadigd. Kort na de feiten heeft de politie een verdachte opgepakt.'),
         ('Drie ooievaarsjongen in Stokkem overleden: "Waarschijnlijk door koude weer en hevige regen"',
          'De 3 ooievaarsjongen die midden mei werden geboren in het natuurgebied Negenoord-Kerkeweerd in Dilsen-Stokkem zijn gestorven. Dat schrijft het Belang van Limburg en het nieuws is bevestigd aan onze redactie. Vermoedelijk zijn ze slachtoffer geworden van het koude weer en de hevige regen.'),
         ('Geert Wilders kiest dan toch voor andere minister van Migratie na veiligheidsonderzoek',
          'Gidi Markuszower, een parlementslid van de radicaal-rechtse partij PVV van Geert Wilders, zal dan toch geen minister van Asiel en Migratie worden in de nieuwe Nederlandse regering. Na een veiligheidsonderzoek door de Nederlandse inlichtingendienst AIVD is zijn kandidatuur opnieuw ingetrokken. Dat meldt RTL Nieuws en de informatie is door Wilders ook bevestigd op de sociaalnetwerksite X.'),
         (
         'Akkoord binnen G7 over lening van 50 miljard dollar aan Oekraïne, Biden en Zelenski tekenen veiligheidsakkoord',
         'De leiders van de G7-landen zijn het eens geraakt over een lening van 50 miljard dollar aan Oekraïne. De 7 landen zullen de toekomstige opbrengst van Russisch geblokkeerd geld gebruiken als waarborg voor die lening. In de marge van de G7-top ondertekenden de Verenigde Staten en Oekraïne ook een bilateraal veiligheidsakkoord.'),
         (
         'Pro-Palestijnse actievoerders krijgen van deurwaarder tot 8.30 uur tijd om UGent-gebouw vrijwillig te verlaten: "We gaan in overleg over wat we nu gaan doen"',
         'De pro-Palestijnse actievoerders die al enkele weken een gebouw van de UGent bezetten, hebben officieel het bevel gekregen om het gebouw te verlaten. Rond 20.30 uur heeft de deurwaarder een officieel bevel tot ontruiming overgemaakt. Op dit moment is er nog een 40-tal actievoerders aanwezig in het gebouw. Ze krijgen 12 uur de tijd - ongeveer tot 8.30 dus - om vrijwillig te vertrekken. Het is nog niet duidelijk of ze gehoor zullen geven aan het bevel.'),
         ('Zware brand bij bedrijf in Ieper: rookpluim van ver te zien, evacuatie van bedrijven in de buurt',
          'In Ieper woedt op dit moment een zware industriebrand bij het bedrijf Orgamex. Bij de brand komt een gigantische rookpluim vrij die tot ver buiten Ieper te zien is. De brandweer is massaal ter plaatse en probeert het vuur te blussen.'),
         ('Opnieuw probleem voor Boeing: defect gesignaleerd bij productie Dreamliner-toestellen',
          'Er is opnieuw een probleem opgedoken bij vliegtuigbouwer Boeing. Het bedrijf heeft medegedeeld dat aan het licht is gekomen dat bevestigingsmiddelen niet goed waren vastgemaakt in de romp van nog niet geleverde Dreamliner-vliegtuigen.'),
         ('Grote brand en ontploffing in loods op terrein Brucargo in Machelen na dakwerken',
          'Er is een zware brand uitgebroken in een loods op de terreinen van Brucargo, de vrachtafdeling van Brussels Airport in Machelen. De brand is ontstaan door dakwerken, er was ook een ontploffing. Voorlopig is er geen sprake van slachtoffers. De omgeving is afgesloten.'),
         (
         'Waait Franse MeToo-beweging over naar Belgische filmindustrie? Regisseur Joachim Lafosse beschuldigd van grensoverschrijdend gedrag',
         'Een tiental oud-medewerkers van Joachim Lafosse beschuldigt de Brusselse regisseur van morele of seksuele intimidatie op de set. Heeft het MeToo-protest uit de Franse filmindustrie ook ons land bereikt? “Als het regent in Frankrijk, druppelt het ook in Franstalig België”, zegt filmjournalist Lieven Trio.'),
         ('Cabaretier Willy Lustenhouwer krijgt tegel aan Stadsschouwburg in Brugge',
          'Voor de Koninklijke Stadsschouwburg van Brugge is een tegel onthuld als eerbetoon aan cabaretier Willy Lustenhouwer. Hij is onder meer bekend van het nummer ‘Zie je van Brugge’. Lustenhouwer heeft bovendien veel betekend voor de stadsschouwburg.'),
         ('Belgische brouwers moeten afrekenen met historische daling bierexport',
          'Zowel de binnenlandse bierconsumptie als de export daalde vorig jaar sterk. Dat meldt sectorkoepel Belgische Brouwers woensdag bij de publicatie van het jaarverslag. Voor de export is sprake van een historische daling. De brouwers verwijzen naar de inflatie, koopkrachtcrisis en een personeelstekort.'),
         ('Hongarije moet 1 miljoen euro per dag betalen zolang het de Europese migratieregels niet naleeft',
          'Hongarije moet een boete van 200 miljoen euro betalen, omdat het land met opzet weigert om de Europese regels rond migratie na te leven. Dat heeft het Europees Hof van Justitie geoordeeld. Hongarije moet bovenop die boete ook 1 miljoen euro per dag betalen, zolang het de EU-regels niet naleeft.'),
         (
         'Kloof tussen Vooruit en centrumrechtse partijen is Vlaams groter dan federaal, blijkt uit De Stemtest (al zegt dat niet alles)',
         'De kloof tussen Vooruit en de centrumrechtse partijen is groter op Vlaams niveau dan op federaal niveau. Dat blijkt uit De Stemtest. Nochtans aarzelt kopstuk Conner Rousseau meer over een federale regeringsdeelname dan een Vlaamse. "Maar er zijn belangrijke nuances", zegt professor politieke communicatie Jonas Lefevere.'),
         ('Kledingketen Scotch & Soda jaar na doorstart weer failliet',
          'Het van oorsprong Nederlandse modemerk Scotch & Soda is ruim een jaar na een doorstart opnieuw failliet, meldt het bedrijf. Het merk ging al eens failliet, maar werd in maart vorig jaar overgenomen door Bluestar Alliance, een Amerikaanse onderneming die meerdere modemerken bezit. Dit keer is ook voor de vestigingen in ons land, maar ook Duitsland, Luxemburg en Oostenrijk het faillissement aangevraagd.'),
         ('Molen van Doel komt opnieuw boven op de Scheldedijk: "We geven hem weer de uitstraling van vroeger"\xa0',
          'In de loop van volgend jaar zal de molen van Doel bij Beveren op de dijk staan in plaats van ernaast. De Maatschappij Linker Schelde Oever (MLSO) is eigenaar van de molen, en gaat in op een vraag van de Dienst Onroerend Erfgoed. Die wil niet dat de nieuwe brasserie boven de molen uitkomt. "Door de molen naar de dijk te verhuizen, zal die zeker goed tot zijn recht komen", luidt het bij MLSO.'),
         (
         'Ontploffing in Hoboken brengt nare herinneringen naar boven rond Paardenmarkt en in Wilrijk: "De nachtmerrie komt terug"',
         'Een ontploffing die een woning vernielt en waarbij doden vallen, het brengt nare herinneringen naar boven. Dat zeggen buurtbewoners van de Paardenmarkt in Antwerpen en het Ridderveld in Wilrijk waar in 2018 en in 2019 een explosie plaatsvond, na het drama in Hoboken. "De nachtmerrie komt terug."'),
         ('Vier dagen na verkiezingen heeft Duitstalige Gemeenschap nieuwe regering: Paasch blijft aan het roer',
          'Vier dagen na de verkiezingen heeft de Duitstalige Gemeenschap al een nieuwe regering. De regionalistische ProDG van minister-president Oliver Paasch gaat in zee met de christendemocratische CSP en de liberale PFF. De socialistische SP verhuist voor het eerst sinds 1990 naar de oppositiebanken.'),
         ('8 EU-landen willen bewegingsvrijheid van Russische diplomaten in Schengenzone beperken',
          '8 EU-ministers van Buitenlandse Zaken willen de bewegingsvrijheid van Russische diplomaten in de Schengenzone beperken. Zo willen ze het moeilijker maken voor de diplomaten om "kwaadwillige acties" uit te voeren tegen de Europese Unie.'),
         ('Brouwerij in Pelt en bakkerij in Bocholt maken bier van oud stokbrood: "Licht blond bier met moutige smaak"',
          'Om voedselverspilling tegen te gaan hebben Bakkerij Knapen in Bocholt en de Microbrouwerij Mølder & Coöp in Pelt samengewerkt aan een nieuw bier met de naam "De Glazen Boterham". Dat bier is gemaakt van verloren brood, ofwel stokbrood dat na 1 dag wordt weggegooid. "Als we producten die we weggooien terug kunnen gebruiken, dan zijn we goed bezig", vindt bakker Jack Knapen.'),
         ('Amerikaans Hooggerechtshof verwerpt poging om toegang tot veelgebruikte abortuspil te beperken',
          'In de Verenigde Staten heeft het Hooggerechtshof geoordeeld dat het gebruik van mifepriston, een veelgebruikte abortuspil, niet mag worden beperkt. Volgens het hof hadden de aanklagers, een groep anti-abortusartsen en activisten, geen wettelijke grond om een zaak aan te spannen.'),
         ('Juf Sofie van basisschool in Neder-Over-Heembeek doet kinderen weer boeken lezen: "Lezen is gewoon plezant"',
          '3 juffen uit het basisonderwijs zijn verkozen tot boekenjuf in 2024. Deze prijs beloont leerkrachten die hun leerlingen stimuleren om te lezen. De winnaars zijn Sofie Glorieus uit Neder-Over-Heembeek, Els De Latter uit Gent en Marianne Flour uit Hoboken. Het is een initiatief van onder andere de stichting Iedereen Leest en de Vlaamse Uitgevers van Kinder- en Jeugdboeken.'),
         ('Oh yes, bien sûr!\xa0Meertaligheid begint al in de buik, blijkt uit onderzoek',
          'Al tijdens de zwangerschap krijgen de kinderen van meertalige moeders een gevoeligheid voor die verschillende talen mee. Dat hebben onderzoekers van de Universiteit van Barcelona op basis van hersenonderzoek ontdekt. "De hersentjes worden er dus zelfs dan al op ingericht om 1 of 2 talen te verwerken", zegt Sofja Volkova, doctor in taalkunde aan de Universiteit Utrecht.'),
         ('Computerchipbedrijf Onsemi wil afdeling Oudenaarde sluiten, ook gevolgen voor afdeling Mechelen\xa0\xa0',
          'In Oudenaarde wil het technologisch bedrijf Onsemi sluiten. Er staan 90 banen op de tocht. Onsemi maakt computerchips en heeft ook een afdeling in Mechelen. Daar zijn 16 banen bedreigd. Naast de ontslagen, zouden 63 werknemers van Oudenaarde in Mechelen mogen gaan werken. Onsemi herstructureert om te besparen, efficiënter te werken en sterker te staan in de wereld van de computerchips.'),
         (
         'Oud-minister Luc Martens opgepakt op verdenking van oplichting en witwassen: "Ik heb nog nooit iemand bestolen, waarom zou ik dat op mijn 78 wél doen?"',
         'Oud-minister Luc Martens is even opgepakt op verdenking van oplichting, valsheid in geschrifte, misbruik van vertrouwen, gebruik van valse stukken en witwassen. Dat meldt het parket van West-Vlaanderen. Hij is intussen wel vrij onder voorwaarden. "Ik heb niets te verbergen", reageert Martens intussen zelf.'),
         (
         '13.000 Limburgers klopten vorig jaar aan bij CAW: "Veel financiële stress, dakloosheid en drugsproblematiek"',
         'In 2023 kwamen meer dan 13.000 mensen aankloppen bij het CAW (Centrum Algemeen Welzijnswerk) in Limburg. Dat blijkt uit een jaarverslag. Een groot deel van hen had financiële stress of kreeg te maken met dak- en thuisloosheid. Elk jaar stijgt het aantal mensen dat naar de welzijnsorganisatie trekt met een probleem.'),
         ('"Slapen is nog altijd moeilijk": Niels Destadsbader blikt terug op brand die zijn loft verwoestte',
          '"Ik zat in bad toen de brand uitbrak en ben maar net op tijd kunnen ontsnappen. Ik heb mijn thuis zien afbranden." Zanger, acteur en presentator Niels Destadsbader vertelt in het VRT 1-programma \'Niks te zien\' voor het eerst op tv over de brand die zijn loft verwoestte. "Ik slaap er nog altijd heel moeilijk door."'),
         ('Atheneum in Landen verbiedt vanaf volgend schooljaar gsm-gebruik: "Leerlingen vinden het een goed idee"',
          "In steeds meer scholen moeten leerlingen vanaf volgend schooljaar hun gsm 's morgens afgeven en krijgen ze die pas op het einde van de dag terug. Ook op GO! campus D'Hek in Landen zijn smartphones vanaf september niet meer welkom. In mei probeerde de school al eens een gsm-vrije week uit. Dat was toen een groot succes, daarom besloot de directie de regel door te trekken naar volgend jaar."),
         ('Politieke partijen hebben tijdens campagne ruim 7,3 miljoen euro uitgegeven aan online-advertenties',
          "Tijdens de laatste 4 maanden voor de verkiezingen van 9 juni hebben alle politieke partijen samen ruim 7,3 miljoen euro uitgegeven aan advertenties op sociale media. Ruim driekwart daarvan is uitgegeven door Vlaamse partijen. Dat blijkt uit onderzoek van AdLens, een collectief dat politieke advertenties onderzoekt op sociale media. Tom Van Grieken en zijn partij Vlaams Belang blijken met voorsprong de 'big spenders' te zijn."),
         ('Al meer dan 100.000 spelers wagen zich aan de Sporza EK-pronostiek: doe zelf ook mee!',
          "Al meer dan 112.000 kanshebbers op het hoogste schavot. De Sporza EK-pronostiek wordt tijdens Euro 2024 talk of the town. Aarzel niet om je - net als 14 BV's - te wagen aan een voorspelling. Een voorzetje nodig? Dit zijn alvast de meest gekozen pronostieken van 5 belangrijke groepsmatchen."),
         ('Theater aan Zee in Oostende wil bruggen bouwen tussen generaties ',
          'In Oostende is het programma voorgesteld voor Theater aan Zee komende zomer. De titel van het festival dit jaar is "neem me mee over golven en generaties". Heel wat voorstellingen en projecten gaan over de manier waarop jong en oud met elkaar omgaan, maar ook over de dingen die we meeslepen uit het verleden en graag zouden overbrengen naar de toekomst.'),
         ('Caravan langs Lovaart in Lo-Reninge is niet van kampeerder, maar van sluikstorters',
          "Langs de Lovaart in Lo-Reninge staat al enkele weken een caravan. Die blijkt niet van een kampeerder of visser te zijn, maar van sluikstorters die hem daar gedumpt hebben. Op de caravan staat 'gratis cadeau', maar het stadsbestuur is allesbehalve blij met het 'cadeau'."),
         (
         'Van grootste producent van luiers en maandverband in Europa tot herstructureringen en banenverlies: hoe het fout liep met Ontex',
         'Een combinatie van stijgende grondstofprijzen, een toenemende concurrentie én de coronacrisis: dat ligt aan de basis van de malaise bij Ontex, de luierfabrikant die 500 banen schrapt in Eeklo en Buggenhout. Nochtans leek het het bedrijf tien jaar geleden nog voor de wind te gaan en kon het jaar na jaar winstcijfers optekenen. Hoe kon het zo fout lopen?'),
         (
         'Lembeek organiseert Belgisch kampioenschap stringschieten: "Wij proberen altijd met iets origineels uit te pakken"',
         'Deze zomer wordt op kermis Hondzocht in Lembeek het Belgisch kampioenschap stringschieten gehouden. De wedstrijd werd jarenlang georganiseerd in Teralfene, een deelgemeente van Affligem. "Nu worden ook dezelfde strings als in Teralfene gebruikt", klinkt het.'),
         ("Van chatbot tot vriendje: steeds meer Chinese vrouwen worden 'verliefd' op AI-bot DAN",
          "In China worden steeds meer vrouwen 'verliefd' op DAN, een variant op ChatGPT die kan flirten en seksueel getinte opmerkingen geeft. Het succes komt grotendeels door Lisa, een studente computerwetenschappen van 30. Ze gebruikte DAN eerst als een taalmodel, maar al snel groeide een intieme band. Veel Chinese vrouwen volgen hun liefdesverhaal op sociale media en zoeken nu zelf hun toevlucht tot een AI-vriendje."),
         ('Voorzitter Franse Les Républicains weigert te vertrekken en vecht ontslag aan voor de rechtbank',
          'Eric Ciotti, de voorzitter van de Franse partij Les Républicains, weigert te vertrekken nadat het partijbestuur hem gisteren uit de partij had gezet. Ciotti wil via de rechtbank bewijzen dat hij nog altijd de voorzitter is.'),
         ('Vrije basisschool Sint-Paulus in Kortrijk maakt kans op belangrijke internationale milieuprijs',
          'De vrije basisschool Sint-Paulus in Kortrijk maakt kans op een belangrijke internationale milieuprijs. Sint-Paulus staat in de top 10 van scholen van over de hele wereld die zich inzetten om klimaatvriendelijker te zijn. De school bouwde bijvoorbeeld de hele speelplaats om tot een groene omgeving en startte ook verschillende milieuvriendelijke projecten. In november kennen we de winnaar.'),
         (
         'Spookbedrijven en valse facturen voor meer dan 4 miljoen: opnieuw huiszoekingen in onderzoek naar boekhoudkantoor dat criminele bendes zou bijstaan',
         'In ons land zijn er opnieuw vier huiszoekingen uitgevoerd in een onderzoek naar een boekhoudkantoor dat andere criminele organisaties financieel advies geeft. Dat laat het parket van Limburg weten. Met die hulp kunnen netwerken dan bijvoorbeeld fiscale fraude plegen of geld witwassen.'),
         ('Ook Limburgse reddingshonden ingezet in zoekactie naar slachtoffers bij explosie in Hoboken',
          'In Hoboken wordt na de ontploffing van vanmorgen nog altijd gezocht naar 4 mensen onder het puin. Daarbij worden reddingshonden ingezet die worden getraind in het Rescue Center Vicky en Alexis in Genk. Dat centrum is vernoemd naar Vicky Storms (24) uit Heusden-Zolder en haar verloofde Alexis Robert (24), twee van de slachtoffers bij een gasontploffing in Luik in 2010. Het trainingscentrum werd opgericht door de ouders van de overleden jongeren.'),
         (
         'Liveblog verkiezingen: Filip Dewinter ziet rooskleurige toekomst voor Jos D\'Haese: "U wordt een van de volgende burgemeesters van Antwerpen"',
         'Vier dagen na de verkiezingen zijn al heel wat stappen gezet. Vlaams informateur Bart De Wever (N-VA) zit morgen samen met Melissa Depraetere (Vooruit) en Sammy Mahdi (CD&V) voor gesprekken over de vorming van een Vlaamse regering. De koning heeft De Wever ook federaal het veld ingestuurd als informateur. In Wallonië gaat het nog sneller: MR en Les Engagés zijn al volop bezig met het vormen van een regering. De Duitstalige Gemeenschap heeft intussen al een regering. Volg hier het verkiezingsnieuws op de voet.'),
         ('Patiënt krijgt gemiddeld 15 minuten bij de huisarts: "Dat is te kort voor kwaliteitsvolle consultatie"',
          'Een huisarts maakt gemiddeld 15 minuten tijd voor een consultatie met een patiënt. Het Vlaams Patiëntenplatform vindt dat te kort om persoonlijke en doelgerichte zorg te kunnen bieden. "Artsen moeten oog hebben voor de persoon in zijn geheel, voor meer dan één symptoom", zegt directeur Else Tambuyzer. "Een praktijkassistent aannemen kan dokters meer tijd daarvoor geven."'),
         ('Fietser sterft bij aanrijding in Kortemark: onduidelijk wie man aanreed',
          'Op de Staatsbaan in Kortemark is een fietser van 75 uit Hooglede om het leven gekomen. Het slachtoffer werd gevonden door een voorbijganger. De hulpdiensten kwamen ter plaatse, maar alle hulp kwam te laat. Volgens de eerste bevindingen van de verkeersdeskundige werd het slachtoffer aangereden door een voertuig. Of de bestuurder dat opmerkte en dus vluchtmisdrijf pleegde, is onduidelijk.'),
         ('Straattekening Rode Duivel Jérémy Doku duikt op in Borgerhout',
          'Op het voetbalpleintje op het Luitenant Naeyaertplein in Borgerhout is het portret van Rode Duivel Jérémy Doku opgedoken. Alle Rode Duivels die geselecteerd zijn voor het EK krijgen een portret op een plek die voor hen belangrijk was in hun jeugd. Doku heeft vaak op het pleintje in Borgerhout gevoetbald.'),
         ('Lisbeth Imbo stopt als co-presentator van De Zevende Dag',
          'Journalist Lisbeth Imbo stopt als co-presentator van De Zevende Dag. 6 jaar lang presenteerde ze het VRT-duidingsprogramma, maar aan het einde van dit seizoen geeft ze de fakkel door. Imbo blijft aan de slag als uitgever en als zelfstandig journalist.'),
         ('Maximumstraf van 15 jaar cel voor Roemeen die studente in Gent verkrachtte',
          'De man die in november vorig jaar een studente van 20 verkrachtte, heeft de maximumstraf van 15 jaar cel gekregen. Hij trok haar in de buurt van de Dampoort van haar fiets, sloeg en verkrachtte haar. Omdat hij in zijn thuisland Roemenië al celstraffen had gekregen voor zware zedenfeiten, was de rechter in Gent streng. Na zijn celstraf blijft hij nog 15 jaar onder toezicht van de rechtbank. Hij verliest levenslang zijn burgerrechten. Het slachtoffer moet hij een schadevergoeding van 10.000 euro betalen.'),
         (
         'Minder praten over klimaat, meer over industrie: dit blijft over van de Europese Green Deal na de verkiezingen',
         'Ondanks de ruk naar rechts tijdens de Europese verkiezingen lijken de fundamenten van het Europees klimaatbeleid overeind te zullen blijven. De tijd van nieuwe, hoge doelstellingen is voorlopig wel voorbij. En het zal nog gaan spannen om enkele symbooldossiers zoals de natuurherstelwet en het verbod op benzinewagens.')]

create_quote(quote, author)
create_date(dayword, day, month, h, m)
create_news(titles)
