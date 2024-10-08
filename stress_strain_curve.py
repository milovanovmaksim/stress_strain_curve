import math
import csv

import matplotlib.pyplot as plt

"""
Calculate stress–strain curve base on 'ASME Boiler and pressure vessel code, Section VIII, Division 2, 2015 – Rules for construction of pressure vessels, ANNEX 3-D'.

Args:
    sigma_ys - engineering yield stress evaluated at the temperature of interest,
    sigma_uts - engineering ultimate tensile stress evaluated at the temperature of interest,
    Ey - modulus of elasticity evaluated at the temperature of interest,
    ε_ys - 0.2% engineering offset strain,
    m 2 - curve fitting exponent for the stress–strain curve equal to the true strain at the true ultimate stress,
    epsilon_p - stress–strain curve fitting parameter.
"""
class StressStraineCurve:
    def __init__(
        self, sigma_ys: float, sigma_uts: float, Ey: float, m2: float, epsilon_p: float, delta_sigma_t: int = 10
    ) -> None:
        self.sigma_ys = sigma_ys
        self.sigma_uts = sigma_uts
        self.Ey = Ey
        self.m2 = m2
        self.ε_p = epsilon_p
        self.ε_ys = 0.002
        self.delta_sigma_t = delta_sigma_t

    def _R(self) -> float:
        """
        Engineering yield to engineering tensile ratio.
        """
        return self.sigma_ys / self.sigma_uts

    def K(self) -> float:
        """
        Material parameter for stress–strain curve model.
        """
        return 1.5 * self._R() ** 1.5 - 0.5 * self._R() ** 2.5 - self._R() ** 3.5

    def _H(self, sigma_t: float) -> float:
        """
        Stress–strain curve fitting parameter.

        Args:
            sigma_t (float): true stress at which the true strain will be evaluated, may be a membrane,
            membrane plus bending, or membrane, membrane plus bending plus peak stress depending on the application.
        """
        return 2 * (sigma_t - (self.sigma_ys + self.K() * (self.sigma_uts - self.sigma_ys))) / (
            self.K() * (self.sigma_uts - self.sigma_ys)
        )

    def _A_2(self) -> float:
        """
        Curve fitting constant for the plastic region of the stress–strain curve.
        """
        return (self.sigma_uts * math.exp(self.m2)) / self.m2 ** self.m2

    def _epsilon_2(self, sigma_t: float) -> float:
        """
        True plastic strain in the macro-strain region of the stress–strain curve.

        Args:
            sigma_t (float): смотри описание этого аргумента в функции  StressStraineCurve.H().
        """
        return (sigma_t / self._A_2()) ** (1 / self.m2)

    def _sigma_uts_t(self) -> float:
        """
        True ultimate tensile stress evaluated at the true ultimate tensile strain.
        """
        return round(self.sigma_uts * math.exp(self.m2), 2)

    def _m1(self) -> float:
        """
        Curve fitting exponent for the stress–strain curve equal to the true strain
        at the proportional limit and the strain hardening coefficient in the large strain region.
        """
        return (math.log10(self._R()) + (self.ε_p - self.ε_ys)) / (
            math.log10((math.log10(1 + self.ε_p)) / (math.log10(1 + self.ε_ys)))
        )

    def _A1(self) -> float:
        """
        Curve fitting constant for the elastic region of the stress–strain curve.
        """
        return (self.sigma_ys * (1 + self.ε_ys)) / (math.log10(1 + self.ε_ys)) ** self._m1()

    def _epsilon_1(self, sigma_t: float) -> float:
        """
        True plastic strain in the micro-strain region of the stress–strain curve.

        Args:
            sigma_t (float): смотри описание этого аргумента в функции  StressStraineCurve.H().
        """
        return (sigma_t / self._A1()) ** (1 / self._m1())
    
    def _gamma_1(self, sigma_t: float) -> float:
        """
        True strain in the micro-strain region of the stress–strain curve.

        Args:
            sigma_t (float): смотри описание этого аргумента в функции  StressStraineCurve.H().
        """
        return (self._epsilon_1(sigma_t) / 2) * (1.0 - math.tanh(self._H(sigma_t)))
    
    def _gamma_2(self, sigma_t: float) -> float:
        """
        True plastic strain in the macro-strain region of the stress–strain curve.

        Args:
            sigma_t (float): смотри описание этого аргумента в функции  StressStraineCurve.H().
        """
        return (self._epsilon_2(sigma_t) / 2) * (1.0 + math.tanh(self._H(sigma_t)))
    
    def to_csv(self):
        """
        Save stress–strain curve to csv file.
        """
        fields = ["true_stress", "true_strain"]
        true_stresses, true_strains  = self.compute()
        filename = "stress_strain_curve.csv"
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=",")
            csvwriter.writerow(fields)
            for true_stress, true_strain in zip(true_stresses, true_strains):
                csvwriter.writerow([true_stress, true_strain])

    def compute(self) -> tuple[list[float], list[float]]:
        """
        Returns:
            tuple[list[float], list[float]]: returns tuple containing two lists. The first list contains true stress, the second true strain.
        """
        current_sigma_t = 0.0
        true_stress = [0.0]
        true_strain = [0.0]
    
        while current_sigma_t < (self._sigma_uts_t() - self.delta_sigma_t):
            current_sigma_t += self.delta_sigma_t
            true_stress.append(current_sigma_t)
            true_strain.append(self._epsilon_t(current_sigma_t))
        true_stress.append(self._sigma_uts_t())
        true_strain.append(self._epsilon_t(self._sigma_uts_t()))

        return (true_stress, true_strain)
    
    def _epsilon_t(self, sigma_t: float) -> float:
        """
        Total true strain.

        Args:
            sigma_t (float): смотри описание этого аргумента в функции  StressStraineCurve.H().
        """
        gamma_1 = self._gamma_1(sigma_t)
        gamma_2 = self._gamma_2(sigma_t)
        if gamma_1 + gamma_2 <= self.ε_p:
            return round(sigma_t / self.Ey, 4)
        
        return round((sigma_t / self.Ey) + gamma_1 + gamma_2, 3)
    
    def show_curve(self):
        true_stress, true_strain  = self.compute()
        fig, ax = plt.subplots()
        ax.plot(true_strain, true_stress)
        ax.set(xlabel='True straine (mm/mm)', ylabel='True stress')
        ax.grid(True, linestyle='-.')
        ax.tick_params(labelsize='medium', width=3)
        fig.savefig("stress_strain_curve.png")
        plt.show()
