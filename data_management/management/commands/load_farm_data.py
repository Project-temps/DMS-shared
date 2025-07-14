import pandas as pd
from pathlib import Path
from django.core.management.base import BaseCommand
from api.models import Farm, SensorReading

class Command(BaseCommand):
    help = "Load hourly_merged_sensor_data.csv into SensorReading"

    def add_arguments(self, parser):
        parser.add_argument("--country", required=True)
        parser.add_argument("--farm", required=True)

    def handle(self, *args, **opts):
        country   = opts["country"]
        farm_name = opts["farm"]
        csv_path  = Path("data/processed") / country / "hourly_merged_sensor_data.csv"
        df        = pd.read_csv(csv_path, parse_dates=["datetime"])

        farm, _ = Farm.objects.get_or_create(name=farm_name, country=country)

        # pivot the wide DataFrame into (datetime, parameter, value) rows
        melted = df.melt(
            id_vars="datetime",
            var_name="parameter",
            value_name="value"
        )

        bulk = [
            SensorReading(
                farm     = farm,
                parameter= row.parameter,
                ts       = row.datetime,
                value    = row.value,
            )
            for row in melted.itertuples(index=False)
        ]

        SensorReading.objects.bulk_create(bulk, ignore_conflicts=True)
        self.stdout.write(
            self.style.SUCCESS(f"Loaded {len(bulk)} readings for {farm.name}")
        )
