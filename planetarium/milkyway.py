import math as mt

import numscrypt as ns

import transforms as tf

__pragma__ ('opov')

twoPi = 2 * mt.pi
halfPi = mt.pi / 2

hourFactor = twoPi/ 24
minuteFactor = hourFactor / 60
degreeFactor = twoPi / 360

skyRadius = 1e20

starCatalogue = '''
    Alpha Canis Majoris        Sirius                 6  45  -16.7  -1.44
    Alpha Carinae              Canopus                6  24  -52.7  -0.62
    Alpha Centauri             Rigil Kentaurus       14  40  -60.8  -0.27
    Alpha Bootis               Arcturus              14  16   19.2  -0.05
    Alpha Lyrae                Vega                  18  37   38.8   0.03
    Alpha Aurigae              Capella                5  17   46.0   0.08
    Beta Orionis               Rigel                  5  15   -8.2   0.18
    Alpha Canis Minoris        Procyon                7  39    5.2   0.40
    Alpha Eridani              Achernar               1  38  -57.2   0.45
    Alpha Orionis              Betelgeuse             5  55    7.4   0.45
    Beta Centauri              Hadar                 14   4  -60.4   0.61
    Alpha Aquilae              Altair                19  51    8.9   0.76
    Alpha Crucis               Acrux                 12  27  -63.1   0.77
    Alpha Tauri                Aldebaran              4  36   16.5   0.87
    Alpha Virginis             Spica                 13  25  -11.2   0.98
    Alpha Scorpii              Antares               16  29  -26.4   1.06
    Beta Geminorum             Pollux                 7  45   28.0   1.16
    Alpha Piscis Austrini      Fomalhaut             22  58  -29.6   1.17
    Beta Crucis                Mimosa                12  48  -59.7   1.25
    Alpha Cygni                Deneb                 20  41   45.3   1.25
    Alpha Leonis               Regulus               10   8   12.0   1.36
    Epsilon Canis Majoris      Adhara                 6  59  -29.0   1.50
    Alpha Geminorum            Castor                 7  35   31.9   1.58
    Gamma Crucis               Gacrux                12  31  -57.1   1.59
    Lambda Scorpii             Shaula                17  34  -37.1   1.62
    Gamma Orionis              Bellatrix              5  25    6.3   1.64
    Beta Tauri                 Elnath                 5  26   28.6   1.65
    Beta Carinae               Miaplacidus            9  13  -69.7   1.67
    Epsilon Orionis            Alnilam                5  36   -1.2   1.69
    Alpha Gruis                Alnair                22   8  -47.0   1.73
    Zeta Orionis               Alnitak                5  41   -1.9   1.74
    Gamma Velorum              Regor                  8  10  -47.3   1.75
    Epsilon Ursae Majoris      Alioth                12  54   56.0   1.76
    Alpha Persei               Mirfak                 3  24   49.9   1.79
    Epsilon Sagittarii         Kaus Australis        18  24  -34.4   1.79
    Alpha Ursae Majoris        Dubhe                 11  04   61.8   1.81
    Delta Canis Majoris        Wezen                  7   8  -26.4   1.83
    Eta Ursae Majoris          Alkaid                13  48   49.3   1.85
    Epsilon Carinae            Avior                  8  23  -59.5   1.86
    Theta Scorpii              Sargas                17  37  -43.0   1.86
    Beta Aurigae               Menkalinan             6   0   44.9   1.90
    Alpha Trianguli Australis  Atria                 16  49  -69.0   1.91
    Gamma Geminorum            Alhena                 6  38   16.4   1.93
    Delta Velorum              Koo She                8  45  -54.7   1.93
    Alpha Pavonis              Peacock               20  26  -56.7   1.94
    Alpha Ursae Minoris        Polaris                2  32   89.3   1.97
    Beta Canis Majoris         Mirzam                 6  23  -18.0   1.98
    Alpha Hydrae               Alphard                9  28   -8.7   1.99
    Alpha Arietis              Hamal                  2   7   23.5   2.01
    Gamma Leonis               Algieba               10  20   19.8   2.01
    Beta Ceti                  Diphda                 0  44  -18.0   2.04
    Sigma Sagittarii           Nunki                 18  55  -26.3   2.05
    Theta Centauri             Menkent               14   7  -36.4   2.06
    Alpha Andromedae           Alpheratz              0   8   29.1   2.07
    Beta Andromedae            Mirach                 1  10   35.6   2.07
    Kappa Orionis              Saiph                  5  48   -9.7   2.07
    Beta Ursae Minoris         Kochab                14  51   74.2   2.07
    Beta Gruis                 Al Dhanab             22  43  -46.9   2.07
    Alpha Ophiuchi             Rasalhague            17  35   12.6   2.08
    Beta Persei                Algol                  3   8   41.0   2.09
    Gamma Andromedae           Almach                 2   4   42.3   2.10
    Beta Leonis                Denebola              11  49   14.6   2.14
    Gamma Cassiopeiae          Cih                    0  57   60.7   2.15
    Gamma Centauri             Muhlifain             12  42  -49.0   2.20
    Zeta Puppis                Naos                   8   4  -40.0   2.21
    Iota Carinae               Aspidiske              9  17  -59.3   2.21
    Alpha Coronae Borealis     Alphecca              15  35   26.7   2.22
    Lambda Velorum             Suhail                 9   8  -43.4   2.23
    Zeta Ursae Majoris         Mizar                 13  24   54.9   2.23
    Gamma Cygni                Sadr                  20  22   40.3   2.23
    Alpha Cassiopeiae          Schedar                0  41   56.5   2.24
    Gamma Draconis             Eltanin               17  57   51.5   2.24
    Delta Orionis              Mintaka                5  32   -0.3   2.25
    Beta Cassiopeiae           Caph                   0   9   59.2   2.28
    Epsilon Centauri           -                     13  40  -53.5   2.29
    Delta Scorpii              Dschubba              16   0  -22.6   2.29
    Epsilon Scorpii            Wei                   16  50  -34.3   2.29
    Alpha Lupi                 Men                   14  42  -47.4   2.30
    Eta Centauri               -                     14  36  -42.2   2.33
    Beta Ursae Majoris         Merak                 11   2   56.4   2.34
    Epsilon Bootis             Izar                  14  45   27.1   2.35
    Epsilon Pegasi             Enif                  21  44    9.9   2.38
    Kappa Scorpii              Girtab                17  42  -39.0   2.39
    Alpha Phoenicis            Ankaa                  0  26  -42.3   2.40
    Gamma Ursae Majoris        Phecda                11  54   53.7   2.41
    Eta Ophiuchi               Sabik                 17  10  -15.7   2.43
    Beta Pegasi                Scheat                23   4   28.1   2.44
    Eta Canis Majoris          Aludra                07  24  -29.3   2.45
    Alpha Cephei               Alderamin             21  19   62.6   2.45
    Kappa Velorum              Markeb                 9  22  -55.0   2.47
    Epsilon Cygni              Gienah                20  46   34.0   2.48
    Alpha Pegasi               Markab                23  05   15.2   2.49
    Alpha Ceti                 Menkar                 3   2    4.1   2.54
    Zeta Ophiuchi              Han                   16  37  -10.6   2.54
    Zeta Centauri              Al Nair al Kentaurus  13  56  -47.3   2.55
    Delta Leonis               Zosma                 11  14   20.5   2.56
    Beta Scorpii               Graffias              16  05  -19.8   2.56
    Alpha Leporis              Arneb                  5  33  -17.8   2.58
    Delta Centauri             -                     12   8  -50.7   2.58
    Gamma Corvi                Gienah Ghurab         12  16  -17.5   2.58
    Zeta Sagittarii            Ascella               19   3  -29.9   2.60
    Beta Librae                Zubeneschamali        15  17   -9.4   2.61
    Alpha Serpentis            Unukalhai             15  44    6.4   2.63
    Beta Arietis               Sheratan               1  55   20.8   2.64
    Alpha Librae               Zubenelgenubi         14  51  -16.0   2.64
    Alpha Columbae             Phact                  5  40  -34.1   2.65
    Theta Aurigae              -                      6   0   37.2   2.65
    Beta Corvi                 Kraz                  12  34  -23.4   2.65
    Delta Cassiopeiae          Ruchbah                1  26   60.2   2.66
    Eta Bootis                 Muphrid               13  55   18.4   2.68
    Beta Lupi                  Ke Kouan              14  59  -43.1   2.68
    Iota Aurigae               Hassaleh               4  57   33.2   2.69
    Mu Velorum                 -                     10  47  -49.4   2.69
    Alpha Muscae               -                     12  37  -69.1   2.69
    Upsilon Scorpii            Lesath                17  31  -37.3   2.70
    Pi Puppis                  -                      7  17  -37.1   2.71
    Delta Sagittarii           Kaus Meridionalis     18  21  -29.8   2.72
    Gamma Aquilae              Tarazed               19  46   10.6   2.72
    Delta Ophiuchi             Yed Prior             16  14   -3.7   2.73
    Eta Draconis               Aldhibain             16  24   61.5   2.73
    Theta Carinae              -                     10  43  -64.4   2.74
    Gamma Virginis             Porrima               12  42   -1.5   2.74
    Iota Orionis               Hatysa                 5  35   -5.9   2.75
    Iota Centauri              -                     13  21  -36.7   2.75
    Beta Ophiuchi              Cebalrai              17  43    4.6   2.76
    Beta Eridani               Kursa                  5  08   -5.1   2.78
    Beta Herculis              Kornephoros           16  30   21.5   2.78
    Delta Crucis               -                     12  15  -58.7   2.79
    Beta Draconis              Rastaban              17  30   52.3   2.79
    Alpha Canum Venaticorum    Cor Caroli            12  56   38.3   2.80
    Gamma Lupi                 -                     15  35  -41.2   2.80
    Beta Leporis               Nihal                  5  28  -20.8   2.81
    Zeta Herculis              Rutilicus             16  41   31.6   2.81
    Beta Hydri                 -                      0  26  -77.3   2.82
    Tau Scorpii                -                     16  36  -28.2   2.82
    Lambda Sagittarii          Kaus Borealis         18  28  -25.4   2.82
    Gamma Pegasi               Algenib                0  13   15.2   2.83
    Rho Puppis                 Turais                 8   8  -24.3   2.83
    Beta Trianguli Australis   -                     15  55  -63.4   2.83
    Zeta Persei                -                      3  54   31.9   2.84
    Beta Arae                  -                     17  25  -55.5   2.84
    Alpha Arae                 Choo                  17  32  -49.9   2.84
    Eta Tauri                  Alcyone                3  47   24.1   2.85
    Epsilon Virginis           Vindemiatrix          13   2   11.0   2.85
    Delta Capricorni           Deneb Algedi          21  47  -16.1   2.85
    Alpha Hydri                Head of Hydrus         1  59  -61.6   2.86
    Delta Cygni                -                     19  45   45.1   2.86
    Mu Geminorum               Tejat                  6  23   22.5   2.87
    Gamma Trianguli Australis  -                     15  19  -68.7   2.87
    Alpha Tucanae              -                     22  19  -60.3   2.87
    Theta Eridani              Acamar                 2  58  -40.3   2.88
    Pi Sagittarii              Albaldah              19  10  -21.0   2.88
    Beta Canis Minoris         Gomeisa                7  27   08.3   2.89
    Pi Scorpii                 -                     15  59  -26.1   2.89
    Epsilon Persei             -                      3  58   40.0   2.90
    Sigma Scorpii              Alniyat               16  21  -25.6   2.90
    Beta Cygni                 Albireo               19  31   28.0   2.90
    Beta Aquarii               Sadalsuud             21  32  -05.6   2.90
    Gamma Persei               -                      9  47  -65.1   2.92
    Eta Pegasi                 Matar                 22  43   30.2   2.93
    Tau Puppis                 -                      6  50  -50.6   2.94
    Delta Corvi                Algorel               12  30  -16.5   2.94
    Alpha Aquarii              Sadalmelik            22   6   -0.3   2.95
    Gamma Eridani              Zaurak                 3  58  -13.5   2.97
    Zeta Tauri                 Alheka                 5  38   21.1   2.97
    Epsilon Leonis             Ras Elased Australis   9  46   23.8   2.97
    Gamma2 Sagittarii          Alnasl                18   6  -30.4   2.98
    Gamma Hydrae               -                     13  19  -23.2   2.99
    Iota1 Scorpii              -                     17  48  -40.1   2.99
    Zeta Aquilae               Deneb el Okab         19   5   13.9   2.99
    Beta Trianguli             -                      2  10   35.0   3.00
    Psi Ursae Majoris          -                     11  10   44.5   3.00
    Gamma Ursae Minoris        Pherkad Major         15  21   71.8   3.00
    Mu1 Scorpii                -                     16  52  -38.0   3.00
    Gamma Gruis                -                     21  54  -37.4   3.00
    Delta Persei               -                      3  43   47.8   3.01
    Zeta Canis Majoris         Phurad                 6  20  -30.1   3.02
    Omicron2 Canis Majoris     -                      7   3  -23.8   3.02
    Epsilon Corvi              Minkar                12  10  -22.6   3.02
    Epsilon Aurigae            Almaaz                 5   2   43.8   3.03
    Beta Muscae                -                     12  46  -68.1   3.04
    Gamma Bootis               Seginus               14  32   38.3   3.04
    Beta Capricorni            Dabih                 20  21  -14.8   3.05
    Epsilon Geminorum          Mebsuta                6  44   25.1   3.06
    Mu Ursae Majoris           Tania Australis       10  22   41.5   3.06
    Delta Draconis             Tais                  19  13   67.7   3.07
    Eta Sagittarii             -                     18  18  -36.8   3.10
    Zeta Hydrae                -                      8  55   05.9   3.11
    Nu Hydrae                  -                     10  50  -16.2   3.11
    Lambda Centauri            -                     11  36  -63.0   3.11
    Alpha Indi                 Persian               20  38  -47.3   3.11
    Beta Columbae              Wazn                   5  51  -35.8   3.12
    Iota Ursae Majoris         Talita                 8  59   48.0   3.12
    Zeta Arae                  -                     16  59  -56.0   3.12
    Delta Herculis             Sarin                 17  15   24.8   3.12
    Kappa Centauri             Ke Kwan               14  59  -42.1   3.13
    Alpha Lyncis               -                      9  21   34.4   3.14
    N Velorum                  -                      9  31  -57.0   3.16
    Pi Herculis                -                     17  15   36.8   3.16
'''

class Star:
    def __init__ (self, milkyway, catalogueLine):
        self.milkyway = milkyway
        
        catalogueWords = [catalogueWord for catalogueWord in catalogueLine.split ('  ') if catalogueWord]

        self.systemName = catalogueWords [0]
        self.nickName = catalogueWords [1]

        self.rightAscension =  hourFactor * float (catalogueWords [2]) + minuteFactor * float (catalogueWords [3])
        self.declination = degreeFactor * float (catalogueWords [4])
        self.inclination = halfPi - self.declination

        self.equatPosition = skyRadius * ns.array ((
            mt.sin (-self.rightAscension) * mt.cos (self.inclination),
            mt.sin (self.rightAscension) * mt.sin (self.inclination),
            mt.cos (self.rightAscension)
        ))

        self.magnitude = float (catalogueWords [5])
        
    def setEarthViewPosition (self):
        rotatedPosition = self.milkyway.planetarium.rotZyxMat @ self.equatPosition   # Neglect distance from earth to sun
        self.earthViewPosition = tf.getProjection (rotatedPosition, self.milkyway.planetarium.solarSystem.getViewDistance ())

    def __repr__ (self):
        return f'{self.systemName}_{self.nickName}_{self.rightAscension}_{self.declination}_{self.equatPosition}_{self.magnitude}'

class Milkyway:
    def __init__ (self, planetarium):
        self.planetarium = planetarium
        self.stars = [Star (self, catalogueLine) for catalogueLine in starCatalogue.split ('\n') if catalogueLine.strip ()]

    def setEarthViewPositions (self):       
        for star in self.stars:
            star.setEarthViewPosition ()

    def __repr__ (self):
        return '\n'.join (star.__repr__ () for star in self.stars)
    
milkyway = Milkyway ()
print (milkyway)
