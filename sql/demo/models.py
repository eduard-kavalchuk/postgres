# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import JSONField
from django.db import models


class AircraftsData(models.Model):
    aircraft_code = models.CharField(primary_key=True, max_length=3)
    model = JSONField()
    range = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'aircrafts_data'


class AirportsData(models.Model, gis_models.PointField):
    airport_code = models.CharField(primary_key=True, max_length=3)
    airport_name = JSONField()
    city = JSONField()
    coordinates = gis_models.PointField()
    timezone = models.TextField()

    class Meta:
        managed = False
        db_table = 'airports_data'


class BoardingPasses(models.Model):
    ticket_no = models.OneToOneField('TicketFlights', models.DO_NOTHING, db_column='ticket_no')
    flight_id = models.IntegerField()
    boarding_no = models.IntegerField()
    seat_no = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'boarding_passes'
        unique_together = (('flight_id', 'boarding_no'), ('flight_id', 'seat_no'), ('ticket_no', 'flight_id'),)


class Bookings(models.Model):
    book_ref = models.CharField(primary_key=True, max_length=6)
    book_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'bookings'


class Flights(models.Model):
    flight_id = models.AutoField(primary_key=True)
    flight_no = models.CharField(max_length=6)
    scheduled_departure = models.DateTimeField()
    scheduled_arrival = models.DateTimeField()
    departure_airport = models.ForeignKey(
        AirportsData,
        models.DO_NOTHING,
        db_column='departure_airport',
        related_name='departure_airport'
    )
    arrival_airport = models.ForeignKey(
        AirportsData,
        models.DO_NOTHING,
        db_column='arrival_airport',
        related_name='arrival_airport'
    )
    status = models.CharField(max_length=20)
    aircraft_code = models.ForeignKey(AircraftsData, models.DO_NOTHING, db_column='aircraft_code')
    actual_departure = models.DateTimeField(blank=True, null=True)
    actual_arrival = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flights'
        unique_together = (('flight_no', 'scheduled_departure'),)


class Seats(models.Model):
    aircraft_code = models.OneToOneField(AircraftsData, models.DO_NOTHING, db_column='aircraft_code')
    seat_no = models.CharField(max_length=4)
    fare_conditions = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'seats'
        unique_together = (('aircraft_code', 'seat_no'),)


class TicketFlights(models.Model):
    ticket_no = models.OneToOneField('Tickets', models.DO_NOTHING, db_column='ticket_no')
    flight = models.ForeignKey(Flights, models.DO_NOTHING)
    fare_conditions = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'ticket_flights'
        unique_together = (('ticket_no', 'flight'),)


class Tickets(models.Model):
    ticket_no = models.CharField(primary_key=True, max_length=13)
    book_ref = models.ForeignKey(Bookings, models.DO_NOTHING, db_column='book_ref')
    passenger_id = models.CharField(max_length=20)
    passenger_name = models.TextField()
    contact_data = JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tickets'
