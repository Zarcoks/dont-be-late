from dataclasses import dataclass, field
from zoneinfo import ZoneInfo
from datetime import datetime

PARIS = ZoneInfo("Europe/Paris")
@dataclass
class Disruption :
    id : str
    title : str
    cause : str
    severity : str
    message : str
    periods : list[dict[str, datetime]] = field(default_factory=list)
    line_ids : set[str] = field(default_factory=set)

    #TODO : More useful for the fonctionnality that takes in account the cause "TRAVAUX"
    stop_names : set[str] = field(default_factory=set)

    #Tell if the disruption is on the trip of the user
    def is_active_during_user_trip(self, start, end):
        for period in self.periods:
            period_begin = period["begin"]
            period_end = period["end"]

            starts_before_trip_ends = period_begin < end
            ends_after_trip_starts = period_end > start

            if starts_before_trip_ends and ends_after_trip_starts:
                return True

        return False

#Transform date in format %Y%m%dT%H%M%S to datetime type
def _parse_datetime_field(date) :
    return datetime.strptime(date, "%Y%m%dT%H%M%S").replace(tzinfo=PARIS)

#Transform JSON to Python objects
def parse_disruptions(data) : 
    #Example of data to understand the next move:
    """ 
    data["disruptions"]: [
        id : 
        title : 
        cause :
        severity : 			
        message	:
        shortMessage :
        applicationPeriods	: 
        [
            {
                "begin": 
                "end": 
            },
            ...
        ]
    data["lines"] : [
        id : 
        impactedObjects : 
            [
                {
                    type : 
                    name : 
                    disruptionIds :
                },
                ...
        ]
    lastUpdate : 
    """
    disruptions = {}

    for json_disrupt in data["disruptions"] : 
        disruptions[json_disrupt["id"]] = Disruption(
            id=json_disrupt["id"],
            title=json_disrupt["title"],
            cause=json_disrupt["cause"],
            severity=json_disrupt["severity"],
            message=json_disrupt["message"],
            periods=[
                    {
                        "begin" : _parse_datetime_field(period["begin"]), 
                        "end" : _parse_datetime_field(period["end"])
                    } for period in json_disrupt["applicationPeriods"] 
            ]
        )
        
    for line in data["lines"]:

        for impacted in line["impactedObjects"]:
        
            for disruption_id in impacted["disruptionIds"]:

                python_disruption = disruptions.get(disruption_id)
                python_disruption.line_ids.add(line["id"])
    
                if impacted["type"] == "stop_point":
                     python_disruption.stop_names.add(impacted["name"])

    return list(disruptions.values())



