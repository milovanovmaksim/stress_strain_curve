from stress_strain_curve import StressStraineCurve


def main():
    sigma_ys = 190.32 # Engineering yield stress evaluated at the temperature of interest  [MPa].
    sigma_uts = 403.38 # Engineering ultimate tensile stress evaluated at the temperature of interest  [MPa].
    Ey = 198.74E+3 # Modulus of elasticity evaluated at the temperature of interest [MPa].
    epsilon_p = 0
    m2 = 0

    stress_strain_curve = StressStraineCurve(
        sigma_ys=sigma_ys,
        sigma_uts=sigma_uts,
        Ey=Ey,
        epsilon_p=epsilon_p,
        m2=m2
        )
    stress_strain_curve.compute()


if __name__ == "__main__":
    main()
