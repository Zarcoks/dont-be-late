DELAY_BY_SEVERITY = {"BLOQUANTE": 60, "PERTURBEE" : 30}

#Estimate the delay_max per event. 
#The param "disruptions" needs to be filter per event already
def estimate_delay_per_event(disruptions):
    delay_max = 0
    for disrupt in disruptions : 
        delay = DELAY_BY_SEVERITY.get(disrupt.severity, 0)

        if delay > delay_max : 
            delay_max = delay

    return delay_max