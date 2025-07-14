from django.db import models

class Farm(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class SensorReading(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=60)          # مثلا temperature، humidity و …
    ts = models.DateTimeField(db_index=True)
    value = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=["parameter", "ts"]),
        ]

    def __str__(self):
        return f"{self.farm}-{self.parameter}@{self.ts}"
