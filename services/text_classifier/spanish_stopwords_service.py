STOPWORDS_ESPANOL = """
a al algo algunas algunos ante antes como con contra cual cuando de del
desde donde durante e el ella ellas ellos en entre era erais eramos eran
eras eres es esa esas ese eso esos esta estaba estabais estabamos estaban
estabas estad estada estadas estado estados estais estamos estan estar
estara estaran estaras estare estareis estaremos estaria estariais
estariamos estarian estarias estas este esto estos estoy estuve estuviera
estuvierais estuvieramos estuvieran estuvieras estuvieron estuviese
estuvieseis estuviesemos estuviesen estuvieses estuvimos estuviste
estuvisteis estuvo fue fuera fuerais fueramos fueran fueras fueron fuese
fueseis fuesemos fuesen fueses fui fuimos ha habeis habia habiais
habiamos habian habias habida habidas habido habidos habiendo han has
hasta hay haya hayais hayamos hayan hayas he hemos hube hubiera hubierais
hubieramos hubieran hubieras hubieron hubiese hubieseis hubiesemos
hubiesen hubieses hubimos hubiste hubisteis hubo la las le les lo los mas
me mi mia mias mientras mio mios mis mucho muchos muy nada ni no nos
nosotras nosotros nuestra nuestras nuestro nuestros o os otra otras otro
otros para pero poco por porque que quien quienes que se sea seais
seamos sean seas sentid sentida sentidas sentido sentidos ser sera seran
seras sere sereis seremos seria seriais seriamos serian serias si siente
sin sintiendo sobre sois somos son soy su sus suya suyas suyo suyos tal
tambien tanto te tendra tendran tendras tendre tendreis tendremos
tendria tendriais tendriamos tendrian tendrias tened teneis tenemos
tenga tengais tengamos tengan tengas tengo tenia teniais teniamos
tenian tenias tenida tenidas tenido tenidos teniendo ti tiene tienen
tienes todo todos tu tus tuve tuviera tuvierais tuvieramos tuvieran
tuvieras tuvieron tuviese tuvieseis tuviesemos tuviesen tuvieses
tuvimos tuviste tuvisteis tuvo tuya tuyas tuyo tuyos un una uno unos
vosostras vosotros vuestra vuestras vuestro vuestros y ya yo
"""


class SpanishStopwordsService:
    """Provee la lista propia de stopwords en español usada por el TF-IDF."""

    def get(self) -> list[str]:
        return STOPWORDS_ESPANOL.split()
