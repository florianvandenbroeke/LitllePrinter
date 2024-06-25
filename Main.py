import copy

from PIL import Image, ImageDraw, ImageFont, ImageOps
from dogtest import get_dog

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
paper = "Paper Banner.ttf"
party = "Party.ttf"


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

    def center_paste(self, im):
        x = (384 - im.width) // 2
        self.image.paste(im, box=(x, self.current_h))
        self.current_h += im.height

    def add_whitespace(self, space):
        self.current_h += space

    def draw_center_text(self, text, font, size, add_offset=0, spacing=4):
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


    def show(self):
        self.image = self.image.crop((0, 0, self.width, self.current_h))
        # self.image.show()


def stitch_images(imagelist):

    totalheight = sum([image.height for image in imagelist])
    height = 0

    image = Image.new("RGB", (384, totalheight), "white")

    for im in imagelist:
        image.paste(im, box=(0, height))
        height += im.height

    image.show()


def create_date(dayword, day, month, h, m):
    frame = Frame()

    frame.add_whitespace(25)
    frame.draw_width(dayword, franchise, 320)
    frame.add_whitespace(15)
    frame.draw_width(f"{day} {month} | {h}:{m}", futura, 320)
    frame.add_whitespace(10)

    frame.show()

    return frame.image


def create_quote(quote, author):
    frame = Frame()

    frame.paste_im("Images/dot_line.png")
    frame.add_whitespace(20)
    frame.paste_im("Images/quote_header.png")
    frame.add_whitespace(20)
    frame.text_wrap(quote, normal, 35, 300)
    frame.add_whitespace(10)
    frame.text_wrap(f"- {author}", product, 20, 100, alignment="r", offset=15)
    frame.add_whitespace(20)

    frame.show()

    return frame.image


def create_news(items):
    frame = Frame()

    frame.paste_im("Images/dot_line.png")
    frame.add_whitespace(20)
    frame.paste_im("Images/news_header.png")
    frame.add_whitespace(20)

    for i in range(3):
        frame.text_wrap(items[i], clab , 20, 350, "r" * (i % 2) + "l" * (not i % 2), 15, spacing=4)
        frame.add_whitespace(16)

    frame.show()

    return frame.image


def create_birthdays(birhdays):

    frame = Frame()

    frame.add_whitespace(5)
    frame.draw_center_text("[BIRTHDAYS]", paper, 46)
    frame.add_whitespace(10)

    for name in birhdays:
        frame.text_wrap(name, party, 45, 200)
        frame.add_whitespace(10)

    frame.show()

    return frame.image


def create_dog(dog_im):

    frame = Frame()

    frame.paste_im("Images/dot_line.png")
    frame.add_whitespace(20)
    frame.paste_im("Images/dog_header.png")
    frame.add_whitespace(20)

    image_width = 280
    scale_factor = dog_im.width / image_width
    new_height = dog_im.height / scale_factor
    dog_im = dog_im.resize((image_width, round(new_height)))

    dog_im = ImageOps.expand(dog_im, 5)

    frame.center_paste(dog_im)
    frame.add_whitespace(10)



    frame.show()

    return frame.image


quote = "\"Ik haat honden, behalve als ze tussen een broodje liggen.\""
author = "Matthijs"
dayword, day, month, h, m = "Tuesday", "25", "June", "15", "47"
birthdays = ["Max", "Florian"]
dog = get_dog()

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

quote_image = create_quote(quote, author)
date_image = create_date(dayword, day, month, h, m)
news_image = create_news(titles)
birthdays_image = create_birthdays(birthdays)
dog_image = create_dog(dog)

stitch_images([date_image, birthdays_image, news_image, quote_image, dog_image])
