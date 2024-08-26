from stress_strain_curve import StressStraineCurve


def main():
    # Example:
    # Material: ASTM A182 F22.
    # T = 121 °С - Design temperature.
    sigma_ys = 190.32 # Engineering yield stress evaluated at the temperature of interest  [MPa].
    sigma_uts = 403.38 # Engineering ultimate tensile stress evaluated at the temperature of interest  [MPa].
    Ey = 198.74E+3 # Modulus of elasticity evaluated at the temperature of interest [MPa].
    epsilon_p = 2E-5 # Stress–strain curve fitting parameter.
    m2 = 0.6 # Curve fitting exponent for the stress–strain curve equal to the true strain at the true ultimate stress.

    stress_strain_curve = StressStraineCurve(
        sigma_ys=sigma_ys,
        sigma_uts=sigma_uts,
        Ey=Ey,
        epsilon_p=epsilon_p,
        m2=m2,
        )
    stress_strain_curve.show()


if __name__ == "__main__":
    main()
