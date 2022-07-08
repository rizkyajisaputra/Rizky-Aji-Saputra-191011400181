def down(x, xmin, xmax):
    return (xmax - x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class Persediaan():
    minimum = 2100
    maximum = 3500

    def Sedikit(self, x):
        if x >= self.maximum:
            return 0
        elif x<= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def Banyak(self, x):
        if x >= self.maximum:
            return 1
        elif x<= self.minimum:
            return 0
        else:
            return up(x, self.minimum, self.maximum)

    def tetap(self, x):
        if x >= self.maximum or x<= self.minimum:
            return 0
        elif self.minimum < x < self.median:
            return up(x, self.minimum, self.median)
        elif self.median < x < self.maximum:
            return down(x, self.median, self.maximum)
        else:
            return 1

class Permintaan():
    minimum = 100
    maximum = 250

    def Sedikit(self, x):
        if x >= self.maximum:
            return 0
        elif x<= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def Banyak(self, x):
        if x >= self.maximum:
            return 1
        elif x<= self.minimum:
            return 0
        else:
            return up(x, self.minimum, self.maximum)

    def tetap(self, x):
        if x >= self.maximum or x<= self.minimum:
            return 0
        elif self.minimum < x < self.median:
            return up(x, self.minimum, self.median)
        elif self.median < x < self.maximum:
            return down(x, self.median, self.maximum)
        else:
            return 1


class Harga():
    minimum = 1000
    maximum = 5000
    permintaan = 0
    persediaan = 0

    def _murah(self, a):
        return self.maximum - a*(self.maximum - self.minimum)

    def _mahal(self, a):
        return a*(self.maximum - self.minimum) + self.minimum

    def _inferensi(self, pmt=Permintaan(), psd=Persediaan()):
        result = []
        # [R1] JIKA Permintaan TURUN, dan Barang BANYAK, MAKA
        # Harga MURAH.
        a1 = min(pmt.turun(self.permintaan), psd.Banyak(self.persediaan))
        z1 = self._murah(a1)
        result.append((a1, z1))
        # [R2] JIKA Permintaan TURUN, dan Barang SEDIKIT, MAKA
        # Harga MURAH.
        a2 = min(pmt.turun(self.permintaan), psd.Sedikit(self.persediaan))
        z2 = self._murah(a2)
        result.append((a2, z2))
        # [R3] JIKA Permintaan NAIK, dan Barang BANYAK, MAKA
        # Harga MAHAL
        a3 = min(pmt.naik(self.permintaan), psd.Banyak(self.persediaan))
        z3 = self._mahal(a3)
        result.append((a3, z3))
        # [R4] JIKA Permintaan NAIK, dan Persediaan SEDIKIT, MAKA
        # Harga MAHAL.
        a4 = min(pmt.naik(self.permintaan), psd.Sedikit(self.persediaan))
        z4 = self._mahal(a4)
        result.append((a4, z4))
        # [R5] JIKA Permintaan TETAP, dan Persediaan BANYAK, MAKA
        # Harga MURAH
        a5 = min(pmt.naik(self.permintaan), psd.Banyak(self.persediaan))
        z5 = self._murah(a5)
        result.append((a5, z5))
        # [R6] JIKA Permintaan TETAP, dan Persediaan SEDIKIT, MAKA
        # Harga MAHAL.
        a6 = min(pmt.turun(self.permintaan), psd.Sedikit(self.persediaan))
        z6 = self._mahal(a6)
        result.append((a6, z6))
        # [R7] JIKA Permintaan NAIK, dan Persediaan TETAP, MAKA
        # Harga MAHAL.
        a7 = min(pmt.naik(self.permintaan), psd.tetap(self.persediaan))
        z7 = self._mahal(a7)
        result.append((a7, z7))
        # [R8] JIKA Permintaan TURUN, dan Persediaan TETAP, MAKA
        # Harga MURAH.
        a8 = min(pmt.naik(self.permintaan), psd.tetap(self.persediaan))
        z8 = self._murah(a8)
        result.append((a8, z8))
        # [R9] JIKA Permintaan TETAP, dan Persediaan TETAP, MAKA
        # Harga TETAP.
        a9 = min(pmt.naik(self.permintaan), psd.tetap(self.persediaan))
        z9 = self._mahal(a9)
        result.append((a9, z9))
        return result
    
    def defuzifikasi(self, data_inferensi=[]):
        # (α1∗z1+α2∗z2+α3∗z3+α4∗z4+α5∗z5+α6∗z6+α7∗z7+α8∗z8+α9∗z9) / (α1+α2+α3+α4+α5+α6+α7+α8+α9)
        data_inferensi = data_inferensi if data_inferensi else self._inferensi()
        res_a_z = 0
        res_a = 0
        for data in data_inferensi:
            # data[0] = a 
            # data[1] = z
            res_a_z += data[0] * data[1]
            res_a += data[0]
        return res_a_z/res_a