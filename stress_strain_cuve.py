import math

"""
σ_ys - engineering yield stress evaluated at the temperature of interest,
σ_uts - engineering ultimate tensile stress evaluated at the temperature of interest,
Ey - modulus of elasticity evaluated at the temperature of interest,
ε_ys - 0.2% engineering offset strain,
m 2 - curve fitting exponent for the stress–strain curve equal to the true strain at the true ultimate stress,
ɛ_p - stress–strain curve fitting parameter
"""


class StressStraineCurve:
    def __init__(
        self, sigma_ys: float, sigma_uts: float, Ey: float, m2: float, ε_p: float, sigma_t_step: int = 10
    ) -> None:
        self.σ_ys = sigma_ys
        self.σ_uts = sigma_uts
        self.Ey = Ey
        self.m2 = m2
        self.ε_p = ε_p
        self.ε_ys = 0.002
        self.sigma_t_step = sigma_t_step

    def R(self) -> float:
        """
        Engineering yield to engineering tensile ratio.
        """
        return self.σ_ys / self.σ_uts

    def K(self) -> float:
        """
        Material parameter for stress–strain curve model.
        """
        return 1.5 * self.R() ** 1.5 - 0.5 * self.R() ** 2.5 - self.R() ** 3.5

    def H(self, sigma_t: float) -> float:
        """
        Stress–strain curve fitting parameter.

        Args:
            sigma_t (float): true stress at which the true strain will be evaluated, may be a membrane,
            membrane plus bending, or membrane, membrane plus bending plus peak stress depending on the application.
        """
        return 2 * (sigma_t - (self.σ_ys + self.K() * (self.σ_uts - self.σ_ys))) / (
            self.K() * (self.σ_uts - self.σ_ys)
        )

    def A_2(self) -> float:
        """
        Curve fitting constant for the plastic region of the stress–strain curve.
        """
        return (self.σ_uts * math.exp(self.m2)) / self.m2**self.m2

    def epsilon_2(self, sigma_t: float) -> float:
        """
        True plastic strain in the macro-strain region of the stress–strain curve.

        Args:
            sigma_t (float): смотри описание этого аргумента в функции  StressStraineCurve.H().
        """
        return (sigma_t / self.A_2()) ** (1 / self.m2)

    def sigma_uts_t(self) -> float:
        """
        True ultimate tensile stress evaluated at the true ultimate tensile strain.
        """
        return self.σ_uts * math.exp(self.m2)

    def m1(self) -> float:
        """
        Curve fitting exponent for the stress–strain curve equal to the true strain
        at the proportional limit and the strain hardening coefficient in the large strain region.
        """
        return (math.log10(self.R()) + (self.ε_p - self.ε_ys)) / (
            math.log10((math.log10(1 + self.ε_p)) / (math.log10(1 + self.ε_ys)))
        )

    def A1(self) -> float:
        """
        curve fitting constant for the elastic region of the stress–strain curve
        """
        return (self.σ_ys * (1 + self.ε_ys)) / (math.log10(1 + self.ε_ys)) ** self.m1()

    def epsilon_1(self, sigma_t: float) -> float:
        """
        True plastic strain in the micro-strain region of the stress–strain curve

        Args:
            sigma_t (float): смотри описание этого аргумента в функции  StressStraineCurve.H().
        """
        return (sigma_t / self.A1()) ** (1 / self.m1())
    
    def gamma_1(self, sigma_t: float) -> float:
        """
        True strain in the micro-strain region of the stress–strain curve

        Args:
            sigma_t (float): смотри описание этого аргумента в функции  StressStraineCurve.H().
        """
        return (self.epsilon_1(sigma_t) / 2) * (1.0 - math.tanh(self.H(sigma_t)))
    
    def gamma_2(self, sigma_t: float) -> float:
        """
        True plastic strain in the macro-strain region of the stress–strain curve

        Args:
            sigma_t (float): смотри описание этого аргумента в функции  StressStraineCurve.H().
        """
        return (self.epsilon_2(sigma_t) / 2) * (1.0 + math.tanh(self.H(sigma_t)))
    
    def to_csv(self):
        pass

    def compute(self) -> tuple[list[float], list[float]]:
        current_sigma_t = 0
        sigma_t = [0]
        epsilon_t = [0]
    
        while current_sigma_t < (self.sigma_uts_t() - self.sigma_t_step):
            current_sigma_t += self.sigma_t_step

        return ([1.0], [1.0])
    
    def epsilon_t(self, sigma_t: float) -> float:
        """
        Total true strain

        Args:
            sigma_t (float): смотри описание этого аргумента в функции  StressStraineCurve.H().
        """
        gamma_1 = self.gamma_1(sigma_t)
        gamma_2 = self.gamma_2(sigma_t)
        
        return 10.0
