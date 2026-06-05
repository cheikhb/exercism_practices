"""Functions to prevent a nuclear meltdown."""


def is_criticality_balanced(temperature, neutrons_emitted):
    """Verify criticality is balanced.

    Parameters:
        temperature (int or float): The temperature value in kelvin.
        neutrons_emitted (int or float): The number of neutrons emitted per second.

    Returns:
        bool: Is criticality balanced?

    Note:
        A reactor is said to be balanced in criticality if it satisfies the following conditions:
            - The temperature is less than 800 K.
            - The number of neutrons emitted per second is greater than 500.
            - The product of temperature and neutrons emitted per second is less than 500000.

    """

    is_temp_safe = temperature < 800
    
    # Condition 2: Number of neutrons emitted per second is greater than 500
    is_neutron_flow_adequate = neutrons_emitted > 500
    
    # Condition 3: Product of temperature and neutrons emitted per second is less than 500,000
    is_product_safe = (temperature * neutrons_emitted) < 500000
    
    # All conditions must be satisfied simultaneously
    return is_temp_safe and is_neutron_flow_adequate and is_product_safe


def reactor_efficiency(voltage, current, theoretical_max_power):
    """Assess reactor efficiency zone.

    Parameters:
        voltage (int or float): Voltage value.
        current (int or float): Current value.
        theoretical_max_power (int or float): The power level that corresponds to a 100% efficiency.

    Returns:
        str: One of ('green', 'orange', 'red', or 'black').

    Note:
        Efficiency can be grouped into 4 bands:
            1. green -> efficiency of 80% or more,
            2. orange -> efficiency of less than 80% but at least 60%,
            3. red -> efficiency below 60%, but still 30% or more,
            4. black ->  less than 30% efficient.

        The percentage value is calculated as
        (generated power/ theoretical max power)*100
        where generated power = voltage * current
    """
    # 1. Calculate the actual generated power
    generated_power = voltage * current
    
    # 2. Calculate efficiency as a percentage float value
    efficiency_percentage = (generated_power / theoretical_max_power) * 100
    
    # 3. Categorize efficiency into the designated bands
    if efficiency_percentage >= 80:
        return 'green'
    elif efficiency_percentage >= 60:  # Matches: < 80% but at least 60%
        return 'orange'
    elif efficiency_percentage >= 30:  # Matches: < 60% but at least 30%
        return 'red'
    else:                              # Matches: < 30%
        return 'black'


def fail_safe(temperature, neutrons_produced_per_second, threshold):
    """Assess and return status code for the reactor.

    Parameters:
        temperature (int or float): The value of the temperature in kelvin.
        neutrons_produced_per_second (int or float): The neutron flux.
        threshold (int or float): The threshold for the category.

    Returns:
        str: One of ('LOW', 'NORMAL', 'DANGER').

    Note:
        1. 'LOW' -> `temperature * neutrons per second` < 90% of `threshold`
        2. 'NORMAL' -> `temperature * neutrons per second` +/- 10% of `threshold`
        3. 'DANGER' -> `temperature * neutrons per second` is not in the above-stated ranges
    """

    # 1. Compute the active metric value
    criticality_value = temperature * neutrons_produced_per_second
    
    # 2. Define the operational boundary thresholds
    low_bound = 0.9 * threshold
    high_bound = 1.1 * threshold
    
    # 3. Assess status ranges
    if criticality_value < low_bound:
        return 'LOW'
    elif low_bound <= criticality_value <= high_bound:  # Within 10% variance of threshold
        return 'NORMAL'
    else:
        return 'DANGER'
